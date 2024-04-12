'''
board 는 3차원 리스트로 관리,
각 칸에는 여러개의 총이 놓여질 수 있으므로
삽입과 삭제는 heap 을 활용
플레이어는 인덱스 별로 주어지므로 리스트를 활용
'''
import heapq

n,m,k = list(map(int,input().split()))
p_r = [0]
p_c = [0]
p_d = [0]
p_s = [1]
p_g = [0]
p_result = [0 for _ in range(m+1)]
g_board = [[[] for _ in range(n+1)]]
p_board = [[set() for _ in range(n+1)] for _ in range(n+1)]

for _ in range(n): #보드 입력 받기
    r = [[]]
    elems = list(map(int, input().split()))
    for elem in elems:
        if elem == 0:
            r.append([])
            continue
        r.append([-elem])
    g_board.append(r)
for p_num in range(1,m+1): #플레이어 입력 받기
    r,c,d,s = list(map(int, input().split()))
    p_r.append(r)
    p_c.append(c)
    p_d.append(d)
    p_s.append(s)
    p_g.append(0)
    p_board[r][c].add(p_num)

def print_all():
    global g_board, p_board, p_r, p_c, p_d, p_s, p_g, p_result
    print("총기 보드")
    for row in g_board: #현재 변수값 상황 프린트
        s = ""
        for elem in row:
            s += str(elem).rjust(10)
        print(s)
    print("사람 보드")
    for row in p_board:
        s = ""
        for elem in row:
            s += str(elem).rjust(10)
        print(s)

    for num in range(1,m+1):
        print(f"{num}번의 좌표: {(p_r[num], p_c[num])}, " +
              f"{num}번의 방향: {p_d[num]}, " +
              f"{num}번의 총합: {p_s[num]+p_g[num]}, " +
              f"{num}번의 현재 점수: {p_result[num]}")

#print_all()

def in_board(r,c):
    if 1 <= r <= n and 1 <= c <= n:
        return True
    return False

def player_move(p_num):
    global g_board, p_board, p_r, p_c, p_d, p_s, p_g, p_result
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    tr = p_r[p_num]
    tc = p_c[p_num]
    td = p_d[p_num]
    nr = tr + dr[td]
    nc = tc + dc[td]
    if not in_board(nr,nc):
        #print(f"플레이어 {p_num}번이 가려는 칸인 {nr, nc}가 격자 바깥이여서 고개를 반대로 돌립니다.")
        p_d[p_num] = (td + 2) % 4
        td = p_d[p_num]
        nr = tr + dr[td]
        nc = tc + dc[td]
    p_r[p_num] = nr
    p_c[p_num] = nc
    p_board[tr][tc].remove(p_num)
    p_board[nr][nc].add(p_num)
    #print(f"플레이어 {p_num}번이 {tr,tc}에서 {nr,nc}로 이동했습니다.")
    return nr,nc

def fight(p1_num,p2_num):
    #print(f"{p1_num} 과 {p2_num} 이 전투를 합니다.")
    global g_board, p_board, p_r, p_c, p_d, p_s, p_g, p_result
    diff = (p_s[p1_num] + p_g[p1_num]) - (p_s[p2_num] + p_g[p2_num])
    if diff > 0: #p1 이 승자
        p_result[p1_num] += diff
        #print(f"승자 {p1_num}이 점수 {diff}를 얻었습니다.")
        return p1_num,p2_num
    elif diff < 0: #p2 가 승자
        p_result[p2_num] += -diff
        #print(f"승자 {p2_num}이 점수 {-diff}를 얻었습니다.")
        return p2_num, p1_num
    else:
        #print(f"두 사람이 기존힘과 총의 합이 동일해 아무도 점수를 얻지 않았습니다.")
        #두명의 원래 힘이 같은 경우는 없음
        if p_s[p1_num] > p_s[p2_num]:
            return p1_num, p2_num
        elif p_s[p1_num] < p_s[p2_num]:
            return p2_num, p1_num

def loser_move(num):
    global g_board, p_board, p_r, p_c, p_d, p_s, p_g, p_result
    #print(f"패자인 {num}이 이동합니다.")
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    tr = p_r[num]
    tc = p_c[num]
    td = p_d[num]
    if p_g[num] != 0:
        heapq.heappush(g_board[tr][tc],-p_g[num])
        #print(f"들고 있던 총인 {p_g[num]} 를 자리에 놓습니다.")
        p_g[num] = 0
    nr = tr + dr[td]
    nc = tc + dc[td]
    while not in_board(nr,nc) or len(p_board[nr][nc]) >= 1:
        #print(f"{nr,nc} 에 사람이 있거나 격자밖이어서 오른쪽으로 90도 회전합니다.")
        p_d[num] = (td + 1) % 4
        td = p_d[num]
        nr = tr + dr[td]
        nc = tc + dc[td]
    p_r[num] = nr
    p_c[num] = nc
    p_board[nr][nc].add(num)
    #print(f"사람이 없고 격자안인 {nr, nc} 로 이동합니다.")
    get_best_gun(num)

def get_best_gun(num):
    global g_board, p_board, p_r, p_c, p_d, p_s, p_g, p_result

    r,c = p_r[num],p_c[num]
    if len(g_board[r][c]) >= 1:
        best_gun = -heapq.heappop(g_board[r][c])
        if p_g[num] == 0:
            p_g[num] = best_gun
            #print(f"플레이어 {num}번이 아무 총을 들고 있지 않다가, 공격력 {best_gun} 인 총을 들었습니다.")
        else:
            if p_g[num] < best_gun:
                heapq.heappush(g_board[r][c], -p_g[num])
                #print(f"플레이어 {num}번이 공격력 {p_g[num]} 인 총을 버리고, 공격력 {best_gun} 인 총을 들었습니다.")
                p_g[num] = best_gun
            else:
                heapq.heappush(g_board[r][c], -best_gun)
                #print(f"플레이어 {num}번이 공격력 {p_g[num]} 인 총은 그대로 유지하고 들고, 공격력 {best_gun} 인 총은 자리에 그대로 나뒀습니다.")
    #else:
        #print(f"플레이어 {num}번이 총을 주우려 했지만, 자리에 총이 한개도 없어 그냥 넘어갑니다.")


for round in range(1,k+1):
    #print("=============================================================================")
    #print(f"현재 라운드는 {round}라운드 입니다.")
    for p_num in range(1,m+1):
        #print("-------------------------------------------------------")
        #print(f"{p_num}번 플레이어가 이제 이동합니다.")
        r,c = player_move(p_num)
        if len(p_board[r][c]) != 2: #이동한 방향에 플레이어가 없는 경우
            #print(f"{p_num}번 플레이어가 이동한 자리에 사람이 없어서 총을 고릅니다.")
            get_best_gun(p_num)
        else: #이동한 방향에 플레이어가 있어서 싸우는 경우
            #print(f"{p_num}번 플레이어가 이동한 자리에 사람이 있어 전투가 일어났습니다.")
            p1_num = p_board[r][c].pop()
            p2_num = p_board[r][c].pop()
            winner, loser = fight(p1_num,p2_num)
            #print(f"결투가 있었고 승자는 {winner}, 패자는 {loser}입니다")
            loser_move(loser)
            p_board[r][c].add(winner)
            get_best_gun(winner)

        #print_all()
print(" ".join(map(str,p_result[1:])))

'''
시간복잡도 분석
k * m ( log(n*n) )
500 * 30 * log(400) -> 통과하고도 남음

코너케이스 분석


'''