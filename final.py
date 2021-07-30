import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from PIL import Image, ImageTk
from matplotlib import figure
from src.ParallelDiv import parallel_divide
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


root = tk.Tk()
root.geometry('1280x720')
root.title('BJT Simulator')


class Input(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master

        self.circuit_type = tk.StringVar()
        self.circuit_type.set('CE')
        self.current_vals = [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar()
        ]
        self.resistor_vals = [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar()
        ]

        self.voltage_vals = [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar()
        ]

        self.beta = tk.StringVar()
        self.vcc = tk.StringVar()
        self.a_v = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        currentRow = 0
        self.input_label = tk.Label(self, text='Inputs:')
        self.input_label.grid(columnspan=2, column=0,
                              row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.input_label = tk.Label(self, text='Circuit Type:')
        self.input_label.grid(column=0,
                              row=currentRow, padx=10, pady=10)
        self.circuit_type_ddl = tk.OptionMenu(
            self, self.circuit_type, 'CE', 'CC', 'CB', command=self.update_elements)
        self.circuit_type_ddl.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.vcc_label = tk.Label(self)
        self.vcc_label['text'] = 'Vcc'
        self.vcc_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.vcc = tk.Entry(self, textvariable=self.vcc)
        self.vcc.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.beta_label = tk.Label(self)
        self.beta_label['text'] = 'β'
        self.beta_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.beta = tk.Entry(self, textvariable=self.beta)
        self.beta.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.r_e_label = tk.Label(self)
        self.r_e_label['text'] = 'Re (kΩ)'
        self.r_e_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.r_e = tk.Entry(self, textvariable=self.resistor_vals[0])
        self.r_e.grid(column=1, row=currentRow, padx=1)
        currentRow += 1
        self.r_b1_label = tk.Label(self)
        self.r_b1_label['text'] = 'Rb1 (kΩ)'
        self.r_b1_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.r_b1 = tk.Entry(self, textvariable=self.resistor_vals[1])
        self.r_b1.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.r_b2_label = tk.Label(self)
        self.r_b2_label['text'] = 'Rb2 (kΩ)'
        self.r_b2_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.r_b2 = tk.Entry(self, textvariable=self.resistor_vals[3])
        self.r_b2.grid(column=1, row=currentRow, padx=10, pady=10)
        currentRow += 1
        self.r_c_label = tk.Label(self)
        self.r_c_label['text'] = 'Rc (kΩ)'
        self.r_c_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.r_c = tk.Entry(self, textvariable=self.resistor_vals[2])
        self.r_c.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.calc = tk.Button(self, text='CACLCULATE!',
                              fg='green', command=self.calc_circuit)
        self.calc.grid(column=0, columnspan=2,
                       row=currentRow, padx=10, pady=10)
        currentRow = 0
        self.input_label = tk.Label(self, text='Outputs:')
        self.input_label.grid(columnspan=2, column=2,
                              row=currentRow, padx=10, pady=10)
        currentRow += 1
        self.i_e_label = tk.Label(self)
        self.i_e_label['text'] = 'Ie (mA)'
        self.i_e_label.grid(column=2, row=currentRow, padx=10, pady=10)

        self.i_e = tk.Entry(self, textvariable=self.current_vals[0])
        self.i_e.grid(column=3, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.i_b_label = tk.Label(self)
        self.i_b_label['text'] = 'Ib (μA)'
        self.i_b_label.grid(column=2, row=currentRow, padx=10, pady=10)

        self.i_b = tk.Entry(self, textvariable=self.current_vals[1])
        self.i_b.grid(column=3, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.i_c_label = tk.Label(self)
        self.i_c_label['text'] = 'Ic (mA)'
        self.i_c_label.grid(column=2, row=currentRow, padx=10, pady=10)

        self.i_c = tk.Entry(
            self, textvariable=self.current_vals[2], state=DISABLED)
        self.i_c.grid(column=3, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.v_c_label = tk.Label(self)
        self.v_c_label['text'] = 'Vc'
        self.v_c_label.grid(column=2, row=currentRow, padx=20, pady=20)

        self.v_c = tk.Entry(self, textvariable=self.voltage_vals[0])
        self.v_c.grid(column=3, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.v_e_label = tk.Label(self)
        self.v_e_label['text'] = 'Ve'
        self.v_e_label.grid(column=2, row=currentRow, padx=10, pady=10)

        self.v_e = tk.Entry(self, textvariable=self.voltage_vals[1])
        self.v_e.grid(column=3, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.v_b_label = tk.Label(self)
        self.v_b_label['text'] = 'Vb'
        self.v_b_label.grid(column=2, row=currentRow, padx=10, pady=10)

        self.v_b = tk.Entry(self, textvariable=self.voltage_vals[2])
        self.v_b.grid(column=3, row=currentRow, padx=10, pady=10)

        currentRow += 2

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(column=2, columnspan=2,
                       row=currentRow, padx=10, pady=10)

        self.av_label = tk.Label(self, text="Av")
        self.av_label.grid(column=4,  row=1, padx=10, pady=10)

        self.av = tk.Entry(self, textvariable=self.a_v)
        self.av.grid(column=5,  row=1, padx=10, pady=10)

        image = Image.open('images/CE.png')
        image = image.resize([int(image.width/2), int(image.height/2)])
        test = ImageTk.PhotoImage(image)

        self.circ_diagram = tk.Label(self, image=test)
        self.circ_diagram.image = test
        self.circ_diagram.grid(row=10, rowspan=10, column=4, columnspan=4)

        self.draw_av_graph()

    def calc_circuit(self):
        circ_type = self.circuit_type.get()
        vcc = float(self.vcc.get())
        beta = float(self.beta.get())
        r_e = float(self.resistor_vals[0].get())
        r_b1 = float(self.resistor_vals[1].get())
        r_c = float(self.resistor_vals[2].get())
        r_b2 = float(self.resistor_vals[3].get())

        if r_e < 1:
            r_e = 0.5

        if r_b1 > 0 and r_b2 > 0:
            v_th = (r_b2/(r_b1+r_b2))*vcc
            r_bth = parallel_divide([r_b1, r_b2])
            i_b = (v_th - 0.7)/(r_bth+(1+beta)*r_e)
        elif r_b1 > 0 and r_b2 <= 0:
            i_b = (vcc - 0.7)/(r_b1+(1+beta)*r_e)
        else:
            i_b = (vcc - 0.7)/(r_b2+(1+beta)*r_e)
        i_e = (1+beta) * i_b
        i_c = (beta) * i_b

        self.current_vals[0].set(round(i_e, 3))
        self.current_vals[1].set(round(i_b, 3) * 1000)
        self.current_vals[2].set(round(i_c, 3))

        v_e = i_e * r_e
        v_b = v_e + .7

        if circ_type == "CE":
            v_c = vcc - (i_c * r_c)
        elif circ_type == "CC":
            v_c = vcc
        else:  # "CB"
            v_c = vcc - i_c * r_c

        self.voltage_vals[0].set(round(v_c, 3))
        self.voltage_vals[1].set(round(v_e, 3))
        self.voltage_vals[2].set(round(v_b, 3))

        r_pi = .0259 / i_b
        gm = i_c / .0259

        if circ_type == "CE":
            A_v = -gm * r_c
        elif circ_type == "CC":
            A_v = ((1 + beta)*r_e)/(r_pi + (1+beta)*r_e)
        else:
            A_v = r_c / r_e * (beta / (beta+1))

        self.a_v.set(A_v)
        self.draw_av_graph(A_v)

    def update_elements(self, args):
        self.set_r_c_vis()
        self.draw_circ_diagram()

    def set_r_c_vis(self):
        circ_type = self.circuit_type.get()
        if circ_type == "CC":
            self.r_c.grid_forget()
        else:
            self.r_c.grid(column=1, row=7, padx=10, pady=10)

    def draw_av_graph(self, A_v=None):
        av_graph = Figure()
        av_plot = av_graph.add_subplot(111)

        if A_v is not None:
            time, input_signal, output_vals = self.create_av_vals(A_v)
            av_plot.plot(time, input_signal)
            av_plot.plot(time, output_vals)
        else:
            av_plot.plot()

        canvas = FigureCanvasTkAgg(av_graph, self)
        canvas.get_tk_widget().grid(row=2, rowspan=8, column=4, columnspan=4)

    def create_av_vals(self, A_v):
        time = np.arange(0, 10, 0.1)
        input_vals = np.sin(time)
        output_vals = A_v * input_vals
        return (time, input_vals, output_vals)

    def draw_circ_diagram(self):
        self.circ_diagram.grid_forget()
        circ_type = self.circuit_type.get()
        image = Image.open(f'images/{circ_type}.png')
        image = image.resize([int(image.width/2), int(image.height/2)])
        test = ImageTk.PhotoImage(image)

        self.circ_diagram = tk.Label(self, image=test)
        self.circ_diagram.image = test
        self.circ_diagram.grid(row=10, rowspan=10, column=4, columnspan=4)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        app1 = Input(master=root)
        app1.grid(rowspan=2, row=0, column=0)


app = Application(master=root)
app.mainloop()
