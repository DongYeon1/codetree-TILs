'''
문제이해
밀려난 기사는 밀려난 위치에 함정이 있으면 데미지를 입음
밀려날때 연쇄적으로 밀려나는데,
마지막 밀려나는 기사 기준 벽이 있으면 안밀려져서 아무일도 안일어남

d는 0, 1, 2, 3 중에 하나이며 각각 위쪽, 오른쪽, 아래쪽, 왼쪽 방향

무조건 한칸씩 움직임

제한조건
체스판 최대 40x40
기사수 1명~30명
명령수 1~100
기사체력 1~100
-> 숫자 충분히 작기에 완전탐색 가능

아이디어
기사별로 인덱스를 부여하고 이를 명령을 받을때 활용
기사별 인덱스를 딕셔너리의 키로 활용하고 밸류값으로 기사들의 정보를 관리
벽과 기사의 정보만 담은 matrix에 기사별 인덱스를 이용하여 표시해두고 작업을 진행
밀려는 방향의 모든 칸수들이 dfs로 가장 끝에꺼까지 조사해서 미는게 가능한지 여부 확인
기사들의 위치가 업데이트 되었을때, 모든 밀쳐진 기사들 위의 함정갯수를 카운트해서 업데이트

# 특정기사가 특정방향으로 움직일때 움직여지는 기사 인덱스 리스트를 반환하는 함수(빈리스트면 못 움직이는 경우)
이동하려는 방향면의 픽셀들이 마주하는 번호를 탐색
해당 번호가 0 이면 q에 더 추가안함
해당 번호가 -2 이면 다 멈추고 반환리스트 빈리스트로 반환
해당 번호가 특정 번호면 해당 번호의 모든 방향면을 큐에 추가하고 해당 기사번호를 반환리스트에 추가


# 밀쳐질 기사들의 정보를 업데이트 하는 함수
만약 밀쳐질 기사들의 set 이 빈set이 아니라면,
맨처음 미는 기사의 정보를 미는 방향으로 업데이트 후
밀쳐질 기사들의 인덱스를 하나씩 받아와서
밀리는 방향으로 정보를 업데이트
이때 업데이트 방법은,
기준 픽셀인 r,c를 해당 방향으로 업데이트 해주면 끝
밀쳐진 기사들은 기준 픽셀을 업데이트 후,
본인의 범위이내에 trap이 몇개가 있는지 count 후 (아래 함수 사용)
해당 count 만큼 본인의 목숨도 업데이트
이때, 목숨이 0 이하면 max_matrix 에서 모든 본인 숫자 삭제후 0으로 초기화

# 특정 범위내 트랩이 몇개있는지 반환하는 함수

# 최종적으로 남은 기사들의 번호를 리턴하는 함수

# 최종적으로 남은 기사들의 초기 목숨수 - 최종적으로 남은 기사들의 최종 목숨수 의 합을 구하는 함수


코너케이스
밀려고 하는데 한칸씩 붙어서 계단식으로 합쳐지는 경우도 있음

살아있는 기사들을 대상으로만 데미지가 계산됨
죽어버린 기사는 체스판에서 사라짐


'''
from collections import defaultdict,deque
from copy import deepcopy

def print_matrix(m):
    for i in range(len(m)):
        print(m[i])

L,N,Q = list(map(int,input().split()))
trap_matrix = []
man_matrix = [[0 for _ in range(L)] for _ in range(L)]
man_dict = defaultdict(list)
order_q = deque([])

#함정체스판 초기화
for l in range(L):
    trap_matrix.append(list(map(int,input().split())))
for row in range(L):
    for col in range(L):
        if trap_matrix[row][col] == 1:
            trap_matrix[row][col] = -1
        elif trap_matrix[row][col] == 2:
            trap_matrix[row][col] = -2
            man_matrix[row][col] = -2

#기사 정보 및 기사체스판 초기화
for n in range(1,N+1):
    r,c,h,w,k = list(map(int,input().split()))
    man_dict[n].append(r)
    man_dict[n].append(c)
    man_dict[n].append(h)
    man_dict[n].append(w)
    man_dict[n].append(k)
    for row in range(r-1,r-1+h):
        for col in range(c-1,c-1+w):
            man_matrix[row][col] = n

#명령 초기화
for q in range(Q):
    order_q.append(list(map(int,input().split())))

initial_man_dict = deepcopy(man_dict)

#print_matrix(trap_matrix)
#print('----------------------------')
#print_matrix(man_matrix)
#print('----------------------------')
#print(initial_man_dict)
#print('----------------------------')
#print(order_q)

dr = [-1,0,1,0]
dc = [0,1,0,-1] 

def moved_man_set(index,direction):
    global man_matrix, man_dict, L, dr, dc

    visited = set()
    q = deque([])
    r,c,h,w,k = man_dict[index]
    #print("man_dict[index]:",man_dict[index])
    if k <= 0:
        return []


    if direction == 0: #위쪽
        for i in range(w):
            q.append((r-1,c-1+i))
    elif direction == 1: #오른쪽
        for i in range(h):
            q.append((r-1+i,c-1+w-1))
    elif direction == 2: #아래쪽
        for i in range(w):
            q.append((r-1+h-1,c-1+i))
    elif direction == 3: #왼쪽
        for i in range(h):
            q.append((r-1+i,c-1))
    #print("q:",q)
    while q:
        tr,tc = q.popleft()
        nr = tr + dr[direction]
        nc = tc + dc[direction]
        if nr < 0 or nr >= L or nc < 0 or nc >= L:
            return set()
        elif man_matrix[nr][nc] == 0:
            visited.add(man_matrix[tr][tc])
            #print(visited)
            #print("added")
        elif man_matrix[nr][nc] == -2:
            return set()
        else:
            if man_matrix[nr][nc] not in visited:
                visited.add(man_matrix[tr][tc])
                tmp_set = moved_man_set(man_matrix[nr][nc],direction)
                if len(tmp_set) != 0:
                    #print('Hello')
                    #print(tmp_set)
                    visited.update(tmp_set)
                    #print(visited)
                    #print('Hello')
                else:
                    return set()
    #print(visited)
    return visited

#print("moved_man_set(1,1):",moved_man_set(1,1))

def update_position(index,direction):
    global man_dict, dr, dc
    man_dict[index][0] += dr[direction]
    man_dict[index][1] += dc[direction]

def update_life(index):
    global man_dict, trap_matrix
    r,c,h,w,k = man_dict[index]
    for row in range(r-1,r-1+h):
        for col in range(c-1,c-1+w):
            if trap_matrix[row][col] == -1:
                man_dict[index][4] -= 1

def update_man_matrix():
    global man_matrix

    for r in range(L):
        for c in range(L):
            if man_matrix[r][c] != -2:
                man_matrix[r][c] = 0

    for key,value in man_dict.items():
        r,c,h,w,k = value
        if k <= 0:
            pass
        else:
            for row in range(r-1,r-1+h):
                for col in range(c-1,c-1+w):
                    man_matrix[row][col] = key

# 최종적으로 남은 기사들의 번호를 리턴하는 함수
def final_index_set(man_matrix):
    result_set = set()
    for r in range(L):
        for c in range(L):
            if man_matrix[r][c] != 0 and man_matrix[r][c] != -2:
                result_set.add(man_matrix[r][c])
    return result_set

# 최종적으로 남은 기사들의 초기 목숨수 - 최종적으로 남은 기사들의 최종 목숨수 의 합을 구하는 함수
def find_result(final_index_set):
    result = 0
    for index in final_index_set:
        result += initial_man_dict[index][4] - man_dict[index][4]
    return result

def simulate():
    global L, N, Q, trap_matrix, man_matrix, man_dict, order_q
    
    for index, direction in order_q:
        mms = moved_man_set(index,direction)
        #print(mms)
        if len(mms) != 0:
            for moving_index in mms:
                update_position(moving_index,direction)
                if moving_index != index:
                    update_life(moving_index)
            update_man_matrix()
        #print_matrix(trap_matrix)
        #print_matrix(man_matrix)
        #print(man_dict)
    print(find_result(final_index_set(man_matrix)))

simulate()