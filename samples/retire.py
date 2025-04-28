#Project: SW Testing and QA Homework 2
#Name: Elijah Magee
#Date Due: Feb 5th, 2020
#Instructor: Tanmay Bhowmik
#retire.py

def retirement(age, salary, saving, wanted):
    try:

        
        if (int(age)+int(wanted)/(float(salary)*float(saving)*1.35/100) >= 100):
            print("Goal cannot be met. You will die first.")
        else:
            print (int(age)+int(wanted)/(float(salary)*float(saving)*1.35/100))

        
    except:
        print("Bad input for retirement function")
