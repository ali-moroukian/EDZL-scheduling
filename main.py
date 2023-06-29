import math
from collections import defaultdict

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from config import *
from uunifast import uunifast


class Task:
    def __init__(self, id_, period, utilization):
        self.id = id_
        self.period = period
        self.utilization = utilization
        print(f'Task {self.id}', f'T={self.period}', f'C={self.computation_time}')

    @property
    def computation_time(self):
        return math.ceil(self.period * self.utilization)

    def __str__(self):
        return f'{self.period} {self.computation_time}'


class Job:
    def __init__(self, id_, s, d, c):
        self.id = id_
        self.s = s
        self.d = d
        self.c = c
        self.f = None
        self.executed_time = 0

    @property
    def laxity(self):
        return self.d - (self.c - self.executed_time)

    @property
    def finished(self):
        return self.executed_time == self.c

    def __str__(self):
        return f'{self.id} {self.s}'


class Core:
    def __init__(self, id_):
        self.id = id_
        self.tasks = []

    @property
    def utilization(self):
        return len([x for x in self.tasks if x is not None]) / len(task_set)

    def __str__(self):
        return ','.join(f'{t.id} {t.c}' if t else 'IDLE' for t in self.tasks)


def select_jobs_for_edzl(ready_queue, time):
    ready_queue = sorted(ready_queue, key=lambda j: j.d)
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
        if len(selected_jobs) < M:
            selected_jobs.append(job)
        else:
            return selected_jobs


def run_jobs_with_load_balancing(jobs, cores):
    # TODO: load balancing
    for i, core in enumerate(sorted(cores, key=lambda c: c.utilization)):
        if len(jobs) <= i:
            core.tasks.append(None)
            continue
        core.tasks.append(jobs[i])
        jobs[i].executed_time += 1


def edzl(tasks, cores):
    jobs, hyper_period = generate_jobs_for_one_hyper_period(tasks)

    ready_queue = set()
    for time in range(hyper_period):
        for job in jobs:
            if job.s == time:
                ready_queue.add(job)
            elif job.s > time:
                break

        selected_jobs = select_jobs_for_edzl(ready_queue, time)

        run_jobs_with_load_balancing(selected_jobs, cores)

        for job in selected_jobs:
            if job.finished:
                ready_queue.remove(job)

        for job in jobs:
            if job.d == time and not job.finished:
                for c in cores:
                    print(c)
                # TODO: Report failure in scheduling
                raise Exception()


def generate_jobs_for_one_hyper_period(tasks):
    hyper_period = math.lcm(*[t.period for t in tasks])
    jobs = []
    for t in tasks:
        for i in range(hyper_period // t.period):
            jobs.append(Job(
                id_=f'J{t.id},{i}',
                s=i * t.period,
                d=(i + 1) * t.period,
                c=t.computation_time
            ))
    return sorted(jobs, key=lambda j: j.s), hyper_period


def create_json(cores):
    result = defaultdict(list)
    for core in cores:
        for i, job in enumerate(core.tasks):
            if job:
                result[job.id].append([i, i + 1, core.id])
    for job, run_times in result.items():
        new_list = []
        s, f, core_id = run_times[0]
        for i in run_times[1:]:
            if i[0] == f and core_id == i[2]:
                f = i[1]
            else:
                new_list.append([s, f, core_id])
                s, f, core_id = i
        new_list.append([s, f, core_id])
        result[job] = new_list
    return [{'Job': key, 'Run Time': value} for key, value in result.items()]


def visualize(json_object):
    fig, ax = plt.subplots()

    task_ids = set()
    for job in json_object:
        task_id = int(job['Job'].split(',')[0][1:])
        task_ids.add(task_id)
        for i in job['Run Time']:
            ax.broken_barh(
                [[i[0], i[1] - i[0]]],
                [5 * task_id, 4],
                facecolors=list(mcolors.TABLEAU_COLORS.keys())[i[2]]
            )
    ax.set_yticks([i * 5 + 2 for i in range(len(task_ids))])
    ax.set_yticklabels([f"Task {id_}" for id_ in task_ids])

    plt.xlabel('Time')
    plt.ylabel('Job')
    plt.show()


if __name__ == '__main__':
    utilizations = uunifast(N, random.random() * M)
    task_set = []
    for k in range(N):
        task_set.append(Task(k, random.choice(PERIODS), utilizations[k]))

    core_set = []
    for k in range(M):
        core_set.append(Core(k))

    edzl(task_set, core_set)
    json_result = create_json(core_set)
    print(json_result)
    visualize(json_result)
