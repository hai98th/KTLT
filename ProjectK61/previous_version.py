# python3
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import numpy as np
import pandas as pd
import sys
from pgmpy.models import BayesianModel
from pgmpy.estimators import BayesianEstimator
from pgmpy.estimators import BaseEstimator
from pgmpy.inference import VariableElimination
import matplotlib.pyplot as plt
import copy
# from openpyxl.drawing.text import TextField


class Application(Frame):
    def choosefile(self):
        self.file_path = filedialog.askopenfilename()
        self.datafile_label["text"] = self.file_path

    def draw_subplots(self, Distribution, max_value_di):
        plt.figure()
        plt.subplot(4, 4, 1)
        plt.bar([1, 2, 3, 4, 5], Distribution['DPQ'])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("design process quality ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 2)
        plt.bar([1, 2, 3, 4, 5], Distribution['C'])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("complexity ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 3)
        plt.bar([1, 2, 3, 4, 5], Distribution['OU'])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("operational usage ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 4)
        plt.bar([1, 2, 3, 4, 5], Distribution['TQ'])
        plt.xticks([1, 2, 3, 4, 5], ['very low', 'low', 'medium', 'high', 'very high'])
        plt.title("Test quality ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 5)
        plt.plot(self.state_names['DI'], Distribution['DI'])
        plt.title("defects inserted ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 6)
        plt.plot(self.state_names['DFT'], Distribution['DFT'])
        plt.title("defects found in testing ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 7)
        plt.plot(self.state_names['RD'], Distribution['RD'])
        plt.title("residual defects ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 8)
        plt.plot(self.state_names['DFO'], Distribution['DFO'])
        plt.title("defects found in operation ")
        plt.ylabel('probability')

        plt.subplot(4, 4, 9)
        plt.plot(self.state_names['DI2'], Distribution['DI2'])
        plt.title("defects inserted 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 10)
        plt.plot(self.state_names['DFT2'], Distribution['DFT2'])
        plt.title("defects found in testing 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 11)
        plt.plot(self.state_names['RD2'], Distribution['RD2'])
        plt.title("residual defects 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 12)
        plt.plot(self.state_names['DFO2'], Distribution['DFO2'])
        plt.title("defects found in operation 2")
        plt.ylabel('probability')

        plt.subplot(4, 4, 13)
        plt.plot(self.state_names['DI3'], Distribution['DI3'])
        plt.title("defects inserted 3")
        plt.ylabel('probability')

        plt.subplot(4, 4, 14)
        plt.plot(self.state_names['DFT3'], Distribution['DFT3'])
        plt.title("defects found in testing 3")
        plt.ylabel('probability')

        plt.subplot(4, 4, 15)
        plt.plot(self.state_names['RD3'], Distribution['RD3'])
        plt.title("residual defects 3")
        plt.ylabel('probability')

        plt.subplot(4, 4, 16)
        plt.plot(self.state_names['DFO3'], Distribution['DFO3'])
        plt.title("defects found in operation 3")
        plt.ylabel('probability')
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, hspace=0.4, wspace=0.4)

    def process_box(self):
        pr = {}
        if not hasattr(self, 'file_path'):
            print("chua chon file")
            exit()

        if self.dpq_box.get() == 'unknown':
            if 'DPQ' in pr.keys():
                del pr['DPQ']
        elif self.dpq_box.get() == 'very low':
            pr['DPQ'] = 0
        elif self.dpq_box.get() == 'low':
            pr['DPQ'] = 1
        elif self.dpq_box.get() == 'medium':
            pr['DPQ'] = 2
        elif self.dpq_box.get() == 'high':
            pr['DPQ'] = 3
        elif self.dpq_box.get() == 'very high':
            pr['DPQ'] = 4
        else:
            pass

        if self.c_box.get() == 'unknown':
            if 'C' in pr.keys():
                del pr['C']
        elif self.c_box.get() == 'very low':
            pr['C'] = 0
        elif self.c_box.get() == 'low':
            pr['C'] = 1
        elif self.c_box.get() == 'medium':
            pr['C'] = 2
        elif self.c_box.get() == 'high':
            pr['C'] = 3
        elif self.c_box.get() == 'very high':
            pr['C'] = 4
        else:
            pass

        if self.tq_box.get() == 'unknown':
            if 'TQ' in pr.keys():
                del pr['TQ']
        elif self.tq_box.get() == 'very low':
            pr['TQ'] = 0
        elif self.tq_box.get() == 'low':
            pr['TQ'] = 1
        elif self.tq_box.get() == 'medium':
            pr['TQ'] = 2
        elif self.tq_box.get() == 'high':
            pr['TQ'] = 3
        elif self.tq_box.get() == 'very high':
            pr['TQ'] = 4
        else:
            pass

        if self.ou_box.get() == 'unknown':
            if 'OU' in pr.keys():
                del pr['OU']
        elif self.ou_box.get() == 'very low':
            pr['OU'] = 0
        elif self.ou_box.get() == 'low':
            pr['OU'] = 1
        elif self.ou_box.get() == 'medium':
            pr['OU'] = 2
        elif self.ou_box.get() == 'high':
            pr['OU'] = 3
        elif self.ou_box.get() == 'very high':
            pr['OU'] = 4
        else:
            pass
        return pr

    def process(self):
        def calculate_distribution_nodes_input():
            for key in pr.keys():
                Distribution[key] = np.array([1 - abs(np.sign(pr[key] - i)) for i in range(5)])
                Distribution[key+'2'] = Distribution[key]
                Distribution[key+'3'] = Distribution[key]
                nodes.remove(key)
                nodes2.remove(key+'2')
                nodes3.remove(key+'3')

        def query_time_frame_1(infer):
            print ('query 1', pr, nodes)
            query = infer.query(nodes, evidence=pr)
            for key, value in query.items():
                Distribution[key].append(value.values)

        def query_time_frame_2(infer):
            global pr2
            for key, value in pr.items():
                pr2[key+'2'] = pr[key]

            print ('query 2', pr2, nodes2)
            query = infer.query(nodes2, evidence=pr2)
            for key, value in query.items():
                Distribution[key].append(value.values)

        def query_time_frame_3(infer):
            global pr3
            for key, value in pr.items():
                pr3[key+'3'] = pr[key]
            print ('query 3', pr3, nodes3)
            query = infer.query(nodes3, evidence=pr3)
            for key, value in query.items():
                Distribution[key].append(value.values)

        def stretch_distributions(max_value_di):
            # sketch number axis with max values = max values DI + 1
            remove_nodes = ['DPQ', 'C', 'TQ', 'OU', 'DPQ2', 'C2', 'TQ2', 'OU2', 'DPQ3', 'C3', 'TQ3', 'OU3']
            for key in [x for x in list(nodes+nodes2+nodes3) if x not in remove_nodes]:
                if self.state_names[key][-1] == max_value_di:
                    self.state_names[key].append(max_value_di+1)
                    Distribution[key] = np.append(Distribution[key], [0])
                elif self.state_names[key][-1] < max_value_di:
                    self.state_names[key].extend([self.state_names[key][-1]+1, max_value_di+1])
                    Distribution[key] = np.append(Distribution[key], [0, 0])

        def process_segments(size):
            global Distribution
            loop = int(np.ceil(float(self.data_size) / size))
            last_size = self.data_size - size * (loop - 1)
            print('size: ', size, ' | last_size ', last_size, ' | loop: ', loop)
            for i in range(loop):
                print ('process: ', i)
                self.model.fit(self.data.loc[i*size:(i+1)*size], estimator_type=BayesianEstimator, prior_type="BDeu",
                          equivalent_sample_size=1, state_names=self.state_names)
                infer = VariableElimination(self.model)
                query_time_frame_1(infer)
                query_time_frame_2(infer)
                query_time_frame_3(infer)

            for node in list(nodes+nodes2+nodes3):
                temp = [0] * len(self.state_names[node])
                length_distribution = len(Distribution[node])
                length_state_name = len(self.state_names[node])
                for distribution_index in range(0, length_distribution-1):
                    for value_distr_index in range(length_state_name):
                        temp[value_distr_index] += Distribution[node][distribution_index][value_distr_index]
                percent = float(last_size) / size
                for value_distr_index in range(length_state_name):
                        temp[value_distr_index] += (Distribution[node][-1][value_distr_index]*percent)
                Distribution[node] = [x*size/self.data_size for x in temp]

        def calculate_expected_value_and_variance():
            print ('Expected value and Variance: ')
            expected_value = {}
            variance = {}
            for key in list(nodes + nodes2 + nodes3):
                expected_value[key] = sum([value*prob for value, prob in zip(self.state_names[key], Distribution[key])])
                # https://en.wikipedia.org/wiki/Variance#Discrete_random_variable
                variance[key] = sum([
                    prob*(value-expected_value[key])*(value-expected_value[key]) for prob, value in
                    zip(Distribution[key], self.state_names[key])
                    ])
                print ('E(', key, ') = ', expected_value[key], ' | Var(', key, ') = ', variance[key])

        global nodes
        global Distribution
        global pr
        global pr2
        global pr3
        pr = self.process_box()
        pr2 = {}
        pr3 = {}
        nodes = ['DPQ', 'C', 'TQ', 'DI', 'DFT', 'RD', 'OU', 'DFO']
        nodes2 = ['DPQ2', 'C2', 'TQ2', 'DI2', 'DFT2', 'RD2', 'OU2', 'DFO2']
        nodes3 = ['DPQ3', 'C3', 'TQ3', 'DI3', 'DFT3', 'RD3', 'OU3', 'DFO3']
        Distribution = {}

        if self.history_file != self.file_path:
            self.data = pd.read_csv(self.file_path)  # "fisrm.csv"
            self.data_size = len(self.data)
            self.history_file = self.file_path

            self.model = BayesianModel(
                [('TQ', 'DFT'), ('DPQ', 'DI'), ('C', 'DI'), ('DI', 'DFT'), ('DI', 'RD'), ('DFT', 'RD'), ('RD', 'DFO'),
                ('OU', 'DFO'),
                ('DPQ', 'DPQ2'), ('C', 'C2'), ('TQ', 'TQ2'), ('OU', 'OU2'), ('RD', 'DI2'),
                ('DI2', 'DFT2'), ('DI2', 'RD2'), ('DFT2', 'RD2'), ('RD2', 'DFO2'), ('OU2', 'DFO2'),
                ('DPQ2', 'DPQ3'), ('C2', 'C3'), ('TQ2', 'TQ3'), ('OU2', 'OU3'),
                ('RD2', 'DI3'), ('DI3', 'DFT3'), ('DI3', 'RD3'), ('DFT3', 'RD3'), ('RD3', 'DFO3'), ('OU3', 'DFO3')])
        self.state_names = BaseEstimator(self.data).state_names

        calculate_distribution_nodes_input()

        for node in nodes:
            Distribution[node] = []
            Distribution[node+'2'] = []
            Distribution[node+'3'] = []

        length = len(pr.keys())
        if length == 0:
            size = 40
        elif length == 1:
            size = 150
        elif length == 2:
            size = 500
        elif length == 3:
            size = 1500
        elif length == 4:
            size = 5000
        process_segments(size)

        calculate_expected_value_and_variance()
        # Draw
        max_value_di = self.state_names['DI'][-1] # array has been sorted
        stretch_distributions(max_value_di)

        self.draw_subplots(Distribution, max_value_di)
        plt.show()

    def createWidgets(self):
        pad_x = 5
        pad_y = 5
        self.firstlabel = Label(self)
        self.firstlabel["text"] = "Choose_file:__",
        # self.text_datafile["command"] = self.say_hi

        # self.firstlabel.grid(row=0, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.datafile_label = Label(self)
        self.datafile_label["text"] = "no_file",
        self.datafile_label.grid(row=0, column=1, padx=pad_x, pady=pad_y,columnspan=3, sticky=W)

        self.choosefilebutton = Button(self)
        self.choosefilebutton["text"] = "Choose_data_file",
        self.choosefilebutton["command"] = self.choosefile
        self.choosefilebutton.grid(row=1, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.dpq_label = Label(self)
        self.dpq_label["text"] = "design_process_quality",
        self.dpq_label.grid(row=2, column=1, padx=pad_x, pady=pad_y, sticky=W)

        # self.dpq_entry = Entry(self, width=10)
        # self.dpq_entry.grid(row=1, column=3, padx=pad_x, pady=pad_y, sticky=W)
        self.dpq_box_value = StringVar()
        self.dpq_box = ttk.Combobox(self, textvariable=self.dpq_box_value)
        self.dpq_box['values'] = ('unknown','very low', 'low', 'medium', 'high', 'very high')
        self.dpq_box.current(0)
        self.dpq_box.grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky=W)

        self.c_label = Label(self)
        self.c_label["text"] = "Complexity",
        self.c_label.grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky=W)

        # self.c_entry = Entry(self, width=10)
        # self.c_entry.grid(row=1, column=5, padx=pad_x, pady=pad_y, sticky=W)
        self.c_box_value = StringVar()
        self.c_box = ttk.Combobox(self, textvariable=self.c_box_value)
        self.c_box['values'] = ('unknown','very low', 'low', 'medium', 'high', 'very high')
        self.c_box.current(0)
        self.c_box.grid(row=2, column=4, padx=pad_x, pady=pad_y, sticky=W)

        self.tq_label = Label(self)
        self.tq_label["text"] = "Test_quality",
        self.tq_label.grid(row=2, column=5, padx=pad_x, pady=pad_y, sticky=W)

        # self.tq_entry = Entry(self, width=10)
        # self.tq_entry.grid(row=1, column=7, padx=pad_x, pady=pad_y, sticky=W)

        self.tq_box_value = StringVar()
        self.tq_box = ttk.Combobox(self, textvariable=self.tq_box_value)
        self.tq_box['values'] = ('unknown','very low','low','medium', 'high','very high')
        self.tq_box.current(0)
        self.tq_box.grid(row=2, column=6, padx=pad_x, pady=pad_y, sticky=W)

        self.ou_label = Label(self)
        self.ou_label["text"] = "operational_usage",
        self.ou_label.grid(row=2, column=7, padx=pad_x, pady=pad_y, sticky=W)

        # self.tq_entry = Entry(self, width=10)
        # self.tq_entry.grid(row=1, column=7, padx=pad_x, pady=pad_y, sticky=W)

        self.ou_box_value = StringVar()
        self.ou_box = ttk.Combobox(self, textvariable=self.ou_box_value)
        self.ou_box['values'] = ('unknown', 'very low', 'low', 'medium', 'high', 'very high')
        self.ou_box.current(0)
        self.ou_box.grid(row=2, column=8, padx=pad_x, pady=pad_y, sticky=W)

        self.processbotton = Button(self)
        self.processbotton["text"] = "Process",
        self.processbotton["command"] = self.process
        self.processbotton.grid(row=3, column=1, padx=pad_x, pady=pad_y, sticky=W)

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit
        self.QUIT.grid(row=3, column=2, padx=pad_x, pady=pad_y, sticky=W)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.history_file = ''

root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
