from algorithm.algorithm import get_tasks_and_cores, run_algorithm
from algorithm.assignments import run_jobs_with_load_balancing
from algorithm.selection import select_jobs_for_edzl, select_jobs_for_gedf
from config import PERIODS
from reports.chart import draw_chart
from utils.failed_schedule_exception import FailedScheduleException


def run_schedulability(M, select_function):
    N = 20
    count = 1000
    data = {}
    U = 0.1
    while U <= M:
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
        U = round(U + 0.1, 1)
    return data


if __name__ == '__main__':
    for M in PERIODS:
        result = run_schedulability(M, select_jobs_for_edzl)
        draw_chart(result, f'edzl_{M}.jpg')
        result = run_schedulability(M, select_jobs_for_gedf)
        draw_chart(result, f'gedf_{M}.jpg')
