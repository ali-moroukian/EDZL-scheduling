from config import M
from models import Job


def run_edzl(tasks, cores):
    jobs, hyper_period = Job.generate_jobs_for_one_hyper_period(tasks)

    ready_queue = set()
    for time in range(hyper_period):
        for job in jobs:
            if job.start == time:
                ready_queue.add(job)
            elif job.start > time:
                break

        selected_jobs = select_jobs_for_edzl(ready_queue, time)

        run_jobs_with_load_balancing(selected_jobs, cores)

        for job in selected_jobs:
            if job.finished:
                ready_queue.remove(job)

        for job in jobs:
            if job.deadline == time and not job.finished:
                for c in cores:
                    print(c)
                # TODO: Report failure in scheduling
                raise Exception()


def select_jobs_for_edzl(ready_queue, time):
    ready_queue = sorted(ready_queue, key=lambda j: j.deadline)
    if len(ready_queue) <= M:
        return ready_queue
    selected_jobs = []
    for job in ready_queue:
        if job.laxity - time <= 0:
            selected_jobs.append(job)
    if len(selected_jobs) > M:
        # TODO: Report failure in scheduling
        raise Exception()
    for job in ready_queue:
        if len(selected_jobs) < M and job not in selected_jobs:
            selected_jobs.append(job)
        else:
            return selected_jobs


def run_jobs_with_load_balancing(jobs, cores):
    for i, core in enumerate(sorted(cores, key=lambda c: c.utilization)):
        if len(jobs) <= i:
            core.jobs.append(None)
            continue
        core.jobs.append(jobs[i])
        jobs[i].computed_time += 1
