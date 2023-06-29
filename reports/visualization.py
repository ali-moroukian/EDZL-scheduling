from matplotlib import pyplot as plt

from config import MATPLOTLIB_COLORS


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
                facecolors=MATPLOTLIB_COLORS[i[2]]
            )
    ax.set_yticks([i * 5 + 2 for i in range(len(task_ids))])
    ax.set_yticklabels([f"Task {id_}" for id_ in task_ids])

    plt.xlabel('Time')
    plt.ylabel('Job')
    plt.show()
