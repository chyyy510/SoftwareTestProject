#Project: SW Testing and QA Homework 2
#Name: Elijah Magee
#Date Due: Feb 5th, 2020
#Instructor: Tanmay Bhowmik
#body.py

def bodymassindex(h1,h2, weight):
    try:
        #if h1 < 0 or h2 < 0 or weight < 0:
        #    raise
        
        height = int(h1)*12+int(h2)
        print(int(weight)*.45/((0.025*int(height))**2))
        if (int(weight)*.45/((0.025*int(height))**2) < 18.5):
            print("Underweight")
        elif (int(weight)*.45/((0.025*int(height))**2) >= 18.5 and int(weight)*.45/((0.025*int(height))**2) < 25):
    
            print("Normal Weight")
        elif (int(weight)*.45/((0.025*int(height))**2) < 30 and int(weight)*.45/((0.025*int(height))**2) >= 25):
            print("Overweight")
        elif (int(weight)*.45/((0.025*int(height))**2) >= 30):
            print("Obese")
            

    except:
        print("Bad input for body mass index function")
