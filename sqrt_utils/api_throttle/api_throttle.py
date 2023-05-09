import asyncio
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class APIThrottle:
    def __init__(self, api_limit: int, interval: int, logger=None):
        self.limit = api_limit
        self.interval = interval
        self.logger = logger
        self.jobs = {}  # (job_hash, start_time) -> end_time

    async def insert_job(self, job_hash):
        self.flush_old_jobs()

        if self.logger is not None:
            self.logger.info(
                f"{self.__class__.__name__} - {len(self.jobs)} jobs in throttle ~ {self.limit} per {self.interval}s"
            )

        while not self.okay_to_insert():
            await asyncio.sleep(0.01)
            self.flush_old_jobs()

        st = time.time()
        self.jobs[(job_hash, st)] = -1  # -1 means the job is not done yet

        return job_hash, st

    def job_done(self, job_hash, st):
        self.jobs[(job_hash, st)] = time.time()

    def okay_to_insert(self) -> bool:
        if len(self.jobs) < self.limit:
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


def throttling(throttle: APIThrottle):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_info = await throttle.insert_job(
                f"{str(func)}{str(args)}{str(kwargs)}"
            )

            try:
                if asyncio.iscoroutinefunction(func):
                    ret = await func(*args, **kwargs)
                else:
                    ret = func(*args, **kwargs)
            except Exception as e:
                throttle.job_done(*start_info)
                raise e

            throttle.job_done(*start_info)
            return ret

        return wrapper

    return decorator


def async_retry(retry_limit=5, retry_sleep=1, logger=None):
    def decorator(async_func):
        async def wrapper(*args, **kwargs):
            for i in range(1, retry_limit + 1):
                try:
                    ret = await async_func(*args, **kwargs)
                    return ret
                except Exception as e:
                    if logger is not None:
                        logger.info(f"Retry! Error in step {i}\n" f"{e}\n")
                    last_exception = e
                    await asyncio.sleep(retry_sleep)
                    continue
            raise last_exception

        return wrapper

    return decorator
