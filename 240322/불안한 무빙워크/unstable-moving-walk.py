from collections import deque

n,k = list(map(int,input().split()))
u = deque([])
d = deque([])
input_list = list(map(int,input().split()))
for i in range(n):
    u.append((input_list[i],False))
for i in range(n,2*n):
    d.appendleft((input_list[i],False))
zero_count = 0
stage = 0

def rotate():
    d.append(u.pop())
    u.appendleft(d.popleft())

def move(idx):
    global zero_count
    if u[idx][1] == True:
        if idx+1 == n:
            u[idx] = (u[idx][0],False)
        else:
            num, occupied = u[idx+1]
            if occupied == False and num > 0:
                u[idx+1] = (num-1,True)
                if num-1 == 0:
                    zero_count += 1
                u[idx] = (u[idx][0],False)

def put_human():
    global zero_count
    num, occupied = u[0]
    if num > 0 and occupied == False:
        u[0] = (num-1,True)
        if num-1 == 0:
                zero_count += 1

def check_last():
    num, occupied = u[-1]
    if occupied == True:
        u[-1] = (num,False)

def simulate():
    global zero_count
    global stage
    while zero_count < k:
        stage += 1
        rotate()
        for i in range(n-1,-1,-1):
            move(i)
        put_human()
        check_last()

simulate()

print(stage)