from ..Metric import Metric

class PytorchAccuracyMetric(Metric):
    def __init__(self, name):
        super().__init__(name)


    def collect(self, data_loader):
        pass
