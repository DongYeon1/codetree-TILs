'''
d가 10억 이고, L도 10억이기 때문에
이동 연산을 할때 선형연산을 해야한다.
최대 선출과정 연산 = 4,000,000
id는 딕셔너리로
id : [d,cnt,score] 형태

'''
from collections import defaultdict

Q = int(input())
input_list = list(map(int, input().split()))
N = input_list[1]
M = input_list[2]
P = input_list[3]
pid_dict = defaultdict(list)
for i in range(1, P + 1):
    pid_dict[input_list[(i + 1) * 2]].append((1, 1))  # 좌표 0
    pid_dict[input_list[(i + 1) * 2]].append(input_list[(i + 1) * 2 + 1])  # d 1
    pid_dict[input_list[(i + 1) * 2]].append(0)  # cnt 2
    pid_dict[input_list[(i + 1) * 2]].append(0)  # score 3

pid_dict[0] = [(100001, 100001), float("inf"), float("inf"), 0]

#print(pid_dict)

# print(pid_dict)

def select_moving_rabbit():
    global pid_dict

    fpid = 0
    for tpid in pid_dict:
        if pid_dict[tpid][2] < pid_dict[fpid][2]:
            fpid = tpid
        elif pid_dict[tpid][2] == pid_dict[fpid][2]:
            if pid_dict[tpid][0][0] + pid_dict[tpid][0][1] < pid_dict[fpid][0][0] + pid_dict[fpid][0][1]:
                fpid = tpid
            elif pid_dict[tpid][0][0] + pid_dict[tpid][0][1] == pid_dict[fpid][0][0] + pid_dict[fpid][0][1]:
                if pid_dict[tpid][0][0] < pid_dict[fpid][0][0]:
                    fpid = tpid
                elif pid_dict[tpid][0][0] == pid_dict[fpid][0][0]:
                    if pid_dict[tpid][0][1] < pid_dict[fpid][0][1]:
                        fpid = tpid
                    elif pid_dict[tpid][0][1] == pid_dict[fpid][0][1]:
                        if tpid < fpid:
                            fpid = tpid
    if fpid == 0:
        raise

    return fpid


def in_board(r, c):
    if 1 <= r <= N and 1 <= c <= M:
        return True
    return False


def move_rabbit(pid):
    global pid_dict

    point, d, cnt, score = pid_dict[pid]
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    candidate_point = []
    for i in range(4):
        tr, tc = point
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
    for update_pid in pid_dict:
        if update_pid == pid:
            pid_dict[pid] = [(fr, fc), d, cnt + 1, score]
        else:
            pid_dict[update_pid][3] += fr + fc


def select_scoring_rabbit(moved_rabbit_set, S):
    global pid_dict

    fr, fc = 0, 0
    fmr_pid = 0
    for mr_pid in moved_rabbit_set:
        tr, tc = pid_dict[mr_pid][0]
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
    pid_dict[fmr_pid][3] += S


for _ in range(Q - 1):
    order = list(map(int, input().split()))
    #print(order)
    if order[0] == 200:
        K = order[1]
        S = order[2]
        moved_rabbit_set = set()
        for _ in range(K):
            mr_pid = select_moving_rabbit()
            move_rabbit(mr_pid)
            moved_rabbit_set.add(mr_pid)
            #print(pid_dict)
        select_scoring_rabbit(moved_rabbit_set, S)
        #print(pid_dict)
    elif order[0] == 300:
        pid = order[1]
        L = order[2]
        pid_dict[pid][1] *= L
    elif order[0] == 400:
        max_score = 0
        for pid in pid_dict:
            max_score = max(max_score, pid_dict[pid][3])
        print(max_score)