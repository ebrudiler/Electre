import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def indexConcordance(data: [], x: int, y: int):
    matrix = []
    temporaryX = data[x-1]
    temporaryY = data[y-1]
    for i, col in enumerate(temporaryX):
        res = 1 if col >= temporaryY[i] else 0
        matrix.append(res)
    
    return matrix

def concordance(data: [], w: []):
    result = []
    for x, row1 in enumerate(data):
        tmp = []
        for y, row2 in enumerate(data):
            if x is y:
                tmp.append(0)
            else:
                tmp_arr = indexConcordance(data, x+1, y+1)
                sum = 0
                for i, cell in enumerate(tmp_arr):
                    sum += 0 if cell is 0 else w[i]
                tmp.append(sum)
        result.append(tmp)
    result = np.array(result)     
    result = result.reshape(len(data), len(w))
    return result

def indexDiscondance(data: [], x: int, y: int):
    matrix = []
    temporaryX = data[x-1]
    temporaryY = data[y-1]
    for i, col in enumerate(temporaryX):
        res = 1 if col < temporaryY[i] else 0
        matrix.append(res)
    return matrix

def discondance(data: [], w:[]):
    result = []
    for x, row1 in enumerate(data):
        for y,row2 in enumerate(data):
            if x is y:
                result.append(0)
            else:
                index = indexDiscondance(data, x+1, y+1)
                paydaList = []
                payList = []
                for k in range(len(index)):
                    payda = abs(round((data[x][k] - data[y][k]), 3))
                    paydaList.append(payda)
                    paydaMax = max(paydaList)
                    
                    if index[k] == 1:
                        pay = round(abs(data[x][k] - data[y][k]), 3)
                        payList.append(pay)
                        payMax = max(payList)
                        temp = payMax/paydaMax
                    else:
                        pay = 0    
                tempResult = round((payMax/paydaMax), 3)
                
                result.append(tempResult)
    result = np.array(result)     
    result = result.reshape(len(data), len(w))             
    return result

def threshold(matrix: []):
    total = 0
    count = 0
    for row in matrix:
        count += 1
        for col in row:
            total += col
    return total / (count*(count-1))

def superority(matrix: [], threshold: float):
    res = []
    for row in matrix:
        tmp = []
        for col in row:
            x = 1 if col > threshold else 0
            tmp.append(x)
        res.append(tmp)
    return np.array(res)

def combined(first, second):
    result = []
    for i in range(len(first)):
        result.append(first[i]*second[i])
    return np.array(result)

def rank(matrix):
    rankList = []
    for i in range(len(matrix)):
        rankList.append(len(matrix) - sum(matrix[i]))
    return rankList

def electre(senarioNumber):
    if senarioNumber == 1:
        concordanceMatrix = concordance(decisionMatrix, weight1)
        discondanceMatrix = discondance(decisionMatrix, weight1)
    elif senarioNumber == 2:
        concordanceMatrix = concordance(decisionMatrix, weight2)
        discondanceMatrix = discondance(decisionMatrix, weight2)
    elif senarioNumber == 3:
        concordanceMatrix = concordance(decisionMatrix, weight3)
        discondanceMatrix = discondance(decisionMatrix, weight3)
    tresholdDiscondance = threshold(discondanceMatrix)
    tresholdConcordance = threshold(concordanceMatrix)
    superorityConcordanceMatrix = superority(concordanceMatrix, tresholdConcordance )
    superorityDiscondanceMatrix = superority(discondanceMatrix, tresholdDiscondance )
    combinedMatrix = combined(superorityConcordanceMatrix,superorityDiscondanceMatrix)
    ranking = rank(combinedMatrix)

    return ranking

def WSM(matrix, w):
    scoreList = []
    for x, row1 in enumerate(matrix):
        score = 0
        for y,row2 in enumerate(matrix):
            score += matrix[x][y]*w[y]
        scoreList.append(round(score, 3))
    scoreList = list(np.argsort(scoreList)+1)
    scoreList.reverse()
    return scoreList

# Getting Input

#counts = input().rstrip().split()
counts = [4, 4]
criteriasCount = int(counts[0])
alternativesCount = int(counts[1])
#weights = list(map(float, input().rstrip().split()))
weight1 = [0.174, 0.267, 0.367, 0.191]
weight2 = [0.25, 0.25, 0.25, 0.25]
weight3 = [0.367, 0.191, 0.174, 0.267]
#decisionMatrix = np.array(list(map(float, input().rstrip().split())))
decisionMatrix = np.array( [0.62, 0.85, 0.42, 0.5, 0.63, 0.76, 0.45, 0.58, 0.63, 0.71, 0.51, 0.63, 0.57, 0.49, 0.51, 0.69] ) 
decisionMatrix = list(decisionMatrix.reshape(criteriasCount,alternativesCount))

print(electre(1))
print(WSM(decisionMatrix, weight1))
result = electre(1)
result2 = WSM(decisionMatrix, weight1)

df=pd.DataFrame({'x': range(1,alternativesCount+1), 'electre': result, 'WSA': result2, })
plt.figure(figsize=(12,6))
plt.plot( 'x', 'electre', data=df, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=8)
plt.plot( 'x', 'WSA', data=df, marker='o', color='pink', markerfacecolor='red', linewidth=4)
plt.xlabel("Alternatives")

plt.ylabel("rank")
plt.title("Comparing result of Electre and WSA")

plt.legend()

#SenarioNumber = 2 (Butun kriterlerin agirliklari esit oldugu zaman meydana gelen)
print(electre(2))
#SenarioNumber = 3 (En dusuk agirliga sahip kritere, en yuksek agirlikli degeri verdigimizde meydana gelen)
print(electre(3))

result = electre(2)
result2 = electre(3)

df=pd.DataFrame({'x': range(1,alternativesCount+1), 'Senario1': result, 'Senario2': result2, })
plt.figure(figsize=(12,6))
plt.plot( 'x', 'Senario1', data=df, marker='o', markerfacecolor='blue', markersize=10, color='skyblue', linewidth=8)
plt.plot( 'x', 'Senario2', data=df, marker='o', color='pink', markersize=10, markerfacecolor='red', linewidth=4)
plt.xlabel("Alternatives")

plt.ylabel("RANK")
plt.title("Representation of senario 1 and senario 2")

plt.legend()
