import os
import numpy as np #numpy or Numerical Python is an inbuilt python library which has function to solve high level scientific problems
import matplotlib.pyplot as plt #matplotlib is a library which provides matlab like interface and function in python itself

# We will create a Class , which will help us assign different data plots for different beams

class Beam:
    
    def __init__(self, length,name="default_beam"): #this automatically creates the intital requirements of the beams
        
        self.name=name
        self.length=length #assigning the given beam length to it
        self.point_loads=[] #array for loads which are in the range(0,L) as [(pos,magnitude)]
        self.udls=[] #array for the uniformly distributed loads as [(start,end,intensity)]
        self.L=0 #Left suppport Reaction
        self.R=0 #Right suppport Reaction

    def add_point_load(self,pos,magnitude): #adds the point loads in the array point_loads
        self.point_loads.append((pos,magnitude))

    def add_udl(self, start,end,intensity): #adds the UDL in the array udls
        self.udls.append((start,end,intensity))


    # Now we need to compute the SFD and BMD

    #this computes the initial values we require to calcualte the SFD and BMD   OR calculation of support reactions
    def compute_reactions(self):    

        total_load = 0
        moment_about_A = 0

        for pos,mag in self.point_loads:# as the loads in range(0,L) in point_loads are in pairs we are using two iterables pos , mag
            total_load+=mag #caluclating the total load 
            moment_about_A+=(mag*pos) #calculating the total moment about A

        for start,end,intensity in self.udls:
            length=end-start #total length of the UDL
            total_load+=(intensity*length) #total intensity over the given length
            center=(start+length) / 2 #calculates the point at which the total load will be applied
            moment_about_A+=(intensity*length*center) #calcualtes the impact of the UDL on the point A

        self.R=(moment_about_A/self.length) # force on right point as Moment=Force*Length
        self.L=total_load-self.R #compatibilty is used


    #Function to calculate the SF at a given point x
    def shear_force_at(self, x):
        V=self.L

        for pos,mag in self.point_loads:
            if x>=pos: #if x is on the right of the load , the load will have an impact on x
                V+=mag

        for start,end,intensity in self.udls:
            if x>=start: #checks if load is on the right of x or left
                if x<=end:
                    V+= intensity*(x-start) #as x is situated in between start and end of the UDL only partial UDL will be accounted for
                else:
                    V+= intensity*(end-start) #total UDL will be added

        return V #returns the shear force at the point x


    #Now we need to calculate the BM at any point x
    def bending_moment_at(self, x):
        M = (self.L)*x # Calculates the total BM if no other force was present between x and 0(Left point of beam)

        for pos,mag in self.point_loads:
            if x>=pos:
                M += mag*(x-pos) # as we are calculating the BM at point x , we know that we have clockwise as positive so we only need to consider the distance between the point x and pos

        for start,end,intensity in self.udls:
            if x>=start:
                if x<=end:
                    a= x-start
                    M+= (intensity*a )* (a/2) #(intensity * a ) calcualtes the total force which is currently imapcting point x, (a/2) is the point at which the said total force is applied so the distance of point x and the total force is also (a/2)
                else:
                    length = end-start
                    M+= (intensity*length)* ((x-((start+length)/2)))

        return M
 
    # Now we need to plot the values using the function formuales we made earlier
    def plot_SFD_BMD(self):
        self.compute_reactions()#executing the function to calcualte the required support reactions

        x_vals = np.linspace(0, self.length, 500) #using linspace to create 500 points between (0,L)
        shear_vals = [self.shear_force_at(x) for x in x_vals]#using the shear force function to calcualte SF at x at all 500 points
        moment_vals = [self.bending_moment_at(x) for x in x_vals]#same for BM

        plt.figure(figsize=(12,6)) #created a figure of size 12,6

        # Shear Force Diagram
        plt.subplot(2,1,1) #now creating a subplot in the 1st row
        plt.plot(x_vals,shear_vals,  color='blue',label='SF')

        plt.axhline(0,color='black',linewidth=0.8)#a horizontal line representing the beam 

        plt.title('Shear Force Diagram') #title of the subplot
        plt.ylabel('Shear Force (kN)')#y axis
        plt.grid(True)#grids are on
        plt.legend()#shows which line is what

        # Bending Moment Diagram
        plt.subplot(2,1,2)
        plt.plot(x_vals,moment_vals,  color='red',label='BM')

        plt.axhline(0,color='black',linewidth=0.8)

        plt.title('Bending Moment Diagram')
        plt.xlabel('Beam Length (m)')
        plt.ylabel('Bending Moment (kNm)')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()#lets make sure nothing overlaps

        #To create a folder for the image
        output_folder="Beam_Outputs"
        os.makedirs(output_folder, exist_ok=True)

        filename = f"{self.name}.png"
        filepath = os.path.join(output_folder, filename)
        plt.savefig(filepath, dpi=300)

        plt.show()#shows the subplot
       


# EDIT THE VALUES IN HERE PLEASE
#-ve value for downwards force and +ve for upwards

if __name__ == "__main__":#makes sure that the function does not run twice if we are accessing it from any other folder
    
    # beamA = Beam(length= )
    # beamA.add_point_load(pos= ,magnitude= )#enter the required values       
    # beamA.add_udl(start= ,end= ,intensity= )     
    # beamA.plot_SFD_BMD()
    
    beam = Beam(length=15,name="Beam A")
    beam.add_point_load(pos=5, magnitude=-10)
    beam.add_point_load(pos=12, magnitude=-6)
    beam.add_udl(start=7, end=14, intensity=-2)
    beam.plot_SFD_BMD()


 
