from threading import Thread
from tkinter import *
from random import randint
from time import sleep, time
import pyodbc
from tkinter import messagebox

services = []
ageGroup = -1

print('Credits to https://github.com/xtekky')
print('-------------------------------------')
print('ReacTime code: Reaction time measurements by Michael K')

print(" Instructions : ")
print(" 1. Click the start button")
print(" 2. immediately after clicking wait for the screen to turn GREEN ")
print(" 3. CLICK THE GREEN SCREEN TO GET YOUR REACTION TIME ")

#defining a class

def connectToDB():
 global conn
 conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\michael\Cirencester College summer task 2021\EXP.WORK\REACT TIME\ReactDB2.accdb;')
 cursor = conn.cursor()

connectToDB()

def runSQL(strSQL, results):
    global conn
    cursor = conn.cursor()
    cursor.execute(strSQL)
    
    if results:
        print("\n")
        columns = [column[0] for column in cursor.description]
        for c in columns:
            print(c, end =", ")
        print("")
        for row in cursor.fetchall():
            for c in row:
                print(c, end = "\t")
        print("")
    else:               # Flips when false runs any other sql command like UPDATE 
        conn.commit()
        print("\n", strSQL, ": Run - ", cursor.rowcount, "record(s) affected")
       
    cursor.close

def coverLabel(self):

    blankLabel = Label(self.window, text=("                                                                                              "),fg='WHITE', bg='#1E272E', font='Calibri 24 bold', width=70) #16TH JAN LABEL ADDED  
    blankLabel.place(relx=.15, rely=.55)


#def updateAgeGroup(Lb1, react_Time):
    
    #name = Lb1.get(ACTIVE)

 # converts so it can concatinate
    #r_time_str = str(react_Time)

    #update
    #if name == "Child":
       #cursor = conn.cursor()
       #cursor.execute("UPDATE ReactData SET Age_Group = ("'1'") WHERE React_Time = " + r_time_str)

    #elif name =="Young Adult":
         #cursor = conn.cursor()
        # cursor.execute("UPDATE ReactData SET Age_Group = ("'2'") WHERE React_Time = " + r_time_str)
         

   # elif name =="Adult":
     #    cursor = conn.cursor()
     #    cursor.execute("UPDATE ReactData SET Age_Group = ("'3'") WHERE React_Time = " + r_time_str)
         

   # elif name =="Elderly":
    #     cursor = conn.cursor()
     #    cursor.execute("UPDATE ReactData SET Age_Group = ("'4'") WHERE React_Time = " + r_time_str)
         

    #else:    
         #name = "0"
         #cursor = conn.cursor()
         #cursor.execute("UPDATE ReactData SET Age_Group = ("'0'") WHERE React_Time = " + r_time_str)
         

       

def showAgeGroup(Lb1, self, react_Time):
    
    name = Lb1.get(ACTIVE)
    
    if name == "Child":
       cursor = conn.cursor()
       cursor.execute("SELECT Avg(React_Time) FROM(ReactData) WHERE Age_Group =("'1'")")
       ageGroup= 1
       
    elif name =="Young Adult":
         cursor = conn.cursor()
         cursor.execute("SELECT Avg(React_Time) FROM(ReactData) WHERE Age_Group =("'2'")")
         ageGroup= 2

    elif name =="Adult":
         cursor = conn.cursor()
         cursor.execute("SELECT Avg(React_Time) FROM(ReactData) WHERE Age_Group =("'3'")")
         ageGroup= 3

    elif name =="Elderly":
         cursor = conn.cursor()
         cursor.execute("SELECT Avg(React_Time) FROM(ReactData) WHERE Age_Group =("'4'")")
         ageGroup= 4

    else:    
         name = "0"
         cursor = conn.cursor()
         cursor.execute("SELECT Avg(React_Time) FROM(ReactData) WHERE Age_Group =("'0'")")
         ageGroup= 0

    r_time_str = str(react_Time)
    ageGroup_str = str(ageGroup)
                                                           
    avgTimeFromDB = cursor.fetchone()
    av=int( avgTimeFromDB[0] )
    print(av)
    
    age_avg_react = Label(self.window, text=" ".join(f'AVERAGE TIME FOR YOUR AGE GROUP:{av}ms'), fg='WHITE', bg='#1E272E', font='Calibri 24 bold', width=70) #16TH JAN LABEL ADDED
    age_avg_react.place(relx=.15, rely=.55)

    #update statement


    cursor = conn.cursor()
    cursor.execute("UPDATE ReactData SET Age_Group = '" + ageGroup_str + "' WHERE React_Time = " + r_time_str) 
    conn.commit()
    
    


class Reactiontest:

    #setting up GUI
    def __init__(self):
        self.window = Tk()
        self.window.state('zoomed') #window dimension
        self.window.title("Reaciton Time Test - Credits to Github xtekky // ReacTime code: Reaction time measurements by Michael K") #window title
        self.window.config(bg='#2b353f')
        self.scores = []
        self.react_ready = False
        self.start_time = None
        self.valid_round = True
        self.round = 0

        # setting up a start button
        self.start_button = Button(self.window, text='CLICK START then click the GREEN SCREEN quickly to measure your reaction time', fg='#1E272E', bg='WHITE', font='Calibri 14 bold', bd=0, width=70, command= lambda: (self.start(), self.start_button.place_forget()))
        self.start_button.place(relx=.210111, rely=.225)
        self.start_button = Button(self.window, text='START', fg='#1E272E', bg='WHITE', font='Calibri 26 bold', bd=0, width=20, command= lambda: (self.start(), self.start_button.place_forget()))
        self.start_button.place(relx=.340625, rely=.425)

        # displaying GUI
        self.window.mainloop()

    #reset function if user clicks too early
    def reset(self):
        self.window.unbind("<Button-1>")
        self.start_button.place(relx=.340625, rely=.425)
        self.scores = []
        self.round = 0
        self.valid_round = True

    #start function - when user presses start button
    def _start(self):
        sleep(randint(750, 2250) / 1000)
        if self.valid_round:
            self.window.config(bg='#00ff00')  # green
            self.start_time = time()
            self.react_ready = True

    def start(self):
        if self.round != 1:
            self.window.bind("<Button-1>", lambda event: self.register())  #left click
            Thread(target=self._start).start()  # this provides a fast event handler
        else:
            self.end()

    # register function
    def register(self):
        if self.react_ready:
            self.scores.append(time() - self.start_time)
            self.window.config(bg='#1E272E')
            self.react_ready = False
            self.round += 1
            self.start()

        else:
            self.valid_round = False
            self.early()

    # function if user clicks too early
    def _early(self):
        self.window.config(bg='#1E272E')
        warning = Label(self.window, text="!", bg='white', fg='#1E272E', font='Calibri 60 bold', width=2)
        warning.place(relx=.27, rely=.4)
        early = Label(self.window, text="You clicked too early!\nRestarting in 1 second...", justify=LEFT, bg='#1E272E', fg='WHITE', font='Calibri 30 bold')
        early.place(relx=.37, rely=.4)
        sleep(1) 
        warning.place_forget()
        early.place_forget()
        self.reset()

    def early(self):
        Thread(target=self._early).start()\
        
    def Score_save():
        react_Time = {int((self.scores[0])) * 1000}# react time in m/s 
        print("YOUR TIME HAS BEEN SUCCESSFULLY SAVED", runSQL("INSERT INTO ReactData(React_Time) VALUES ('" + react_Time + "')", False))

    def end(self):
        score_items = []                                                          # converts s to ms
        score_ = Label(self.window, text=" ".join(f'REACTION TIME: {int((sum(self.scores)) * 1000)}ms'), bg='#1E272E', fg='WHITE', font='Calibri 24 bold') # returns the sum of the numbers 
        score_.place(relx=.25, rely=.35)

        #avg_score = Label(self.window, text="Your average time was", avg_score)

        #SAVE = Button(self.window, text="▶ SAVE", bg='#1E272E', fg='WHITE', font='Calibri 30', height=1, bd=0, command=lambda: ([item.place_forget() for item in score_items],self.reset()))
        #SAVE.place(relx=.391, rely=.62)
                          
        restart = Button(self.window, text="▶ RESTART", bg='#1E272E', fg='WHITE', font='Calibri 30', height=1, bd=0, command=lambda: ([item.place_forget() for item in score_items],self.reset(),Lb1.destroy(),coverLabel(self))) # ,Lb1.destroy() destroys listbox after restart is clicked      
        restart.place(relx=.391, rely=.62)

        #get ALL AGES average Rtime:
        cursor = conn.cursor()
        cursor.execute("SELECT Avg(React_Time) FROM(ReactData)")
        #avgTimeFromDB = cursor.fetchall()Z
        avgTimeFromDB = cursor.fetchone()
        av=int( avgTimeFromDB[0] )
        print(av)

        avg_react = Label(self.window, text=" ".join(f'ALL AGES AVERAGE TIME FROM DB:{av}ms'), fg='WHITE', bg='#1E272E', font='Calibri 24 bold')
        avg_react.place(relx=.15, rely=.45)

        #age_avg_react = Label(self.window, text="AVERAGE TIME FOR YOUR AGE GROUP: ms", fg='WHITE', bg='#1E272E', font='Calibri 24 bold') #16TH JAN LABEL ADDED
        #age_avg_react.place(relx=.15, rely=.55)

        

        
        react_Time = int( (self.scores[0]) * 1000 ) # just measured user react time in m/s 
        r_time_str = str(react_Time)




        #######################################################################################

        Lb1 = Listbox(self.window,)
        Lb1.insert(1, "Child")
        Lb1.insert(2, "Young Adult")
        Lb1.insert(3, "Adult")
        Lb1.insert(4, "Elderly")

        Lb1.pack()



        #########################################################################################

        Instructions = Label(self.window, text="To find out the average time for your age, select from the list above", bg='#1E272E', fg='WHITE', font='Calibri 21', width=70)
        Instructions.place(relx=.101111, rely=.225)
        #prompt that tells the user to select their age group
        #for i in range(4):
             #Append int variables for each checkbox
            #option = IntVar()
            #option.set(0)
            #services.append(option)
        
        #childButton = Checkbutton(self.window, text= "Child", font='Calibri 11',variable=services[0]).pack()
        #Pack manages our widgets in blocks before placing them onto our root window (Widget button or checkbox)

        #youngAdultButton = Checkbutton(self.window, text= "Young Adult", font='Calibri 11', variable=services[1]).pack()
        
        #adultButton = Checkbutton(self.window, text= "Adult", font='Calibri 11', variable=services[2]).pack()
        
        #elderlyButton = Checkbutton(self.window, text= "Elderly", font='Calibri 11',  variable=services[3]).pack()
                     
        age_button = Button(self.window, text="Confirm age group", font='Calibri 11')#command=showAgeGroup)
        age_button.bind("<Button-1>", lambda event: showAgeGroup(Lb1, self, react_Time)) #lambda event: [showAgeGroup(Lb1, self, react_Time), updateAgeGroup(Lb1, react_Time)]) # Creating a button with more than one command using lambda
        age_button.place(relx=.291, rely=.025)

        ############################################################################################

        cursor = conn.cursor()
        cursor.execute("INSERT INTO ReactData (React_Time) VALUES (?)", react_Time) # adds react time to age group 0 all ages
        conn.commit()
        print("\n", ": Run - ", cursor.rowcount, "record(s) affected")

        score_items.extend((score_, restart, avg_react, self.start_button, Instructions, age_button)) # reset all buttons
        self.window.unbind("<Button-1>")
    
#starting script
if __name__ == '__main__':
    Reactiontest()
    
