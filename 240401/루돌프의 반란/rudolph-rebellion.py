'''
6:40
문제이해
좌상단 : 1,1
게임이 끝났을때 각 산타가 얻은 최종 점수

산타는 이미 산타가 있는 칸으로 움직일 수 없음
산타 정보에 좌표정보와 기절 스택 정보, 생존여부정보도 함께 저장
기절은 무조건 루돌프와 충돌한 직후에 생기므로
해당 K턴과 K+1턴 총 2번을 쉬어야한다. 즉, 충돌하면 기절 스택이 2로 업데이트된다.

제한조건
초기 산타 루돌프는 겹쳐져서 주어지지 않음
N, M, P, C, D

아이디어
단순 구현 문제
루돌프는 8가지 방향
산타는 4가지 방향
격자칸 정보는 편의상 1x1 부터 시작
0번째 있으면 격자바깥으로 나갔다고 간주
산타 정보는 [생존여부,기절스택,[r,c]] 로 저장
거리 계산은 (r1-r2)^2 + (c1-c2)^2

함수
# simulate()
M의 턴을 순서대로 진행, 루돌프, 산타들
한턴 끝나고 살아남는 산타들의 점수 업데이트 +1

# 거리 계산 함수(rr,rc,santa_idx)
(r1-r2)^2 + (c1-c2)^2

# rudolf_move(Rr,Rc)
먼저, 가장 가까운 산타를 찾고
8가지 방향으로 이동해본 후
해당 산타와 가장 가까워질 수 있는 방향으로 이동
추후 과정을 위해 리턴값을
어느방향으로 움직였는지와 충돌이 일어나는지 여부를 리턴함
u,ur,r,dr,d,dl,l,ul,u

#santa_move(santa_idx)
탈락했으면 pass
기절했으면 기절cnt -1
산타가 없는 게임판 내 이동 가능한 네가지 방향으로 이동해본 후
루돌프와 거리가 가장 가까워지는 방향으로 이동
가까워지지 않으면 이동 x
여러개와 가까워질 수 있으면 상우하좌 우선순위에 맞춰 이동
추후 과정을 위해 리턴값을
어느방향으로 움직였는지와 충돌이 일어나는지 여부를 리턴함
u,r,d,l

#bump(idx)
충돌이 일어나면 진행
점수 정산
만약 대각선 방향 충돌이라면 대각선 이동 1개가 1칸 움직임
밀려난 산타의 정보를 업데이트(생존여부,기절cnt,좌표)
밀려난 산타에 의해 생기는
상호작용 발생여부를 체크해야함

# interaction(idx)
bump 에 의해 확인되는 값으로 연쇄작용여부 판단
연쇄작용은 stack 으로 구현
stack 에 있는 모든 산타 정보 업데이트


좌표값은
1,1 ~ N,N까지
0 이나 N+1 부터는 게임판 바깥으로 나간 것으로 간주
'''

N, M, P, C, D = list(map(int,input().split()))
board = [[0 for _ in range(N+1)] for _ in range(N+1)]
Rr, Rc = list(map(int,input().split()))
santa_info = [0 for _ in range(P+1)]
for _ in range(P):
    Pn, Sr, Sc = list(map(int,input().split()))
    santa_info[Pn] = [True,0,[Sr,Sc],0]
santa_info[0] = [False,float("inf"),[0,0],0]

# print(N, M, P, C, D)
# print(Rr,Rc)
# print(santa_info)

dr = [-1,0,1,0,-1,1,1,-1] #0~3번째까지는 상우하좌
dc = [0,1,0,-1,1,1,-1,-1] #4~7번째까지는 상우,하우,하좌,상좌

def init_board(Rr,Rc,santa_info): #루돌프는 -1 번, 산타는 각 idx
    board[Rr][Rc] = -1
    for idx in range(1,len(santa_info)):
        Sr,Sc = santa_info[idx][2]
        board[Sr][Sc] = idx

def print_board(b):
    for i in range(1,len(b)):
        print(b[i][1:])
def distance(r1,c1,r2,c2):
    return (r1-r2)**2 + (c1-c2)**2

def in_board(r,c):
    global N
    if r <= 0 or r >= N + 1 or c <= 0 or c >= N + 1:
        return False
    return True

def rudolf_move(Rr,Rc,santa_info): #루돌프가 좌표바깥으로 이동하는 경우는 없는것 같아 고려해주지 않았음.
    c_santa_idx = 0
    c_dist = float("inf")
    for idx in range(1,len(santa_info)):
        alive, _, pos,_ = santa_info[idx]
        tSr, tSc = pos
        if alive == True:
            tmp_dist = distance(Rr,Rc,tSr,tSc)
            if c_dist > tmp_dist:
                c_santa_idx = idx
                c_dist = tmp_dist
            elif c_dist == tmp_dist:
                if santa_info[c_santa_idx][2][0] < tSr:
                    c_santa_idx = idx
                elif santa_info[c_santa_idx][2][0] == tSr:
                    if santa_info[c_santa_idx][2][1] < tSc:
                        c_santa_idx = idx
    # #가장 가까운 산타 찾기 완료
    # if c_dist == float("inf"):
    #     print("Error:c_dist is infinite")

    cSr , cSc = santa_info[c_santa_idx][2]
    c_direction = -1
    c_direction_dist = float("inf")
    for direction in range(8):
        nRr = Rr + dr[direction]
        nRc = Rc + dc[direction]
        t_direction_dist = distance(nRr,nRc,cSr,cSc)
        if c_direction_dist > t_direction_dist:
            c_direction_dist = t_direction_dist
            c_direction = direction
    #가장 가까워질 수 있는 방향 찾기 완료
    nRr = Rr + dr[c_direction]
    nRc = Rc + dc[c_direction]
    return nRr,nRc,c_direction,c_santa_idx

def bump_to_santa(direction,bumped_santa_idx):
    global board, C, D
    alive, rest_cnt, pos, score = santa_info[bumped_santa_idx]
    tSr,tSc = pos
    nSr = tSr + dr[direction]*C
    nSc = tSc + dc[direction]*C
    if in_board(nSr,nSc):
        if board[nSr][nSc] > 0: #밀려난 칸에 다른 산타가 있어서 상호작용이 발생하는 경우
            interaction(nSr,nSc,dr[direction],dc[direction])
        board[nSr][nSc] = bumped_santa_idx
        rest_cnt = 2
        pos = [nSr,nSc]
        score += C
        santa_info[bumped_santa_idx] = [alive,rest_cnt,pos,score]
    else:
        alive = False
        rest_cnt = float("inf")
        pos = [nSr,nSc]
        score += C
        santa_info[bumped_santa_idx] = [alive,rest_cnt,pos,score]

def interaction(tr,tc,tdr,tdc):
    global board
    stack = []
    while in_board(tr,tc) and board[tr][tc] > 0:
        stack.append(board[tr][tc])
        tr += tdr
        tc += tdc
    while stack:
        slided_santa_idx = stack.pop()
        pos = santa_info[slided_santa_idx][2]
        tr,tc = pos
        nr = tr + tdr
        nc = tc + tdc
        if in_board(nr,nc):
            board[nr][nc] = slided_santa_idx
            santa_info[slided_santa_idx][2] = [nr,nc]
        else:
            santa_info[slided_santa_idx][0] = False
            santa_info[slided_santa_idx][2] = [nr,nc]

def santa_move(Rr,Rc,idx):
    alive,rest_cnt,pos,score = santa_info[idx]
    tr, tc = pos
    if alive == False:
        return tr, tc, -1
    elif rest_cnt > 0:
        santa_info[idx][1] -= 1
        return tr, tc, -1
    cnr,cnc = [-1,-1]
    o_dist = distance(Rr,Rc,tr,tc)
    c_dist = float("inf")
    c_direction = -1
    for i in range(3,-1,-1):
        nr = tr + dr[i]
        nc = tc + dc[i]
        if in_board(nr,nc) == False or board[nr][nc] > 0:
            continue
        if distance(Rr,Rc,nr,nc) < o_dist and distance(Rr,Rc,nr,nc) <= c_dist:
            cnr = nr
            cnc = nc
            c_dist = distance(Rr,Rc,nr,nc)
            c_direction = i
    if [cnr,cnc] == [-1,-1]:
        return tr, tc, -1
    return cnr, cnc, c_direction

def bump_to_rudolf(direction,bumping_santa_idx):
    global board, D, Rr, Rc
    alive, rest_cnt, pos, score = santa_info[bumping_santa_idx]
    op_dr = dr[direction]*(-1)
    op_dc = dc[direction]*(-1)
    nSr = Rr + op_dr*D
    nSc = Rc + op_dc*D
    if in_board(nSr, nSc):
        if board[nSr][nSc] > 0:  # 밀려난 칸에 다른 산타가 있어서 상호작용이 발생하는 경우
            if board[nSr][nSc] != bumping_santa_idx:
                interaction(nSr, nSc, op_dr,op_dc)
        tr, tc = pos
        board[tr][tc] = 0
        board[nSr][nSc] = bumping_santa_idx
        rest_cnt = 1
        pos = [nSr, nSc]
        score += D
        santa_info[bumping_santa_idx] = [alive, rest_cnt, pos, score]
    else:
        tr,tc = pos
        board[tr][tc] = 0
        alive = False
        rest_cnt = float("inf")
        pos = [nSr,nSc]
        score += D
        santa_info[bumping_santa_idx] = [alive,rest_cnt,pos,score]

def print_santa_score(santa_info):
    result = ""
    for idx in range(1,len(santa_info)):
        result += str(santa_info[idx][3])
        result += " "
    return result.strip()

def print_score(santa_info):
    result = ""
    for idx in range(1,len(santa_info)):
        result += f"{idx}:{santa_info[idx][3]} "
    print("score:",result)

def print_rest_cnt(santa_info):
    result = ""
    for idx in range(1,len(santa_info)):
        result += f"{idx}:{santa_info[idx][1]} "
    print("r_cnt:",result)
def simulate():
    global Rr,Rc,santa_info,board
    init_board(Rr,Rc,santa_info)
    # print_board(board)
    for turn in range(1,M+1):
        # print("round:", turn)
        nRr,nRc,c_direction,target_santa_idx = rudolf_move(Rr,Rc,santa_info)
        if board[nRr][nRc] > 0: #루돌프가 산타에 충돌한 경우
            bump_to_santa(c_direction,target_santa_idx)
        board[Rr][Rc] = 0
        Rr = nRr
        Rc = nRc
        board[Rr][Rc] = -1
        # print("rudolf turn")
        # print_board(board)
        # print_score(santa_info)
        # print_rest_cnt(santa_info)
        # print("=====================")
        #루돌프 이동 끝나고, 산타가 번호순대로 움직일 차례
        for santa_idx in range(1, len(santa_info)):
            nSr,nSc,c_direction = santa_move(Rr, Rc, santa_idx)
            if c_direction != -1: #산타가 움직이는 경우
                if board[nSr][nSc] == -1: #산타가 루돌프에 충돌한 경우
                    bump_to_rudolf(c_direction, santa_idx)
                else: #산타가 그냥 이동한 경우
                    tSr,tSc = santa_info[santa_idx][2]
                    board[tSr][tSc] = 0
                    santa_info[santa_idx][2] = [nSr,nSc]
                    board[nSr][nSc] = santa_idx

        #산타이동이 끝나고, 이제 살아있는 산타들에게 +1 점씩
        for santa_idx in range(1, len(santa_info)):
            if santa_info[santa_idx][0] == True:
                santa_info[santa_idx][3] += 1
        # print("santa turn")
        # print_board(board)
        # print_score(santa_info)
        # print_rest_cnt(santa_info)
        # print("=====================")

    print(print_santa_score(santa_info))



simulate()