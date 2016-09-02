import datetime
import unittest
import sys


class QuantizeStepCalculator():
    def __init__(self):
        self.availableQuantizeSteps = [
            datetime.timedelta(seconds=1).seconds * 1000,
            datetime.timedelta(seconds=5).seconds * 1000,
            datetime.timedelta(seconds=10).seconds * 1000,
            datetime.timedelta(seconds=15).seconds * 1000,
            datetime.timedelta(seconds=30).seconds * 1000,
            datetime.timedelta(minutes=1).seconds * 1000,
            datetime.timedelta(minutes=5).seconds * 1000,
            datetime.timedelta(minutes=10).seconds * 1000,
            datetime.timedelta(minutes=15).seconds * 1000,
            datetime.timedelta(minutes=30).seconds * 1000,
            datetime.timedelta(hours=1).seconds * 1000,
            datetime.timedelta(hours=2).seconds * 1000,
            datetime.timedelta(hours=4).seconds * 1000,
            datetime.timedelta(hours=6).seconds * 1000,
            datetime.timedelta(hours=12).seconds * 1000,
            datetime.timedelta(days=1).days * 24 * 3600 * 1000,
            datetime.timedelta(days=7).days * 24 * 3600 * 1000]

    def calculateQuantizeStep(self, requestedDataPoints, maxPoints, queryTimeRange):
        dReq = queryTimeRange / requestedDataPoints
        dMax = queryTimeRange / maxPoints
        if dReq < self.availableQuantizeSteps[0]:
            return self.availableQuantizeSteps[0]

        if dReq > self.availableQuantizeSteps[len(self.availableQuantizeSteps) - 1]:
            return self.availableQuantizeSteps[len(self.availableQuantizeSteps) - 1]

        S = [step for step in self.availableQuantizeSteps if dMax <= step & step <= dReq]
        if len(S) != 0:
            return S[len(S) - 1]

        S1 = [step for step in self.availableQuantizeSteps if step >= dReq]
        return S1[0]


class QuantizeStepCalculatorTest(unittest.TestCase):
    def test_correctness(self):
        calculator = QuantizeStepCalculator()
        self.assertTrue(calculator.calculateQuantizeStep(5, 6, datetime.timedelta(seconds=60).seconds * 1000) == 10000)
        self.assertTrue(calculator.calculateQuantizeStep(5, 5, datetime.timedelta(seconds=60).seconds * 1000) == 15000)
        self.assertTrue(calculator.calculateQuantizeStep(5, 60, datetime.timedelta(seconds=60).seconds * 1000) == 10000)


if __name__ == '__main__':
    print("Usage: python calcQuantizeStep requestedDataPoints maxPoints queryTimeRangeInSeconds")
    if (len(sys.argv) != 4):
        print("Wrong inputs!!!!")
        print("Usage: python calcQuantizeStep requestedDataPoints maxPoints queryTimeRangeInSeconds")
        sys.exit(-1)

    requestedDataPoints = int(sys.argv[1])
    maxPoints = int(sys.argv[2])
    queryTimeRange = datetime.timedelta(seconds=int(sys.argv[3])).seconds * 1000
    calculator = QuantizeStepCalculator()
    quantizeStep = calculator.calculateQuantizeStep(requestedDataPoints, maxPoints, queryTimeRange)
    print ("Quantize Step Size is: {} seconds".format(quantizeStep / 1000))
    #unittest.main()
