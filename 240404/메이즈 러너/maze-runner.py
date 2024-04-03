'''
문제이해
단순 구현 및 시뮬레이션
사람의 이동과 회전, 그리고 점수를 구하는 문제

제한조건
미로크기 최대 10x10
참가자수 1~10
게임시간 1~100

아이디어
(1,1)부터 시작
벽의 내구도 1~9
내구도 0 되면 빈칸
출구 도착하면 즉시 탈출
한칸 2명 참가자 있을 수 있음
상하 움직이는 우선

함수
시뮬레이션 함수
참가자 이동 함수
정사각형 선출 함수
정사각형 시계방향 90도 회전 함수(좌상단 좌표,크기)
'''

from collections import deque

N,M,K = list(map(int,input().split()))
board = [[-1 for _ in range(N+1)]]
p_r = [0 for _ in range(M+1)]
p_c = [0 for _ in range(M+1)]
move_cnt = 0
escape_cnt = 0
for _ in range(N):
    row = [-1]
    for elem in list(map(int, input().split())):
        if elem == 0:
            row.append(set())
        else:
            row.append(elem)
    board.append(row)
for i in range(1,M+1):
    r,c = list(map(int, input().split()))
    p_r[i] = r
    p_c[i] = c
    board[r][c].add(i)
r,c = list(map(int, input().split()))
p_r[0] = r
p_c[0] = c
board[r][c].add(0)

def print_board(board):
    print("-------------------------------------------------------------------")
    for r in range(1,N+1):
        row = ""
        for c in range(1,N+1):
            row = row + str(board[r][c]) + " "*(15-len(str(board[r][c])))
        print(row)

#print(N,M,K)
#print_board(board)

def in_board(r,c):
    global N
    if 1<=r<=N and 1<=c<=N:
        return True
    return False

def movable(r,c):
    if in_board(r,c) and type(board[r][c]) == set:
        return True
    return False
def distance(er,ec,pr,pc):
    return abs(er-pr) + abs(ec-pc)

def move_player():
    global N,M,K,board,move_cnt,escape_cnt
    ter, tec = p_r[0], p_c[0]
    dr = [0, 0, 1, -1]
    dc = [1, -1, 0, 0]
    for i in range(1,M+1):
        #print(f"p{i}")
        tpr,tpc = p_r[i],p_c[i]
        if not in_board(tpr,tpc):
            continue
        fnpr,fnpc = tpr,tpc
        for j in range(4):
            npr = tpr + dr[j]
            npc = tpc + dc[j]
            if movable(npr,npc):
                if distance(ter,tec,npr,npc) < distance(ter,tec,tpr,tpc):
                    fnpr, fnpc = npr,npc
        if fnpr != tpr or fnpc != tpc:
            p_r[i], p_c[i] = fnpr, fnpc
            board[tpr][tpc].remove(i)
            board[fnpr][fnpc].add(i)
            move_cnt += 1
            if p_r[i] == p_r[0] and p_c[i] == p_c[0]:
                p_r[i] = -1
                p_c[i] = -1
                board[fnpr][fnpc].remove(i)
                escape_cnt += 1

def make_square(er,ec,pr,pc): #보드 안에 있을때만 진행하도록 추가
    h = abs(er-pr) + 1
    w = abs(ec-pc) + 1
    side = max(h,w)
    sr,sc = min(er,pr),min(ec,pc)
    #print(sr,sc)
    if w > h:
        cnt = w-h
        while sr > 1 and cnt > 0:
            sr -= 1
            cnt -= 1
    elif h > w:
        cnt = h - w
        while sc > 1 and cnt > 0:
            sc -= 1
            cnt -= 1
    return sr,sc,side

def select_square():
    global N, M, K, board, move_cnt
    er = p_r[0]
    ec = p_c[0]
    fr,fc,fside = N+1,N+1,N+1
    for i in range(1,M+1):
        pr = p_r[i]
        pc = p_c[i]
        if pr == -1 and pc == -1:
            continue
        #print(er,ec,pr,pc)
        sr,sc,side = make_square(er,ec,pr,pc)
        #print(sr,sc,side)
        if fside > side:
            fr,fc,fside = sr,sc,side
        elif fside == side:
            if fr > sr:
                fr, fc, fside = sr, sc, side
            elif fr == sr:
                if fc > sc:
                    fr, fc, fside = sr, sc, side
    return fr, fc, fside

def rotate_square(sr,sc,side_len):
    global N, M, K, board, move_cnt
    if side_len == 1:
        if type(board[sr][sc]) == int:
            board[sr][sc] -= 1
        return
    if side_len == 0:
        return
    q = deque([])

    for i in range(side_len-1):
        q.append(board[sr][sc+i])

    for i in range(side_len-1):
        q.append(board[sr+i][sc+side_len-1])
    for i in range(side_len - 1):
        q.append(board[sr+side_len-1][sc+side_len-1-i])
    for i in range(side_len - 1):
        q.append(board[sr+side_len-1-i][sc])
    for i in range(len(q)):
        if type(q[i]) == int:
            q[i] -= 1
    for _ in range(side_len-1):
        q.appendleft(q.pop())
    for i in range(side_len-1):
        board[sr][sc+i] = q.popleft()
    for i in range(side_len - 1):
        board[sr + i][sc + side_len - 1] = q.popleft()
    for i in range(side_len - 1):
        board[sr + side_len - 1][sc + side_len - 1 - i] = q.popleft()
    for i in range(side_len - 1):
        board[sr + side_len - 1 - i][sc] = q.popleft()

    rotate_square(sr+1,sc+1,side_len-2)

def zero_to_set(sr,sc,side_len):
    global N, M, K, board, move_cnt
    for r in range(sr,sr+side_len):
        for c in range(sc,sc+side_len):
            if type(board[r][c])==int and board[r][c] == 0:
                board[r][c] = set()

def update_info():
    global N, M, K, board, move_cnt
    for r in range(1,N+1):
        for c in range(1,N+1):
            if type(board[r][c]) == set:
                for idx in board[r][c]:
                    p_r[idx] = r
                    p_c[idx] = c

def simulate():
    global N, M, K, board, move_cnt, escape_cnt
    #print_board(board)
    for i in range(1,K+1):
        move_player()
        #print(f"{i}초- 참가자 이동(총 이동횟수:{move_cnt})")
        #print_board(board)
        if escape_cnt == M:
            break
        sr,sc,side_len = select_square()
        #print(p_r[0],p_c[0])
        #print(sr,sc,side_len)
        rotate_square(sr, sc, side_len)
        zero_to_set(sr, sc, side_len)
        update_info()
        #print(f"{i}초 후 최종 결과")
        #print_board(board)
    print(move_cnt)
    print(p_r[0],p_c[0])

simulate()