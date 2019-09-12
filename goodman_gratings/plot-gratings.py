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
        plt.rcParams['font.size'] = 24
        plt.rcParams['figure.figsize'] = (16, 9)
        plt.title('Gratings Requested During 2019')
        plt.bar(range(len(self.occurrence)), self.occurrence)
        plt.xticks(range(len(self.valid_grating)), self.valid_grating)
        for i in range(len(self.occurrence)):
            plt.text(i, self.occurrence[i] + 1, '{:d}'.format(self.occurrence[i]), horizontalalignment='center')
        plt.xlabel("Grating $(l/mm)$")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.savefig('requested-gratings-2019.png')
        plt.show()



if __name__ == '__main__':
    plot_grating = PlotRequestedGratings(file_name='gratings_2019.txt')
    plot_grating()
