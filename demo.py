from reproduce import *

import os

class DummyExperiment(Experiment):

    def __init__(self, name, parameters={}):
        super().__init__(name, parameters)

    def get_default_parameters(self):

        return {
            "int_param": 1,
            "string_param": "hello"
        }

    def run(self):
        print("{}")


class DummyExperiment2(Experiment):

    def __init__(self, name, parameters={}):
        super().__init__(name, parameters)

    def get_default_parameters(self):

        return {
            "int_param": 1,
            "string_param": "hello"
        }

    def run(self):
        print("{}")


experiments = [
    DummyExperiment("Dummy"),
    DummyExperiment2("Dummy"),
]

main_dir = os.path.dirname(os.path.abspath(__file__))
exp_history_filename = "./exp_history"
result_directory = os.path.join(main_dir, "report/results")
runner = ExperimentRunner(exp_history_filename, result_directory)

arg_parser = ArgParser(experiments)
experiment = arg_parser.parse_args()

runner.run(experiment, result_directory)
