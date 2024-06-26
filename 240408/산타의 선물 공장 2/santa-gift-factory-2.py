'''
아이디어
각 선물들의 속해있는 벨트 정보를 가지고 있을 필요가 없음.

각 선물들의 속해있는 벨트 정보를 모두 변경하면 안되고,
포인터만 바꿔주는 식으로 업데이트 해야함.
이렇게 하면, 선물 정보의 앞뒤를 얻을때 문제가 안됨.

즉, 그냥 양방향 링크드 리스트 문제 느낌임
각 선물들은 내 앞과 뒤 정보만 알고 있으면 되고,
내가 맨앞인지 맨뒤인지 정보만 알고 있으면 됨.

각 벨트들은 맨앞 맨뒤 선물번호와 몇개 들고 있는지만 알고 있으면 됨.
'''
import math

'''
제한조건
명령갯수 최대 10^5
벨트갯수 최대 10^5
선물갯수 최대 10^5
'''

'''
자료구조
벨트번호 = [[선물갯수,맨앞선물번호,맨뒤선물번호] . . . ] 선물이 없으면 맨앞,맨뒤번호가 -1 임
각 선물 = [[앞번호, 뒷번호] . . . ] 앞번호 뒷번호가 없으면 내가 맨 처음이거나 마지막인 경우, 이 경우는 -1 로 표현
'''

def make_factory(n,m,p_list):
    global b_num_list, p_num_list

    for _ in range(n):
        b_num_list.append([0,-1,-1])
    for _ in range(m):
        p_num_list.append([-1,-1])
    for idx,b_num in enumerate(p_list):
        p_num = idx + 1
        if b_num_list[b_num][0] == 0:
            b_num_list[b_num] = [1,p_num,p_num]
        elif b_num_list[b_num][0] >= 1:
            b_num_list[b_num][0] += 1
            p_num_list[b_num_list[b_num][2]][1] = p_num
            p_num_list[p_num][0] = b_num_list[b_num][2]
            b_num_list[b_num][2] = p_num

def move_all(m_src,m_dst):
    global b_num_list, p_num_list

    src_cnt = b_num_list[m_src][0]
    dst_cnt = b_num_list[m_dst][0]
    if src_cnt != 0:
        if dst_cnt == 0:
            b_num_list[m_dst] = b_num_list[m_src]
            b_num_list[m_src] = [0, -1, -1]
        else:
            new_start = b_num_list[m_src][1] #4
            src_end = b_num_list[m_src][2] #5
            b_num_list[m_src] = [0,-1,-1]
            b_num_list[m_dst][0] += src_cnt
            dst_start = b_num_list[m_dst][1] #3
            b_num_list[m_dst][1] = new_start #4
            p_num_list[dst_start][0] = src_end #5
            p_num_list[src_end][1] = dst_start #

    print(b_num_list[m_dst][0])

def move_front(m_src,m_dst): ## 3가지 케이스 다 테스트 돌려봐야함
    global b_num_list, p_num_list

    if b_num_list[m_src][0] == 0 and b_num_list[m_dst][0] == 0:
        pass
    elif b_num_list[m_src][0] == 0:
        dst_start = b_num_list[m_dst][1]
        dst_second = p_num_list[dst_start][1]
        b_num_list[m_src] = [1,dst_start,dst_start]
        p_num_list[dst_start] = [-1,-1]
        b_num_list[m_dst][0] -= 1
        if b_num_list[m_dst][0] == 0:
            b_num_list[m_dst][1] = -1
            b_num_list[m_dst][2] = -1
        else:
            b_num_list[m_dst][1] = dst_second
            p_num_list[dst_second][0] = -1
    elif b_num_list[m_dst][0] == 0:
        src_start = b_num_list[m_src][1]
        src_second = p_num_list[src_start][1]
        b_num_list[m_dst] = [1,src_start,src_start]
        p_num_list[src_start] = [-1,-1]
        b_num_list[m_src][0] -= 1
        if b_num_list[m_src][0] == 0:
            b_num_list[m_src][1] = -1
            b_num_list[m_src][2] = -1
        else:
            b_num_list[m_src][1] = src_second
            p_num_list[src_second][0] = -1
    else: #테스트 완료
        src_start = b_num_list[m_src][1]
        src_second = p_num_list[src_start][1]
        dst_start = b_num_list[m_dst][1]
        dst_second = p_num_list[dst_start][1]
        b_num_list[m_src][1] = dst_start
        b_num_list[m_dst][1] = src_start
        p_num_list[src_start][1] = dst_second
        p_num_list[dst_second][0] = src_start
        p_num_list[dst_start][1] = src_second
        p_num_list[src_second][0] = dst_start
        if b_num_list[m_src][0] == 1:
            b_num_list[m_src][2] = dst_start
        if b_num_list[m_dst][0] == 1:
            b_num_list[m_dst][2] = src_start


    print(b_num_list[m_dst][0])

def move_half(m_src,m_dst): #옮기지 않으면 출력하지 않는가?? 문제 설명이 애매
    global b_num_list, p_num_list

    n = b_num_list[m_src][0]

    if n > 1:
        target = n // 2
        src_start = b_num_list[m_src][1]
        target_p_num = src_start

        for _ in range(target-1):
            target_p_num = p_num_list[target_p_num][1]
        new_src_start = p_num_list[target_p_num][1]

        if b_num_list[m_dst][0] == 0:
            b_num_list[m_src][0] -= target
            b_num_list[m_dst][0] += target
            b_num_list[m_dst] = [target,src_start,target_p_num]
            p_num_list[src_start][0] = -1
            p_num_list[target_p_num][1] = -1
        else:
            dst_start = b_num_list[m_dst][1]
            b_num_list[m_src][0] -= target
            b_num_list[m_dst][0] += target
            p_num_list[dst_start][0] = target_p_num
            p_num_list[target_p_num][1] = dst_start
            p_num_list[new_src_start][0] = -1
            b_num_list[m_src][1] = new_src_start
            b_num_list[m_dst][1] = src_start

    print(b_num_list[m_dst][0])

def p_num_info(p_num):
    global b_num_list, p_num_list

    a = p_num_list[p_num][0]
    b = p_num_list[p_num][1]
    print(a+2*b)

def b_num_info(b_num):
    global b_num_list, p_num_list

    a = b_num_list[b_num][1]
    b = b_num_list[b_num][2]
    c = b_num_list[b_num][0]

    print(a + 2*b + 3*c)


b_num_list = [[]]
p_num_list = [[]]
q = int(input())
for stage in range(1,q+1):
    order = list(map(int,input().split()))
    #print(stage,":",order)
    if order[0] == 100:
        n = order[1]
        m = order[2]
        p_list = order[3:]
        make_factory(n, m, p_list)
        #print(b_num_list)
        #print(p_num_list)
    elif order[0] == 200:
        m_src = order[1]
        m_dst = order[2]
        move_all(m_src, m_dst)
        #print(b_num_list)
        #print(p_num_list)
    elif order[0] == 300:
        m_src = order[1]
        m_dst = order[2]
        move_front(m_src, m_dst)
        #print(b_num_list)
        #print(p_num_list)
    elif order[0] == 400:
        m_src = order[1]
        m_dst = order[2]
        move_half(m_src, m_dst)
        #print(b_num_list)
        #print(p_num_list)
    elif order[0] == 500:
        p_num = order[1]
        p_num_info(p_num)
    elif order[0] == 600:
        b_num = order[1]
        b_num_info(b_num)
    # print(b_num_list)
    # print(p_num_list)