#Project: SW Testing and QA Homework 2
#Name: Elijah Magee
#Date Due: Feb 5th, 2020
#Instructor: Tanmay Bhowmik
#main.py

import body
import retire

#Main loop
while(True):

    #We use a try block to catch bad input
    try:
        
        x = int(input("\nFor Body Mass Index Type 1\nFor Retirement type 2\nTo quit type 3\n: "))

        #Go down the menus
        if (x == 1):

            body.bodymassindex(input("Input you height in feet: "),input("Input your height in inches: "), input("Input your weight in pounds: "))
        elif(x==2):
            retire.retirement(input("Input your age in years: "),input("How much do you make per year?: "),input("What percentage will you save per year?: "), input("How much do you want when you retire?: "))
        elif(x==3):
            
            #Quiting the program will break from the loop which stops program
            print("Have a good day!\n")
            break
        else:
            
            #Raise an exception for input that isn't on list
            raise

    except:
        
        #Print error message and let loop rerun
        print("Bad input\n")
