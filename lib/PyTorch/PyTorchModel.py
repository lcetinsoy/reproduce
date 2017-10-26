import torch.nn as nn
import torch


class PytorchClassificationModel(nn.Module):

    def __init__(self):
        super(PytorchClassificationModel, self).__init__()

    def predict(self, input_data):
        output = self.forward(input_data)
        _, output = torch.max(output, 1)
        return output

    def forward(self, input_data):
        raise "Must be implemented"


    def get_weights(self):

        for param in self.parameters():
            print(type(param.data), param.size())

    def get_weights_as_vector(self):

        vectors = []
        for param in self.parameters():
            vectors.append(param.view(-1))

        return torch.cat(vectors)

    def get_n_parameters(self):

        pass