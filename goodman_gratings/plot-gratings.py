import re
import matplotlib.pyplot as plt


class PlotRequestedGratings(object):

    def __init__(self, file_name):
        self.valid_grating = [400, 600, 930, 1200, 1800, 2100, 2400]
        self.occurrence = []
        self.__all_values = []
        self.file_name = file_name

    def __call__(self, *args, **kwargs):
        self.read_file()
        self.count_events()
        print(self.valid_grating, self.occurrence)
        self.create_plot()

    @property
    def values(self):
        return self.__all_values

    @values.setter
    def values(self, value):
        try:
            if int(value) in self.valid_grating:
                self.__all_values.append(int(value))
            else:
                print("Value not in valid gratings: {:d}".format(int(value)))
        except ValueError:
            if value != '\n':
                for sub_value in value.split(' '):
                    print(repr(sub_value))

    def read_file(self):
        with open(self.file_name) as fl:
            for line in fl.readlines():
                new_line = re.sub('[A-Z_a-z()/"-]', '', line)
                for value in new_line.split(','):
                    try:
                        value = int(value)
                        self.values = value
                    except ValueError:
                        for sub_value in value.split(' '):
                            self.values = sub_value

    def count_events(self):
        for grating in self.valid_grating:
            print(grating, self.values.count(grating))
            self.occurrence.append(self.values.count(grating))

    def create_plot(self):
        plt.bar(self.valid_grating, self.occurrence, width=30)
        plt.xticks(self.valid_grating)
        plt.tight_layout()
        plt.show()



if __name__ == '__main__':
    plot_grating = PlotRequestedGratings(file_name='gratings.txt')
    plot_grating()
