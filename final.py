import tkinter as tk


root = tk.Tk()
root.geometry('600x400')

class Application(tk.Frame):
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
        self.resistor_vals= [
            tk.StringVar(),
            tk.StringVar(),
            tk.StringVar()
        ]
        self.beta = tk.StringVar()
        self.vcc = tk.StringVar()
        self.create_widgets()


    def create_widgets(self):

        self.circuit_type_ddl = tk.OptionMenu(self, self.circuit_type, 'CE', 'CC', 'CB')
        self.circuit_type_ddl.pack(side='top')

        self.vcc_label= tk.Label(self)
        self.vcc_label['text'] = 'Vcc'
        self.vcc_label.pack(side='top')

        self.vcc = tk.Entry(self, textvariable=self.vcc)
        self.vcc.pack(side='top')

        self.beta_label = tk.Label(self)
        self.beta_label['text'] = 'β'
        self.beta_label.pack(side='top')

        self.beta = tk.Entry(self, textvariable=self.beta)
        self.beta.pack(side='top')

        self.r_e_label = tk.Label(self)
        self.r_e_label['text'] = 'Re (kΩ)'
        self.r_e_label.pack(side='top')

        self.r_e = tk.Entry(self, textvariable=self.resistor_vals[0])
        self.r_e.pack(side='top')

        self.r_b_label = tk.Label(self)
        self.r_b_label['text'] = 'Rb (kΩ)'
        self.r_b_label.pack(side='top')

        self.r_b = tk.Entry(self, textvariable=self.resistor_vals[1])
        self.r_b.pack(side='top')

        self.r_c_label = tk.Label(self)
        self.r_c_label['text'] = 'Rc (kΩ)'
        self.r_c_label.pack(side='top')

        self.r_c = tk.Entry(self, textvariable=self.resistor_vals[2])
        self.r_c.pack(side='top')
        self.i_e_label = tk.Label(self)
        self.i_e_label['text'] = 'Ie (mA)'
        self.i_e_label.pack(side='top')

        self.i_e = tk.Entry(self, textvariable=self.current_vals[0])
        self.i_e.pack(side='top')

        self.i_b_label = tk.Label(self)
        self.i_b_label['text'] = 'Ib (μA)' 
        self.i_b_label.pack(side='top')

        self.i_b = tk.Entry(self, textvariable=self.current_vals[1])
        self.i_b.pack(side='top')

        self.i_c_label = tk.Label(self)
        self.i_c_label['text'] = 'Ic (mA)'
        self.i_c_label.pack(side='top')

        self.i_c = tk.Entry(self, textvariable=self.current_vals[2])
        self.i_c.pack(side='top')

        self.calc = tk.Button(self, text='CACLCULATE!', fg='green', command=self.calc_circuit)
        self.calc.pack(side='top')

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def calc_circuit(self):
        circ_type = self.circuit_type.get()
        vcc = float(self.vcc.get())
        beta = float(self.beta.get())
        r_e  = float(self.resistor_vals[0].get())
        r_b  = float(self.resistor_vals[1].get())
        r_c  = float(self.resistor_vals[2].get())


        i_b = (vcc - 0.7)/(r_b+(1+beta)*r_e)
        i_e = (1+beta) * i_b
        i_c = (beta) * i_b
        
        self.current_vals[0].set(round(i_e,3))
        self.current_vals[1].set(round(i_b,3)  * 1000)
        self.current_vals[2].set(round(i_c,3))

        


app = Application(master=root)
app.mainloop()
