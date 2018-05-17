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

  def chart_drawing(self, distribution):
    """
      TODO: Vẽ biểu đồ phân phối xác suất gía trị của mỗi nút sử dụng thư viện matplotlib.
      Sử dụng plt.subplot(...) để vẽ nhiều biểu đồ trên cùng một figure.
    """
    pass

  def process_selection(self):
    nodes = {}
    if not hasattr(self, 'file_path'):
      print('Chưa chọn file.')
      exit()

    select_values = ['very low', 'low', 'medium', 'high', 'very high']
    nodes['DPQ'] = select_values.index(self.dpq_box.get())
    nodes['C'] = select_values.index(self.c_box.get())
    nodes['TQ'] = select_values.index(self.tq_box.get())
    nodes['OU'] = select_values.index(self.ou_box.get())
    return nodes

  def static_bayesian_model(self):
    model = None
    """
      TODO: Xây dựng mạng Bayesian tĩnh như bài báo:
        "Using Bayesian Networks to Predict Software Defects and Reliability"
        Phần 2. A simple causal model for software defect prediction
        Sử dụng dữ liệu từ file data/data.csv, trong đó DI=RDP+NDI (xem thêm data_explaination.txt)
    """
    return model

  def dynamic_bayesian_model(self):
    model = None
    """
      TODO: Giả sử mỗi khi thêm một chức năng vào phần mềm, ta muốn dự đoán số lỗi của phần mềm,
        số lỗi này sẽ phụ thuộc vào việc thiết kế chức năng, khả năng lập trình viên,...,
        và số lỗi có sẵn trước đó nhưng chưa tìm thấy.
        Hãy đề xuất một mô hình Bayesian để thực hiện việc này, gọi là mô hình Bayesian động.
        (có thể tham khảo từ các nguồn, sử dụng dữ liệu có sẵn hoặc dữ liệu tự sinh có thể chấp nhận,
        sử dụng mạng DynamicBayesian (ưu tiên) hoặc mạng Bayesian thông thường).

      Lưu ý: Có thể sử dụng các mô hình khác như mạng Neural, các mô hình regression,...
    """
    return model

  def process(self):
    """
      TODO:
      1. Học mạng: Đọc dữ liệu từ file đã chọn và đưa vào mạng Bayesian để học
        (sử dụng hàm fit(...) trong class BayesianModel).
      2. Với đầu vào DPQ, TQ, C, OU đã chọn, vẽ phân phối xác suất của các nút trong mạng
        (sử dụng hàm query trong VariableElimination).
      Chú ý: Có thể lưu lại model Bayesian đã học, lần kế tiếp chạy chương trình không cần học mạng ở bước 1
        mà load lại model từ file model đã lưu trước đó.
        (Tìm hàm save model của thư viện, nếu không có sẵn -> lưu lại CPD các nút)
    """
    pass

  def createWidgets(self):
    pad_x = 5
    pad_y = 5
    self.firstlabel = Label(self)
    self.firstlabel["text"] = "Choose_file:__",

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

    self.dpq_box_value = StringVar()
    self.dpq_box = ttk.Combobox(self, textvariable=self.dpq_box_value)
    self.dpq_box['values'] = ('unknown','very low', 'low', 'medium', 'high', 'very high')
    self.dpq_box.current(0)
    self.dpq_box.grid(row=2, column=2, padx=pad_x, pady=pad_y, sticky=W)

    self.c_label = Label(self)
    self.c_label["text"] = "Complexity",
    self.c_label.grid(row=2, column=3, padx=pad_x, pady=pad_y, sticky=W)

    self.c_box_value = StringVar()
    self.c_box = ttk.Combobox(self, textvariable=self.c_box_value)
    self.c_box['values'] = ('unknown','very low', 'low', 'medium', 'high', 'very high')
    self.c_box.current(0)
    self.c_box.grid(row=2, column=4, padx=pad_x, pady=pad_y, sticky=W)

    self.tq_label = Label(self)
    self.tq_label["text"] = "Test_quality",
    self.tq_label.grid(row=2, column=5, padx=pad_x, pady=pad_y, sticky=W)

    self.tq_box_value = StringVar()
    self.tq_box = ttk.Combobox(self, textvariable=self.tq_box_value)
    self.tq_box['values'] = ('unknown','very low','low','medium', 'high','very high')
    self.tq_box.current(0)
    self.tq_box.grid(row=2, column=6, padx=pad_x, pady=pad_y, sticky=W)

    self.ou_label = Label(self)
    self.ou_label["text"] = "operational_usage",
    self.ou_label.grid(row=2, column=7, padx=pad_x, pady=pad_y, sticky=W)

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
