import asyncio
import aiohttp
import os
import html
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from time import perf_counter


class Scraper:
    def __init__(
            self,
            batch_size: int = 1000, 
            verbose: bool = False
            ):
        self.verbose = verbose
        self.batch_size = batch_size
        self._empty_dicts()
        self.client = requests.Session()
        self.engine = create_engine(f'postgresql://{os.environ["DBUSER"]}:{os.environ["DBPW"]}@localhost:5432/hndb')
        self.max_id = self._get_max()
        self.last_id = self._get_last()
        self.type_mapping = {
            'story': ['id', 'title', 'by', 'descendants', 'score', 'time', 'url'],
            'job': ['id', 'title', 'text', 'by', 'score', 'time', 'url'],
            'comment': ['id', 'text', 'by', 'time', 'parent'],
            'poll': ['id', 'title', 'text', 'by', 'descendants', 'score', 'time'],
            'pollopt': ['id', 'text', 'by', 'poll', 'score', 'time'],
        }
        if self.verbose:
            print(f'Initialized scraper. Last ID: {self.last_id}, Max ID: {self.max_id}, Batch Size: {self.batch_size}')

    async def begin_scraping(self):
        while self.last_id < self.max_id:
            start = perf_counter()
            self._empty_dicts()
            self.ids = range(self.last_id+1, min(self.last_id+1+self.batch_size, self.max_id+1))
            self.jsons = await self._scrape_batch(self.ids)
            for json in self.jsons:
                self._to_dict(json)
            self._insert_sql()
            self.last_id = self._get_last()
            self.max_id = self._get_max()
            stop = perf_counter()
            if self.verbose:
                print(f'Processing of batch took {(stop-start):.2f} seconds')

    async def _scrape_batch(self, ids):
        async with aiohttp.ClientSession() as session:
            jsons = await self._fetch_batch(session, ids)
            return jsons

    async def _fetch_batch(self, s, ids):
        tasks = []
        for id in ids:
            task = asyncio.create_task(self._fetch(s, id))
            tasks.append(task)
        res = await asyncio.gather(*tasks)
        return res

    async def _fetch(self, s, id):
        async with s.get(f'https://hacker-news.firebaseio.com/v0/item/{id}.json') as r:
            if r.status != 200:
                r.raise_for_status()
            return await r.json()

    def _empty_dicts(self):
        self.stories = {
            'id':[],
            'title':[],
            'by':[],
            'descendants':[],
            'score':[],
            'time':[],
            'url':[]
        }
        self.jobs = {
            'id':[],
            'title':[],
            'text':[],
            'by':[],
            'score':[],
            'time':[],
            'url':[],
        }
        self.comments = {
            'id':[],
            'text':[],
            'by':[],
            'time':[],
            'parent':[]
        }
        self.polls = {
            'id':[],
            'title':[],
            'text':[],
            'by':[],
            'descendants':[],
            'score':[],
            'time':[],
        }
        self.pollopts = {
            'id':[],
            'text':[],
            'by':[],
            'poll':[],
            'score':[],
            'time':[],
        }
        self.deleted = {
            'item':[]
        }
        self.dead = {
            'item':[]
        }
        self.scrape = {
            'id':[],
            'scrape_time':[]
        }
        self.skipped = []

    def _get(self, id):
        url = f'https://hacker-news.firebaseio.com/v0/item/{id}.json'
        response = self.client.get(url)
        return response.json()

    def _get_last(self):
        last_query = """
        SELECT id
        FROM scrape
        ORDER BY scrape_time DESC
        LIMIT 1
        """
    
        with self.engine.begin() as con:
            return pd.read_sql(sql=last_query, con=con).values[0][0]

    def _get_max(self):
        url = 'https://hacker-news.firebaseio.com/v0/maxitem.json'
        response = self.client.get(url)
        return int(response.text)
    
    def _sanitize_text(self, text: str):
        try:
            return html.unescape(text).replace('\\x00','').replace('\x00','')
        except TypeError:
            return np.nan
    
    def _append_data(self, data_store, type, **kwargs):
        if type in self.type_mapping and type in data_store:
            fields = self.type_mapping[type]
            store = data_store[type]

            for field in fields:
                if field in kwargs:
                    store[field].append(kwargs[field])

    def _to_dict(self, json):
        id = json.get('id')
        type = json.get('type')

        # sanity check
        if type == None:
            self.skipped.append(id)
            return
        
        # get scrape time
        self.scrape['id'].append(id)
        self.scrape['scrape_time'].append(datetime.now())

        # check if deleted or dead
        if json.get('deleted'):
            self.deleted['item'].append(id)
        if json.get('dead'):
            self.dead['item'].append(id)

        title = self._sanitize_text(json.get('title'))
        text = self._sanitize_text(json.get('text'))
        by = json.get('by')
        score = json.get('score')
        time = json.get('time')
        try:
            time = datetime.fromtimestamp(int(time))
        except TypeError:
            time = np.nan
        url = json.get('url')
        descendants = json.get('descendants')
        poll = json.get('poll')
        parent = json.get('parent')

        data_store = {
            'story': self.stories,
            'job': self.jobs,
            'comment': self.comments,
            'poll': self.polls,
            'pollopt': self.pollopts,
        }

        self._append_data(
            data_store=data_store,
            type=type,
            id=id,
            title=title,
            by=by,
            text=text,
            descendants=descendants,
            score=score,
            time=time,
            url=url,
            parent=parent,
            poll=poll
        )

    def _insert_sql(self):
        with self.engine.begin() as con:
            pd.DataFrame(self.scrape).to_sql(name='scrape', con=con, if_exists='append', index=False)
            pd.DataFrame(self.skipped).to_sql(name='skipped', con=con, if_exists='append', index=False)
            pd.DataFrame(self.deleted).to_sql(name='deleted', con=con, if_exists='append', index=False)
            pd.DataFrame(self.dead).to_sql(name='dead', con=con, if_exists='append', index=False)
            pd.DataFrame(self.stories).to_sql(name='stories', con=con, if_exists='append', index=False)
            pd.DataFrame(self.jobs).to_sql(name='jobs', con=con, if_exists='append', index=False)
            pd.DataFrame(self.comments).to_sql(name='comments', con=con, if_exists='append', index=False)
            pd.DataFrame(self.polls).to_sql(name='polls', con=con, if_exists='append', index=False)
            pd.DataFrame(self.pollopts).to_sql(name='pollopts', con=con, if_exists='append', index=False)


async def main():
    scraper = Scraper(batch_size=100000, verbose=True)
    await scraper.begin_scraping()

if __name__ == '__main__':
    asyncio.run(main())