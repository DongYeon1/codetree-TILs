from collections import deque
import math

matrix = []
n,L,R = list(map(int,input().split()))
for i in range(n):
    matrix.append(list(map(int,input().split())))
dr = [1,0,-1,0]
dc = [0,1,0,-1]
visited = set()
group_list = []


def init():
    global visited
    global group_list

    visited = set()
    group_list = []

def bfs(r,c):
    global visited
    group = [(r,c)]
    q = deque([(r,c)])
    while q:
        tr,tc = q.popleft()
        for i in range(4):
            nr = tr + dr[i]
            nc = tc + dc[i]
            if 0 <= nr < n and 0 <= nc < n and (nr,nc) not in visited:
                if L <= abs(matrix[nr][nc] - matrix[tr][tc]) <= R:
                    group.append((nr,nc))
                    visited.add((nr,nc))
                    q.append((nr,nc))
    return group


def grouping():
    global visited
    global group_list
    for r in range(n):
        for c in range(n):
            if (r,c) not in visited:
                visited.add((r,c))
                group_list.append(bfs(r,c))

def split():
    global group_list
    for group in group_list:
        tmp_sum = 0
        count = 0
        for r,c in group:
            tmp_sum += matrix[r][c]
            count += 1
        tmp_avg = math.floor(tmp_sum/count)
        for r,c in group:
            matrix[r][c] = tmp_avg

def simulate():
    stage = 0
    while True:
        init()
        grouping()
        if len(group_list) == n**2:
            print(stage)
            break
        else:
            stage += 1
            split()

simulate()