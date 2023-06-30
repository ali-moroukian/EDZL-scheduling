from config import *
from edzl import run_edzl
from models import Task, Core
from reports.report import get_schedule_result
from reports.report_file import write_on_file
from reports.visualization import visualize
from utils.failed_schedule_exception import FailedScheduleException
from utils.uunifast import uunifast

if __name__ == '__main__':
    utilizations = uunifast(N, random.random() * M)
    tasks = []
    for k in range(N):
        tasks.append(Task(k, random.choice(PERIODS), utilizations[k]))

    cores = []
    for k in range(M):
        cores.append(Core(k))

    try:
        run_edzl(tasks, cores)
        result = get_schedule_result(cores)
        print(result)
        visualize(result)
        write_on_file(result)

        for core in cores:
            print(core.utilization)

    except FailedScheduleException as e:
        print(f'{bcolors.FAIL}{e}{bcolors.ENDC}')
