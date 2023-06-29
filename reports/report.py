from collections import defaultdict


def get_schedule_result(cores):
    result = defaultdict(list)
    for core in cores:
        for i, job in enumerate(core.jobs):
            if job:
                result[job.id].append([i, i + 1, core.id])
    for job, run_times in result.items():
        merged_result = []
        s, f, core_id = run_times[0]
        for i in run_times[1:]:
            if i[0] == f and core_id == i[2]:
                f = i[1]
            else:
                merged_result.append([s, f, core_id])
                s, f, core_id = i
        merged_result.append([s, f, core_id])
        result[job] = merged_result
    return [{'Job': key, 'Run Time': value} for key, value in result.items()]
