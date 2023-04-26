import math
import time

alternativeRoute = []

def two_opt(route, dist_matrix, pred_matrix):
    n = len(route)
    improvement = True
    best_route = route
    best_distance = route_distance(route, dist_matrix)
    while improvement:
        improvement = False
        for i in range(0, n):
            for j in range(i, n):
                #print(str(i) + " - " + str(j))
                if i == j:
                    continue
                #print(str(i) + " <-> " + str(j))
                new_route = route[:]
                #print(str(route.index(i)) + " : " + str(route.index(j) + 1))
                #print(new_route)
                new_route[route.index(i)] = route[route.index(j)]
                new_route[route.index(j)] = route[route.index(i)]
                #print(new_route)
                if not check_pred(new_route, pred_hash):
                    #print("You can't")
                    continue
                new_distance = route_distance(new_route, dist_matrix)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_route = new_route
                    #print("Improvement")
                    improvement = True
                else:
                    alternativeRoute.append(new_route)
        route = best_route
    return best_route, best_distance


def route_distance(route, dist_matrix):
    distance = 0
    for i in range(len(route) - 1):
        distance += dist_matrix[route[i]][route[i+1]]
    return distance

def check_pred(route, pred_hash):
    for i in pred_hash:
        if(route.index(i) > route.index(pred_hash[i])):
            return False
    return True
'''
dist_matrix = [[0, 2, 6, 2],
                [4, 0, 8, 5],
                [6, 3, 0, 1],
                [4, 6, 1, 0]]


pred_hash = {0: 1, 1: 2, 3: 2}

route = [3, 0, 1, 2]
'''

import random

def generate_dist_matrix(size, max_val):
    random.seed(time.time())
    dist_matrix = []
    for i in range(size):
        row = []
        for j in range(size):
            if i == j:
                row.append(0)
            else:
                val = random.randint(1, max_val)
                row.append(val)
        dist_matrix.append(row)
    return dist_matrix

dist_matrix = generate_dist_matrix(20, 10)

pred_hash = {0: 4, 1: 3, 7: 8, 3: 6, 4: 11, 5: 14, 0: 9, 6: 9, 8: 9, 11: 15, 11: 14, 18: 11, 13: 12, 14: 17, 15: 19, 16: 18, 17: 19, 18: 19}

route = [0, 2, 1, 3, 6, 5, 4, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10]

n_experiement = 1
sum = 0
minMultistartList = []
for i in range(0, n_experiement):
    multiStart = int(len(route))
    dist_matrix = generate_dist_matrix(20, 50)
    #print("start Route : (" + str(route) + ", " + str(route_distance(route, dist_matrix)) + ")")
    result = two_opt(route, dist_matrix, pred_hash)
    #print("final Route : (" + str(result))
    resulMin = result
    min = result[1]
    c = 1
    minMultistart = 1
    for r in alternativeRoute[:multiStart-1]:
        #print("start Route : (" + str(r) + ", " + str(route_distance(r, dist_matrix)) + ")")
        result = two_opt(r, dist_matrix, pred_hash)
        #print("final Route : (" + str(two_opt(r, dist_matrix, pred_hash)))
        c += 1
        if(result[1] < min):
            resulMin = result
            min = result[1]
            minMultistart = c
            minMultistartList.append(minMultistart)
    sum += minMultistart

average = sum/n_experiement
print("Average : " + str(average))
sum2 = 0
for i in minMultistartList:
    sum2 += (i - average)**2

print("Variance : " + str(math.sqrt(sum2/n_experiement)))
print(minMultistartList)
#print("min : " + str(min))
#print("resulMin : " + str(resulMin))
#print("minMultistart : " + str(minMultistart))




