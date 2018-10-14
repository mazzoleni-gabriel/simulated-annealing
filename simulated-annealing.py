from random import *

#STATIC VARIABLES
FILE_NAME = "uf20-01.cnf"
ITERATIONS = 250000

#GLOBAL VARIABLES
clauses = []
variables = [] # 1 = true

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
    with open(FILE_NAME) as f:
        content = f.readlines()

    data = [[int(n) for n in line.split() if n != '0'] for line in content if line[0] not in ('c', 'p','%', '0')]

    return data

def lottery(prob):
    return False if randint(0, 100) > prob else True

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
    pos = randint(0, len(variables))
    if variables[pos] == 1:
        variables[pos] = 0
    else:
        variables[pos] = 1

def randomSearch():
    lastValue = 0
    for i in range (ITERATIONS):
        calculatedValue = calculateTrueClauses()
        if calculatedValue > lastValue:
            lastValue = calculatedValue
    return lastValue

initClausules()
initVariables()
print(randomSearch())
