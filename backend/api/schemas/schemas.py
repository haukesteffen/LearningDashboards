from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Story Pydantic Schemas
class StoryBase(BaseModel):
    title: Optional[str]
    by: Optional[str]
    descendants: Optional[int]
    score: Optional[int]
    time: Optional[datetime]
    url: Optional[str]


class StoryCreate(StoryBase):
    title: str
    by: str
    time: datetime


class StoryResponse(StoryBase):
    id: int

    class Config:
        orm_mode = True


# Job Pydantic Schemas
class JobBase(BaseModel):
    title: Optional[str]
    text: Optional[str]
    by: Optional[str]
    score: Optional[int]
    time: Optional[datetime]
    url: Optional[str]


class JobCreate(JobBase):
    title: str
    by: str
    time: datetime


class JobResponse(JobBase):
    id: int

    class Config:
        orm_mode = True


# Comment Pydantic Schemas
class CommentBase(BaseModel):
    text: Optional[str]
    by: Optional[str]
    time: Optional[datetime]
    parent: Optional[int]


class CommentCreate(CommentBase):
    text: str
    by: str
    time: datetime


class CommentResponse(CommentBase):
    id: int

    class Config:
        orm_mode = True


# Poll Pydantic Schemas
class PollBase(BaseModel):
    title: Optional[str]
    text: Optional[str]
    by: Optional[str]
    descendants: Optional[int]
    score: Optional[int]
    time: Optional[datetime]


class PollCreate(PollBase):
    title: str
    by: str
    time: datetime


class PollResponse(PollBase):
    id: int

    class Config:
        orm_mode = True


# PollOption Pydantic Schemas
class PollOptionBase(BaseModel):
    text: Optional[str]
    by: Optional[str]
    poll: Optional[int]
    score: Optional[int]
    time: Optional[datetime]


class PollOptionCreate(PollOptionBase):
    text: str
    by: str
    poll: int
    time: datetime


class PollOptionResponse(PollOptionBase):
    id: int

    class Config:
        orm_mode = True


# Deleted Pydantic Schemas
class DeletedBase(BaseModel):
    item: Optional[int]


class DeletedCreate(DeletedBase):
    item: int


class DeletedResponse(DeletedBase):
    item: int

    class Config:
        orm_mode = True


# Dead Pydantic Schemas
class DeadBase(BaseModel):
    item: Optional[int]


class DeadCreate(DeadBase):
    item: int


class DeadResponse(DeadBase):
    item: int

    class Config:
        orm_mode = True


# Scrape Pydantic Schemas
class ScrapeBase(BaseModel):
    scrape_time: Optional[datetime]


class ScrapeCreate(ScrapeBase):
    scrape_time: datetime


class ScrapeResponse(ScrapeBase):
    id: int

    class Config:
        orm_mode = True


# Skipped Pydantic Schemas
class SkippedBase(BaseModel):
    item: Optional[int]


class SkippedCreate(SkippedBase):
    item: int


class SkippedResponse(SkippedBase):
    item: int

    class Config:
        orm_mode = True


# TermPop Terms Pydantic Schemas
class TermPopTermBase(BaseModel):
    id: int
    term: str

class TermPopTermCreate(TermPopTermBase):
    pass

class TermPopTermUpdate(BaseModel):
    term: Optional[str] = None

class TermPopTermInDBBase(TermPopTermBase):
    id: int

    class Config:
        orm_mode = True

class TermPopTerm(TermPopTermInDBBase):
    pass

class TermPopTermWithAggregations(TermPopTermInDBBase):
    aggregations: List['TermPopAgg'] = []


# TermPop Agg Pydantic Schemas
class TermPopAggBase(BaseModel):
    year: int
    month: Optional[int] = None
    week: Optional[int] = None
    occurrence_count: int

    class Config:
        orm_mode = True

class TermPopAggCreate(TermPopAggBase):
    term_id: int

class TermPopAggInDBBase(TermPopAggBase):
    term_id: int

    class Config:
        orm_mode = True

class TermPopAgg(TermPopAggInDBBase):
    pass
