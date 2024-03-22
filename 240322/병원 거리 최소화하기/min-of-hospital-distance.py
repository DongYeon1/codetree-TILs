from itertools import combinations

n,m = list(map(int,input().split()))
matrix = []
persons = []
hospitals = []
for i in range(n):
    matrix.append(list(map(int,input().split())))

for r in range(n):
    for c in range(n):
        if matrix[r][c] == 1:
            persons.append((r,c))
        elif matrix[r][c] == 2:
            hospitals.append((r,c))

def hospital_comb(hospitals):
    comb_list = []
    for comb in combinations(hospitals,m):
        comb_list.append(list(comb))
    return comb_list

def min_distance(pr,pc,final_hospital_list):
    min_dist = float("inf")
    for hr,hc in final_hospital_list:
        min_dist = min(min_dist,abs(pr-hr) + abs(pc-hc))
    return min_dist


min_overall_dist = float("inf")
for final_hospital_list in hospital_comb(hospitals):
    overall_dist = 0
    for pr,pc in persons:
        overall_dist += min_distance(pr,pc,final_hospital_list)
    min_overall_dist = min(min_overall_dist,overall_dist)
print(min_overall_dist)