from aioretry import RetryInfo


def retry_policy(info: RetryInfo):
    print(info.exception)
    return False, (info.fails - 1) % 10 + 1
