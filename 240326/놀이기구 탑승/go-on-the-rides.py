'''
문제이해
학생들을 격자판에 일정한 규칙에 따라 배치하는 문제

제한조건
n은 3~20 최대 20x20 = 400 -> n^3 까지도 무리 없음

아이디어
n*n 학생들을 순서대로 받아와서
모든 좌표를 탐색해서 후보좌표를 선택하고 배치
모든 학생을 배치하면 최종적으로 점수 정산

함수
특정 픽셀의 상하좌우에 좋아하는 친구가 몇명있는지 리턴하는 함수
특정 픽셀의 상하좌우에 비어있는 칸이 몇개인지 리턴하는 함수
전체 픽셀을 탐색하며 조건1,2,3,4 를 만족하는 특정좌표를 정해주는 함수
전체 학생을 순회하는 함수
학생 배치 완료후 최종적으로 점수 정산하는 함수

자료구조
큐 안에 [n0,{n1~n4}] 의 구조로 초기화
'''
from collections import deque,defaultdict

n = int(input())
q = deque([])
like_dict = defaultdict(set)
for i in range(n*n):
    n0,n1,n2,n3,n4 = list(map(int,input().split()))
    q.append([n0,set([n1,n2,n3,n4])])
    like_dict[n0].add(n1)
    like_dict[n0].add(n2)
    like_dict[n0].add(n3)
    like_dict[n0].add(n4)
matrix = [[-1 for _ in range(n)] for _ in range(n)]
dr = [1,0,-1,0]
dc = [0,1,0,-1]

def valid(r,c):
    global n
    if 0 <= r < n and 0 <= c < n:
        return True
    return False

def count_like_blank(r,c,like_set):
    global matrix, n
    like_cnt = 0
    blank_cnt = 0
    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]
        if valid(nr,nc):
            if matrix[nr][nc] in like_set:
                like_cnt += 1
            if matrix[nr][nc] == -1:
                blank_cnt += 1
    return like_cnt, blank_cnt

def find_best_pos(like_set):
    global matrix, n
    mlc = 0
    mbc = 0
    best_pos = (0,0)
    for r in range(n):
        for c in range(n):
            if matrix[r][c] == -1:
                tlc,tbc = count_like_blank(r,c,like_set)
                if mlc < tlc:
                    mlc = tlc
                    mbc = tbc
                    best_pos = (r,c)
                elif mlc == tlc and mbc < tbc:
                    mbc = tbc
                    best_pos = (r,c)
                elif matrix[best_pos[0]][best_pos[1]] != -1:
                    best_pos = (r,c)
    return best_pos

def print_matrix():
    for r in range(len(matrix)):
        print(matrix[r])
    print("---------------------")
    
def simulate(queue):
    global matrix, n
    while queue:
        student_num, like_set = queue.popleft()
        fr,fc = find_best_pos(like_set)
        matrix[fr][fc] = student_num
        #print(print_matrix())

def calculate():
    global matrix, n
    result = 0
    for r in range(n):
        for c in range(n):
            like_set = like_dict[matrix[r][c]]
            lc, bc = count_like_blank(r,c,like_set)
            if lc == 1:
                result += 1
            elif lc == 2:
                result += 10
            elif lc == 3:
                result += 100
            elif lc == 4:
                result += 1000
    return result

#print(q)
simulate(q)
#print(matrix)
print(calculate())