
import asyncio
import itertools
import json
import time

import aiohttp
from aiolimiter import AsyncLimiter
from aioretry import RetryInfo, RetryPolicyStrategy, retry
from decouple import config
from sqlalchemy import select
import math

def defaullt_retry_policy(info: RetryInfo):
    print(info.exception)
    return (info.fails >= 8), [0, 0.5, 2, 5, 10, 15, 20, 30, 60][info.fails - 1]
