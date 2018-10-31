from random import *
import matplotlib.pyplot as plt

#STATIC VARIABLES
FILE_NAME = "uf20-01"
FOLDER_NAME = "FORMULA"
ITERATIONS = 25000

#GLOBAL VARIABLES
clauses = []
variables = [] # 1 = true
lastVariable = 0;
results = []
temperature = 100
temperatureHistory = []
cont = 0

class Clause:
    def __init__(self, variables):
        self.variables = variables

    def isTrue(self):
        for i in range( len(self.variables) ):
            if not isVariableTrue(self.variables[i]):
                return False
        return True

def readFile():
    stringData = []
    data = []
    with open(FILE_NAME + '.cnf') as f:
        content = f.readlines()

    data = [[int(n) for n in line.split() if n != '0'] for line in content if line[0] not in ('c', 'p','%', '0')]

    return data

def lottery(prob):
    rand = randint(0, 100)
    return not rand >= prob

def lotteryFloat(prob):
    return not uniform(0, 100) >= prob

def initClausules():
    fileData = readFile()
    for i in range (len(fileData)):
        if len(fileData[i]) > 0:
            clauses.append(Clause(fileData[i]))

def initVariables():
    for i in range (getNVariables()):
        variables.append(0)
        if lottery(50):
            variables[i] = 1

def modulo(num):
    if num < 0:
        return num * (-1)
    return num

def isVariableTrue(variable):
    if variable > 0 and variables[modulo(variable)-1] == 1:
        return True
    if variable < 0 and variables[modulo(variable)-1] == 0:
        return True
    return False

def getNVariables():
    i = 2
    stringNVariables = ''
    while (FILE_NAME[i] != '-'):
        stringNVariables = stringNVariables + FILE_NAME[i]
        i = i + 1
    return int(stringNVariables)

def calculateTrueClauses():
    nTrue = 0
    for i in range (len(clauses)):
        if clauses[i].isTrue():
            nTrue = nTrue + 1
    return nTrue

def perturbate():
    global lastVariable
    pos = randint(0, len(variables)-1)
    while pos == lastVariable:
        pos = randint(0, len(variables)-1)
    lastVariable = pos
    if variables[pos] == 1:
        variables[pos] = 0
    else:
        variables[pos] = 1

def plotGraph(num):
    plt.cla()
    plt.plot(results)
    # plt.plot(results)
    plt.grid(True)
    plt.ylabel('best result')
    # plt.show()
    plt.savefig(FOLDER_NAME + '-' + FILE_NAME + '/' + str(num) + '-' + str(finalResuls) + '.png')

def randomSearch():
    lastValue = 0
    for i in range (ITERATIONS):
        perturbate()
        calculatedValue = calculateTrueClauses()
        if calculatedValue > lastValue:
            lastValue = calculatedValue
        results.append(calculatedValue)
    return lastValue

def updateTemperature(iteration):
    global temperature
    temperatureHistory.append(temperature)
    if temperature > 0:
        # temperature =  100/(iteration + 1) # y = 1/x
        # temperature = 100 - (iteration/ITERATIONS)*100
        # temperature = 50 - (iteration/ITERATIONS)*50
        # temperature = 20 - (iteration/ITERATIONS)*20
        temperature = 100*(0.000001/float(100))**(iteration/float(ITERATIONS))
        # 100*(13/float(100))**(iteration/float(ITERATIONS))
        # temperature = temperature*(1-0.01)
    # print (temperature)
    # print (iteration)


def simulatedAnnealing():
    lastValue = 0
    lastVariables = []
    lastTen = []
    global variables
    for i in range (ITERATIONS):
        lastVariables = variables.copy()
        perturbate()
        calculatedValue = calculateTrueClauses()
        if calculatedValue > lastValue:
            lastValue  = calculatedValue
        else:
            if lotteryFloat(temperature):
                lastValue  = calculatedValue
            else:
                variables = lastVariables.copy()
        results.append(calculatedValue)
        updateTemperature(i)
    return lastValue



initClausules()
initVariables()
# finalResuls = randomSearch()
for i in range(1):
    results = []
    finalResuls = simulatedAnnealing()
    print(finalResuls)
    plotGraph(i)

# plt.plot(temperatureHistory)
# # plt.plot(results)
# # plt.grid(True)
# plt.savefig('formula.png')
