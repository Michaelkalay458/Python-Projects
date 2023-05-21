import pyodbc #problem fixed uninstall reinstall
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Tk, Text
import webbrowser
import subprocess as sp

def connectToDB(): # def which allows python to connect to ms access DB
    global conn # conn is set to global
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=F:\OCS_Task 2\Task2_Database_[LL-000011429]_[Kalaydjiyski]_[M].py.accdb') # connection string including file path of MS Acc DB
    #conn string # requires the right file path for program to run
    cursor = conn.cursor() # cursor object initialized
    

connectToDB()

def runSQL(strSQL, results): #def which allows SQL commands to be ran
    global conn
    cursor = conn.cursor()
    cursor.execute(strSQL)
    
    if results:
        print("\n")
        columns = [column[0] for column in cursor.description]
        for c in columns:
            print(c, end =", ")
        print("")                                                                              # pyodbc used from github
        for row in cursor.fetchall():
            for c in row:
                print(c, end = "\t")
        print("")
    else:               # Flips when false runs any other sql command like UPDATE 
        conn.commit()
        print("\n", strSQL, ": Run - ", cursor.rowcount, "record(s) affected")
       
    cursor.close



def signup_win(): # this is the main sign up window for the user
   signUp= Toplevel(root)

   signUp.state('zoomed') # .state('zoomed opens new window in fullscreen mode
   signUp.title("User Sign-Up Window") # establish a window title
   signUp.configure(bg="light blue")
   stu_sign = Label(signUp, text="User Sign Up", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold underline')
   stu_sign.pack()

   missDetail = Label(signUp, text=" *** All Details Are Required *** ", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold') #user missing details prompt label 
   missDetail.pack()
   
   userpwordHelp = Label(signUp, text=" Tip - Strong PWord's are 8 Char Long", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold') # label that provides a helpful user btip 
   userpwordHelp.pack()
   
   user_sign = Label(signUp, text="Enter Username", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold') 
   user_sign.pack()

   #username textbox
   u_name = ttk.Entry(signUp, width= 15) #entry widget used to collect username data
   u_name.place(relx= 0.4, rely=0.2)
   u_name.pack()


   pass_label = Label(signUp, text="Enter Password", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
   pass_label.pack()

   #password textbox
   password = ttk.Entry(signUp, width= 15) #entry widget used to collect password data
   password.place(relx= 0.4, rely=0.2)
   password.pack()


   location_select = Label(signUp, text="Please Select your location:", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
   location_select.pack()

   #Location listbox - displays all available locations
   Lb1 = Listbox(signUp)
   Lb1.insert(1, "Bristol")
   Lb1.insert(2, "London")
   Lb1.insert(3, "Cardiff")

   Lb1.pack()

   ill_label = Label(signUp, text="Do you have an illness?", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
   ill_label.pack()

   #illness textbox
   ill_name = ttk.Entry(signUp, width= 15) # entry is used to collect the user illness type
   ill_name.place(relx= 0.4, rely=0.4)
   ill_name.pack()

   confirm = Button(signUp, text="Confirm Details", fg='#1E272E', bg='orange', width= 30, font='Calibri 15 bold')
   confirm.bind("<Button-1>", lambda event: dataVal(Lb1, ill_name, password, u_name, signUp)) # when clicked it fire's an event
   confirm.pack()

   darkMode = Button(signUp, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2) #dark mode button
   darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, signUp)) 
   darkMode.place(relx= 0.8, rely= 0.3)


   lightMode = Button(signUp, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
   lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, signUp))
   lightMode.place(relx= 0.8, rely= 0.4)

   reset = Button(signUp, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2) #resets the bg to the default colourway
   reset.bind("<Button-1>", lambda event: resetBackground(reset, signUp))
   reset.place(relx= 0.8, rely= 0.5)

    

def dataVal(Lb1, ill_name, password, u_name, signUp):
    

    if len(password.get()) and len(u_name.get()) and len(Lb1.get(ACTIVE)) and len(ill_name.get()) > 0: # prescence/length check all data types
       print("data exists")# debug
       pwordVal(Lb1, ill_name, password, u_name, signUp)
       
    else:
        # missing data
        missingData = messagebox.askretrycancel("missing data", " missing data, make sure to add details ?")
        signUp.destroy() #.destroy() closes the signup winsow
        signup_win() #re-uses sign up function to open the sign up page 



def pwordVal(Lb1, ill_name, password, u_name, signUp): 
    
    if len(password.get()) >= 8: # strong passwords 

       cursor = conn.cursor()
       
       cursor.execute("INSERT INTO Users (Username, Password, Location, Illness) VALUES('" + u_name.get() + "', '" + password.get() + "', '" + Lb1.get(ACTIVE) + "', '" + ill_name.get() + "')")
       #inserts all of the data supplied by the users into the DB if they have supplied a strong password

       conn.commit()

       dashbAccess = messagebox.showinfo("Saved","Your details have been saved click <Ok> to continue") # data saved + dashboard access message 
       HAGDashboard() # open dashboard 

       signUp.destroy() #closes previous window

       
    #weak passwords:
    else: 
        weakPword = messagebox.askretrycancel("weak password or username", " Weak password at least 8 char long?") # error message weak password
        signup_win() # re-opens signUp window
        
        
     
def signIn_win(): #Sign in window for all users
    signIn= Toplevel(root)

    signIn.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    signIn.title("User Sign-In Window")
    signIn.configure(bg="light blue")
    user_signin = Label(signIn, text="User Sign-In Window", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold underline')
    user_signin.pack()
   
    user_sign = Label(signIn, text="Enter Username", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
    user_sign.pack()

    #username textbox
    u_name = ttk.Entry(signIn, width= 15)
    u_name.place(relx= 0.4, rely=0.2)
    u_name.pack()


    pass_label = Label(signIn, text="Enter Password", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
    pass_label.pack()

    #password textbox
    password = ttk.Entry(signIn, width= 15)
    password.place(relx= 0.4, rely=0.2)
    password.pack()

    confirm = Button(signIn, text="Confirm Details", fg='#1E272E', bg='orange', width= 30, font='Calibri 15 bold')
    confirm.bind("<Button-1>", lambda event: signData(password, u_name, signIn)) #fire's an event to check if data exists
    confirm.pack()

    darkMode = Button(signIn, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2) #dark mode
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, signIn))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(signIn, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2) #light mode
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, signIn))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(signIn, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2) #background reseter
    reset.bind("<Button-1>", lambda event: resetBackground(reset, signIn))
    reset.place(relx= 0.8, rely= 0.5)


def signData(password, u_name, signIn):  

    if len(u_name.get()) > 0 and len(password.get()) >= 8 : # prescence/length check all data types 
       print("passed presc check")# debug
       
       signPwordVal(password, u_name, signIn)
       
    else:
        missingData = messagebox.askretrycancel("Invalid Username Or Password", " Details provided are Wrong")
        signIn.destroy()
        signIn_win()
        


def signPwordVal(password, u_name, signIn):

    cursor= conn.cursor()

    cursor.execute("SELECT DISTINCT Username FROM Users WHERE Password = ('" + password.get() + "')") # retrieves a username that has the same password as password.get()
       
    user_name_rec = cursor

    user_name_rec = cursor.fetchone()[0] 

    conn.commit()

    #print(user_rec) #test - prints users rec if its exists - #[('Nomad321', )] what is returned

    print(user_name_rec)
    
    if user_name_rec == u_name.get(): # if the username returned from the database matches the username supplied

       validUser = messagebox.showinfo("Welcome Back !!!", " Welcome Back, Click <OK> to access the menu") #messagebox that welcomes the user back to the HAG dashboard

       HAGDashboard() 

       signIn.destroy()

    else:
         invalidUser = messagebox.askretrycancel("No user", " No User Found, <Retry> ? ") #if the username dosn't match a error message appears

         signIn_win()


def HAGDashboard():
    
    HAGDash= Toplevel(root)
    HAGDash.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    HAGDash.title("Health Advice Group Dashboard")
    HAGDash.configure(bg="light blue")
        
    label = Label(HAGDash, text="Health Advice Group Dashboard", fg='#1E272E', bg='orange', width= 32, font='Kalinga 30 bold underline', height = 2) # label used for branding
    label.pack()

    #all features in the forms of buttons in the HAG Dashboard

    WeatherRes = Button(HAGDash,text="Weather Forecast info", fg='#1E272E', bg='Orange', width= 30, font='Calibri 15 bold', command= weatherInfo) #command allows weather forecast module to open when clicked
    WeatherRes.place(relx= 0.4, rely= 0.1)

    AQDRes = Button(HAGDash,text="Air Quality Dashboard", fg='#1E272E', bg='Orange', width= 30, font='Calibri 15 bold', command= airQualDashboard)#command allows Air Quality Dashboard to open when clicked
    AQDRes.place(relx= 0.4, rely= 0.2)

    HAWRes = Button(HAGDash,text="Advice on health affected by weather", fg='#1E272E', bg='Orange', width= 35, font='Calibri 15 bold', command= habw_advice) #command allows Advice on health affected by health to open when clicked
    HAWRes.place(relx= 0.4, rely= 0.3)

    PHLRes = Button(HAGDash,text="Personalised Health advice based on location", fg='#1E272E', bg='Orange', width= 40, font='Calibri 15 bold', command= persHadv) #command allows Personalised health advice window to open
    PHLRes.place(relx= 0.4, rely= 0.4)

    PHTTRes = Button(HAGDash,text="Personal Health Tracking Tool", fg='#1E272E', bg='Orange', width= 30, font='Calibri 15 bold', command= personalHealthTool) #command allows Personal Health tracker tool to open when clicked
    PHTTRes.place(relx= 0.4, rely= 0.5)

    UserHelpGuide = Button(HAGDash,text=" User Help Guide ", fg='#1E272E', bg='Orange', width= 30, font='Calibri 15 bold', command = userhelpGuide)#command allows user help guide to open when clicked
    UserHelpGuide.place(relx= 0.4, rely= 0.6)





def weatherInfo():
    
    weathWin= Toplevel(root)
    weathWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    weathWin.title("Weather forecast window")
    weathWin.configure(bg="light blue")
        
    label = Label(weathWin, text="Weather forecast window", fg='#1E272E', bg='Orange', width= 32, font='Kalinga 30 bold underline', height = 2)
    label.pack()

    label2 = Label(weathWin, text="Please choose a day of the week: ", fg='#1E272E', bg='Orange', width= 40, font='Kalinga 15 bold underline', height = 2)
    label2.pack()

    MondayShowcase = Button(weathWin,text="Monday", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=MondayResource)
    MondayShowcase.place(relx= 0.4, rely= 0.2)

    TuesdayShowcase = Button(weathWin,text="Tuesday", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=TuesdayResource)
    TuesdayShowcase.place(relx= 0.4, rely= 0.3)

    WednesdayShowcase = Button(weathWin,text="Wednesday", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=WednesdayResource)
    WednesdayShowcase.place(relx= 0.4, rely= 0.4)

    ThursdayShowcase = Button(weathWin,text="Thursday", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=ThursdayResource)
    ThursdayShowcase.place(relx= 0.4, rely= 0.5)

    FridayShowcase = Button(weathWin,text="Friday", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=FridayResource)
    FridayShowcase.place(relx= 0.4, rely= 0.6)

    SaturdayShowcase = Button(weathWin,text=" Saturday ", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=SaturdayResource)
    SaturdayShowcase.place(relx= 0.4, rely= 0.7)

    SundayShowcase = Button(weathWin,text=" Sunday ", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=SundayResource)
    SundayShowcase.place(relx= 0.4, rely= 0.8)

    returnHome = Button(weathWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)

def MondayResource():
    Monday_res_win= Toplevel(root)
    Monday_res_win.title("Monday Resource")
    Monday_res_win.state('zoomed')
    Monday_res_win.configure(bg="light blue")
    T= Text(Monday_res_win, height= 15, width = 30)

    windTitle = Label(Monday_res_win, text= "General Weather forecast for Monday: ", bg='orange') 
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Monday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Monday: 
                           
                        Today
                        -----
                        Cloud will tend to break up this afternoon
                        winter sunshine developing in the late afternoon

                        Tonight
                        -------
                        Tonight will continue to be cold.
                        Spells of light snow are likely to
                        advance from the south.

                           

                        ''') # description from BBC weather


    monURL = Button(Monday_res_win, text="Click for more info online", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    monURL.pack()

    darkMode = Button(Monday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Monday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Monday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Monday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Monday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Monday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Monday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)

    
    root.mainloop()



def TuesdayResource():
    Tuesday_res_win= Toplevel(root)
    Tuesday_res_win.title("Tuesday Resource")
    Tuesday_res_win.state('zoomed')
    Tuesday_res_win.configure(bg="light blue")
    T= Text(Tuesday_res_win, height= 15, width = 30)

    windTitle = Label(Tuesday_res_win, text= "General Weather forecast for Tuesday: ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Tuesday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Tuesday:

                           Today
                           -----
                           This morning we will see dry conditions and
                           plenty of sunshine to start. 

                           Tonight
                           -------
                           This evening will start with cloudy skies and
                           spells of heavy and persistent rain. 

                           

                        ''')


    tueURL = Button(Tuesday_res_win, text="Click for more info online", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    tueURL.pack()

    darkMode = Button(Tuesday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Tuesday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Tuesday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Tuesday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Tuesday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Tuesday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Tuesday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)

    
    root.mainloop()



def WednesdayResource():
    Wednesday_res_win= Toplevel(root)
    Wednesday_res_win.title("Wednesday Resource")
    Wednesday_res_win.state('zoomed')
    Wednesday_res_win.configure(bg="light blue")
    T= Text(Wednesday_res_win, height= 15, width = 30)

    windTitle = Label(Wednesday_res_win, text= "General Weather forecast for Wednesday: ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Wednesday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Wednesday:

                           Today
                           -----
                           Cloud will tend to develop this morning Cold.

                           Tonight
                           ------
                           Tonight will continue to be cold.Predicted to be
                           the coldest day in british history.

                           

                        ''')


    wedURL = Button(Wednesday_res_win, text="Click for more info online", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    wedURL.pack()

    darkMode = Button(Wednesday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Wednesday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Wednesday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Wednesday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Wednesday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Wednesday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Wednesday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)

    root.mainloop()



def ThursdayResource():
    Thursday_res_win= Toplevel(root)
    Thursday_res_win.title("Thursday Resource")
    Thursday_res_win.state('zoomed')
    Thursday_res_win.configure(bg="light blue")
    T= Text(Thursday_res_win, height= 15, width = 30)

    windTitle = Label(Thursday_res_win, text= "General Weather forecast for Thursday: ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Thursday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Thursday:
                           

                        Today
                        -----
                        Sunny spells will continue to advance throughout
                        the north and north east of england.

                        Tonight
                        -------
                        rain is expected to develop as heavy clouds advance.

                           

                        ''')


    thurURL = Button(Thursday_res_win, text="Click for more info online", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    thurURL.pack()

    darkMode = Button(Thursday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Thursday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Thursday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Thursday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Thursday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Thursday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Thursday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    root.mainloop()


def FridayResource():
    Friday_res_win= Toplevel(root)
    Friday_res_win.title("Friday Resource")
    Friday_res_win.state('zoomed')
    Friday_res_win.configure(bg="light blue")
    T= Text(Friday_res_win, height= 15, width = 30)

    windTitle = Label(Friday_res_win, text= "General Weather forecast for Friday: ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Friday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Friday:
                           

                        Today
                        -----
                        Cloud will tend to break up this afternoon, with plenty
                        of Sunshine. warm.

                        Tonight
                        -------
                        Tonight snow has been developing potentially
                        leaving a dust of snow on the ground in some places.

                           

                        ''')


    friURL = Button(Friday_res_win, text="Click for more info online", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    friURL.pack()

    darkMode = Button(Friday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Friday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Friday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Friday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Friday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Friday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Friday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)

    root.mainloop() 


def SaturdayResource():
    Saturday_res_win= Toplevel(root)
    Saturday_res_win.title("Friday Resource")
    Saturday_res_win.state('zoomed')
    Saturday_res_win.configure(bg="light blue")
    T= Text(Saturday_res_win, height= 15, width = 30)

    windTitle = Label(Saturday_res_win, text= "General Weather forecast for Saturday: ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Saturday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Saturday:
                           
                           
                        Today
                        -----
                        Sunny spells and high temperatures in some places, warm.

                        Tonight
                        -------
                        Tonight will continue to be hot and humid.

                           

                        ''')


    satURL = Button(Saturday_res_win, text="Click for more info online", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    satURL.pack()

    darkMode = Button(Saturday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Saturday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Saturday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Saturday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Saturday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Saturday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Saturday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    
    root.mainloop()



def SundayResource():
    Sunday_res_win= Toplevel(root)
    Sunday_res_win.title("Friday Resource")
    Sunday_res_win.state('zoomed')
    Sunday_res_win.configure(bg="light blue")
    T= Text(Sunday_res_win, height= 15, width = 30)

    windTitle = Label(Sunday_res_win, text= "General Weather forecast for Sunday: ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(Sunday_res_win, height=15)
    text.pack()

    text.insert('1.0', ''' Weather forecast for Sunday:
                           

                        Today
                        -----
                        Cloud will tend to break up this afternoon,
                        with plenty of winter rain developing in the late
                        afternoon. Very Cold.

                        Tonight
                        -------
                        Snow storms will develop, closure of roads etc.

                           

                        ''')


    satURL = Button(Sunday_res_win, text="Online Weather", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=WeatherURL)
    satURL.pack()

    darkMode = Button(Sunday_res_win, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, Sunday_res_win))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(Sunday_res_win, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, Sunday_res_win))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(Sunday_res_win, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, Sunday_res_win))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(Sunday_res_win, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)


    root.mainloop()

    


def WeatherURL():
    url = "https://www.bbc.co.uk/weather/2643743"
    webbrowser.open(url, new=0, autoraise=True)




def airQualDashboard():
    
    airQualDash= Toplevel(root)
    airQualDash.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    airQualDash.title("Air quality Dashboard")
    airQualDash.configure(bg="light blue")
        
    windTitle = Label(airQualDash, text="Air quality Dashboard", fg='#1E272E', bg='Orange', width= 32, font='Kalinga 30 bold underline', height = 2)
    windTitle.pack()

    prompt = Label(airQualDash, text="Please choose a location you would like to moitor: ", fg='#1E272E', bg='Orange', width= 40, font='Kalinga 15 bold underline', height = 2)
    prompt.pack()

    locID = Listbox(airQualDash)
    locID.insert(1, "London")
    locID.insert(2, "Bristol")
    locID.insert(3, "Cardiff")

    locID.pack()


    confirm = Button(airQualDash, text="Confirm Details", fg='#1E272E', bg='orange', width= 30, font='Calibri 15 bold')
    confirm.bind("<Button-1>", lambda event: airDataSQL(locID, airQualDash)) #event handler - binds left click to execute signUpSQL() subroutine
    confirm.pack()

    returnHome = Button(airQualDash, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)

    root.mainloop()


def airDataSQL(locID, airQualDash):

    cursor = conn.cursor()
        
    cursor.execute("SELECT WindSpeed, AirQualityLevel, Humidity, Temperature FROM AirData WHERE Location = ('" + locID.get(ACTIVE) + "')") 
    
    air_rec = cursor

    air_rec = cursor.fetchall() 

    print(air_rec)
    
    conn.commit()

    details = Label(airQualDash, text="Windspeed <Mph> | Air Quality Level | Humidity <%> | Temp <Degrees C*>", fg='#1E272E', bg='Orange', width= 70, font='Kalinga 10 bold underline', height = 2)
    details.place(relx= 0.4, rely= 0.4)

    
    airData = Label(airQualDash, text="", fg='#1E272E', bg='Orange', width= 70, font='Kalinga 10 bold underline', height = 2)

    
    airData.config(text="{}".format(air_rec))
    airData.place(relx= 0.4, rely= 0.5)
      
    


def habw_advice():

    habwWin= Toplevel(root)
    habwWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    habwWin.title("Health affected by weather")
    habwWin.configure(bg="light blue")

    l = Label(habwWin, text= " Health affected by weather ", bg='orange')
    l.config(font =("Courier", 14))
    l.pack()

    text = Text(habwWin, height=30)
    text.pack()

    text.insert('1.0', ''' Health Conditions and mitigations :

                           weather/climate conditions
                           --------------------------
                           
                           1. Air pollution

                            .Asthma

                           2. Extreme heat

                            .Heat stroke
                            .sunburn
 
                           3. Cold temperatures

                            . Hypothermia & Frostbite
                           
                           
                          Mitigations
                          -----------
                          1. Ask for a prescribed inhaler
                           . Make sure your getting enough exercise
                             and oxygen in your household

                          2. Choose lightweight, loose-fitting clothing.
                            Drink Plenty of Fluids
                            Use suncream / after sun etc.  

                        3. Extra blankets, sleeping bags, and warm winter coats



                        ''')  

    label4 = Label(habwWin, text= " Click <More Info> for extra information: ", bg='orange', width= 50, font='Calibri 15 bold')
    label4.place(relx= 0.4, rely= 0.6)

    moreInfo = Button(habwWin, text="More Info", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = moreHealthInfo)
    moreInfo.place(relx= 0.4, rely= 0.7)

    darkMode = Button(habwWin, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, habwWin))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(habwWin, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, habwWin))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(habwWin, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, habwWin))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(habwWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)


    root.mainloop()
        
    
def moreHealthInfo():
    url = "https://www.cdc.gov/climateandhealth/effects/default.htm"
    webbrowser.open(url, new=0, autoraise=True)


def persHadv():

    persHadvWin= Toplevel(root)
    persHadvWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    persHadvWin.title("Personal Health advice based on location")
    persHadvWin.configure(bg="light blue")
        
    label = Label(persHadvWin, text="Personal Health advice based on location", fg='#1E272E', bg='Orange', width= 32, font='Kalinga 30 bold underline', height = 2)
    label.pack()

    label2 = Label(persHadvWin, text="Please choose a location: ", fg='#1E272E', bg='Orange', width= 40, font='Kalinga 15 bold underline', height = 2)
    label2.pack()

    LondonShowcase = Button(persHadvWin,text="London", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=london_res)
    LondonShowcase.place(relx= 0.4, rely= 0.2)

    CardiffShowcase = Button(persHadvWin,text="Cardiff", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=cardiff_res)
    CardiffShowcase.place(relx= 0.4, rely= 0.3)

    BristolShowcase = Button(persHadvWin,text="Bristol", fg='#1E272E', bg='Orange', width= 15, font='Calibri 15 bold', command=Bristol_res)
    BristolShowcase.place(relx= 0.4, rely= 0.4)

    returnHome = Button(persHadvWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    


def london_res():
    londonWin= Toplevel(root)
    londonWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    londonWin.title("Health advice London")
    londonWin.configure(bg="light blue")

    l = Label(londonWin, text= " Health Advice For London ", bg='orange')
    l.config(font =("Courier", 14))
    l.pack()

    text = Text(londonWin, height=30)
    text.pack()

    text.insert('1.0', ''' Health advice for London:

                    Exercises can help improve:

                    1. Physical health 
                    2. Mental health

                    examples of exercise with locations:
                                     
                    . Walking / Dog walking - Hyde Park, St james's park
                                   
                    . Cycling - Greenwhich park 
                                   
                    . Running - Richmond park 
                                   
                    . Swimming - Pool that you can Visit without membership -
                      The Porchester Spa · BAYSWATER: Queensway, London W2 5HS

                   Healthy eating locations:

                   . Avobar (24 Henrietta St)
                   . Grain Kitchen (13 Harrow Place)
                   . Eat Activ (26 Noel St)
                   
                        ''') 
    label4 = Label(londonWin, text= " Click <Exercises> for more info: ", bg='orange', width= 50, font='Calibri 15 bold')
    label4.place(relx= 0.4, rely= 0.5)

    swimInfo = Button(londonWin, text="Exercises", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = lonfitnessInfo)
    swimInfo.place(relx= 0.5, rely= 0.55)

    label5 = Label(londonWin, text= " Click <Healthy Eating> for more info: ", bg='orange', width= 50, font='Calibri 15 bold')
    label5.place(relx= 0.4, rely= 0.6)

    eatInfo = Button(londonWin, text="Healthy Eating", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = loneatingInfo)
    eatInfo.place(relx= 0.5, rely= 0.65)

    darkMode = Button(londonWin, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, londonWin))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(londonWin, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, londonWin))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(londonWin, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, londonWin))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(londonWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    root.mainloop()


def lonfitnessInfo():
    url = "https://www.porchesterspatreatments.co.uk/"
    webbrowser.open(url, new=0, autoraise=True)

def loneatingInfo():
    url = "https://www.avobar.co.uk/"
    webbrowser.open(url, new=0, autoraise=True)




def cardiff_res():
    cardiffWin= Toplevel(root)
    cardiffWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    cardiffWin.title("Health Advice For Cardiff")
    cardiffWin.configure(bg="light blue")

    l = Label(cardiffWin, text= " Health Advice For Cardiff ", bg='orange')
    l.config(font =("Courier", 14))
    l.pack()

    text = Text(cardiffWin, height=30)
    text.pack()

    text.insert('1.0', ''' Health advice for Cardiff:

                    Exercises can help improve:

                    1. Physical health 
                    2. Mental health

                    examples of exercise with locations:
                                     
                    . Badminton / Table tennis  - Llandaff North and Gabalfa Hub
                                   
                    . Walking -  Roath park, Thompsons park and Victoria park 
                                   
                    . Running - Bute park 

                   Healthy eating locations:

                   . Anna Loka
                   . Thehealthyhangoutuk
                   . Cleanbite 
                   
                        ''') 
    label4 = Label(cardiffWin, text= " Click <Exercises> for more info: ", bg='orange', width= 50, font='Calibri 15 bold')
    label4.place(relx= 0.4, rely= 0.5)

    Info = Button(cardiffWin, text="Exercises", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = cardfitnessInfo)
    Info.place(relx= 0.5, rely= 0.55)

    label5 = Label(cardiffWin, text= " Click <Healthy Eating> for more info: ", bg='orange', width= 50, font='Calibri 15 bold')
    label5.place(relx= 0.4, rely= 0.6)

    eatInfo = Button(cardiffWin, text="Healthy Eating", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = cardeatingInfo)
    eatInfo.place(relx= 0.5, rely= 0.65)

    darkMode = Button(cardiffWin, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, cardiffWin))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(cardiffWin, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, cardiffWin))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(cardiffWin, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, cardiffWin))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(cardiffWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    root.mainloop()


def cardfitnessInfo():
    url = "https://cardiffhubs.co.uk/event/badminton-and-table-tennis-st-mellons-hub/2023-03-09/"
    webbrowser.open(url, new=0, autoraise=True)

def cardeatingInfo():
    url = "https://restaurantguru.com/healthy-Cardiff-c173"
    webbrowser.open(url, new=0, autoraise=True)



def Bristol_res():
    BristolWin= Toplevel(root)
    BristolWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    BristolWin.title("Health Advice For Bristol")
    BristolWin.configure(bg="light blue")

    l = Label(BristolWin, text= " Health Advice For Bristol ", bg='orange')
    l.config(font =("Courier", 14))
    l.pack()

    text = Text(BristolWin, height=30)
    text.pack()

    text.insert('1.0', ''' Health advice for Bristol:

                    Exercises can help improve:

                    1. Physical health 
                    2. Mental health

                    examples of exercise with locations:
                                     
                    . Luxe fitness - health club
                                   
                    . rock climbing - (Crazy Climb) 
                                   
                    . Running/Walking/Dog Walking - Brandon Hill park. 

                   Healthy eating locations:

                   . The Bowl Shed
                   . Stoked Food
                   . StreatWok 
                   
                        ''') 
    label4 = Label(BristolWin, text= " Click <Exercises> for more info: ", bg='orange', width= 50, font='Calibri 15 bold')
    label4.place(relx= 0.4, rely= 0.5)

    Info = Button(BristolWin, text="Exercises", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = brisfitnessInfo)
    Info.place(relx= 0.5, rely= 0.55)

    label5 = Label(BristolWin, text= " Click <Healthy Eating> for more info: ", bg='orange', width= 50, font='Calibri 15 bold')
    label5.place(relx= 0.4, rely= 0.6)

    eatInfo = Button(BristolWin, text="Healthy Eating", fg='#1E272E', bg='Orange', width= 20, font='Calibri 15 bold', command = briseatingInfo)
    eatInfo.place(relx= 0.5, rely= 0.65)

    darkMode = Button(BristolWin, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, BristolWin))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(BristolWin, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, BristolWin))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(BristolWin, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, BristolWin))
    reset.place(relx= 0.8, rely= 0.5)

    returnHome = Button(BristolWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    root.mainloop()
    
    root.mainloop()


def brisfitnessInfo():
    url = "https://redpointbristol.co.uk/session/crazy-climb/"    # taken from github url code
    webbrowser.open(url, new=0, autoraise=True)

def briseatingInfo():
    url = "https://www.tripadvisor.co.uk/Restaurants-g186220-c10679-Bristol_England.html"
    webbrowser.open(url, new=0, autoraise=True)
    

    

    confirm.pack()

def personalHealthTool():

    PhttWin= Toplevel(root)
    PhttWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    PhttWin.title("Personal health tracking tool")
    PhttWin.configure(bg="light blue")

    phttCaption= Label(PhttWin, text="Personal Health Tracking Tool", fg='#1E272E', bg='orange', width= 99, font='Calibri 20 bold')
    phttCaption.pack()

    twoFA = Label(PhttWin, text="Sensitive info like your medical and geo location requires a secondary login for security/privacy reasons", fg='#1E272E', bg='orange', width= 99, font='Calibri 20 bold')
    twoFA.pack()
    #informs the user that sensitive info is being accessed and 2fa is required

    firststeptwoFA = Label(PhttWin, text="<First Step>", fg='#1E272E', bg='orange', width= 99, font='Calibri 20 bold')
    firststeptwoFA.pack()
    #first step of 2FA 

    user_sign = Label(PhttWin, text="Enter Username", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
    user_sign.pack()

    #username textbox
    u_name = ttk.Entry(PhttWin, width= 15)
    u_name.place(relx= 0.4, rely=0.2)
    u_name.pack()

    pass_label = Label(PhttWin, text="Enter Password", fg='#1E272E', bg='orange', width= 35, font='Calibri 20 bold')
    pass_label.pack()

    #password textbox
    password = ttk.Entry(PhttWin, width= 15)
    password.place(relx= 0.4, rely=0.2)
    password.pack()

    prompt = Label(PhttWin, text="Health data will be presented below this message when <First Step> is complete:", fg='#1E272E', bg='orange', width= 67, font='Calibri 20 bold')
    prompt.place(relx= 0.4, rely= 0.3)

    confirm = Button(PhttWin, text="Confirm Details", fg='#1E272E', bg='orange', width= 30, font='Calibri 15 bold')
    confirm.bind("<Button-1>", lambda event: htrackerData(u_name,password, PhttWin))
    confirm.pack()

    returnHome = Button(PhttWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)


def htrackerData(u_name,password, PhttWin):

    if len(u_name.get()) > 0 and len(password.get()) >= 8 : # prescence/length check all data types 
       print("passed presc check")# debug
       
       htrackerPwordVal(password, u_name, PhttWin)
       
    else:
        missingData = messagebox.askretrycancel("Invalid Username Or Password", " Details provided are Wrong")
        PhttWin.destroy()
        personalHealthTool()

def htrackerPwordVal(password, u_name, PhttWin):

    cursor= conn.cursor()

    cursor.execute("SELECT DISTINCT Username FROM Users WHERE Password = ('" + password.get() + "')")
       
    user_rec = cursor

    user_rec = cursor.fetchone()[0] 

    conn.commit()

    print(user_rec)
    
    if user_rec == u_name.get():

       displayhtData(password, u_name, PhttWin)

    else:
         invalidUser = messagebox.askretrycancel("No user", " No User Found, <Retry> ? ")


def displayhtData(password, u_name, PhttWin): #function only runs if the users has 2fa success

    cursor = conn.cursor()
        
    cursor.execute("SELECT Location, Illness FROM Users WHERE Username = ('" + u_name.get() + "')") 
    
    pht_rec = cursor

    pht_rec = cursor.fetchall() 
    
    conn.commit()

    phtDetails = Label(PhttWin, text="Location | Illness/Illness Type", fg='#1E272E', bg='Orange', width= 70, font='Kalinga 10 bold underline', height = 2)
    phtDetails.place(relx= 0.4, rely= 0.4)

    
    phtData = Label(PhttWin, text="", fg='#1E272E', bg='Orange', width= 70, font='Kalinga 10 bold underline', height = 2)   
    phtData.config(text="{}".format(pht_rec)) #allows the text of the label to be the concatenation of pht_rec and an empty string
    phtData.place(relx= 0.4, rely= 0.5)



def userhelpGuide():

    uhgWin= Toplevel(root)
    uhgWin.state('zoomed') # .state('zoomed opens new window in fullscreen mode
    uhgWin.title("Personal health advice group user guide")
    uhgWin.configure(bg="light blue")

    windTitle = Label(uhgWin, text= " Health Advice Group User Guide ", bg='orange')
    windTitle.config(font =("Courier", 14))
    windTitle.pack()

    text = Text(uhgWin, height=50)
    text.pack()

    text.insert('1.0', '''   USER HELP GUIDE 

                             Health Advice Group
                             -------------------

                             Advice on how to Access features:
                             ---------------------------------
                             
                           - To access all main medical records
                             click on the <Personal Health Tracker>
                             you will have to re-enter your Uname
                             and Pword as it is sensitive info.

                           - If we have missed one of your health
                             concers regarding the weather, in the
                             <Health Affected By Weather> window
                             at the bottom of the window there is
                             a <More Info> button that will redirect
                             you to a new window with more information.

                           - If you find our descriptions of the weather
                             innaccurate or you require extra info
                             on future weather click the <more info online>
                             button.

                           - If you would like to find out Air Quality data
                             on your location (London, Brisol, Cardiff)
                             Click <Air Quality Dashboard> in the HAG
                             dashboard and simply select and confirm your
                             location with the listbox box and confirm button

                           - If your would like to get health advice based
                             on your location:
                             Click <Personalised Health advice based on location>
                             and select your location, and you will have info
                             that is specifically tailored to that current
                             location.

                             ---------------------------------------------

                             Health Advice Group Accessibility Features:
                             
                             -------------------------------------------
             
                             Health advice group offers the following:

                             Return to Home button - returns user to HAG
                             Homepage from current window.
                             
                             Dark mode - Changes screens Background
                             colour to Black

                              
                             Light mode - Changes screens Background
                             colour to White

                             Reset mode - Reset the current colour of
                             your background to default.
                             
                             -------------------------------------------


                             
                            ''') #text box which displays all user help guide info to user

    returnHome = Button(uhgWin, text="HAG Homepage", fg='#1E272E', bg='orange',font='Calibri 15 bold', height=2, command =HAGDashboard) #allows the users to return to the home screen (command=HAGDashboard)
    returnHome.place(relx=0.8, rely=0.2)
    
    darkMode = Button(uhgWin, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
    darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, uhgWin))
    darkMode.place(relx= 0.8, rely= 0.3)


    lightMode = Button(uhgWin, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
    lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, uhgWin))
    lightMode.place(relx= 0.8, rely= 0.4)

    reset = Button(uhgWin, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
    reset.bind("<Button-1>", lambda event: resetBackground(reset, uhgWin))
    reset.place(relx= 0.8, rely= 0.5)





# dark / light mode buttons for all relevant windows

#toggles reset in Bristol window

def resetBackground(reset, BristolWin):
    switch_value= True

        
    if switch_value == True:
        BristolWin.config(bg='light blue')
        BristolWin.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        BristolWin.config(bg='#F0F0F8')
        BristolWin.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Bristol window              
def toggledarkSwitch(darkMode, BristolWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        BristolWin.config(bg="#26242f")
        BristolWin.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        BristolWin.config(bg='#F0F0F8')
        BristolWin.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Bristol window       
def togglelightSwitch(lightMode, BristolWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        BristolWin.config(bg='#F0F0F8')
        BristolWin.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        BristolWin.config(bg='#F0F0F8')
        BristolWin.config(bg='#F0F0F8')
        switch_value = True
###########################################

#toggles reset in cardiff window

def resetBackground(reset, cardiffWin):
    switch_value= True

        
    if switch_value == True:
        cardiffWin.config(bg='light blue')
        cardiffWin.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        cardiffWin.config(bg='#F0F0F8')
        cardiffWin.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in cardiff window              
def toggledarkSwitch(darkMode, cardiffWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        cardiffWin.config(bg="#26242f")
        cardiffWin.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        cardiffWin.config(bg='#F0F0F8')
        cardiffWin.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in cardiff window       
def togglelightSwitch(lightMode, cardiffWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        cardiffWin.config(bg='#F0F0F8')
        cardiffWin.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        cardiffWin.config(bg='#F0F0F8')
        cardiffWin.config(bg='#F0F0F8')
        switch_value = True
###########################################


#toggles reset in london window

def resetBackground(reset, londonWin):
    switch_value= True

        
    if switch_value == True:
        londonWin.config(bg='light blue')
        londonWin.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        londonWin.config(bg='#F0F0F8')
        londonWin.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in london window              
def toggledarkSwitch(darkMode, londonWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        londonWin.config(bg="#26242f")
        londonWin.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        londonWin.config(bg='#F0F0F8')
        londonWin.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in london window       
def togglelightSwitch(lightMode, londonWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        londonWin.config(bg='#F0F0F8')
        londonWin.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        londonWin.config(bg='#F0F0F8')
        londonWin.config(bg='#F0F0F8')
        switch_value = True
###########################################
#toggles reset in habwWin window

def resetBackground(reset, habwWin):
    switch_value= True

        
    if switch_value == True:
        habwWin.config(bg='light blue')
        habwWin.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        habwWin.config(bg='#F0F0F8')
        habwWin.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in habwWin window              
def toggledarkSwitch(darkMode, habwWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        habwWin.config(bg="#26242f")
        habwWin.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        habwWin.config(bg='#F0F0F8')
        habwWin.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in habwWin window       
def togglelightSwitch(lightMode, habwWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        habwWin.config(bg='#F0F0F8')
        habwWin.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        habwWin.config(bg='#F0F0F8')
        habwWin.config(bg='#F0F0F8')
        switch_value = True

#toggles reset in Sunday window

def resetBackground(reset, Sunday_res_win):
    switch_value= True

        
    if switch_value == True:
        Sunday_res_win.config(bg='light blue')
        Sunday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Sunday_res_win.config(bg='#F0F0F8')
        Saturday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Sunday window              
def toggledarkSwitch(darkMode, Sunday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Sunday_res_win.config(bg="#26242f")
        Sunday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Sunday_res_win.config(bg='#F0F0F8')
        Sunday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Sunday window       
def togglelightSwitch(lightMode, Sunday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Sunday_res_win.config(bg='#F0F0F8')
        Sunday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Sunday_res_win.config(bg='#F0F0F8')
        Sunday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles reset in Saturday window

def resetBackground(reset, Saturday_res_win):
    switch_value= True

        
    if switch_value == True:
        Saturday_res_win.config(bg='light blue')
        Saturday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Saturday_res_win.config(bg='#F0F0F8')
        Saturday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Saturday window              
def toggledarkSwitch(darkMode, Saturday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Saturday_res_win.config(bg="#26242f")
        Saturday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Saturday_res_win.config(bg='#F0F0F8')
        Saturday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Saturday window       
def togglelightSwitch(lightMode, Saturday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Saturday_res_win.config(bg='#F0F0F8')
        Saturday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Saturday_res_win.config(bg='#F0F0F8')
        Saturday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles reset in Friday window

def resetBackground(reset, Friday_res_win):
    switch_value= True

        
    if switch_value == True:
        Friday_res_win.config(bg='light blue')
        Friday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Friday_res_win.config(bg='#F0F0F8')
        Friday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Friday window              
def toggledarkSwitch(darkMode, Friday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Friday_res_win.config(bg="#26242f")
        Friday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Friday_res_win.config(bg='#F0F0F8')
        Friday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Friday window       
def togglelightSwitch(lightMode, Friday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Friday_res_win.config(bg='#F0F0F8')
        Friday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Friday_res_win.config(bg='#F0F0F8')
        Friday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
###############################################

def resetBackground(reset, Thursday_res_win):
    switch_value= True

        
    if switch_value == True:
        Thursday_res_win.config(bg='light blue')
        Thursday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Thursday_res_win.config(bg='#F0F0F8')
        Thursday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Thursday window              
def toggledarkSwitch(darkMode, Thursday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Thursday_res_win.config(bg="#26242f")
        Thursday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Thursday_res_win.config(bg='#F0F0F8')
        Thursday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Thursday window       
def togglelightSwitch(lightMode, Thursday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Thursday_res_win.config(bg='#F0F0F8')
        Thursday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Thursday_res_win.config(bg='#F0F0F8')
        Thursday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
###############################################

#toggles reset in Wednesday window

def resetBackground(reset, Wednesday_res_win):
    switch_value= True

        
    if switch_value == True:
        Wednesday_res_win.config(bg='light blue')
        Wednesday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Wednesday_res_win.config(bg='#F0F0F8')
        Wednesday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Wednesday window              
def toggledarkSwitch(darkMode, Wednesday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Wednesday_res_win.config(bg="#26242f")
        Wednesday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Wednesday_res_win.config(bg='#F0F0F8')
        Wednesday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Wednesday window       
def togglelightSwitch(lightMode, Wednesday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Wednesday_res_win.config(bg='#F0F0F8')
        Wednesday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Wednesday_res_win.config(bg='#F0F0F8')
        Wednesday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
###############################################
        
def resetBackground(reset, Tuesday_res_win):
    switch_value= True

        
    if switch_value == True:
        Tuesday_res_win.config(bg='light blue')
        Tuesday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Tuesday_res_win.config(bg='#F0F0F8')
        Tuesday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in tuesday window              
def toggledarkSwitch(darkMode, Tuesday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Tuesday_res_win.config(bg="#26242f")
        Tuesday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Tuesday_res_win.config(bg='#F0F0F8')
        Tuesday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Tuesday window       
def togglelightSwitch(lightMode, Tuesday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Tuesday_res_win.config(bg='#F0F0F8')
        Tuesday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Tuesday_res_win.config(bg='#F0F0F8')
        Tuesday_res_win.config(bg='#F0F0F8')
        switch_value = True

#############################################


#toggles reset in monday window
def resetBackground(reset, Monday_res_win):
    switch_value= True

        
    if switch_value == True:
        Monday_res_win.config(bg='light blue')
        Monday_res_win.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        Monday_res_win.config(bg='#F0F0F8')
        Monday_res_win.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in monday window              
def toggledarkSwitch(darkMode, Monday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Monday_res_win.config(bg="#26242f")
        Monday_res_win.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        Monday_res_win.config(bg='#F0F0F8')
        Monday_res_win.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in monday window       
def togglelightSwitch(lightMode, Monday_res_win): 
    switch_value= True

        #dark mode
    if switch_value == True:
        Monday_res_win.config(bg='#F0F0F8')
        Monday_res_win.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        Monday_res_win.config(bg='#F0F0F8')
        Monday_res_win.config(bg='#F0F0F8')
        switch_value = True

#############################################

#toggles reset in userGuide window
def resetBackground(reset, uhgWin):
    switch_value= True

        
    if switch_value == True:
        uhgWin.config(bg='light blue')
        uhgWin.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        uhgWin.config(bg='#F0F0F8')
        uhgWin.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in signIn window              
def toggledarkSwitch(darkMode, uhgWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        uhgWin.config(bg="#26242f")
        uhgWin.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        uhgWin.config(bg='#F0F0F8')
        uhgWin.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in signIn window       
def togglelightSwitch(lightMode, uhgWin): 
    switch_value= True

        #dark mode
    if switch_value == True:
        uhgWin.config(bg='#F0F0F8')
        uhgWin.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        uhgWin.config(bg='#F0F0F8')
        uhgWin.config(bg='#F0F0F8')
        switch_value = True

##############################################

#toggles reset in signIn window
def resetBackground(reset, signIn):
    switch_value= True

        
    if switch_value == True:
        signIn.config(bg='light blue')
        signIn.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        signIn.config(bg='#F0F0F8')
        signIn.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in signIn window              
def toggledarkSwitch(darkMode, signIn): 
    switch_value= True

        #dark mode
    if switch_value == True:
        signIn.config(bg="#26242f")
        signIn.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        signIn.config(bg='#F0F0F8')
        signIn.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in signIn window       
def togglelightSwitch(lightMode, signIn): 
    switch_value= True

        #dark mode
    if switch_value == True:
        signIn.config(bg='#F0F0F8')
        signIn.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        signIn.config(bg='#F0F0F8')
        signIn.config(bg='#F0F0F8')
        switch_value = True

##############################################


#toggles reset in signUp window
def resetBackground(reset, signUp):
    switch_value= True

        
    if switch_value == True:
        signUp.config(bg='light blue')
        signUp.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        signUp.config(bg='#F0F0F8')
        signUp.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in signUp window              
def toggledarkSwitch(darkMode, signUp): 
    switch_value= True

        #dark mode
    if switch_value == True:
        signUp.config(bg="#26242f")
        signUp.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        signUp.config(bg='#F0F0F8')
        signUp.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in signUp window       
def togglelightSwitch(lightMode, signUp): 
    switch_value= True

        #dark mode
    if switch_value == True:
        signUp.config(bg='#F0F0F8')
        signUp.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        signUp.config(bg='#F0F0F8')
        signUp.config(bg='#F0F0F8')
        switch_value = True

##############################################


    #toggles reset in Sign Up/In menu
def resetBackground(reset, root):
    switch_value= True

        
    if switch_value == True:
        root.config(bg='light blue')
        root.config(bg='light blue')
        switch_value = False

         #light mode
    else:
        root.config(bg='#F0F0F8')
        root.config(bg='#F0F0F8')
        switch_value = True
        
        #toggles dark mode in Sign Up/In menu              
def toggledarkSwitch(darkMode, root): 
    switch_value= True

        #dark mode
    if switch_value == True:
        root.config(bg="#26242f")
        root.config(bg="#26242f")
        switch_value = False

         #light mode
    else:
        root.config(bg='#F0F0F8')
        root.config(bg='#F0F0F8')
        switch_value = True

#toggles light mode in Sign Up/In menu        
def togglelightSwitch(lightMode, root): 
    switch_value= True

        #dark mode
    if switch_value == True:
        root.config(bg='#F0F0F8')
        root.config(bg='#F0F0F8')
        switch_value = False

         #light mode
    else:
        root.config(bg='#F0F0F8')
        root.config(bg='#F0F0F8')
        switch_value = True

    

#####################################################################################################################################
root=Tk()

root.title("Health Advice Group Sign Up/In")
root.state('zoomed') 
root.configure(bg="light blue")

programName = "notepad.exe"
fileName = "F:\OCS_Task 2\Task2_Terms of service_[LL-000011429]_[Kalaydjiyski]_[M].txt"      #OPENS TERMS OF SERVICE
sp.Popen([programName, fileName]) # requires the right file path for program to run


windTitle = Label(root, text="Health Advice Group Sign Up/In", fg='#1E272E', bg='orange', width= 32, font='Kalinga 30 bold underline', height = 2)
windTitle.pack()

cookiesOpt = messagebox.askquestion("Health Advice Group Cookies", "Enable Cookies?") 

SignUpBut = Button(text="Sign Up", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command=signup_win) # opens the sign up window for the user
SignUpBut.place(relx= 0.4, rely= 0.2)

SignInBut = Button(text="Sign In", fg='#1E272E', bg='Orange', width= 25, font='Calibri 20 bold', command = signIn_win) # opens the sign in window for the user
SignInBut.place(relx= 0.4, rely= 0.3)


darkMode = Button(root, text="Dark Mode", fg='#1E272E', bg='grey',font='Calibri 15 bold', height=2)
darkMode.bind("<Button-1>", lambda event: toggledarkSwitch(darkMode, root))
darkMode.place(relx= 0.8, rely= 0.3)


lightMode = Button(root, text="Light Mode", fg='#1E272E', bg='#F0F0F8',font='Calibri 15 bold',height=2)
lightMode.bind("<Button-1>", lambda event: togglelightSwitch(lightMode, root))
lightMode.place(relx= 0.8, rely= 0.4)

reset = Button(root, text="Reset", fg='#1E272E', bg='green',font='Calibri 15 bold', height = 2)
reset.bind("<Button-1>", lambda event: resetBackground(reset, root))
reset.place(relx= 0.8, rely= 0.5)



root.mainloop()




