# load library
import tkinter as tk
from tkinter import filedialog, Text, Menu
from tkinter import *
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# create window
root = tk.Tk()
root.title("PyHRM-GUI")
# root.geometry('800x400')

class panel(object):
    filename = ""
    temp = ""
    temp0 = ""
    ref = ""
    read = ""
    OPTIONS = [
    "Bio-Rad",
    # "Applied Biosystem"
    ]

    def __init__(self, rows=8, columns=12):
        # create parameter panel
        panel = tk.LabelFrame(root, text=" Parameter Settings ", height=100)
        panel.grid(row=0, columnspan=7, sticky='NW', padx=5, pady=5, ipadx=5, ipady=5)

        tk.Label(panel, text="Instrument Type").grid(row=0, column=0, sticky="W")
        variable = StringVar(root)
        variable.set(self.OPTIONS[0]) # default value
        OptionMenu(panel, variable, *self.OPTIONS).grid(row=0, column=1, sticky="nesw")

        tk.Label(panel, text="Input File (.CSV)").grid(row=1, column=0, sticky="W")
        tk.Button(panel, text="Browse", command=self.browsefunc).grid(row=1, column=1, sticky="nesw")
        self.file = tk.Label(panel)
        self.file.grid(row=2, column=1, columnspan=7, sticky="W")
        # tk.Label(panel, text="example").grid(row=1, column=3, sticky="W")
        
        tk.Label(panel, text="Set Temp Range").grid(row=3, column=0, sticky="W")
        self.temp = tk.Entry(panel)
        self.temp.grid(row=3, column=1, sticky="W")
        # tk.Label(text="To")
        self.temp1 = tk.Entry(panel)
        self.temp1.grid(row=3, column=2, sticky="W")
        # tk.Label(panel, text="example").grid(row=3, column=3, sticky="W")
        
        tk.Label(panel, text="Set Reference Well").grid(row=4, column=0, sticky="W")
        self.ref = tk.Entry(panel)
        self.ref.grid(row=4, column=1, sticky="W")
        # tk.Label(panel, text="example: A1").grid(row=4, column=3, sticky="W")

        tk.Button(panel, text="Analyze", command=self.analyze).grid(row=5, column=0, columnspan=3, sticky="nesw")

        # create well panel
        panel1 = tk.LabelFrame(root, text=" Well Settings ")
        panel1.grid(row=0, column=9, columnspan=7, sticky='NW', padx=5, pady=5, ipadx=5, ipady=5)

        rowrange = range(rows)
        colrange = range(columns)

        # create grid label
        for x in colrange:
            w = tk.Label(panel1, text=x + 1)
            w.grid(row=0, column=x+10)

        for y in rowrange:
            w = tk.Label(panel1, text=chr(64+(y + 1)))
            w.grid(row=y+1, column=9)

        # create grid checkbutton label
        self.grid = []
        for y in rowrange:
            row = []
            for x in colrange:
                b = tk.Checkbutton(panel1)
                b.var = tk.IntVar()
                b.config(variable=b.var)
                b.grid(row=y+1, column=x+10)
                row.append(b)
            self.grid.append(row)

        #Track the number of on buttons in each row
        # self.rowstate = rows * [0]

    def get_checked(self):
        ''' Make a list of the selected Groups in each row'''
        data = []
        for idxr, row in enumerate(self.grid):
            for idx, item in enumerate(row):
                if(item.var.get() != 0):
                    data.append(chr(64+idxr+1)+str(idx+1))
        return data

    def getter(self):
        return self.filename, self.temp.get(), self.temp1.get(), self.ref.get().capitalize(), self.get_checked()

    def update(self):
        self.file.config(text = self.filename)
        # insert temp
        # insert temp1
        # insert ref
        # make checked

    def save(self):
        # write self.getter() as .sav
        print()

    def browsefunc(self):
        self.filename = filedialog.askopenfilename()
        self.update()

    def analyze(self):
        try:
            self.readData(*self.getter())
        
        except:
            print("Please check your input!")

    def readData(self, file, temp, temp1, ref, read):
        plt.close()

        # ### Read and Plot Melting Data
        df = pd.read_csv(file)

        # drop empty column
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # ### Select melting range
        df_melt=df.loc[(df.iloc[:,0]>int(temp)) & (df.iloc[:,0]<int(temp1))]
        final = list(set(read) & set(df_melt))
        df_data=df_melt[final]
  
        # ### Normalizing 
        df_norm= (df_data - df_data.min()) / (df_data.max()-df_data.min())*100
 
        # ### Calculate and Show Diff Plot 
        dfdif = df_norm.sub(df_norm[ref],axis=0)

        print('file: '+file)
        print('temperature: '+temp+'-'+temp1)
        print('well analyzed: ')
        print(final)
        print('data table: ')
        print(df_data)
        print('reference well: '+ref)

        # plt.plot(df.iloc[:,[0]],df.iloc[:,1:])
        # plt.plot(df_melt.iloc[:,[0]],df_data)
        # plt.plot(df_melt.iloc[:,[0]],df_norm)
        plt.plot(df_melt.iloc[:,[0]],dfdif)
        plt.legend(final)
        plt.show()

        # # ### Clustering
        # # Use KMeans module from SciKit-Learn to cluster your sample into three groups (WT, KO, HET). Be careful, your samples may have less than three groups. So always check the diff plots first.
        # import sklearn.cluster as sc
        # from IPython.display import display

        # mat = dfdif.T.values
        # hc = sc.KMeans(n_clusters=3)
        # hc.fit(mat)

        # labels = hc.labels_
        # results = pd.DataFrame([dfdif.T.index,labels])
        # display(results.loc[:0,results.iloc[1]==0])
        # display(results.loc[:0,results.iloc[1]==1])
        # display(results.loc[:0,results.iloc[1]==2])

        # # My controls are 
        # # * WT: I12, J12
        # # * KO: I13, J13
        # # * HET: I14, J14
        # # 
        # # So you can identify your genotyping results by looking at: to which control they cluster.
        # # Ploting with plot.ly, so you can look at individual lines for better pattern recognition
        # import plotly.plotly as py
        # import cufflinks as cf
        # import plotly.graph_objs as go

        # cf.set_config_file(offline=False, world_readable=True, theme='ggplot')

        # dfpy = dfdif.set_index(df_melt.iloc[:,0])

        # # Plot and embed in ipython notebook!
        # dfpy.iplot(kind='scatter', filename='pyHRM')

control = panel()
root.mainloop()
