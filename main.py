import random

from algorithm.algorithm import run_algorithm, get_tasks_and_cores
from algorithm.assignments import *
from algorithm.selection import *
from config import *
from reports.report import get_schedule_result
from reports.report_file import write_on_file
from reports.visualization import visualize
from utils.failed_schedule_exception import FailedScheduleException

if __name__ == '__main__':
    M = random.choice(MS)
    utilization = U or random.random() * M
    print(f'{bcolors.OKCYAN}Utilization: {utilization}{bcolors.ENDC}')
    tasks, cores = get_tasks_and_cores(M, N, utilization)
    print(f'{bcolors.HEADER}{N} Tasks:{bcolors.ENDC}')
    for task in tasks:
        print(f'Task {task.id}', f'T={task.period}', f'C={task.computation_time}')

    print(f'{bcolors.OKCYAN}{M} Cores{bcolors.ENDC}')

    try:
        run_algorithm(select_jobs_for_edzl, run_jobs_with_less_context_switch_and_load_balance, tasks, cores)
        result = get_schedule_result(cores)
        print(f'{bcolors.HEADER}Result:{bcolors.ENDC}')
        print(result)
        visualize(result)
        write_on_file(result)

        print(f'{bcolors.HEADER}Cores utilization:{bcolors.ENDC}')
        for core in cores:
            print(core.utilization)

    except FailedScheduleException as e:
        print(f'{bcolors.FAIL}{e}{bcolors.ENDC}')
