N = 10  # No. of Tasks
MS = [4, 8, 16]  # No. of Cores

U = None # Utilization

PERIODS = [10, 20, 100]

REPORT_FILE_NAME = 'report.json'

MATPLOTLIB_COLORS = [
    'tab:blue',
    'tab:orange',
    'tab:green',
    'tab:red',
    'tab:purple',
    'tab:brown',
    'tab:pink',
    'tab:gray',
    'tab:olive',
    'tab:cyan',
    'black',
    'chocolate',
    'gold',
    'lime',
    'navy',
    'silver',
]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
