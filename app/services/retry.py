from tenacity import retry, stop_after_attempt, wait_fixed

"""try max 3 times with 2 seconds wait in between """

@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(2)
)
def retryable(func, *args, **kwargs):
    return func(*args, **kwargs)