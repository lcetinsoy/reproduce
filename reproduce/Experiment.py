import os

class Experiment(object):

    def __init__(self, name, parameters={}):

        self.merge_parameters(parameters)
        self.parameters_labels = {}
        self.name = name
        self.metrics = {}

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def metrics_are(self):
        raise NotImplementedError

    def set_parameter(self, name, value, label=None):
        self.parameters[name] = value
        self.parameters_labels[name] = label

    def set_parameters(self, parameters):
        self.parameters.update(parameters)

    def merge_parameters(self, parameters):

        self.parameters = self.get_default_parameters()
        self.parameters.update(**parameters)

    def get_default_parameters(self):
        raise NotImplementedError

    def get_parameters(self):
        return self.parameters

    def get_parameter(self, name):

        if not name in self.parameters.keys():
            raise Exception("Experiment {} ({}) does not have a parameter named {}. Available parameters are: {}".format(
                self.__class__, str(self), name, [key for key in self.parameters.keys()]
            ))

        return self.parameters.get(name)


    def persist_metrics(self, metric_dictionnaries, result_directory):

        for metrics in metric_dictionnaries:
            for metric in metrics.values():
                metric.persist(result_directory)

    def _get_loader(self, batch_size):
        loader_name = self.get_parameter("data_loader")
        return self.compatible_data_loader.get(loader_name)(batch_size)

    def useParameterForName(self, name, value):
        pass

    def get_metrics(self):
        return self.metrics

    def before_run(self):
        pass

    def after_run(self):
        pass

    def reset(self):
        pass

    def run(self):
        raise NotImplementedError

    @staticmethod
    def load_from_disk():
        pass

    def save_to_disk(self):
        pass

    def notify_end(self):
        soundNotification()


def soundNotification():
    """Ring a bell as notification"""
    os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.6, 330))
