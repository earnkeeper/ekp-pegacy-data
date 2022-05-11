
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
    return (info.fails >= 5), [0, 0.5, 2, 5, 10, 10][info.fails - 1]
