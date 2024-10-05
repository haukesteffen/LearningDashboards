#!/usr/bin/env python

from fastapi import FastAPI
from .endpoints.page1_endpoints import page1_router
from .endpoints.page2_endpoints import page2_router

app = FastAPI()
app.include_router(page1_router)
app.include_router(page2_router)