n, k = 5, 4
g = [[1], [1], [1, 2], [2, 3], [3, 4]]
mt = [-1] * k
used = list()

def try_kuhn(v):
    if used[v]:
        return False
    used[v] = True
    i = 0
    while i < len(g[v]):
        to = g[v][i]-1
        if mt[to] == -1 or try_kuhn(mt[to]):
            mt[to] = v
            return True
        i += 1
    return False

for v in range(n):
    used = [False] * n
    try_kuhn(v)

for i in range(k):
    if mt[i] != -1:
        print(str(mt[i]+1), str(i+1))