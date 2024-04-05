from collections import deque
from copy import deepcopy

N,M,K = list(map(int,input().split()))
graph = []
last_attack_timing = [[0 for _ in range(M)] for _ in range(N)]
alive_tower = set()

for i in range(N):
    graph.append(list(map(int,input().split())))

for r in range(N):
    for c in range(M):
        if graph[r][c] != 0:
            alive_tower.add((r,c))

# for g in graph:
#     print(g)
'''
문제이해
단순 구현 및 시뮬레이션
NxM 격자판
리턴값은 게임종료후 남아있는 포탑중 가장 강한 포탑 공격력 출력
최초에 0인 값 입력가능
최소 2개이상 1이상인 값 주어짐
부서지지 않은 포탑이 1개가 되는순간 그 즉시 중단.
즉, 포탑 부서짐 단계에서 중단됨.
공격자 및 공격당할자 선정을 위해서,
언제 공격했는지에 대한 정보도 리스트 인덱싱하에 저장되어야함
격자판을 넘어선 좌표에 접근할때는 반대편 격자로 이동할 수 있게
처리해줘야한다.
턴마다 이미 0 된 포탑을 제외한
해당턴에 공격하거나, 공격을 받을 포탑인지 아닌지 구분해서 저장해줘야한다.
이를 위해서
살아있는 포탑, 죽어있는 포탑, 공격과 관련된 포탑들을
저장하는 set을 가지면 좋을것 같다.
'''
def select_attacker(K): #K는 반드시 1부터 시작해서 K에 끝나야함
    global graph
    attacker = (float("inf"),-1,-1,0)
    for r in range(len(graph)):
        for c in range(len(graph[0])):
            if graph[r][c] == 0:
                continue
            if attacker[0] > graph[r][c]:
                attacker = (graph[r][c],r,c,last_attack_timing[r][c])
            elif attacker[0] == graph[r][c]:
                if attacker[3] < last_attack_timing[r][c]:
                    attacker = (graph[r][c], r, c,last_attack_timing[r][c])
                elif attacker[3] == last_attack_timing[r][c]:
                    if attacker[1] + attacker[2] < r+c:
                        attacker = (graph[r][c], r, c,last_attack_timing[r][c])
                    elif attacker[1] + attacker[2] == r+c:
                        if attacker[2] < c:
                            attacker = (graph[r][c], r, c,last_attack_timing[r][c])
    graph[attacker[1]][attacker[2]] += N+M
    last_attack_timing[attacker[1]][attacker[2]] = K
    return attacker

'''
함수
공격자 선정
0이 아닌 포탑중 가장 작은 숫자 포탑이 공격자로 선정
N+M만큼 공격력 영구 증가
숫자가 같은게 있을땐, 가장 최근에 공격한 포탑이 선정됨
그래도 똑같으면 행과열 합이 가장큰 포탑
그래도 똑같으면 열값이 가장 큰 포탑
(즉, 오른쪽아래로 갈수록 선정가능성 높음)
'''

def select_victim():
    global graph
    victim = (-1,N,M,1001)
    for r in range(len(graph)):
        for c in range(len(graph[0])):
            if graph[r][c] == 0:
                continue
            if victim[0] < graph[r][c]:
                victim = (graph[r][c], r, c,last_attack_timing[r][c])
            elif victim[0] == graph[r][c]:
                if victim[3] > last_attack_timing[r][c]:
                    victim = (graph[r][c], r, c,last_attack_timing[r][c])
                elif victim[3] == last_attack_timing[r][c]:
                    if victim[1] + victim[2] > r+c:
                        victim = (graph[r][c], r, c,last_attack_timing[r][c])
                    elif victim[1] + victim[2] == r+c:
                        if victim[2] > c:
                            victim = (graph[r][c], r, c,last_attack_timing[r][c])
    return victim

'''
공격자의 공격
자신을 제외한 가장 강한 포탑 공격
공격력이 가장 강한 포탑 선정
똑같으면 공격한지 가장 오래된 포탑
그래도 똑같으면, 행열합 가장 작은거
그래도 똑같으면, 열값이 가장 작은거
(즉, 왼쪽위로 갈수록 선정가능성 높음)
'''
def in_board(r,c):
    if 0 <= r < N and 0 <= c < M:
        return True
    else:
        return False

def convert_point(r,c):
    if r == -1:
        r = N-1
    if r == N:
        r = 0
    if c == -1:
        c = M-1
    if c == M:
        c = 0
    return r,c

def lazer_route(graph,attacker,victim):
    dr = [0,1,0,-1]
    dc = [1,0,-1,0]
    q = deque([])
    route = set()
    visited = set()
    start = (attacker[1], attacker[2])
    end = (victim[1],victim[2])
    route.add(start)
    visited.add(start)
    q.append((attacker[1], attacker[2], route))
    while q:
        tr, tc, troute = q.popleft()
        for i in range(4):
            nr = tr + dr[i]
            nc = tc + dc[i]
            if not in_board(nr,nc):
                nr,nc = convert_point(nr,nc)
            if graph[nr][nc] == 0 or (nr,nc) in visited:
                continue
            nroute = deepcopy(troute)
            nroute.add((nr, nc))
            visited.add((nr,nc))
            q.append((nr,nc,nroute))
            if (nr, nc) == end:
                return nroute
    return set()

#print(lazer_route(graph,select_attacker(graph,1),select_victim(graph)))

'''
공격의 종류(레이저, 포탄)

레이저공격
상하좌우 4방향
부서진 포탑은 지날수없음
격자 바깥으로 나가면 반대편으로 나옴
최단경로로 공격함
( min_heap bfs인데, 0인 포탑은 벽으로 간주
큐에 순서대로 상하좌우 순으로 넣을건데, visited 한거나, 0 인건 안넣음,
또, 좌표넘어가는건 반대편으로 출력되게 바꿔야되고, 
큐에 넣을때, 현좌표랑, 이제까지 진행해온 좌표들 세트 넣어놔야함
최종적으로 처음 도착하는 경로를 리턴 도착하는 경로가 없으면 포탄공격 시행 )

경로 길이가 똑같다면, 우하좌상 을 우선순위로 선택
그러한 경로가 없다면, 포탄 공격
레이저 공격을 받은 포탑은 공격한 포탑의 공격력 만큼 피해를 입고
경로상에 존재하는 모든 포탑을 //2 만큼 피해를 입힌다.
'''


def bomb_range(graph, attacker, victim):
    dr = [0, 1, 1, 1, 0, -1, -1, -1]
    dc = [1, 1, 0, -1, -1, -1, 0, 1]
    bomb_range = set()
    bomb_range.add((attacker[1], attacker[2]))
    bomb_range.add((victim[1], victim[2]))
    tr, tc = victim[1], victim[2]
    for i in range(8):
        nr = tr + dr[i]
        nc = tc + dc[i]
        if not in_board(nr, nc):
            nr, nc = convert_point(nr, nc)
        if graph[nr][nc] == 0 or (nr,nc) == (attacker[1], attacker[2]):
            continue
        bomb_range.add((nr,nc))
    return bomb_range

#print(bomb_range(graph, select_attacker(1), select_victim()))
'''
포탄공격
공격받은 포탑은 공격력만큼 피해를 입고
주위 8개 방향에 피해를 추가로 주는데 //2 만큼 준다.
단, 공격자는 영향을 받지 않는다.
만약 가장자리에 포탄이 떨어졌다면, 반대편 격자에 영향을 미친다.
'''

def attack(attacker,victim):
    global graph
    global alive_tower
    lazer_route_set = lazer_route(graph, attacker, victim)
    non_related_tower = deepcopy(alive_tower)
    power = graph[attacker[1]][attacker[2]]
    if len(lazer_route_set) != 0:
        for related in lazer_route_set:
            non_related_tower.remove(related)
        lazer_route_set.remove((attacker[1],attacker[2]))
        graph[victim[1]][victim[2]] -= power
        if graph[victim[1]][victim[2]] < 0:
            graph[victim[1]][victim[2]] = 0
        lazer_route_set.remove((victim[1],victim[2]))
        for r,c in lazer_route_set:
            graph[r][c] -= power//2
            if graph[r][c] < 0:
                graph[r][c] = 0
        return non_related_tower
    else: #포탄공격
        #print(attacker,victim)
        bomb_range_set = bomb_range(graph, attacker, victim)
        for related in bomb_range_set:
            non_related_tower.remove(related)
        bomb_range_set.remove((attacker[1],attacker[2]))
        graph[victim[1]][victim[2]] -= power
        if graph[victim[1]][victim[2]] < 0:
            graph[victim[1]][victim[2]] = 0
        bomb_range_set.remove((victim[1],victim[2]))
        for r,c in bomb_range_set:
            graph[r][c] -= power//2
            if graph[r][c] < 0:
                graph[r][c] = 0
        return non_related_tower
'''
포탑부서짐
공격 받아 공격력이 0 이하가 된 포탑은 부서져서 벽으로 변한다.
'''

def repair_tower(non_related_tower):
    global graph
    for r,c in non_related_tower:
        graph[r][c] += 1
'''
포탑정비
부서지지 않은 포탑중
해당턴에 공격을 받지 않은 포탑은 공격력이 1씩 오른다.
공격과 무관하다는 뜻은 공격자도 아니고 피해입은 포탑도 아니다.
'''

def find_max_and_count_not_zero():
    global graph
    global alive_tower

    alive_tower = set()
    max_val = -1
    not_zero_cnt = 0
    for r in range(len(graph)):
        for c in range(len(graph[0])):
            max_val = max(max_val,graph[r][c])
            if graph[r][c] != 0:
                not_zero_cnt += 1
                alive_tower.add((r,c))
    return max_val,not_zero_cnt


def simulate():
    global graph,N,M,K,last_attack_timing,alive_tower

    for turn in range(1,K+1):
        # for g in graph:
        #     print(g)

        victim = select_victim()
        attacker = select_attacker(turn)
        non_related_tower = attack(attacker, victim)
        max_val, not_zero_cnt = find_max_and_count_not_zero()
        if not_zero_cnt == 1:
            return max_val
        repair_tower(non_related_tower)
    max_val, not_zero_cnt = find_max_and_count_not_zero()
    return max_val

print(simulate())