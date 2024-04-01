'''
문제 이해
단순 구현 및 시뮬레이션 문제

제한조건
격자 크기 최대 25x25
라운드 수 최대 1~100


아이디어

그래프에서 순차적으로 큐에 넣음

큐, 리스트, 재귀, 반복, 회전, 디버깅을 위한 프린트 구현

함수
그래프 정보를 통해 순차적으로 큐를 만들어 표현하는 함수
큐 정보를 통해 순차적으로 그래프를 만드는 함수
큐 정보를 통해 새로운 큐를 만드는 함수

과정
상하좌우 공격에 의해 큐에 있는 원소들을 제거하는 과정
큐에 있는 원소들을 순차탐색하여 연속 4개 나오면 제거하는 과정 (없을때까지 반복)
큐 정보를 활용해 새로운 큐를 만드는 과정
큐에 있는 원소들을 다시 그래프로 표현하는 과정
라운드가 다 소진될때까지 반복
'''

from collections import deque

n,m = list(map(int,input().split()))
board = []
d_round= []
p_round = []
score = 0
for _ in range(n):
    board.append(list(map(int,input().split())))
for _ in range(m):
    d,p = list(map(int,input().split()))
    d_round.append(d)
    p_round.append(p)


# for l in board:
#     print(l)
# print(d_round)
# print(p_round)

def in_board(r,c):
    global n

    if 0 <= r <= n-1 and 0 <= c <= n-1:
        return True
    return False

def not_zero(r,c):
    global board
    if board[r][c] == 0:
        return False
    return True

def list_from_board(board,n):
    num_list = []
    tn_r = n//2
    tn_c = n//2
    for rotate in range(3,n+1,2):
        tn_c -= 1
        if in_board(tn_r,tn_c) and not_zero(tn_r,tn_c):
            num_list.append(board[tn_r][tn_c])
        else:
            return num_list
        for down in range(rotate-2):
            tn_r += 1
            if in_board(tn_r,tn_c) and not_zero(tn_r,tn_c):
                num_list.append(board[tn_r][tn_c])
            else:
                return num_list
        for right in range(rotate-1):
            tn_c += 1
            if in_board(tn_r,tn_c) and not_zero(tn_r,tn_c):
                num_list.append(board[tn_r][tn_c])
            else:
                return num_list
        for up in range(rotate-1):
            tn_r -= 1
            if in_board(tn_r,tn_c) and not_zero(tn_r,tn_c):
                num_list.append(board[tn_r][tn_c])
            else:
                return num_list
        for left in range(rotate-1):
            tn_c -= 1
            if in_board(tn_r,tn_c) and not_zero(tn_r,tn_c):
                num_list.append(board[tn_r][tn_c])
            else:
                return num_list
    return num_list

def remove_zero(num_list):
    new_num_list = []
    for num in num_list:
        if num == 0:
            continue
        new_num_list.append(num)
    return new_num_list

def attack(direction,p_num, num_list):
    global score

    if direction == 0: #오른쪽
        ti = 4
        step = 13
    elif direction == 1: #아래
        ti = 2
        step = 11
    elif direction == 2: #왼쪽
        ti = 0
        step = 9
    elif direction == 3: #위쪽
        ti = 6
        step = 15

    for p in range(1,p_num+1):
        if ti > len(num_list)-1:
            break
        score += num_list[ti]
        num_list[ti] = 0
        ti += step
        step += 8

    new_num_list = remove_zero(num_list)

    return new_num_list

def interaction(num_list):
    global score
    flag = 0
    new_num_list = []
    stack = []
    for idx,num in enumerate(num_list):
        if stack:
            if stack[-1][1] == num:
                stack.append((idx,num))
            else:
                if len(stack) >= 4:
                    for i,n in stack:
                        score += n
                        num_list[i] = 0
                    flag = 1
                    stack = [(idx,num)]
                else:
                    stack = [(idx,num)]
        else:
            stack.append((idx,num))
    if stack:
        if len(stack) >= 4:
            for i, n in stack:
                score += n
                num_list[i] = 0
            flag = 1

    if flag == 0:
        return num_list, flag

    new_num_list = remove_zero(num_list)

    return new_num_list, flag

def update_num_list(num_list):
    updated_num_list = []
    stack = []
    for num in num_list:
        if stack:
            if stack[-1] == num:
                stack.append(num)
            else:
                updated_num_list.append(len(stack))
                updated_num_list.append(stack[-1])
                stack = [num]
                if len(updated_num_list) > (n**2)-1:
                    updated_num_list = updated_num_list[:(n**2)-1]
                    stack = []
                    break
        else:
            stack.append(num)
    if stack:
        updated_num_list.append(len(stack))
        updated_num_list.append(stack[-1])
        if len(updated_num_list) > (n**2)-1:
            updated_num_list = updated_num_list[:(n**2)-1]

    return updated_num_list


def simulate():
    global board,n,m,d_round,p_round,score
    num_list = list_from_board(board,n)
    for i in range(m):
        direction = d_round[i]
        p_num = p_round[i]
        num_list = attack(direction,p_num, num_list)
        num_list, flag = interaction(num_list)
        while flag == 1:
            num_list, flag = interaction(num_list)
        num_list = update_num_list(num_list)
    return score

print(simulate())