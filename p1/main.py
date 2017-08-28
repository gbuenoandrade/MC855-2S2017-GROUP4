import time

from threading import Thread
from hadoop import *
from twitter import *
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkinter import *

# ********** PAY ATTENTION TO THESE VALUES **********
DEBUG = True
HADOOP_USER_FOLDER = '/user/gandrade'
# ***************************************************


def get_points(keywords, since, until):
    if DEBUG:
        time.sleep(1)
        vals = [('2016-08-27', 662.0), ('2016-10-02', -3008.0), ('2016-11-08', -624201.0), ('2016-12-14', -4461.0), ('2017-01-20', -33.0), ('2017-02-25', 44705.0), ('2017-04-03', -71635.0), ('2017-05-09', 18293.0), ('2017-06-15', -244.0), ('2017-07-21', -14407.0), ('2017-08-27', -30.0)]
    else:
        Twitter.get_tweets(keywords, since, until, points=20, tweets_per_point=5)
        vals = Hadoop(HADOOP_USER_FOLDER).run('tweets.txt')
    acc = 0
    xs = list()
    ys = list()
    for date, val in vals:
        acc += val
        x = datetime.strptime(date, '%Y-%m-%d').timestamp()
        y = acc
        xs.append(x)
        ys.append(y)
    return xs, ys


class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainFrame,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(MainFrame)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        inputs_frame = Frame(self)
        inputs_frame.pack(side=TOP)

        # date labels
        date_frame = Frame(inputs_frame)
        date_frame.grid(row=0, column=0)
        since_vars = [StringVar() for _ in range(3)]
        until_vars = [StringVar() for _ in range(3)]
        MainFrame.new_date(date_frame, 0, 'Since:', since_vars)
        MainFrame.new_date(date_frame, 1, 'Until:', until_vars)

        # keywords entry
        keywords_frame = Frame(inputs_frame)
        keywords_frame.grid(row=1, column=0, pady=4)
        Label(keywords_frame, text='Keywords (OR):').grid(row=0, column=0, pady=5)
        keywords = StringVar()
        keywords.set('immigrants muslims')
        Entry(keywords_frame, textvariable=keywords).grid(row=0, column=1)

        # get button
        button_frame = Frame(inputs_frame)
        button_frame.grid(row=2, column=0)
        Button(button_frame, text="Generate",
               command=lambda: self.generate_and_plot_graph(since_vars, until_vars, keywords)).grid()

    @staticmethod
    def get_date(vars):
        date = '%0.4d-%0.2d-%0.2d' % (int(vars[0].get()), int(vars[1].get()), int(vars[2].get()))
        return date

    def generate_and_plot_graph(self, since_vars, until_vars, keywords_var):
        since = MainFrame.get_date(since_vars)
        until = MainFrame.get_date(until_vars)
        keywords = keywords_var.get().split()
        Thread(target=lambda: self.update_graph(get_points(keywords, since, until)), daemon=True).start()

    @staticmethod
    def set_to_today(vars):
        today = datetime.today()
        vars[0].set(today.year)
        vars[1].set(today.month)
        vars[2].set(today.day)

    @staticmethod
    def new_date(root, row, name, vars):
        MainFrame.set_to_today(vars)
        ws = list()
        ws.append(Label(root, text=name))
        ws.append(OptionMenu(root, vars[0], *[x for x in range(2007, 2018)]))
        ws.append(OptionMenu(root, vars[1], *[x for x in range(1, 13)]))
        ws.append(OptionMenu(root, vars[2], *[x for x in range(1, 32)]))
        for idx, w in enumerate(ws):
            if idx > 0:
                w.config(width=8)
            w.grid(row=row, column=idx, padx=5, pady=2)

    def update_graph(self, points):
        xs, ys = points
        print(xs, ys)
        for child in self.winfo_children()[1:]:
            child.destroy()
        Label(self, text='Epoch x Accumulated Sentiment').pack(side=TOP, fill=BOTH, expand=True)
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.plot(xs, ys)
        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=True)


if __name__ == '__main__':
    App().mainloop()
