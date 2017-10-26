
# Reproduce

A tool to easily manage and reproduce experiments.

It allows convenient save of results. No more previous result deletions
because of having forgotten to change the result filenames.

This is a Work In progress.

Similar Tools:

- https://github.com/IDSIA/sacred
- https://github.com/williamFalcon/test-tube

I started the developpement of reproduce before knowing such tools.
Depending on the relevance, I still might continue the developement.

## Installation

$ git clone https://github.com/lcetinsoy/reproduce

PIP installation comming soon

## Usage

For each of your experiment define a class extending Experiment

```python

class MyExperiment(Experiment):

    def __init__(self):
        pass

    def get_default_parameters(self):

        return {

        }


```

Then define a main.py file with the following :


```python

import os

from lib.ExperimentRunner import ExperimentRunner
from lib.ExpArgParser import ArgParser

import myExperiment

experiments = [
    myExperiment()
]


main_dir = os.path.dirname(os.path.abspath(__file__))
exp_history_filename = "./exp_history"
result_directory = os.path.join(main_dir, "report/results")
runner = ExperimentRunner(exp_history_filename, result_directory)

arg_parser = ArgParser(experiments)
experiment = arg_parser.parse_args()

runner.run(experiment, result_directory)

```


$ python main.py

Relaunching the previous one
$ python main.py --previous

Specifying the experiment
$ python main.py --experiment <exprimentname>

Overriding parameters from the CLI with json format

$ python main.py --override="{name: value, name: value, ...}"

You can choose (with autocompletion) which experiment to run and with
the desired parameters. For each pair of experiment, parameter_set, a folder
will be created ensuring all experiment results are kept.

### demo

$ python demo/main.py

## Roadmap

- Automatically registering Experiments
- Lazy loading of Experiments
- Automatic retry on fail

