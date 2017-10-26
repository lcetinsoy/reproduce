import re
import matplotlib.pyplot as plt
import numpy as np
import os
from scipy.stats import stats
import json


def parameters_to_filename(parameters):
    s = []
    for name, value in parameters.items():
        if isinstance(value, dict):
            return parameters_to_filename(value)

        s.append("{}_{}".format(name, value))

    return "_".join(s)

class Metric(object):

    def __init__(self, name, experiment):
        self.name = re.sub(" ", "_", name)
        self.experiment = experiment

    def __str__(self):
        return self.name

    def collect(self, visitable):

        raise NotImplementedError

    def persist(self, result_directory):

        raise NotImplementedError

    def _save_figure(self, result_directory, fig, suffix = ""):

        exp_name = re.sub(" ", "_", str(self.experiment))
        parameters = parameters_to_filename(self.experiment.get_parameters())
        target_directory = os.path.join(result_directory, exp_name)

        if not os.path.exists(target_directory):
            os.mkdir(target_directory)

        target_directory = os.path.join(target_directory, parameters)
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)

        filename = self.build_file_name(suffix)
        target_file = os.path.join(target_directory, filename)
        fig.savefig(target_file)
        print(target_file)

    def get_target_dir(self, result_directory):

        exp_name = re.sub(" ", "_", str(self.experiment))
        parameters = parameters_to_filename(self.experiment.get_parameters())
        target_directory = os.path.join(result_directory, exp_name)

        if not os.path.exists(target_directory):
            os.mkdir(target_directory)

        target_directory = os.path.join(target_directory, parameters)
        if not os.path.exists(target_directory):
            os.mkdir(target_directory)

        return target_directory

    def build_file_name(self, file_suffix, extension="png"):

        if file_suffix == "":
            return self.name

        name = "{}_{}.{}".format(self.name, file_suffix, extension)
        return name


class CorrelationMetric(Metric):

    def __init__(self, name, experiment, variable_names):

        if not name.find("correlation"):
            name += "correlation"

        super().__init__(name, experiment)
        self.variable1 = []
        self.variable2 = []

        self.variable_names = variable_names

        self.n_color = 3


    def persist(self, result_folder):

        f = plt.figure()

        v1 = np.asarray(self.variable1)
        v2 = np.asarray(self.variable2)
        first_idx = int(len(v1) / 2)

        plt.scatter(v1[:first_idx], v2[:first_idx])
        plt.scatter(v1[first_idx:], v2[first_idx:], color="red")
        plt.xlabel(self.variable_names[0])
        plt.ylabel(self.variable_names[1])

        coef_full = self.compute_correlation_coefficient(v1, v2)
        coef_first_part = self.compute_correlation_coefficient(v1[:first_idx], v2[:first_idx])
        coef_second_part = self.compute_correlation_coefficient(v1[first_idx:], v2[first_idx:])


        coefs = {
            'full_train': str(coef_full[0]),
            'first_half': str(coef_first_part[0]),
            'coef_second_part': str(coef_second_part[0])
        }

        filename = self.build_file_name("coefficients", "json")

        d = self.get_target_dir(result_folder)

        path = os.path.join(d, filename)

        json_coeff = json.dumps(coefs)

        file = open(path, "w")
        file.write(json_coeff)
        file.close

        print(path)
        print("Full train correlation coefficient of {}: {}".format(str(self), coef_full))
        print("First half train correlation coefficient of {}: {}".format(str(self), coef_first_part))
        print("Second half train correlation coefficient of {}: {}".format(str(self), coef_second_part))

        self._save_figure(result_folder, f)


    def compute_correlation_coefficient(self, np_v1, np_v2):

        coeff = stats.pearsonr(np_v1, np_v2)

        return coeff

    def collect(self, numpy_variable1, numpy_variable2):

        if hasattr(numpy_variable1, "__len__"):
            if len(numpy_variable1) > 1:
                raise "Correlation metric exception array have more than one element"
            numpy_variable1 = numpy_variable1[0]

        if hasattr(numpy_variable2, "__len__"):
            if len(numpy_variable2) > 1:
                raise "Correlation metric exception array have more than one element"
            numpy_variable2 = numpy_variable2[0]

        self.variable1.append(numpy_variable1)
        self.variable2.append(numpy_variable2)

    def get_last_collected_values(self):
        return self.variable1[-1], self.variable2[-1]

class ScatterMetric(Metric):

    def __init__(self, name, experiment):
        super().__init__(name, experiment)
        self.x = []
        self.y = []

    def collect(self, x, y):

        self.x.append(x)
        self.y.append(y)

    def persist(self):
        plt.scatter(self.x, self.y)
