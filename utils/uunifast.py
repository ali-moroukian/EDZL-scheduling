import random


def uunifast(n, u):
    tries = 0
    while True:
        utilizations = []
        sumU = u
        for i in range(1, n):
            nextSumU = sumU * random.random() ** (1.0 / (n - i))
            utilizations.append(sumU - nextSumU)
            sumU = nextSumU
        utilizations.append(sumU)

        if all(ut <= 1 for ut in utilizations):
            return utilizations

        tries += 1
        if tries % 1000 == 0:
            print('UUnifast failed after 1000 tries!')
