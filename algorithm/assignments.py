def run_jobs_with_load_balancing(jobs, cores):
    for i, core in enumerate(sorted(cores, key=lambda c: c.utilization)):
        if len(jobs) <= i:
            core.jobs.append(None)
            continue
        core.jobs.append(jobs[i])
        jobs[i].computed_time = round(jobs[i].computed_time + 0.1, 1)
        jobs[i].last_core = core


def run_jobs_with_less_context_switch(jobs, cores, load_balance=False):
    cores = list(sorted(cores, key=lambda c: c.utilization))
    core_index = 0
    cores_usued = []
    for job in jobs:
        if job.last_core and job.last_core not in cores_usued and (not load_balance or job.last_core.jobs[-1] == job):
            core = job.last_core
        else:
            while cores[core_index] in cores_usued:
                core_index += 1
            core = cores[core_index]
            core_index += 1
        core.jobs.append(job)
        job.computed_time = round(job.computed_time + 0.1, 1)
        job.last_core = core
        cores_usued.append(core)

    for core in cores:
        if core not in cores_usued:
            core.jobs.append(None)


def run_jobs_with_less_context_switch_and_load_balance(jobs, cores):
    run_jobs_with_less_context_switch(jobs, cores, True)
