"""
Author: Hila Rahimipour
homework exercise 5
The program creates an app that contains a quiz
using tkinter

"""

#importing libraries
from tkinter import *
from tkinter import font
from tkinter.filedialog import asksaveasfile
import os
import random
import datetime
from PIL import ImageTk, Image  


#the function clears widgets in the tkinter root
def clear(menu):
    for i in root.winfo_children():
        if not i==menu:
            i.destroy()

#the function runs the game            
def play(menu):
    clear(menu)
    create_quiz()

#the function adds date and players name to a variable
#in order to save it, starts the game
def first_play(menu, defult):
    global text_to_save
    global leader
    current_time = datetime.datetime.now() 
    player = defult.get()
    text_to_save = ''
    text_to_save += 'name: ' + player +'\n'
    text_to_save += 'date: ' + str(current_time.day) + '-' + str(current_time.month) + '-' + str(current_time.year) + '\n'
    leader += player + '\n'
    leader += str(current_time.day) + '-' + str(current_time.month) + '-' + str(current_time.year) + '\n'
    clear(menu)
    create_quiz()

#the function shows the Home Page of the app
def play_end(menu):
    global questions
    global lines
    global point
    global grade
    grade = 0
    clear(menu)
    load_questions()
    point = 100/len(questions)
    tk_color = "#%02x%02x%02x" % (232, 255, 237)
            
    fnt = font.Font(family="Comic Sans MS", size=50, weight='bold')
    title = Label(root, text='Welcome to my quiz!', bg="#%02x%02x%02x" % (178, 255, 196), pady=10, font=fnt)
    title.pack(fill='x', pady=30)

    text = Label(root, text='To begin, enter your name and press start', bg=tk_color,
                 font=font.Font(family="Comic Sans MS", size=20), pady=20)
    text.pack()

    defult = StringVar()
    defult.set("Anonymous")

    name = Entry(root, font=font.Font(family="Comic Sans MS", size=20), textvariable=defult)
    name.pack(pady=20)
    player = defult.get()

    start = Button(root, text='Start', font=font.Font(family="Comic Sans MS", size=18, weight='bold'), height=1, width=8,
               bg="#%02x%02x%02x" % (110, 255, 144), command=lambda: first_play(menubar, defult))
    start.pack(pady=10)    

#the function shows the end page when user finishes the quiz        
def end_quiz(v, menu):
    global grade
    global text_to_save
    global leader
    if not v.get()==0:
        clear(menu)
        label = Label(root, text='you finished the quiz', bg=tk_color, font=font.Font(family="Comic Sans MS", size=20))
        label.pack()
        text = Label(root, text=f'your grade is {round(grade, 2)}', bg=tk_color, font=font.Font(family="Comic Sans MS", size=20))
        text.pack()
        text_to_save += 'grade: ' + str(round(grade,2)) + '\n'
        leader += str(round(grade,2)) + '\n\n'
        add_result()
        img = ImageTk.PhotoImage(Image.open("img.gif").resize((250, 250), Image.ANTIALIAS))
        panel = Label(root, image = img)
        panel.image = img
        panel.pack(pady=30)
        Button(root, text='Exit', font=font.Font(family="Comic Sans MS", size=18, weight='bold'), height=1, width=8,
               bg="#%02x%02x%02x" % (110, 255, 144), command=lambda: exit(menu)).pack(pady=30)                            

#the function check if the answer the user entered is correct
#it adds the result into a variable that saves it in case the user wants to save the data
def check(b, v, correct_index, correct, qusetion_index, menu):
    global grade
    global text_to_save
    global point
    if not v.get()==0:
        for i in root.winfo_children():
            if not i==menu:
                i['state'] =DISABLED
        text_to_save += 'answer: (' + str(v.get()) + ')'
        if v.get() == correct_index:
            response = Label(root, text=random.choice(correct), bg=tk_color, font=font.Font(family="Comic Sans MS", size=15), pady=10)
            response.pack()
            grade = grade + point
            text_to_save += '- Correct\n'
        else:
            response = Label(root, text=random.choice(wrong), bg=tk_color, font=font.Font(family="Comic Sans MS", size=15), pady=10)
            response.pack()
            correct = Label(root, text=f'the correct answer is {lines[qusetion_index+1]}({correct_index})',
                            bg=tk_color, font=font.Font(family="Comic Sans MS", size=15), pady=10)
            correct.pack()
            text_to_save += '- Wrong\n'
        if questions:
            button = Button(root, text='Next', font=font.Font(family="Comic Sans MS", size=15), height=1, width=8,
               bg="#%02x%02x%02x" % (110, 255, 144), command=lambda: play(menubar))
            button.pack()
        else:
            button = Button(root, text='End Quiz', font=font.Font(family="Comic Sans MS", size=15), height=1, width=8,
               bg="#%02x%02x%02x" % (110, 255, 144), command=lambda: end_quiz(v, menubar))
            button.pack()
    else:
        label = Label(root, text='you must enter an answer', bg=tk_color, font=font.Font(family="Comic Sans MS", size=15))
        label.pack()

#the function shows the question and possible answers and gets the data from the user
def create_quiz():
    global grade
    global text_to_save
    global questions
    global lines
    question = random.choice(questions)
    text_to_save += 'question: ' + question + '\n'
    qusetion_index = lines.index(question)
    answers = [lines[qusetion_index+1], lines[qusetion_index+2],
               lines[qusetion_index+3], lines[qusetion_index+4]]
    tk_color = "#%02x%02x%02x" % (232, 255, 237)
    text = Label(root, text=question, bg="#%02x%02x%02x" % (178, 255, 196),
                 font=font.Font(family="Comic Sans MS", size=20, weight='bold'), pady=20)
    text.pack(fill="x", pady=30)
    MODES = []
    v = IntVar()
    v.set(0)
    for i in range(4):
        answer = random.choice(answers)
        if lines[qusetion_index+1] == answer:
            correct_index = i+1
        MODES.append((answer, i+1))
        del answers[answers.index(answer)]
    for text, mode in MODES:
        b = Radiobutton(root, text=text, variable=v, value=mode, bg=tk_color, font=font.Font(family="Comic Sans MS", size=15))
        b.pack()    
    del questions[questions.index(question)]
    button = Button(root, text='Check', font=font.Font(family="Comic Sans MS", size=15), height=1, width=8,
                command=lambda: check(b, v, correct_index, correct,qusetion_index, menubar), bg="#%02x%02x%02x" % (110, 255, 144))
    button.pack(pady=30)

#the function shows the help window
def help(menu):
    clear(menu)
    fnt = font.Font(family="Comic Sans MS", size=40, weight='bold')
    text = Label(root, text='Info', bg=tk_color, pady=10, font=fnt)
    text.pack()
    content = Label(root, text='To play the game, enter your name and press start\n' +
                    'choose your answer to the question from the possible answers\n' +
                    'press the "check" button and then press "next"\n' +
                    'at the end, press "end game" and see your grade!'
                    , bg=tk_color, pady=10, font=font.Font(family="Comic Sans MS", size=20))
    content.pack()

def info(menu):
    clear(menu)
    fnt = font.Font(family="Comic Sans MS", size=40, weight='bold')
    text = Label(root, text='Help', bg=tk_color, pady=10, font=fnt)
    text.pack()
    content = Label(root, text='Hi! Thank you for trying my quiz!\n' +
                    "My name is Hila Rahimipour and I'm in the 11th grade\n" +
                    'I made this quiz as a part of my Cyber lessons\n' +
                    'I hope will enjoy the quiz :)'
                    , bg=tk_color, pady=10, font=font.Font(family="Comic Sans MS", size=20))
    content.pack()

#the function saves the data taken so far
def save():
    global text_to_save
    if text_to_save != '':
        name=asksaveasfile(mode='w',defaultextension=".txt")
        name.write(text_to_save)
        name.close
    else:
        info_root = Toplevel(root)
        info_lable = Label(info_root, font=("Comic Sans MS", 30, 'bold'),
                           text="Sorry, there is no information yet :(", bg="#%02x%02x%02x" % (110, 255, 144))
        info_lable.pack()
        
#the function gets information in order to add a question
def add_question(menu):
    clear(menu)
    if os.path.isfile('homework.txt'):
        title = Label(root, text='Update Quiz - add question', font=font.Font(family="Comic Sans MS", size=30, weight='bold'), bg=tk_color) 
        title.pack()
        
        q = StringVar()
        q.set('')
        enter_text = Label(root, text='please enter your question', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
        enter_text.pack(pady=10)
        question = Entry(root, font=font.Font(family="Comic Sans MS", size=16), textvariable=q, width=60)
        question.pack(pady=10)

        a1 = StringVar()
        a1.set('')
        enter_answer1 = Label(root, text='enter the correct answer', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
        enter_answer1.pack(pady=5)
        answer1 = Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a1)
        answer1.pack(pady=5)

        a2 = StringVar()
        a2.set('')
        enter_answer2 = Label(root, text='enter an answer', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
        enter_answer2.pack(pady=5)
        answer2 = Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a2)
        answer2.pack(pady=5)

        a3 = StringVar()
        a3.set('')
        enter_answer3 = Label(root, text='enter an answer', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
        enter_answer3.pack(pady=5)
        answer3 = Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a3)
        answer3.pack(pady=5)

        a4 = StringVar()
        a4.set('')
        enter_answer4 = Label(root, text='enter an answer', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
        enter_answer4.pack(pady=5)
        answer4 = Entry(root,  width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a4)
        answer4.pack(pady=5)
        
        Button(root, text='Add Question', font=font.Font(family="Comic Sans MS", size=15), command=lambda:add(q, a1, a2, a3, a4),
                bg="#%02x%02x%02x" % (110, 255, 144)).pack(pady=30)

#the question checks if there is an answer that is the same as another
def duplicate(listOfElems):
    if len(listOfElems) == len(set(listOfElems)):
        return False
    else:
        return True

#the function adds the question and its answers                
def add(q, a1, a2, a3, a4):
    global questions
    answers = []
    question = q.get()
    answer1 = a1.get()
    answer2 = a2.get()
    answer3 = a3.get()
    answer4 = a4.get()

    answers.append(answer1)
    answers.append(answer2)
    answers.append(answer3)
    answers.append(answer4)
    if answer1!='' and answer2!='' and answer3!='' and answer4!='' \
       and not duplicate(answers) and not question in questions and not "?" in question:
        input_file = open(r"homework.txt", "a")
        input_file.write('\n' + question + '\n')
        input_file.write(answer1 + '\n')
        input_file.write(answer2 + '\n')
        input_file.write(answer3 + '\n')
        input_file.write(answer4)
        input_file.close
        clear(menubar)
        Label(root, text='question added successfully :)', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()
        Button(root, text='return to Home Page', font=font.Font(family="Comic Sans MS", size=15), command=lambda:play_end(menubar),
                bg="#%02x%02x%02x" % (110, 255, 144)).pack(pady=30)
    else:
        clear(menubar)
        Label(root, text='please enter different answers and a question that doesnt already exists with a question mark ("?")',
              font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()
        Button(root, text='try again', font=font.Font(family="Comic Sans MS", size=15), command=lambda:add_question(menubar),
                bg="#%02x%02x%02x" % (110, 255, 144)).pack(pady=30)

#the function shows the "update page"       
def update(menu):
    clear(menu)
    frame = Frame(root, bg=tk_color)
    Label(frame, text='Update Quiz', font=font.Font(family="Comic Sans MS", size=30, weight='bold'),
          bg=tk_color).grid(row=0, column=1, pady=50)
    Button(frame, text='Add Question', font=font.Font(family="Comic Sans MS", size=15),  bg="#%02x%02x%02x" % (110, 255, 144),
           command=lambda:add_question(menu)).grid(row=1, column=0, padx=5)
    Button(frame, text='Delete Question', font=font.Font(family="Comic Sans MS", size=15),  bg="#%02x%02x%02x" % (110, 255, 144),
           command=lambda:delete_question(menu)).grid(row=1, column=1, padx=5)
    Button(frame, text='Update Question', font=font.Font(family="Comic Sans MS", size=15),  bg="#%02x%02x%02x" % (110, 255, 144),
           command=lambda:update_question(menu)).grid(row=1, column=2, padx=5)
    frame.pack(pady=100)

#the function shows the exit page and exits the program
def exit(menu):
    clear(menu)
    Label(root, text="thank's for playing!\nHope to see you soon! :)", font=font.Font(family="Comic Sans MS", size=30, weight='bold'),
          bg=tk_color).pack(pady=30)
    Button(root, text='Exit', font=font.Font(family="Comic Sans MS", size=15),  bg="#%02x%02x%02x" % (110, 255, 144),
           command=root.destroy).pack(pady=30)

#the function gets the information about the question that needs to be deleted
def delete_question(menu):
    global questions
    global listbox
    question = ''
    load_questions()
    clear(menu)
    title = Label(root, text='Update Quiz - delete question', font=font.Font(family="Comic Sans MS", size=30, weight='bold'), bg=tk_color) 
    title.pack()
    listbox = Listbox(root, )
    for item in questions:
        listbox.insert(END, item)
    listbox.config(width=100)
    listbox.pack(pady=30)
        
    Button(root, text='Delete Question', font=font.Font(family="Comic Sans MS", size=15), bg="#%02x%02x%02x" % (110, 255, 144),
           command=lambda:delete(menu, listbox)).pack(pady=30)

#the function deletes the question
def delete(menu, listbox):
    global questions
    content = ''
    if listbox.curselection() != ():
        question = str(listbox.get(listbox.curselection()[0]))
        if os.path.isfile('homework.txt'):
            input_file = open(r"homework.txt", "r")
            lines = input_file.read().split("\n")
            question_index = lines.index(question)
            del lines[question_index]

            load_questions()
            
            answers = get_answers(question)
            for i in range(len(answers)):
                del lines[lines.index(answers[i])]
            for i in range(len(lines)):
                content += lines[i] + '\n'
            input_file.close
            write_to = open(r"homework.txt", "w")
            write_to.write(content)
            write_to.close            
        clear(menu)
        Label(root, text='question deleted successfully :)', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()
        Button(root, text='return to Home Page', font=font.Font(family="Comic Sans MS", size=15), command=lambda:play_end(menubar),
                    bg="#%02x%02x%02x" % (110, 255, 144)).pack(pady=30)
    else:
        Label(root, text='you must choose a question', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()

#the function gets the question that is going to be updated
def update_question(menu):
    global questions
    global listbox
    question = ''
    load_questions()
    clear(menu)
    title = Label(root, text='Update Quiz - update question', font=font.Font(family="Comic Sans MS", size=30, weight='bold'), bg=tk_color) 
    title.pack()
    listbox = Listbox(root, )
    for item in questions:
        listbox.insert(END, item)
    listbox.config(width=100)
    listbox.pack(pady=30)
        
    Button(root, text='Update Question', font=font.Font(family="Comic Sans MS", size=15),  bg="#%02x%02x%02x" % (110, 255, 144),
           command=lambda:change(menu, listbox)).pack(pady=30)

#the function get the question and its answers for the update
def change(menu, listbox):
    global questions
    content = ''
    if listbox.curselection() != ():
        question = str(listbox.get(listbox.curselection()[0]))
        if os.path.isfile('homework.txt'):
            input_file = open(r"homework.txt", "r")
            lines = input_file.read().split("\n")
            question_index = lines.index(question)
            clear(menu)
            Label(root, text='the question', font=font.Font(family="Comic Sans MS bold", size=18), bg=tk_color).pack()

            defult = StringVar()
            defult.set(question)
            Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=defult).pack()
            answers = get_answers(question)
            
            a1 = StringVar()
            a1.set(answers[0])
            enter_answer1 = Label(root, text='answer 1 (correct)', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
            enter_answer1.pack(pady=5)
            answer1 = Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a1)
            answer1.pack(pady=5)

            a2 = StringVar()
            a2.set(answers[1])
            enter_answer2 = Label(root, text='answer 2', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
            enter_answer2.pack(pady=5)
            answer2 = Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a2)
            answer2.pack(pady=5)

            a3 = StringVar()
            a3.set(answers[2])
            enter_answer3 = Label(root, text='answer 3', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
            enter_answer3.pack(pady=5)
            answer3 = Entry(root, width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a3)
            answer3.pack(pady=5)

            a4 = StringVar()
            a4.set(answers[3])
            enter_answer4 = Label(root, text='eanswer 4', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color)
            enter_answer4.pack(pady=5)
            answer4 = Entry(root,  width=50, font=font.Font(family="Comic Sans MS", size=16), textvariable=a4)
            answer4.pack(pady=5)

            Button(root, text='Update Question', font=font.Font(family="Comic Sans MS", size=15),  bg="#%02x%02x%02x" % (110, 255, 144),
           command=lambda:save_changes(question, defult, a1, a2, a3, a4)).pack(pady=30)
    else:
        Label(root, text='you must choose a question', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()

#the function updates the question
def save_changes(question, defult, a1, a2, a3, a4):
    global questions
    if os.path.isfile('homework.txt'):
            input_file = open(r"homework.txt", "r")
            lines = input_file.read().split("\n")
            question_index = lines.index(question)
            answers = []
            q = defult.get()
            answer1 = a1.get()
            answer2 = a2.get()
            answer3 = a3.get()
            answer4 = a4.get()

            answers.append(answer1)
            answers.append(answer2)
            answers.append(answer3)
            answers.append(answer4)
            if answer1!='' and answer2!='' and answer3!='' and answer4!='' and not duplicate(answers) and not "?" in question:
                lines[question_index] = q
                lines[question_index + 1] = answer1
                lines[question_index + 2] = answer2
                lines[question_index + 3] = answer3
                lines[question_index + 4] = answer4
                input_file.close
                file = open(r"homework.txt", "w")
                content = ''
                for i in range(len(lines)):
                    content += lines[i] + '\n'
                file.write(content)
                file.close
                clear(menubar)
                Label(root, text='question updated successfully :)', font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()
                Button(root, text='return to Home Page', font=font.Font(family="Comic Sans MS", size=15), command=lambda:play_end(menubar),
                        bg="#%02x%02x%02x" % (110, 255, 144)).pack(pady=30)
            else:
                clear(menubar)
                Label(root, text='please enter different answers and a question that doesnt already exists',
                      font=font.Font(family="Comic Sans MS", size=18), bg=tk_color).pack()
                Button(root, text='try again', font=font.Font(family="Comic Sans MS", size=15), command=lambda:update_question(menubar),
                        bg="#%02x%02x%02x" % (110, 255, 144)).pack(pady=30)
                

#the function updates the questions                
def load_questions():
    global questions
    file = open(r"homework.txt", "r")
    lines = file.read().split("\n")
    questions = []
    for i in lines:
        if "?" in i:
            questions.append(i)
    file.close

#the function get the ansewrs of a given question
def get_answers(question):
    file = open(r"homework.txt", "r")
    lines = file.read().split("\n")
    load_questions()
    file.close
    qusetion_index = lines.index(question)
    answers = [lines[qusetion_index+1], lines[qusetion_index+2],
               lines[qusetion_index+3], lines[qusetion_index+4]]
    return answers
    
#the function displays the last 10 players and their score
def chart(menu):
    clear(menu)
    frame = Frame(root, bg=tk_color)
    Label(frame, text='Players so far :)', font=font.Font(family="Comic Sans MS", size=30, weight='bold'),
          bg=tk_color).grid(row=0, column=1, pady=50)
    
    if os.path.isfile('results.txt'):
        input_file = open(r"results.txt", "r")
        lines = input_file.read().split("\n\n")
        if (len(lines)>10):
            while len(lines)>10:
                del lines[0]
        lines.sort(reverse=True)
        Label(frame, text='Name', font=font.Font(family="Comic Sans MS", size=18, weight='bold'),
          bg=tk_color).grid(row=1, column=0)
        Label(frame, text='Date', font=font.Font(family="Comic Sans MS", size=18, weight='bold'),
          bg=tk_color).grid(row=1, column=1)
        Label(frame, text='Grade', font=font.Font(family="Comic Sans MS", size=18, weight='bold'),
          bg=tk_color).grid(row=1, column=2)
        for i in range(len(lines)):
            person = lines[i].split("\n")
            for j in range(len(person)):
                Label(frame, text=person[j], font=font.Font(family="Comic Sans MS", size=16),
                  bg=tk_color).grid(row=i+2, column=j)
        frame.pack()

#the function adds the player to the players list
def add_result():
    global leader
    if os.path.isfile('results.txt'):
        input_file = open(r"results.txt", "a")
        input_file.write(leader)
        input_file.close
        leader = ''

#checking if the quiz ia avilable
if os.path.isfile('homework.txt'):
    input_file = open(r"homework.txt", "r")
    lines = input_file.read().split("\n")
else:
    print("file does not exists, sorry :(")

#assigning variables    
questions = []
correct = ['Good job!', 'You are right!', 'Correct!', 'Amazing!']
wrong = ["Don't worry, there will be another chance", 'You were so close!',
         'You are wrong, sorry!', 'Wrong answer...']
correct_index = 0
grade = 0
text_to_save = ''
leader = ''

#getting out questions and finding out the point value
for i in lines:
    if "?" in i:
        questions.append(i)
if len(questions)!=0:
    point = 100/len(questions)
else:
    point = 0

#creating root
root = Tk()


#def size(event):
#    print(root.geometry())

#root.bind("<Configure>", size)


#creating menu- File and About
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Update Quiz", command=lambda:update(menubar))
filemenu.add_command(label="Run Quiz", command=lambda:play_end(menubar))
filemenu.add_command(label="Save Results", command=lambda:save())
filemenu.add_command(label="Exit", command=lambda:exit(menubar))
menubar.add_cascade(label="File", menu=filemenu)

aboutbar = Menu(menubar, tearoff=0)
aboutbar.add_command(label="Show Results", command=lambda:chart(menubar))
aboutbar.add_command(label="Help", command=lambda:help(menubar))
aboutbar.add_command(label="Info", command=lambda:info(menubar))
menubar.add_cascade(label="About", menu=aboutbar)
root.config(menu=menubar)

#applying title and max and min size of the program
root.state('zoomed')
root.title("Hila Rahimipour's quiz")

root.maxsize(root.winfo_screenwidth(), root.winfo_screenheight())
root.minsize(870, 628)

#color of the program
tk_color = "#%02x%02x%02x" % (232, 255, 237)
root["background"] = tk_color

#font of the title
fnt = font.Font(family="Comic Sans MS", size=50, weight='bold')
title = Label(root, text='Welcome to my quiz!', bg="#%02x%02x%02x" % (178, 255, 196), pady=10, font=fnt)
title.pack(fill='x', pady=30)

text = Label(root, text='To begin, enter your name and press start', bg=tk_color, font=font.Font(family="Comic Sans MS", size=20), pady=20)
text.pack()

#getting variable of the player
defult = StringVar()
defult.set("Anonymous")

name = Entry(root, font=font.Font(family="Comic Sans MS", size=20), textvariable=defult)
name.pack(pady=20)

start = Button(root, text='Start', font=font.Font(family="Comic Sans MS", size=18, weight='bold'), height=1, width=8,
               bg="#%02x%02x%02x" % (110, 255, 144), command=lambda: first_play(menubar, defult))
start.pack(pady=10)

#close the root
root.mainloop()
