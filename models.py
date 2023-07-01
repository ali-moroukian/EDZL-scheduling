import math


class Task:
    def __init__(self, id_, period, utilization):
        self.id = id_
        self.period = period
        self.utilization = utilization

    @property
    def computation_time(self):
        return round(self.period * self.utilization, 1) or 0.1

    def __str__(self):
        return f'{self.period} {self.computation_time}'


class Job:
    def __init__(self, id_, s, d, c):
        self.id = id_
        self.start = s
        self.deadline = d
        self.computation = c
        self.finish = None
        self.computed_time = 0
        self.last_core = None

    @property
    def laxity(self):
        return self.deadline - (self.computation - self.computed_time)

    @property
    def finished(self):
        return self.computed_time == self.computation

    @staticmethod
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
        return sorted(jobs, key=lambda j: j.start), hyper_period

    def __str__(self):
        return f'{self.id} {self.start}'


class Core:
    def __init__(self, id_):
        self.id = id_
        self.jobs = []

    @property
    def utilization(self):
        if len(self.jobs) == 0:
            return 0
        return len([j for j in self.jobs if j is not None]) / len(self.jobs)

    def __str__(self):
        return ','.join(f'{j.id} {j.computation}' if j else 'IDLE' for j in self.jobs)
