# EDZL-scheduling

N Task

M Core

Tasks: Period, Utilization

Check Schedulability: U < m

---

Global EDF algorithm: Execute m task with the closest deadline, if there is not enough tasks some core will be idle.

EDZL algorithm: Earliest Deadline Zero Laxity: Algorithm applies global EDF as long as the laxity of jobs is greater
than zero.

---

Implementation:

- Generate tasks with uunifast algorithm
- Run EDZL algorithm
- Implement load balancing

- Inputs:
    - No. of Cores: [4, 8, 16]
    - Period of Tasks: [10, 20, 100]
    - C = u * T

- Outputs:
    - If tasks are schedulable: Json file of a hyper-period schedule. format:
      ```python
        [
          {
            "Job": "Job ID",
            "Run Time": [[start1, finish1], [start2, finish2], ...]
          },
          ...
        ]```
  else: Time of deadline miss & Job that misses its deadline.
    - DVFS result
    - Core utilizations
    - Rate of schedulability & Compare with global EDF
