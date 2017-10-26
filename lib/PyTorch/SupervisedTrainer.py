from torch.autograd import Variable


class SupervisedTrainer(object):

    def __init__(self, model):
        self.model = model

    def fit(self, n_epoch, optimizer, train_loader, test_loader):

        model = self.model
        loss_function = self.loss_function

        for i_epoch in range(n_epoch):
            print('Epoch {}'.format(i_epoch + 1))
            for (images, labels) in train_loader:
                optimizer.zero_grad()

                images = Variable(images)
                labels = Variable(labels)

                probabilities = model.forward(images)

                loss = loss_function(probabilities, labels)
                loss.backward()
                optimizer.step()

            n_prediction = 0
            n_true_prediction = 0.

            for (images, labels) in test_loader:
                predictions = model.predict(Variable(images))
                n_true_prediction += (predictions.data == labels).sum()
                n_prediction += labels.size(0)
            print(" - training loss {}, test accuracy {}".format(loss, 100 * n_true_prediction / n_prediction))
