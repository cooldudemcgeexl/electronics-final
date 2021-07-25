import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from PIL import Image, ImageTk
from src.ParallelDiv import parallel_divide
root = tk.Tk()
root.geometry('1280x720')


class Input(tk.Frame):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.pack()

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
            tk.StringVar()
        ]

        self.voltage_vals = [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar()
        ]
        
        self.beta = tk.StringVar()
        self.vcc = tk.StringVar()
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
            self, self.circuit_type, 'CE', 'CC', 'CB', command=self.set_r_c_vis)
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
        self.r_e.grid(column=1, row=currentRow, padx=1 )
        currentRow += 1
        self.r_b_label = tk.Label(self)
        self.r_b_label['text'] = 'Rb (kΩ)'
        self.r_b_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.r_b = tk.Entry(self, textvariable=self.resistor_vals[1])
        self.r_b.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.r_c_label = tk.Label(self)
        self.r_c_label['text'] = 'Rc (kΩ)'
        self.r_c_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.r_c = tk.Entry(self, textvariable=self.resistor_vals[2])
        self.r_c.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.i_e_label = tk.Label(self)
        self.i_e_label['text'] = 'Ie (mA)'
        self.i_e_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.i_e = tk.Entry(self, textvariable=self.current_vals[0])
        self.i_e.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.i_b_label = tk.Label(self)
        self.i_b_label['text'] = 'Ib (μA)'
        self.i_b_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.i_b = tk.Entry(self, textvariable=self.current_vals[1])
        self.i_b.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.i_c_label = tk.Label(self)
        self.i_c_label['text'] = 'Ic (mA)'
        self.i_c_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.i_c = tk.Entry(
            self, textvariable=self.current_vals[2], state=DISABLED)
        self.i_c.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.v_c_label = tk.Label(self)
        self.v_c_label['text'] = 'Vc'
        self.v_c_label.grid(column=0, row=currentRow, padx=20, pady=20)

        self.v_c = tk.Entry(self, textvariable=self.voltage_vals[0])
        self.v_c.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.v_e_label = tk.Label(self)
        self.v_e_label['text'] = 'Ve'
        self.v_e_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.v_e = tk.Entry(self, textvariable=self.voltage_vals[1])
        self.v_e.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.v_b_label = tk.Label(self)
        self.v_b_label['text'] = 'Vb'
        self.v_b_label.grid(column=0, row=currentRow, padx=10, pady=10)

        self.v_b = tk.Entry(self, textvariable=self.voltage_vals[2])
        self.v_b.grid(column=1, row=currentRow, padx=10, pady=10)

        currentRow += 1
        self.calc = tk.Button(self, text='CACLCULATE!',
                              fg='green', command=self.calc_circuit)
        self.calc.grid(column=0, row=currentRow, padx=10, pady=10)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(column=1, row=currentRow, padx=10, pady=10)

    def calc_circuit(self):
        circ_type = self.circuit_type.get()
        vcc = float(self.vcc.get())
        beta = float(self.beta.get())
        r_e = float(self.resistor_vals[0].get())
        r_b = float(self.resistor_vals[1].get())
        r_c = float(self.resistor_vals[2].get())

        i_b = (vcc - 0.7)/(r_b+(1+beta)*r_e)
        i_e = (1+beta) * i_b
        i_c = (beta) * i_b

        self.current_vals[0].set(round(i_e, 3))
        self.current_vals[1].set(round(i_b, 3) * 1000)
        self.current_vals[2].set(round(i_c, 3))

        v_e = i_e * r_e
        v_b = v_e + .7

        if circ_type == "CE":
            v_c = vcc - i_c * r_c
        elif circ_type == "CC":
            v_c = vcc
        else: # "CB"
            v_c = vcc - i_c * r_c
    
        self.voltage_vals[0].set(round(v_c, 3))
        self.voltage_vals[1].set(round(v_e, 3))
        self.voltage_vals[2].set(round(v_b, 3))

        

    def set_r_c_vis(self, args):
        circ_type = self.circuit_type.get()
        if circ_type == "CC":
            self.r_c.grid_forget()
        else:
            self.r_c.grid(column=1, row=6, padx=10, pady=10)

    def calc_hybrid_pi(self, i_b: float, i_c: float):
        circ_type = self.circuit_type.get()
        r_pi = .0259 / i_b
        gm = i_c / .0259

        if circ_type == "CE":
            pass
        elif circ_type == "CC":
            pass
        else: # "CB"
            pass

class CircImages(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        image = Image.open('images/test.png')
        #image = image.resize([1000,1000],0)
        test = ImageTk.PhotoImage(image)

        label = tk.Label(image=test)
        label.image = test
        label.grid(row=0,column=4, columnspan=2)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        app1 = Input(master=root)
        app1.grid(rowspan=2,row=0, column=0)
        circImg = CircImages(master=root)
        circImg.grid(row=0,column=3)


app = Application(master=root)
app.mainloop()
