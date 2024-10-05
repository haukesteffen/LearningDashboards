from sqlalchemy import Column, SmallInteger, Integer, String, Text, TIMESTAMP, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Stories table
class Story(Base):
    __tablename__ = 'stories'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    by = Column(String(15))
    descendants = Column(Integer)
    score = Column(Integer)
    time = Column(TIMESTAMP)
    url = Column(Text)


# Jobs table
class Job(Base):
    __tablename__ = 'jobs'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    text = Column(Text)
    by = Column(String(15))
    score = Column(Integer)
    time = Column(TIMESTAMP)
    url = Column(Text)


# Comments table
class Comment(Base):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    by = Column(String(15))
    time = Column(TIMESTAMP)
    parent = Column(Integer)


# Polls table
class Poll(Base):
    __tablename__ = 'polls'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    text = Column(Text)
    by = Column(String(15))
    descendants = Column(Integer)
    score = Column(Integer)
    time = Column(TIMESTAMP)


# Pollopts table
class PollOption(Base):
    __tablename__ = 'pollopts'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    by = Column(String(15))
    poll = Column(Integer, ForeignKey('raw.polls.id'))
    score = Column(Integer)
    time = Column(TIMESTAMP)

    # Relationship with Polls
    poll_rel = relationship("Poll", backref="options")


# Deleted table
class Deleted(Base):
    __tablename__ = 'deleted'
    __table_args__ = {'schema': 'raw'}

    item = Column(Integer, primary_key=True, index=True)


# Dead table
class Dead(Base):
    __tablename__ = 'dead'
    __table_args__ = {'schema': 'raw'}

    item = Column(Integer, primary_key=True, index=True)


# Scrape table
class Scrape(Base):
    __tablename__ = 'scrape'
    __table_args__ = {'schema': 'raw'}

    id = Column(Integer, primary_key=True, index=True)
    scrape_time = Column(TIMESTAMP)


# Skipped table
class Skipped(Base):
    __tablename__ = 'skipped'
    __table_args__ = {'schema': 'raw'}

    item = Column(Integer, primary_key=True, index=True)


# Termpop Terms
class TermPopTerm(Base):
    __tablename__ = 'termpop_terms'
    __table_args__ = {'schema': 'dwh'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    term = Column(Text, nullable=False)

    # Relationship to TermPopAgg
    aggregations = relationship('TermPopAgg', back_populates='term')

# Termpop Agg
class TermPopAgg(Base):
    __tablename__ = 'termpop_agg'
    __table_args__ = (
        PrimaryKeyConstraint('term_id', 'year', 'month', 'week', name='termpop_agg_pkey'),
        {'schema': 'dwh'}
    )

    term_id = Column(Integer, ForeignKey('dwh.termpop_terms.id'), nullable=False)
    year = Column(SmallInteger, nullable=False)
    month = Column(SmallInteger, nullable=False)
    week = Column(SmallInteger, nullable=False)
    occurrence_count = Column(Integer, nullable=False)

    # Relationship to TermPopTerm
    term = relationship('TermPopTerm', back_populates='aggregations')

