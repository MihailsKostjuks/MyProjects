from tkinter import *
from tkinter import Menu
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk
import mysql.connector
from email.message import EmailMessage
import smtplib
import ssl
conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db3"
    )


# WINDOW SETTINGS
window = Tk()
window.geometry("1160x1000")
window.title("Calcium Consumption Calculator")
window.resizable(False, False)



# FUNCTIONS
def store_to_database():
    if 'x2' not in globals():
        pregnantdb = '-'
    elif x2.get()==1:
        pregnantdb = 'yes'
    elif x2.get()==2:
        pregnantdb = 'no'

    if x1.get() == 1:
        genderdb = 'male'
    elif x1.get() == 2:
        genderdb = 'female'
    age1 = agee

    cursor = conn.cursor()
    #cursor.execute("CREATE DATABASE IF NOT EXISTS db3")
    #cursor.execute("CREATE TABLE IF NOT EXISTS data3(user_id INT AUTO_INCREMENT, gender VARCHAR(7), pregnant VARCHAR(5), age INT DEFAULT NULL, weight INT DEFAULT NULL, activity INT DEFAULT NULL, calciumneeded FLOAT(10,0) DEFAULT NULL, consumption FLOAT(10,0) DEFAULT NULL, PRIMARY KEY (user_id))")
    query = "INSERT INTO data3(gender,pregnant, age, weight, activity, calciumneeded, consumption) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, [genderdb, pregnantdb, age1.get(), weight1, act1, calcium, consumption])
    conn.commit()

def readmorelink():
    webbrowser.open_new_tab(r"https://www.teamiblends.com/blogs/lifestyle/10-surprising-benefits-of-calcium")

def persondata():
    global calcium
    global weight1
    global act1
    global weight1
    global act1
    calcium = 0
    if x1.get()==1:
        print("male")
        calcium+=200
    elif x1.get()==2:
        print("female")
        pass

    if 'x2' in globals():
        if x2.get()==1:
            print("pregnant")
            calcium+=300
        elif x2.get()==2:
            print("not pregnant")
            pass

    print(f"Age: {agee.get()}")

    if agee.get() < 4:
        calcium = 700
    elif agee.get() >= 4 and agee.get() < 9:
        calcium = 1000
    elif agee.get() >= 9 and agee.get() < 19:
        calcium = 1300
    elif agee.get() > 18 and agee.get() < 51:
        calcium += 900
    elif agee.get() > 50 and agee.get() < 150:
        calcium = 1100
    else:
        print("error. You ain't no 150+ years old!")

    if kgorlb.get()=="kg":
        print(f"Weight: {weightt.get()} kg")
        if weightt.get() > 70 and x1.get()==1:
            calcium = calcium + (weightt.get()-70)*5
        elif weightt.get() > 50 and x1.get()==2:
            calcium = calcium + (weightt.get()-50)*5
        weight1 = weightt.get()
    else:
        print(f"Weight: {weightt.get()} lb")
        if (weightt.get()/2.2) > 70 and x1.get()==1:
            calcium = calcium + ((weightt.get()/2.2)-70)*5
        elif (weightt.get()/2.2) > 50 and x1.get()==2:
            calcium = calcium + ((weightt.get()/2.2)-50)*5
        weight1 = weightt.get()/2.2

    if act.get()==activities[0]:
        pass
        act1=1
    elif act.get()==activities[1]:
        calcium+= 100
        act1=2
    elif act.get()==activities[2]:
        calcium+= 300
        act1=3
    elif act.get()==activities[3]:
        calcium+= 500
        act1=4
    else:
        act1 = 1

    print(calcium)
    analysis =f"""
    Good! According to data you've just submitted
    - your body needs {calcium} mg of calcium daily.
    Now, fill the form you can see below!
    """
    calcneeded = Label(frame2, text=analysis, justify=LEFT, font=(13)).grid(row=0, rowspan=5, column=9)
    global checkmarkimage
    checkmarkimage1 = Label(frame2, image=checkmarkimage).grid(row=0, rowspan=5, column=8, padx=(10,0))

def hidegender():
    if 'L4' in globals():
        L4.destroy()
    if 'pregnant' in globals():
        pregnant.destroy()
    if 'notpregnant' in globals():
        notpregnant.destroy()

def showgender():
    global L4
    global pregnant
    global notpregnant
    L4 = Label(frame2, text="Are you pregnant?", bg='red')
    L4.grid(row=2, column=0)
    global x2
    x2 = IntVar()
    yesorno = ["Yes", "No"]
    pregnant = Radiobutton(frame2, text=yesorno[0], variable=x2, value=1)
    notpregnant = Radiobutton(frame2, text=yesorno[1], variable=x2, value=2)
    pregnant.grid(row=2, column=1)
    notpregnant.grid(row=2, column=2)

def calculate():
    global consumption
    consumption = 0
    consumption += milk.get()*1.2
    consumption += cheese.get()*4
    consumption += greek.get()*2
    consumption += casein.get()*5
    consumption += fish.get()*2.5
    consumption += veggies.get()*0.8
    consumption += nuts.get()
    consumption += tofu.get()*3.2
    consumption = consumption / 7
    consumption += 200
    print(consumption)

    store_to_database()
    showresults()
def showresults():
    global results
    global calcium
    global consumption
    global email_entry
    global def_or_surp
    results = Tk()

    if calcium<=consumption:
        def_or_surp = f"Congratulations! You've no calcium deficit."
    elif calcium>consumption:
        def_or_surp = f"""Your body lacks {calcium-int(consumption)}mg of calcium.
        Please take care of your nutrition.
        Probably, you need some additional calcium supplements."""
    t1 = f"""
    Your daily calcium needed : {calcium} mg
    Your current daily consumption: {int(consumption)} mg
    {def_or_surp}
    """
    conclusion = Label(results, text=t1, font=(12)).grid(row=0, column=0, columnspan=2)

    suggestemail = Label(results, text='In order not to lose your analysis results, we can send you them per email:').grid(row=1, column=0, columnspan=2, padx=20, sticky='w')

    email_entry = Entry(results, width='36')
    email_entry.grid(row=2, column=0, padx=(23,0), sticky='w',pady=(0,10))
    emailbutton = Button(results, text='send results', command=sendresults, width=20).grid(row=2, column=1, sticky='w',pady=(0,10))
    results.mainloop()

def sendresults():
    try:
        email_sender = 'calculatorcalcium@gmail.com'
        email_password = ''
        email_receiver = email_entry.get()
        subject = 'Calcium Analysis Results'
        body = f'''Your results:
        Calcium daily needed - {calcium}mg.
        Your average daily calcium consumption - {int(consumption)}mg.
        {def_or_surp}
        
        Best wishes,
        Your CCC
        '''

        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
            smpt.login(email_sender, email_password)
            smpt.sendmail(email_sender, email_receiver, em.as_string())
    except:
        print('Email was not sent')
        Label(results, text="Email was not sent. Enter valid email address!", fg='red').grid(row=3, column=0, columnspan=2, pady=10)
    else:
        print('email was sent')
        Label(results, text="Email was sent successfully. Stay healthy =)",fg='green').grid(row=4, column=0, columnspan=2, pady=10)
# FRAMES
#frame0 = Frame(window, highlightbackground="black", highlightthickness=3) # delete later highlightbg and highlightthickness
frame1 = Frame(window, highlightbackground="black", highlightthickness=3)
frame2 = Frame(window)
frame4 = Frame(window, highlightbackground="black", highlightthickness=3)

#frame0.grid(row=0, column=0, padx=20, pady=3, sticky="n") # delete pady
frame1.grid(row=0, column=0, padx=40, pady=3, sticky='w')
frame2.grid(row=1, column=0, padx=40, pady=3, sticky="w")
#frame3.grid(row=3, column=0, padx=20, pady=3, sticky="n")
frame4.grid(row=2, column=0, padx=40, pady=3, sticky="w")



# TEXTS
text0 = """Calcium 
Consumption
Calculator"""

text1 = """
Calcium is an essential mineral found in many foods and plays a role in many 
other functions. BUT: Your body doesn’t make calcium on its own. This means 
you need to consume calcium through a nutritious diet or with supplements. For 
this reason, we highly recommend you to use our Calcium Consumption Calculator 
in order to clarify either your diet is balanced or your body lacks calcium."""


# IMAGES
calciumimageraw = Image.open("calcium1.jpg")
calciumresized = calciumimageraw.resize((220,170))
calciumimage = ImageTk.PhotoImage(calciumresized)
calciumimage1 = Label(frame1, image=calciumimage).grid(row=0, rowspan=2, column=2)

checkmarkraw = Image.open('checkmarkpic.jpg')
checkmarkresized = checkmarkraw.resize((120, 120))
checkmarkimage = ImageTk.PhotoImage(checkmarkresized)



# LABELS
title = Label(frame1, justify=LEFT, text=text0, font=(None, 30)).grid(row=0, column=0, rowspan=2)
intro1 = Label(frame1, justify=LEFT, text=text1, font=(None, 12)).grid(row=0, column=1, padx=20)
intro2 = Label(frame2, text="Please fill required fields:", font=12, bg='red').grid(row=0, column=0, columnspan=3, pady=(0,10), sticky="w")

L1 = Label(frame2, text="Enter your gender", bg='red').grid(row=1, column=0, sticky='w')
L2 = Label(frame2, text="Enter your age", bg='red').grid(row=3, column=0, sticky='w')
L3 = Label(frame2, text="Enter your bodyweight", bg='red').grid(row=1, column=3, padx=(10,0), sticky='w')
L6 = Label(frame2, text="Choose your physical activity", bg='red').grid(row=2, column=3, padx=(10,0), sticky='w')

c1 = Label(frame4, text="How much [mililiters] of MILK do you consume WEEKLY?").grid(row=0, column=0, sticky='w')
c2 = Label(frame4, text="How much [grams] of CHEESE do you consume WEEKLY?").grid(row=1, column=0, sticky='w')
c3 = Label(frame4, text="How much [grams] of GREEK YOGURT and COTTAGE CHEESE do you consume WEEKLY?").grid(row=2, column=0, sticky='w')
c4 = Label(frame4, text="How much [grams] of CASEIN do you consume WEEKLY?").grid(row=3, column=0, sticky='w')
c5 = Label(frame4, text="How much [grams] of SARDING and ANCHOVY do you consume WEEKLY?").grid(row=4, column=0, sticky='w')
c6 = Label(frame4, text="How much [grams] of SHRIMPS, OCTOPUS, CRAB and other seafood do you consume WEEKLY?").grid(row=5, column=0, sticky='w')
c7 = Label(frame4, text="How much [grams] of VEGETABLES and FRUITS do you consume WEEKLY?").grid(row=6, column=0, sticky='w')
c8 = Label(frame4, text="How much [grams] of NUTS do you consume WEEKLY?").grid(row=7, column=0, sticky='w')
c9 = Label(frame4, text="How much [grams] of TOFU do you consume WEEKLY?").grid(row=8, column=0, sticky='w')
c10 = Label(frame4, text="How much [miligrams] of CALCIUM SUPPLEMENTS do you consume DAILY?").grid(row=9, column=0, sticky='w')

# RADIO BUTTONS
x1 = IntVar()
genders = ["Male", "Female"]
male = Radiobutton(frame2, text=genders[0], variable=x1, value=1, command=hidegender).grid(row=1, column=1)
female = Radiobutton(frame2, text=genders[1], variable=x1, value=2, command=showgender).grid(row=1, column=2)


# ENTRY
agee = IntVar()
age = Entry(frame2, textvariable=agee).grid(row=3, column=1, columnspan=2, sticky='w')
weightt = IntVar()
weight = Entry(frame2, textvariable=weightt).grid(row=1, column=4, padx=(12,0), sticky='w')



# SCALES
milk = DoubleVar()
milkscale = Scale(frame4, from_=0, to=3000, orient=HORIZONTAL, length=500, tickinterval=300, resolution=100, variable=milk).grid(row=0, column=1, padx=(58,0))

cheese = DoubleVar()
cheesescale = Scale(frame4, from_=0, to=3000, orient=HORIZONTAL, length=500, tickinterval=300, resolution=100, variable=cheese).grid(row=1, column=1, padx=(58,0))

greek = DoubleVar()
greekscale = Scale(frame4, from_=0, to=3000, orient=HORIZONTAL, length=500, tickinterval=300, resolution=100, variable=greek).grid(row=2, column=1, padx=(58,0))

casein = DoubleVar()
caseinscale = Scale(frame4, from_=0, to=500, orient=HORIZONTAL, length=500, tickinterval=50, resolution=10, variable=casein).grid(row=3, column=1, padx=(58,0))

fish = DoubleVar()
fishscale = Scale(frame4, from_=0, to=1500, orient=HORIZONTAL, length=500, tickinterval=150, resolution=50, variable=fish).grid(row=4, column=1, padx=(58,0))

sea = DoubleVar()
seascale = Scale(frame4, from_=0, to=1500, orient=HORIZONTAL, length=500, tickinterval=150, resolution=50, variable=sea).grid(row=5, column=1, padx=(58,0))

veggies = DoubleVar()
veggiesscale = Scale(frame4, from_=0, to=5000, orient=HORIZONTAL, length=500, tickinterval=500, resolution=100, variable=veggies).grid(row=6, column=1, padx=(58,0))

nuts = DoubleVar()
nutsscale = Scale(frame4, from_=0, to=1500, orient=HORIZONTAL, length=500, tickinterval=150, resolution=50, variable=nuts).grid(row=7, column=1, padx=(58,0))

tofu = DoubleVar()
tofuscale = Scale(frame4, from_=0, to=3000, orient=HORIZONTAL, length=500, tickinterval=300, resolution=100, variable=tofu).grid(row=8, column=1, padx=(58,0))

supps = DoubleVar()
suppsscale = Scale(frame4, from_=0, to=1000, orient=HORIZONTAL, length=500, tickinterval=100, resolution=50, variable=supps).grid(row=9, column=1, padx=(58,0))

# BUTTONS
readmore = Button(frame1, text="Read more about calcium", command=readmorelink, fg='white', bg='black').grid(row=1, column=1)
submit1 = Button(frame2, text="Submit", command=persondata, width=10, fg='white', bg='black').grid(row=3, column=3, padx=(12,0), sticky='w')
calculatebutton = Button(frame4, text="Calculate", font=(15), command=calculate, width=10, fg='white', bg='black').grid(row=10, column=1, pady=(20,0), padx=(0,3), sticky='e')


# MENUS
weightvar = ["kg","lb",]
kgorlb = StringVar(window)
kgorlb.set(weightvar[0]) # default value
menu1 = OptionMenu(frame2, kgorlb, *weightvar).grid(row=1, column=5, sticky='e')

activities = ["No physical activity", "Some physical activity", "Amateur sport or physical job", "Professional sport"]
act = StringVar(window)
act.set("Please select") # default value
menu2 = OptionMenu(frame2, act, *activities).grid(row=2, column=4, columnspan=2, padx=(10,0), sticky='w')


window.mainloop()

