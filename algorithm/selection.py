from utils.failed_schedule_exception import FailedScheduleException


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