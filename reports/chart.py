import matplotlib.pyplot as plt


def draw_chart(edzl_result, gedf_result, file_name):
    x1 = list(edzl_result.keys())
    y1 = list(edzl_result.values())
    x2 = list(gedf_result.keys())
    y2 = list(gedf_result.values())

    fig, ax = plt.subplots()
    ax.plot(x1, y1, label='edzl')
    ax.plot(x2, y2, label='gedf')
    ax.legend()

    ax.set_xlabel('Utilization')
    ax.set_ylabel('Schedulability')
    ax.set_title(file_name)

    plt.savefig(f'{file_name}.png')
    plt.show()
