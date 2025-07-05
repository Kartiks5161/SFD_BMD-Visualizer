import os
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt

class Beam: 
    def __init__(self,length,name="default_beam"):#default function , creating the arrrays of point loads and UDLs , also creating the edge vertical forces
        self.name=name
        self.length=length
        self.point_loads=[]
        self.udls=[]
        self.L=0
        self.R=0

    def add_point_load(self, pos, magnitude):#simply appends the user given point loads to the array
        self.point_loads.append((pos, magnitude))

    def add_udl(self, start, end, intensity):#same for this
        self.udls.append((start, end, intensity))

    def compute_reactions(self):#NOW we need to compute hte support reactions at the edges
        total_load = 0
        moment_about_A = 0

        for pos, mag in self.point_loads:
            total_load += mag
            moment_about_A += mag * pos

        for start, end, intensity in self.udls:
            length = end - start
            total_load += intensity * length
            center = (start + end) / 2  
            moment_about_A += intensity * length * center

        self.R = moment_about_A / self.length
        self.L = total_load - self.R

    def shear_force_at(self,x):#calcualting shear force at any point x, at 0 pos the shear force is equal to the support raction but as we move forward the support reaction reduces if the point load faces downwards 
        V=self.L
        for pos,mag in self.point_loads:
            if x>=pos:
                V-= mag  
        for start,end,intensity in self.udls:
            if x>=start:
                if x<=end:
                    V-= intensity * (x-start)  
                else:
                    V-= intensity * (end-start) 
        return V

    def bending_moment_at(self, x):
        M=self.L * x

        for pos,mag in self.point_loads:
            if x>=pos:
                M-= mag * (x-pos) 

        for start, end, intensity in self.udls:
            if x>=start:
                if x<=end:
                    a=x-start
                    M-= (intensity * (a ** 2))/2 
                else:
                    length=end-start
                    centroid=(start + end)/2
                    M-= intensity * length * (x-centroid) 

        return M

    def plot_SFD_BMD(self):
        self.compute_reactions()

        x_vals=np.linspace(0,self.length,500)
        shear_vals=[self.shear_force_at(x) for x in x_vals]
        moment_vals=[self.bending_moment_at(x) for x in x_vals]

        plt.figure(figsize=(12,6))

        plt.subplot(2,1,1)
        plt.plot(x_vals,shear_vals,color='blue',label='SF')
        plt.axhline(0,color='black',linewidth=0.8)
        plt.title('Shear Force Diagram')
        plt.ylabel('Shear Force (kN)')
        plt.grid(True)
        plt.legend()

        plt.subplot(2,1,2)
        plt.plot(x_vals,moment_vals,color='red',label='BM')
        plt.axhline(0,color='black',linewidth=0.8)
        plt.title('Bending Moment Diagram')
        plt.xlabel('Beam Length (m)')
        plt.ylabel('Bending Moment (kNm)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()

        output_folder="Beam_Outputs"
        os.makedirs(output_folder, exist_ok=True)
        filename=f"{self.name}.png"
        filepath=os.path.join(output_folder, filename)
        plt.savefig(filepath, dpi=300)

        plt.show()


class Beam_GUI:
    def __init__(self, root):
        self.root=root
        self.root.title("Beam SFD & BMD")
        self.point_loads=[]
        self.udls=[]

        #creating the labels and entries 

        tk.Label(root,text="Beam Length:").grid(row=0,column=0)
        self.length_entry=tk.Entry(root)
        self.length_entry.grid(row=0,column=1)

        tk.Label(root,text="Point Load (pos,mag):").grid(row=1,column=0)
        self.point_loads_entry=tk.Entry(root)
        self.point_loads_entry.grid(row=1,column=1)

        tk.Label(root, text="UDL (start,end,intensity):").grid(row=2, column=0)
        self.UDL_entry=tk.Entry(root)
        self.UDL_entry.grid(row=2,column=1)

        #creating the buttons and assigning them commands

        tk.Button(root,text="CLEAR", command=self.clear_entries).grid(row=0,column=2)
        tk.Button(root,text="Add Point Load", command=self.add_point_load).grid(row=1,column=2)
        tk.Button(root,text="Add UDL", command=self.add_udl).grid(row=2,column=2)
        tk.Button(root,text="Plot Beam", command=self.plot_beam).grid(row=3,column=1)

        #creating a log sheet , just to know which forces have been added

        self.log=tk.Text(root,height=8,width=50)
        self.log.grid(row=4,column=0,columnspan=3)


    def add_point_load(self):

        try:

            pos,mag =map(float,self.point_loads_entry.get().split(','))
            self.point_loads.append((pos,mag))
            self.log.insert(tk.END,f"Added Point Load: {mag} kN at {pos} m\n")

        except:

            messagebox.showerror("Error","Enter point load as: pos, magnitude")

    def add_udl(self):

        try:

            start,end,intensity = map(float,self.UDL_entry.get().split(','))
            self.udls.append((start,end,intensity))
            self.log.insert(tk.END,f"Added UDL: {intensity} kN/m from {start} to {end} m\n")

        except:

            messagebox.showerror("Error", "Enter UDL as: start, end, intensity")

    def plot_beam(self):

        try:

            length = float(self.length_entry.get())
            beam = Beam(length=length, name="GUI_Beam")

            for pos, mag in self.point_loads:

                beam.add_point_load(pos,mag)

            for start, end, intensity in self.udls:

                beam.add_udl(start, end, intensity)


            beam.plot_SFD_BMD()


        except:
            messagebox.showerror("Error", "Please enter a valid beam length")

    def clear_entries(self):
        #clearing the entries
        self.length_entry.delete(0,tk.END)
        self.point_loads_entry.delete(0,tk.END)
        self.UDL_entry.delete(0, tk.END)

        #clearing the logs
        self.log.delete('1.0',tk.END)

        #clearing the arrays
        self.point_loads.clear()
        self.udls.clear()



if __name__ == "__main__":

    root = tk.Tk()
    gui = Beam_GUI(root)
    root.mainloop()
