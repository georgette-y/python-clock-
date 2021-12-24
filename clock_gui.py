from tkinter import * #all these modules come with python , so you don't have to install any
import threading 
import math 
import time 

window = Tk() #creating a window
window.geometry("600x600") #adjusting the window's width and length, that is 600x600
WIDTH =  500 #width and height of the canvas, both are constants
HEIGHT = 500

canvas = Canvas(window, width = WIDTH, height = HEIGHT) #creating a canvas
canvas.pack() #packing the canvas to the screen
oval = canvas.create_oval(10,10,500,500) #the oval's arguments are(top_left_on_x_axis,top_left_on_y_axis,button_right_on_x_axis,button_right_on_y_axis)
line_minutes = canvas.create_line(250,250,250,100,fill="black")#creating the clock hand,the one that points on the minutes
line_seconds = canvas.create_line(250,250,250,50,fill="red")#creating the 2nd clock hand,the one that points on the seconds
line_hours = canvas.create_line(250,250,250,150,fill="black")#creating the 3rd clock hand,the one that points on the hours
hours_list = list(range(1,25)) #a list containing the hours from 1 to 24
seconds_list = list(range(1,60)) + [0]#a list containing the seconds from 1 to 59
angles = range(60,-660,-30)#the angles needed to rotate the hour hand each time by 30 degrees
angle_seconds = range(84,-276,-6)#the angles needed to rotate the 2nd clock hand each time by 6 degrees
hours_angles_pairs = dict(zip(hours_list, angles))#a dict containing the hours as key_name and the angles as key_value
seconds_angles_pairs = dict(zip(seconds_list, angle_seconds))#a dict containing the seconds as key_name and the angles as key_value
center_x = 250 #center of the clock hands on the x axis and y axis and these don't change.
center_y = 250
time_text = 0 
rotating = True

for x in angle_seconds[:60]:#this for loop will loop over the angle_seconds until the 60th element,during each iteration,the clock hand will rotate 6 degrees and add a "."
    angle_in_radians = x * math.pi / 180 
    end_x = center_x + 215 * math.cos(angle_in_radians)
    end_y = center_y - 215 * math.sin(angle_in_radians)
    widget = Label(canvas, text=".")
    widget.pack() 
    canvas.create_window(end_x, end_y, window=widget)
    window.update() #updating the window after each iteration is necessary.

for x in angles[:12]:#this for loop will loop over the angles until the 12th element,during each iteration,the clock hand will rotate 30 degrees and add the clock hours.
    time_text += 1
    angle_in_radians = x * math.pi / 180 
    end_x = center_x + 215 * math.cos(angle_in_radians)
    end_y = center_y - 215 * math.sin(angle_in_radians)
    widget = Label(canvas, text=str(time_text), font = ("arial", 16, "bold"))
    widget.pack() 
    canvas.create_window(end_x, end_y, window=widget)
    window.update() 


l = Label(window,text=time.strftime("%I:%M:%S %p",time.localtime()),font=("Verdana",16))
l.pack() #the label above shows your local time .
def hours(): #this function will check first the local hour time,based on that, it will then look in the dictionary for its corresponding angle and rotate the hour hand.
    while rotating:#the math that i've come up with is pure trigonometry, it might take some time to understand. it was only used to find the new ending positions of the clock hands after each rotation.
        t = time.localtime()
        l.config(text=time.strftime("%I:%M:%S %p",t))
        angle_in_radians = hours_angles_pairs[t[3]] * math.pi / 180 
        end_x = center_x + 150 * math.cos(angle_in_radians) #150 is the line length
        end_y = center_y - 150 * math.sin(angle_in_radians)
        canvas.coords(line_hours, center_x, center_y, end_x, end_y)
        window.update()  

def seconds():#this function will check first the local seconds time,based on that, it will then look in the dictionary for its corresponding angle and rotate the clock hand.
    while rotating:
        t = time.localtime()
        angle_in_radians = seconds_angles_pairs[t[5]] * math.pi / 180 
        end_x_prime = center_x + 200 * math.cos(angle_in_radians) #200 is the line length
        end_y_prime = center_y - 200 * math.sin(angle_in_radians)
        canvas.coords(line_seconds, center_x, center_y, end_x_prime, end_y_prime)
        window.update() 

def minutes():#this function will check first the local minutes time,based on that, it will then look in the dictionary for its corresponding angle and rotate the clock hand.
    while rotating:
        t = time.localtime()
        angle_in_radians = seconds_angles_pairs[t[4]] * math.pi / 180 
        end_x = center_x + 150 * math.cos(angle_in_radians) #150 is the line length
        end_y = center_y - 150 * math.sin(angle_in_radians)
        canvas.coords(line_minutes, center_x, center_y, end_x, end_y)
        window.update()

threading.Thread(target=seconds).start() #threading.Thread() allows all three of the funct to run in parallel
threading.Thread(target=hours).start()
threading.Thread(target=minutes).start()
window.mainloop() 
