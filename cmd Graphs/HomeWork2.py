"""
Author: Hila Rahimipour
homework exercise 2
The program gets an equation involving x and x&y limits
The program asks to enter a new variables in case of an error
The program returns a drawing of the equation in the given limits
"""
#importing math in order to allow functions
from math import *

#setting x and y
global x
global y

#setting the max length of the function's drawing
prop_x_max = 40
prop_y_max = 20

#explaning the program to the user
print("Hello! Please use x as a variable.\nYou can use all math functions such as sin, cos, tan, sqrt, log...")
print("multiplation: *\ndivision: / or //\naddition: +\nsubtraction: -\nexponent: **\n")

#getting variables (the equation and the x&y limits),
#checking for errors in the entered input using try and except
check = False
while not check:
    formula = input('Provide a formula involving x: ')
    x = 5
    try:
        eval(formula)
        check = True
    except NameError:
        print("you are using an undefined variable, please use x")
    except SyntaxError:
        print("you must enter a formula")
    except ZeroDivisionError:
        continue
    except:
        print("an unknown error occurred in formula")
        raise
    
check = False
while not check:
    try:    
        start_x = int(input('Left bound x value: '))
        if start_x<=0:
            check = True
        else:
            print("start_x must be smaller or equal to 0")
    except ValueError:
        print("start_x must be an integre")
    except SyntaxError:
        print("you must enter a start_x")
    except:
        print("an unknown error occurred in start_x")
        raise

check = False
while not check:
    try:
        end_x = int(input('Right bound x value: '))
        if end_x>=0:
            check = True
        else:
            print("end_x must be bigger or equal to 0")
    except ValueError:
        print("end_x must be an integre")
    except SyntaxError:
        print("you must enter a end_x")
    except:
        print("an unknown error occurred in end_x")
        raise

check = False
while not check:
    try:
        start_y = int(input('Bottom bound y value: '))
        if start_y<=0:
            check = True
        else:
            print("start_y must be smaller or equal to 0")
    except ValueError:
        print("start_y must be an integre")
    except SyntaxError:
        print("you must enter a start_y")
    except:
        print("an unknown error occurred in start_y")
        raise

check = False
while not check:
    try:
        end_y = int(input('Top bound y value: '))
        if end_y>=0:
            check = True
        else:
            print("start_y must be bigger or equal to 0")
    except ValueError:
        print("end_y must be an integre")
    except SyntaxError:
        print("you must enter a end_y")
    except:
        print("an unknown error occurred in end_y")
        raise

#creating the foundations for the axis system and the function itself usint list
list_y = []

#the function creats the axis system and adds the y axis
#if the x range or the y range is bigger than prop, the function will create the function into scale.
def creating_y_axis(start_x, end_x, start_y, end_y, list_y):
    if end_y-start_y<=prop_y_max:
        for i in range(start_y, end_y+1):
            if end_x-start_x<=prop_x_max:
                list_x = [' ']*(end_x+1-start_x)
                list_x[0-start_x] = '|'
                list_y.append(list_x)
            else:
                list_x = [' ']*((end_x+1-start_x)//((end_x - start_x) // prop_x_max))
                list_x[0-start_x//((end_x - start_x) // prop_x_max)] = '|'
                list_y.append(list_x)
    else:
        for i in range(start_y//((end_y - start_y) // prop_y_max), end_y//((end_y - start_y) // prop_y_max)+1):
            if end_x-start_x<=prop_x_max:
                list_x = [' ']*(end_x+1-start_x)
                list_x[0-start_x] = '|'
                list_y.append(list_x)
            else:
                list_x = [' ']*((end_x+1-start_x)//((end_x - start_x) // prop_x_max))
                list_x[0-start_x//((end_x - start_x) // prop_x_max)] = '|'
                list_y.append(list_x)

#the function creats the x axis in the given axis system
#if the x range or the y range is bigger than prop, the function will create the function into scale.
def creating_x_axis(start_x, end_x, start_y, list_y):
    if end_y-start_y<=prop_y_max:
        if end_x-start_x<=prop_x_max:
            for x in range(end_x-start_x+1):
                list_y[0-start_y][x] = '-'
        else:
            for x in range(start_x//((end_x - start_x) // prop_x_max), end_x//((end_x - start_x) // prop_x_max)+1):
                list_y[0-start_y][x//((end_x - start_x) // prop_x_max)] = '-'
    else:
        if end_x-start_x<=prop_x_max:
            for x in range(end_x-start_x+1):
                list_y[0-start_y//((end_y - start_y) // prop_y_max)][x] = '-'  # Error
        else:
            for x in range(start_x//((end_x - start_x) // prop_x_max), end_x//((end_x - start_x) // prop_x_max)+1):
                list_y[0-start_y//((end_y - start_y) // prop_y_max)][x] = '-'

#the function finds the position of each point (x, y) and places it in the given axis system
#the program moves on in case of division by zero or value out of function range
#if the x range or the y range is bigger than prop, the function will create the function into scale.
def drawing_function(start_x, end_x, start_y, end_y, list_y):
    if end_y-start_y<=prop_y_max:
        if end_x-start_x<=prop_x_max:
            for x in range(start_x, end_x+1):
                try:
                    y = round(eval(formula))
                except (ValueError, TypeError, ZeroDivisionError):
                    continue
                if start_y<=y<=end_y:
                    list_y[y-start_y][x-start_x] = 'x'
        else:
            for x in range(start_x//((end_x - start_x) // prop_x_max), end_x//((end_x - start_x) // prop_x_max)+1):
                try:
                    y = round(eval(formula))
                except (ValueError, TypeError, ZeroDivisionError):
                    continue
                if start_y<=y<=end_y:
                    list_y[y-start_y][x-start_x//((end_x - start_x) // prop_x_max)] = 'x'
                    
    else:
        if end_x-start_x<=prop_x_max:
            for x in range(start_x, end_x+1):
                try:
                    y = round(eval(formula))
                except (ValueError, TypeError, ZeroDivisionError):
                    continue
                if start_y//((end_y - start_y) // prop_y_max)<=y<=end_y//((end_y - start_y) // prop_y_max):
                    list_y[y-start_y//((end_y - start_y) // prop_y_max)][x-start_x] = 'x'
        else:
            for x in range(start_x//((end_x - start_x) // prop_x_max), end_x//((end_x - start_x) // prop_x_max)+1):
                try:
                    y = round(eval(formula))
                except (ValueError, TypeError, ZeroDivisionError):
                    continue
                if start_y//((end_y - start_y) // prop_y_max)<=y<=end_y//((end_y - start_y) // prop_y_max):
                    list_y[y-start_y//((end_y - start_y) // prop_y_max)][x-start_x//((end_x - start_x) // prop_x_max)] = 'x'
    list_y.reverse()

#the function prints the equation with the axis system 
def print_function(list_y):
    print(f'\nyour function looks like this: {formula}\n\n')
    print(f'each scale mark (x) represents {((end_x - start_x) // prop_x_max)} units')
    print(f'each scale mark (y) represents {((end_y - start_y) // prop_y_max)} units')
    for y in range(len(list_y)):
        for x in range(len(list_y[y])):
            print(list_y[y][x], end=' ')
        print()

#applying the functions
creating_y_axis(start_x, end_x, start_y, end_y, list_y)
creating_x_axis(start_x, end_x, start_y, list_y)
drawing_function(start_x, end_x, start_y, end_y, list_y)
print_function(list_y)

input()
