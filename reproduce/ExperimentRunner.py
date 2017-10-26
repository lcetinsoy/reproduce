import os
from os import mkdir

import datetime

class ExperimentRunner(object):

    def __init__(self, exp_history_filename, debug_mode=True):
        super(ExperimentRunner, self).__init__()
        self.exp_history_filename = exp_history_filename
        self.debug_mode = debug_mode

    def run(self, experiment, result_directory, **kwargs):

        self.save_run(experiment)
        exp_parameters = experiment.get_parameters()
        print("Running {} with {}".format(experiment.get_name(), exp_parameters))
        experiment.run(result_directory, **kwargs)

    def run_experiments(self, experiments, result_directory):

        if not self.debug_mode:
            print("Running experiment without debug mode! Any failing expiriment will prevent the run of subsequent ones")
            for experiment in experiments:
                experiment.run(result_directory)
        else:
            for experiment in experiments:
                try:
                    experiment.run(result_directory)
                except Exception:
                    print("{} failed: {}".format(str(experiment), str(Exception)))


    def format_parameters(self, dictionary):

        d = []
        for key, value in enumerate(dictionary):
            d.append("{}_{}".format(key, value))

        return "_".join(d)

    def save_run(self, experiment):

        name = experiment.get_name()
        parameters = self.format_parameters(experiment.get_parameters())
        start_date = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")

        f = open(self.exp_history_filename, 'a')
        f.write("[{}]: {}\n".format(start_date, name, parameters))
        f.close()

    def create_dir(self, name):
        result_dir = self.result_dir
        mkdir(os.path.join([result_dir, name]))
