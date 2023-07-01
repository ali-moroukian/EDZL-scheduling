def list_rindex(li, x):
    for i in reversed(range(len(li))):
        if li[i] == x:
            return i
    return -1
