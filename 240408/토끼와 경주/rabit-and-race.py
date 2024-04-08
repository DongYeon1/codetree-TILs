'''
d가 10억 이고, L도 10억이기 때문에
이동 연산을 할때 선형연산을 해야한다.
최대 선출과정 연산 = 4,000,000
id는 딕셔너리로
id : [d,cnt,score] 형태

'''
from collections import defaultdict
import heapq

Q = int(input())
input_list = list(map(int, input().split()))
N = input_list[1]
M = input_list[2]
P = input_list[3]
pq_select = []
pid_d_dict = {}
pid_score_dict = {}
pid_rc_dict = {}
for i in range(1, P + 1):
    pid = input_list[(i + 1) * 2]
    pid_d = input_list[(i + 1) * 2 + 1]
    heapq.heappush(pq_select,(0,2,1,1,pid))
    pid_d_dict[pid] = pid_d
    pid_score_dict[pid] = 0
    pid_rc_dict[pid] = (0,0)

def in_board(r, c):
    if 1 <= r <= N and 1 <= c <= M:
        return True
    return False

def select_and_move_rabbit():
    global pq_select

    cnt, r_c, r, c, pid = heapq.heappop(pq_select)
    d = pid_d_dict[pid]
    score = pid_d_dict[pid]

    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    candidate_point = []
    for i in range(4):
        tr,tc = r, c
        if i == 0 or i == 2:
            real_d = d % ((M-1)*2)
        elif i == 1 or i == 3:
            real_d = d % ((N-1)*2)
        for _ in range(real_d):
            tr += dr[i]
            tc += dc[i]
            if not in_board(tr, tc):
                i = (i + 2) % 4
                tr += dr[i] * 2
                tc += dc[i] * 2
        candidate_point.append((tr, tc))
    fr, fc = 0, 0
    for tr, tc in candidate_point:
        if fr + fc < tr + tc:
            fr, fc = tr, tc
        elif fr + fc == tr + tc:
            if fr < tr:
                fr, fc = tr, tc
            elif fr == tr:
                if fc < tc:
                    fr, fc = tr, tc

    for tpid in pid_score_dict:
        s = fr + fc
        if tpid == pid:
            heapq.heappush(pq_select,(cnt+1,fr + fc,fr,fc,tpid))
            pid_rc_dict[tpid] = (fr,fc)
        else:
            pid_score_dict[tpid] += s
    #print("fr,fc:",fr,fc)
    return pid


def select_scoring_rabbit(moved_rabbit_set, S):
    global pq_select

    fr, fc = 0, 0
    fmr_pid = 0
    for mr_pid in moved_rabbit_set:
        tr, tc = pid_rc_dict[mr_pid]
        if fr + fc < tr + tc:
            fr, fc = tr, tc
            fmr_pid = mr_pid
        elif fr + fc == tr + tc:
            if fr < tr:
                fr, fc = tr, tc
                fmr_pid = mr_pid
            elif fr == tr:
                if fc < tc:
                    fr, fc = tr, tc
                    fmr_pid = mr_pid
                elif fc == tc:
                    if fmr_pid < mr_pid:
                        fmr_pid = mr_pid
    pid_score_dict[fmr_pid] += S


for _ in range(Q - 1):
    order = list(map(int, input().split()))
    # print(order)
    # print("--------------------")
    if order[0] == 200:
        K = order[1]
        S = order[2]
        moved_rabbit_set = set()
        for k in range(K):
            # print("round:",k+1)
            mr_pid = select_and_move_rabbit()
            moved_rabbit_set.add(mr_pid)
            # print(pid_d_dict)
            # print(pid_score_dict)
            # print(pid_rc_dict)
        select_scoring_rabbit(moved_rabbit_set, S)
        # print(pid_d_dict)
        # print(pid_score_dict)
        # print(pid_rc_dict)
    elif order[0] == 300:
        pid = order[1]
        L = order[2]
        pid_d_dict[pid] *= L
    elif order[0] == 400:
        max_score = 0
        for pid in pid_score_dict:
            max_score = max(max_score, pid_score_dict[pid])
        print(max_score)
    # print(pid_d_dict)
    # print(pid_score_dict)
    # print(pid_rc_dict)