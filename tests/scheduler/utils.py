"""Test helper functions"""

from asyncio import Task

from sqlalchemy.ext.asyncio import async_sessionmaker

from warden.lib.models import Job, Session


async def create_n_jobs(db_session_maker: async_sessionmaker, n_jobs: int):
    """Creates n_jobs mock jobs to run in the warden db"""
    SLURM_USER_ID = "1234"

    jobs_to_run = [
        Job(
            id=i,
            sequence="{}",
            status="PENDING",
            shots=100,
            session=Session(slurm_job_id=1, user_id=SLURM_USER_ID),
        )
        for i in range(n_jobs)
    ]

    async with db_session_maker() as session:
        session.add_all(jobs_to_run)
        await session.commit()


@staticmethod
def raise_main_scheduler_task_exception(task: Task) -> None:
    """
    The main scheduler is an infinite loop that we don't await
    so if it encounters an exception it fails silently
    and we don't see it when tests fail

    So if the task is done, it must have encoutered an exception
    """
    if task.done() and task.exception():
        raise task.exception()
    else:
        task.cancel()
