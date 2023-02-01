from aiohttp import web
from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from app import config

DEFAULT = "default"

job_stores = {
    DEFAULT: MemoryJobStore()
}
executors = {DEFAULT: AsyncIOExecutor()}
job_defaults = {"coalesce": False, "max_instances": 3, "misfire_grace_time": 3600}

scheduler = AsyncIOScheduler(
    jobstores=job_stores, executors=executors, job_defaults=job_defaults, timezone=utc
)


async def on_startup(_):
    scheduler.start()


async def on_shutdown(_: web.Application):
    scheduler.shutdown()


def setup(app: web.Application) -> None:
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
