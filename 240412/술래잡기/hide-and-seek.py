'''
n x n 격자 진행
술래는 정중앙 고정 (n은 반드시 홀수)
m명의 도망자, 도망자가 중앙 시작인 경우는 없음
좌우 유형 : 오른쪽 보고 시작
상하 유형 : 아래쪽 보고 시작
나무가 h개 있음
나무는 도망자와 초기에 겹쳐지는 것이 가능, 나무가 술래와 겹쳐질 수도 있음
k번 턴 진행 도망자 전체 동시에 1번, 술래 1번이 1턴
거리가 3이하인 도망자만 움직일 수 있음
거리는  |x1 - x2| + |y1 - y2|로 정의

도망자의 이동규칙
    바라보고 있는 방향으로 1칸 움직인다 가정
    격자 벗어나지 않는 경우
        다음칸에 술래가 있다면 움직이지 않음
        다음칸에 술래가 없다면 움직임 (나무가 있어도 움직임)
    격자 벗어나는 경우
        방향을 반대로 틀어줌
        반대방향 이동시 술래가 없다면 이동
        술래가 있다면 움직이지 않음

술래의 이동규칙
처음 위로 이동후 spiral 방식으로 움직임 (1,1,2,2,3,3,4,4, . . . )
1턴에 1칸만 이동
끝에 도달하면 다시 거꾸로 spiral하게 중앙으로 돌아옴
만약 이동방향이 틀어지는 구간이라면 이동 후 바로 고개를 돌려놓고 다음턴을 대기
(중앙과 (1,1) 에서도 이 규칙은 지켜져야함)
(nxn 크기가 어떻든 무조건 1,1 이 끝지점이다)
턴이 끝나기전 본인칸 포함 바라보고있는 방향 3칸 내 도망자를 잡음.
(항상 시야는 본인칸 포함 3칸)
이때 해당칸에 도망자가 있지만, 나무도 있으면 해당 도망자는 생존
잡힌 도망자는 보드에서 사라짐
현재 턴이 t턴이라면 t x 잡은 도망자 수 만큼 점수를 얻음 (턴은 1턴부터 시작)


아이디어
k턴 이후 술래가 얻게된 총 점수를 출력

술래의 위치 - 정수형 튜플
술래의 방향 - 정수
도망자의 위치 - 정수형 튜플 리스트
도망자의 방향 - 정수형 림스트
나무정보 보드 - 정수형 이차원 리스트
사람정보 보드 - 정수형 이차원 set (술래는 0번, 도망자는 각 idx, 외부벽은 -1)
나무정보 보드와

술래와 도망자보드 정보를 따로 초기화 및 업데이트

'''

from copy import deepcopy

#상우하좌
dr = [-1,0,1,0]
dc = [0,1,0,-1]
n, m, h, k = list(map(int, input().split()))
c_p = (n//2 + 1,n//2 + 1)
c_d = 0
c_s_d = 0
c_max= 1
c_cnt = 0
e_p = [(-1,-1)]
e_d = [-1]
t_board = [[0 for _ in range(n+1)] for _ in range(n+1)]
h_board = [[set() for _ in range(n+1)] for _ in range(n+1)]
score = 0

for e_n in range(1,m+1):
    p_r,p_c,d = list(map(int, input().split()))
    e_p.append((p_r,p_c))
    e_d.append(d)
for t in range(1,h+1):
    t_r,t_c = list(map(int, input().split()))
    t_board[t_r][t_c] = 1
h_board[c_p[0]][c_p[1]].add(-1)
for c_num in range(1,len(e_p)):
    r,c = e_p[c_num]
    h_board[r][c].add(c_num)

def direction(num):
    if num == 0:
        return "↑"
    elif num == 1:
        return "→"
    elif num == 2:
        return "↓"
    elif num == 3:
        return "←"

def print_all():
    global dr, dc, n, m, h, k, c_p, c_d, e_p, e_d, t_board, h_board, score
    print("t_board")
    for i,t in enumerate(t_board):
        if i == 0:
            continue
        s = ""
        for j,elem in enumerate(t):
            if j == 0:
                continue
            s += str(elem).rjust(10)
        print(s)
    print("-----------------------------")
    print("h_board")
    for i,h in enumerate(h_board):
        if i == 0:
            continue
        s = ""
        for j,elem in enumerate(h):
            if j == 0:
                continue
            s += str(elem).rjust(10)
        print(s)
    print("-----------------------------")
    print("tmp_direction")
    print(f"술래 방향:{direction(c_d)}")
    s = ""
    for e_num in range(1,m+1):
        s += f"도망자{e_num}번 방향:{direction(e_d[e_num])}, "
    print(s)
    print(f"현재점수:{score}")

#print_all()

def in_board(r,c):
    if 1 <= r <= n and 1 <= c <= n:
        return True
    return False

def escaper_move(e_num):
    global dr, dc, n, m, h, k, c_p, c_d, e_p, e_d, t_board, h_board

    tr, tc = e_p[e_num][0], e_p[e_num][1]
    td = e_d[e_num]
    nr = tr + dr[td]
    nc = tc + dc[td]
    if in_board(nr,nc):
        if -1 in h_board[nr][nc]:
            pass
        else:
            e_p[e_num] = (nr,nc)
            h_board[tr][tc].remove(e_num)
            h_board[nr][nc].add(e_num)
    else:
        e_d[e_num] = (td + 2) % 4
        td = e_d[e_num]
        nr = tr + dr[td]
        nc = tc + dc[td]
        if -1 in h_board[nr][nc]:
            pass
        else:
            e_p[e_num] = (nr,nc)
            h_board[tr][tc].remove(e_num)
            h_board[nr][nc].add(e_num)


def distance(c_p,e_p):

    return abs(c_p[0] - e_p[0]) + abs(c_p[1] - e_p[1])

def catcher_move():
    global dr, dc, n, m, h, k, c_p, c_d, c_s_d, c_max, c_cnt, e_p, e_d, t_board, h_board
    if c_s_d == 0: #밖으로 나가는경우면
        tr, tc = c_p[0], c_p[1]
        td = c_d
        if td == 0 or td == 1:
            nr = tr + dr[td]
            nc = tc + dc[td]
            c_cnt += 1
            if c_max == c_cnt:
                td += 1
                c_cnt = 0
                if td == 2:
                    c_max += 1
        elif td == 2 or td == 3:
            nr = tr + dr[td]
            nc = tc + dc[td]
            c_cnt += 1
            if c_max == c_cnt:
                td += 1
                c_cnt = 0
                if td == 4:
                    td = 0
                    c_max += 1
        c_p = (nr,nc)
        h_board[tr][tc].remove(-1)
        h_board[nr][nc].add(-1)
        c_d = td
        if (nr,nc) == (1,1): #바깥끝지점 도달한 경우
            c_s_d = 1
            c_d = 2
            c_cnt = 0
            c_max -= 1

    elif c_s_d == 1: #안으로 들어가는 경우면
        tr, tc = c_p[0], c_p[1]
        td = c_d
        if td == 1 or td == 0:
            nr = tr + dr[td]
            nc = tc + dc[td]
            c_cnt += 1
            if c_max == c_cnt:
                td -= 1
                c_cnt = 0
                if td == -1:
                    td = 3
                    c_max -= 1
        elif td == 3 or td == 2:
            nr = tr + dr[td]
            nc = tc + dc[td]
            c_cnt += 1
            if c_max == c_cnt:
                td -= 1
                c_cnt = 0
                if td == 1:
                    if (nr,nc) == (n,1):
                        pass
                    else:
                        c_max -= 1
        c_p = (nr, nc)
        h_board[tr][tc].remove(-1)
        h_board[nr][nc].add(-1)
        c_d = td
        if (nr, nc) == (n//2 + 1,n//2 + 1):  # 안쪽끝지점 도달한 경우
            c_s_d = 0
            c_d = 0
            c_cnt = 0
            c_max += 1

    '''

턴이 끝나기전 본인칸 포함 바라보고있는 방향 3칸 내 도망자를 잡음.
(항상 시야는 본인칸 포함 3칸)
이때 해당칸에 도망자가 있지만, 나무도 있으면 해당 도망자는 생존
잡힌 도망자는 보드에서 사라짐
현재 턴이 t턴이라면 t x 잡은 도망자 수 만큼 점수를 얻음 (턴은 1턴부터 시작)

    '''

def kill_escaper(turn_num):
    global dr, dc, n, m, h, k, c_p, c_d, e_p, e_d, t_board, h_board, score

    r, c = c_p[0], c_p[1]
    d = c_d
    for i in range(3):
        nr = r + dr[d]*i
        nc = c + dc[d]*i
        if in_board(nr,nc):
            for e_num in deepcopy(h_board[nr][nc]):
                if e_num != -1: #위험지역에 있는사람번호가 술래도 아니고
                    if t_board[nr][nc] != 1: #해당 자리에 나무도 없으면
                        e_p[e_num] = (-1,-1)
                        h_board[nr][nc].remove(e_num)
                        score += turn_num

def simulate():
    global dr, dc, n, m, h, k, c_p, c_d, e_p, e_d, t_board, h_board, score
    for turn_num in range(1,k+1):
        #print("================================================")
        #print(f"현재턴:{turn_num}")
        for e_num in range(1,m+1):
            if in_board(e_p[e_num][0],e_p[e_num][1]): #도망자가 아직 안죽었고,
                if distance(c_p,e_p[e_num]) <= 3: #술래와 거리가 3이하이면
                    escaper_move(e_num)
        #print_all()
        catcher_move()
        #print_all()
        kill_escaper(turn_num)
        #print_all()
    print(score)

simulate()