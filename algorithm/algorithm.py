import numpy

from models import Job
from utils.failed_schedule_exception import FailedScheduleException


def run_algorithm(select_function, assign_function, tasks, cores):
    jobs, hyper_period = Job.generate_jobs_for_one_hyper_period(tasks)

    ready_queue = set()
    for time in list(numpy.arange(0, hyper_period, 0.1)):
        time = round(time, 1)
        for job in jobs:
            if job.start == time:
                ready_queue.add(job)
            elif job.start > time:
                break

        selected_jobs = select_function(len(cores), ready_queue, time)

        assign_function(selected_jobs, cores)

        for job in selected_jobs:
            if job.finished:
                ready_queue.remove(job)

        for job in jobs:
            if job.deadline == time and not job.finished:
                raise FailedScheduleException(time, job)
