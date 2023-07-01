from config import Algorithm
from models import Job
from utils.failed_schedule_exception import FailedScheduleException


def run_algorithm(algorithm, tasks, cores):
    jobs, hyper_period = Job.generate_jobs_for_one_hyper_period(tasks)

    select_function = select_jobs_for_edzl if algorithm == Algorithm.EDZL else select_jobs_for_gedf

    ready_queue = set()
    for time in range(hyper_period):
        for job in jobs:
            if job.start == time:
                ready_queue.add(job)
            elif job.start > time:
                break

        selected_jobs = select_function(len(cores), ready_queue, time)

        run_jobs_with_load_balancing(selected_jobs, cores)

        for job in selected_jobs:
            if job.finished:
                ready_queue.remove(job)

        for job in jobs:
            if job.deadline == time and not job.finished:
                raise FailedScheduleException(time, job)


def select_jobs_for_edzl(M, ready_queue, time):
    ready_queue = sorted(ready_queue, key=lambda j: j.deadline)
    if len(ready_queue) <= M:
        return ready_queue
    selected_jobs = []
    for job in ready_queue:
        if job.laxity - time <= 0:
            selected_jobs.append(job)
    if len(selected_jobs) > M:
        raise FailedScheduleException(time, selected_jobs[-1])
    for job in ready_queue:
        if len(selected_jobs) < M and job not in selected_jobs:
            selected_jobs.append(job)
        elif len(selected_jobs) == M:
            return selected_jobs


def select_jobs_for_gedf(M, ready_queue, time):
    ready_queue = sorted(ready_queue, key=lambda j: j.deadline)
    return ready_queue[:M]


def run_jobs_with_load_balancing(jobs, cores):
    for i, core in enumerate(sorted(cores, key=lambda c: c.utilization)):
        if len(jobs) <= i:
            core.jobs.append(None)
            continue
        core.jobs.append(jobs[i])
        jobs[i].computed_time += 1
        jobs[i].last_core = core


def run_jobs_with_less_context_switch(jobs, cores):
    core_index = 0
    cores_usued = []
    for job in jobs:
        if job.last_core and job.last_core not in cores_usued:
            core = job.last_core
        else:
            while cores[core_index] in cores_usued:
                core_index += 1
            core = cores[core_index]
            core_index += 1
        core.jobs.append(job)
        job.computed_time += 1
        job.last_core = core
        cores_usued.append(core)

    for core in cores:
        if core not in cores_usued:
            core.jobs.append(None)
