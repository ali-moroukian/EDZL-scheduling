import random

from config import *
from algorithm import run_algorithm
from models import Task, Core
from reports.report import get_schedule_result
from reports.report_file import write_on_file
from reports.visualization import visualize
from utils.failed_schedule_exception import FailedScheduleException
from utils.uunifast import uunifast

if __name__ == '__main__':
    M = random.choice(MS)
    utilizations = uunifast(N, random.random() * M)
    tasks = []
    print(f'{bcolors.HEADER}{N} Tasks:{bcolors.ENDC}')
    for k in range(N):
        tasks.append(Task(k, random.choice(PERIODS), utilizations[k]))

    cores = []
    print(f'{bcolors.OKCYAN}{M} Cores{bcolors.ENDC}')
    for k in range(M):
        cores.append(Core(k))

    try:
        run_algorithm(Algorithm.EDZL, tasks, cores)
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
