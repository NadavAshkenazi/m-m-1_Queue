# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random
from queue import Queue
import sys
from collections import namedtuple
import math



class MessageQueue:
    def __init__(self, totalTime, arrivalRate, dispatchRate, probList):
        self.totalTime = int(totalTime)
        self.arrivalRate = int(arrivalRate)
        self.dispatchRate = int(dispatchRate)
        self.probList = probList

        self.messagesDispatched = 0
        self.messagesThrown = 0
        self.messagesInSystem = 0

        self.totalWaitTime = 0.0
        self.totalServiceTime = 0.0
        self.clock = 0.0

        self.nextArrival = random.expovariate(arrivalRate)
        self.nextDispatch = float('inf')
        self.Ti = [0 for i in range(len(probList))]

    def action(self, nextEvent):
        if nextEvent['Type'] == "arrival":
            self.messageArrive()
        else:
            self.messageDispatch()

    def messageArrive(self):
        prob = self.probList[self.messagesInSystem]
        if prob <= random.random():
            # dump message
            self.nextArrival = self.clock + random.expovariate(self.arrivalRate)
            self.messagesThrown += 1
            return
        # insert message into buffer
        self.messagesInSystem += 1

        # buffer was empty before arrival
        if self.messagesInSystem <= 1:
            messageDispatchTime = random.expovariate(self.dispatchRate)
            self.nextDispatch = self.clock + messageDispatchTime
            self.totalServiceTime += messageDispatchTime
        self.nextArrival = self.clock + random.expovariate(self.arrivalRate)

    def messageDispatch(self):
        # dispatch
        self.messagesDispatched += 1
        self.messagesInSystem -= 1

        #buffer is empty
        if self.messagesInSystem <= 0:
            self.nextDispatch = float('inf')
            return

        #buffer is not  empty
        messageDispatchTime = random.expovariate(self.dispatchRate)
        self.nextDispatch = self.clock + messageDispatchTime
        self.totalServiceTime += messageDispatchTime


    def run(self):
        while True:
            if self.nextArrival > self.totalTime:
                self.nextArrival = float('inf')
                if self.messagesInSystem == 0:
                    return

            nextEvent = {"Type": "", "Time": 0}
            if self.nextArrival < self.nextDispatch:
                nextEvent["Type"] = "arrival"
                nextEvent["Time"] = self.nextArrival
            else:
                nextEvent["Type"] = "dispatch"
                nextEvent["Time"] = self.nextDispatch

            self.totalWaitTime += (nextEvent['Time'] - self.clock) * self.messagesInSystem
            self.Ti[self.messagesInSystem] += (nextEvent['Time'] - self.clock)
            self.clock = nextEvent['Time']

            self.action(nextEvent)


    def analysis(self):
        return {"Y": self.messagesDispatched,
                "X": self.messagesThrown,
                "T'": self.clock,
                "Ti": self.Ti,
                "Zi": [i/self.clock for i in self.Ti],
                "Tw": self.totalWaitTime/self.messagesDispatched,
                "Ts": self.totalServiceTime/self.messagesDispatched,
                "LambdaA": self.messagesDispatched/self.totalTime}



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    args = sys.argv
    for i in list(range(1, len(args))):
        args[i] = float(args[i])
    simulationTimes = random.randint(10,100)
    resultSum = {"Y": 0, "X": 0, "T'": 0, "Ti": [0 for i in range(len(args[4:]))],
                 "Zi": [0 for i in range(len(args[4:]))], "Tw": 0, "Ts": 0, "LambdaA": 0}
    for i in range(simulationTimes):
        messageQueue = MessageQueue(totalTime=args[1], arrivalRate=args[2], dispatchRate=args[3], probList=args[4:])
        messageQueue.run()
        iterationRes = messageQueue.analysis()
        for key in resultSum.keys():
            if key == "Ti" or key == "Zi":
                resultSum[key] = [resultSum[key][i] + iterationRes[key][i] for i in range(len(iterationRes[key]))]
            else:
                resultSum[key] += iterationRes[key]
    avgResult = list()
    for key in resultSum.keys():
        if key == "Ti" or key == "Zi":
            avgResult.append([resultSum[key][i] / simulationTimes for i in range(len(iterationRes[key]))])
        else:
            avgResult.append(resultSum[key] / simulationTimes)
    resultString = ""
    for i in range(len(avgResult)):
        if i == 0 or i == 1:
            resultString += str(math.floor(avgResult[i])) + " "
        elif i == 3 or i == 4:
            resultString += " ".join(map(str, avgResult[i])) + " "
        else:
            resultString += str(avgResult[i]) + " "
    print(resultString)
