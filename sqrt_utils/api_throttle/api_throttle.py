import asyncio
import time
from functools import wraps
from sqrt_utils.logging.dummy_logger import DummyLogger


class APIThrottle:
    def __init__(
        self,
        api_limit: int,
        interval: int,
        logger=DummyLogger(print_msg=False),
    ):
        self.limit = api_limit
        self.interval = interval
        self.logger = logger
        self.jobs = {}  # (job_hash, start_time, weight) -> end_time

    async def insert_job(self, job_hash, weight) -> tuple:
        self.flush_old_jobs()

        self.logger.info(
            f"try to insert job: {job_hash} with weight {weight}\n"
            f"{self.__class__.__name__} - {sum([i[2] for i in self.jobs.keys()])} "
            f"weights using in throttle ~ {self.limit} per {self.interval}s"
        )

        while not self.okay_to_insert(weight):
            await asyncio.sleep(0.01)
            self.flush_old_jobs()

        st = time.time()
        self.jobs[(job_hash, st, weight)] = -1

        self.logger.info(
            f"job inserted: {job_hash} with weight {weight}\n"
            f"{self.__class__.__name__} - {sum([i[2] for i in self.jobs.keys()])} "
            f"weights using in throttle ~ {self.limit} per {self.interval}s"
        )

        return job_hash, st, weight

    def job_done(self, job_hash, st, weight):
        self.jobs[(job_hash, st, weight)] = time.time()

        self.logger.info(
            f"job done: {job_hash} with weight {weight}\n"
            f"{self.__class__.__name__} - {sum([i[2] for i in self.jobs.keys()])} "
            f"weights using in throttle ~ {self.limit} per {self.interval}s"
        )

    def okay_to_insert(self, weight) -> bool:
        if sum([i[2] for i in self.jobs.keys()]) <= self.limit - weight:
            return True
        else:
            return False

    def flush_old_jobs(self):
        ct = time.time()
        self.jobs = {
            job_key: end_time
            for job_key, end_time in self.jobs.items()
            if ((end_time == -1) or (ct - end_time < self.interval))
            and ((ct - job_key[1]) < 600)
        }


def throttling(throttle: APIThrottle, weight: int = 1):
    def decorator(func):
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_info = await throttle.insert_job(
                job_hash=f"{str(func)}{str(args)}{str(kwargs)}", weight=weight
            )

            try:
                if is_coroutine:
                    ret = await func(*args, **kwargs)
                else:
                    ret = func(*args, **kwargs)
            except Exception as e:
                raise e
            finally:
                throttle.job_done(*start_info)

            return ret

        return wrapper

    return decorator


def async_retry(retry_limit=5, retry_sleep=1, logger=DummyLogger(print_msg=False)):
    def decorator(async_func):
        @wraps(async_func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(1, retry_limit + 1):
                try:
                    ret = await async_func(*args, **kwargs)
                    return ret
                except Exception as e:
                    last_exception = e
                    logger.info(f"Retry! Error in step {i}\n" f"{e}\n")
                    await asyncio.sleep(retry_sleep)
                    continue
            raise last_exception

        return wrapper

    return decorator
