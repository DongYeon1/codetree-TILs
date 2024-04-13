'''
bfs 를 활용해서 편의점에서 최단거리의 사용되지 않은 베이스 캠프를 구하는 함수

bfs 를 활용해서 편의점에서 최단거리의 다음 이동가능 칸을 구하는 함수

'''

import heapq
from copy import deepcopy

n,m = list(map(int,input().split()))
b_board = []
s_r = [-1]
s_c = [-1]
p_r = [-1]
p_c = [-1]
p_num_set = set()
f_num_set = set()

for _ in range(n):
    b_board.append(list(map(int,input().split())))
for _ in range(m):
    r,c = list(map(int,input().split()))
    s_r.append(r-1)
    s_c.append(c-1)

def print_all():
    global n, m, b_board, s_r, s_c, p_r, p_c, p_num_set, f_num_set

    print("b_board 현황")
    for b in b_board:
        s = ""
        for elem in b:
            s += str(elem).rjust(5)
        print(s)
    print("편의점 위치 정보")
    s = ""
    for i in range(1,len(s_r)):
        s += f"{i}번 편의점 위치:({s_r[i]},{s_c[i]}), "
    print(s)
    print("사람 위치 정보")
    s = ""
    for i in range(1,len(p_r)):
        s += f"{i}번 사람 위치:({p_r[i]},{p_c[i]}), "
    print(s)
    print(f"진행중인 사람 번호:{p_num_set}")
    print(f"끝난 사람 번호:{f_num_set}")


def in_board(r,c):
    global n
    if 0 <= r <= n-1 and 0 <= c <= n-1:
        return True
    return False

def find_best_base_camp(t):
    global n, m, b_board, s_r, s_c, p_r, p_c, p_num_set, f_num_set

    dr = [-1,0,0,1]
    dc = [0,-1,1,0]
    tr = s_r[t]
    tc = s_c[t]
    visited = set((tr,tc))
    min_heap = [(0,tr,tc)]

    while min_heap:
        cnt,r,c = heapq.heappop(min_heap)
        if b_board[r][c] == 1:
            return (r,c)
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if in_board(nr,nc) and (nr,nc) not in visited and b_board[nr][nc] != -1:
                visited.add((nr,nc))
                heapq.heappush(min_heap,(cnt+1,nr,nc))

def best_next(num):
    global n, m, b_board, s_r, s_c, p_r, p_c, p_num_set, f_num_set

    dr = [-1, 0, 0, 1]
    dc = [0, -1, 1, 0]
    tr = p_r[num]
    tc = p_c[num]
    possible_next = set()
    for i in range(4):
        nr = tr + dr[i]
        nc = tc + dc[i]
        if in_board(nr,nc) and b_board[nr][nc] != -1:
            possible_next.add((nr,nc))
    sr = s_r[num]
    sc = s_c[num]
    visited = set((sr,sc))
    pq = [(0,sr,sc)]
    while pq:
        cnt,r,c = heapq.heappop(pq)
        if (r,c) in possible_next:
            return r,c
        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]
            if in_board(nr, nc) and (nr,nc) not in visited and b_board[nr][nc] != -1:
                visited.add((nr,nc))
                heapq.heappush(pq,(cnt+1, nr, nc))

def simulate():
    global n, m, b_board, s_r, s_c, p_r, p_c, p_num_set, f_num_set
    t = 0
    #a = 0
    while len(f_num_set) < m:
    #while a < 5:
        #a += 1
        t += 1
        #print("=================================")
        #print(f"현재시간: {t}분")
        for p_num in deepcopy(p_num_set):
            nr,nc = best_next(p_num)
            p_r[p_num] = nr
            p_c[p_num] = nc
        #print("-----------------------------------")
        #print("모든 플레이어가 이동합니다.")
        #print_all()
        for p_num in deepcopy(p_num_set):
            if (p_r[p_num],p_c[p_num]) == (s_r[p_num],s_c[p_num]):
                p_num_set.remove(p_num)
                f_num_set.add(p_num)
                b_board[p_r[p_num]][p_c[p_num]] = -1
        #print("-----------------------------------")
        #print("편의점에 도착한 플레이어가 있다면 해당칸이 벽으로 바뀝니다.")
        #print_all()
        if t <= m:
            #t분에 t번 사람 best basecamp 에 놓기
            p_num_set.add(t)
            br,bc = find_best_base_camp(t)
            p_r.append(br)
            p_c.append(bc)
            b_board[br][bc] = -1
        #print("-----------------------------------")
        #print("베이스캠프에서 출발하는 플레이어가 있다면 해당칸이 벽으로 바뀝니다.")
        #print_all()

    print(t)

simulate()