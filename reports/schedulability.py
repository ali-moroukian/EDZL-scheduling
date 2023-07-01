import numpy

from algorithm.algorithm import get_tasks_and_cores, run_algorithm
from algorithm.assignments import run_jobs_with_load_balancing
from algorithm.selection import select_jobs_for_edzl, select_jobs_for_gedf
from config import MS
from reports.chart import draw_chart
from utils.failed_schedule_exception import FailedScheduleException


def run_schedulability(M, select_function):
    N = 20
    count = 100
    data = {0.0: 1.0}
    step = M / 40
    for U in numpy.arange(step, M, step):
        U = round(U, 1)
        passed = 0
        for i in range(count):
            try:
                tasks, cores = get_tasks_and_cores(M, N, U)
                run_algorithm(select_function, run_jobs_with_load_balancing, tasks, cores)
                passed += 1
            except FailedScheduleException:
                pass
        data[U] = passed / count
        print(f'{U} is done')
    return data


if __name__ == '__main__':
    for M in MS:
        edzl_result = run_schedulability(M, select_jobs_for_edzl)
        gedf_result = run_schedulability(M, select_jobs_for_gedf)
        draw_chart(edzl_result, gedf_result, f'{M}_chart.jpg')
