import colored_traceback.auto

from argparse import ArgumentParser

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter
import json
# import ast

parser = ArgumentParser(description="Experiment argument parser")
parser.add_argument("--experiment", default="")
parser.add_argument("--override", default="")
parser.add_argument("--previous", action="store_true")
args = parser.parse_args()


class ArgParser(object):

    def __init__(self, experiments):

        super().__init__()

        self.str_experiments = map(str, experiments)
        self.experiments = {str(exp): exp for exp in experiments}

        # print(self.experiments);exit()

    def parse_args(self):

        experiment_name = args.experiment

        if args.previous:
            return self.get_previous_experiment()

        if experiment_name == "":
            print("Choose an experiment to run")
            completer = WordCompleter(self.str_experiments)
            experiment_name = prompt('> ', completer=completer)

        if not bool(experiment_name):
            self.print_available_experiments()
            exit()

        experiment = self.experiments.get(experiment_name)

        print("Choose experiment parameters")
        self.set_parameter_from_prompt(experiment, experiment.get_parameters())
        self.save_experiment(experiment)

        return experiment

    def set_parameter_from_prompt(self, experiment, parameters={}, new_parameters={}, tail=True):

        for name, default_value in parameters.copy().items():

            if isinstance(default_value, dict):
                new_parameters[name] = {}
                self.set_parameter_from_prompt(experiment, default_value, new_parameters[name], False)
                continue

            param = prompt('{}: [{}] '.format(name, default_value))

            if param == "":
                param = default_value
            else:
                param = type(default_value)(param)
            new_parameters[name] = param

        if tail:
            experiment.set_parameters(new_parameters)


    def print_available_experiments(self):

        print("No experiment where chosen, leaving")
        print("The following experiments are available:")
        for exp in self.experiments:
            print("{}".format(exp))



    def get_previous_experiment(self):

        print('Loading previous experiment')
        f = open('./last_experiment', 'r')
        data = f.readline()
        data = json.loads(data)
        experiment_name = data.get('experiment')

        experiment = self.experiments.get(experiment_name)
        experiment.set_parameters(data.get('parameters'))

        if args.override != "":
            import demjson

            parameters = demjson.decode(args.override)
            # parameters = ast.literal_eval(args.override)
            experiment.set_parameters(parameters)

            self.save_experiment(experiment)

        return experiment

    def save_experiment(self, experiment):

        jsonExperiment = json.dumps({
            'experiment': str(experiment),
            'parameters': experiment.get_parameters()
        })

        f = open('./last_experiment', 'w')
        f.write(jsonExperiment)
        f.close()

