class DataLoader(object):

    def get_n_feature(self):

        raise NotImplementedError


class ClassificationDataLoader(DataLoader):

    def __init__(self, batch_size):
        super(ClassificationDataLoader, self).__init__()
        self.batch_size = batch_size

    def get_classe_counts(self):
        raise NotImplementedError


    def get_data_info(self):

        return self.get_n_feature(), self.get_classe_counts()

    def get_batch_size(self):
        return self.batch_size

