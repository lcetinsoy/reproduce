from src.lib.Experiment import Experiment


class BatchExperiment(Experiment):

    def __init__(self, experiments, parameters={}):
        name = "batch_experiment"
        super(BatchExperiment, self).__init__(name, parameters)
        self.experiments = experiments

    def run(self):

        for experiment in self.experiments:
            experiment.run()


