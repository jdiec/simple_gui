
import sys
from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename
from tkMessageBox import showerror, showinfo
import subprocess
import os.path
import os
from src import controller
import csv
import fileinput
from collections import Counter

load = ""
rulefile = ""
classlist = ""

load_classlist = ""
load_studentID = ""
load_group_size = ""
load_specGroups = ""
load_cluster = ""
load_cv = ""
load_aggregate = ""
load_av = ""
load_distribute = ""
load_dv =""


cValues = ""
aValues = ""
dValues = ""

clusterPriority = 0
aggregatePriority = 0
distributePriority = 0
functionList = []
functionList2 = []

BASE = RAISED
SELECTED = FLAT

# a base tab class
class Tab(Frame):
	def __init__(self, master, name):
		Frame.__init__(self, master)
		self.tab_name = name

# the bulk of the logic is in the actual tab bar
class TabBar(Frame):
	def __init__(self, master=None, init_name=None):
		Frame.__init__(self, master)
		self.tabs = {}
		self.buttons = {}
		self.current_tab = None
		self.init_name = init_name
	
	def show(self):
		self.pack(side=TOP, expand=YES, fill=X)
		self.switch_tab(self.init_name or self.tabs.keys()[-1])# switch the tab to the first tab
	
	def add(self, tab):
		tab.pack_forget()									# hide the tab on init
		
		self.tabs[tab.tab_name] = tab						# add it to the list of tabs
		b = Button(self, text=tab.tab_name, relief=BASE,	# basic button stuff
			command=(lambda name=tab.tab_name: self.switch_tab(name)))	# set the command to switch tabs
		b.pack(side=LEFT)												# pack the buttont to the left mose of self
		self.buttons[tab.tab_name] = b											# add it to the list of buttons
	
	def delete(self, tabname):
		
		if tabname == self.current_tab:
			self.current_tab = None
			self.tabs[tabname].pack_forget()
			del self.tabs[tabname]
			self.switch_tab(self.tabs.keys()[0])
		
		else: del self.tabs[tabname]
		
		self.buttons[tabname].pack_forget()
		del self.buttons[tabname] 
		
	
	def switch_tab(self, name):
		if self.current_tab:
			self.buttons[self.current_tab].config(relief=BASE)
			self.tabs[self.current_tab].pack_forget()			# hide the current tab
		self.tabs[name].pack(side=BOTTOM)							# add the new tab to the display
		self.current_tab = name									# set the current tab to itself
		
		self.buttons[name].config(relief=SELECTED)
		

"""Creates a base (default) rule file """
def baseFile():
    name = "test_groups.txt" 
    try:
        file = open(name,'a+')   
        file.close()
        with open(name, 'r+') as s:        
            s.write("#Project Name : " + name + "\n"
                    + "classlist : \n"
                    + "student_identifier : " + "\n"
                    + "group_size : " + "\n"
                    + "- cluster : " + "\n" + " values : " + "\n"
                    + "- aggregate : " + "\n" + " values : " + "\n"
                    + "- distribute : " + "\n" + " values : ")
    except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0) # quit Python
    return



#To use later
def beenClicked():
    radioValue = relStatus.get()
    tkMessageBox.showinfo("You clicked", radioValue)
    return
#To use later
def changeLabel():
    name = "Thanks for the click " + yourName.get()
    labelText.set(name)
    yourName.delete(0, END)
    

""" Display the contents of the csv file in a drop down menu. """
def display():
    name = rulefile if rulefile != "" else "test_groups.txt"
    x = fileinput.input(name, inplace=1) 
    for line in x:
        if "classlist" in line:
            line = line.replace("classlist : ", "", 1)
            global classlist
            classlist = line
    x.close()
    spreadsheet = (classlist if classlist != "" else "sample_class_1.csv" )
    spreadsheet = spreadsheet.strip("\n")
    csvReader = csv.reader(open(spreadsheet, 'rb'), delimiter=',')
    options = [" "]
    for row in csvReader:
        for column in row:
            options.append(column)
        break    
    return options

def displayValues(choice):
    if choice == " " or choice == "Select an option":
        return " "
    name = ("sample_class_1.csv" if uploadText.get() == "Upload a list of students"
            else uploadText.get())   
    csvReader = csv.reader(open(name, 'rb'), delimiter=',')
    options = [" "]
    value = 0
    for row in csvReader:
        for column in row:
            if column == choice:
                value += row.index(column)
                break
        options.append(row[value])
    options = list(set(options))
    if choice in options : options.remove(choice)
    if load == "":
        global cvLabel
        cvLabel.pack_forget()
        global cvDropDown
        if cvDropDown != None : cvDropDown.destroy() #cvDropDown.pack_forget()
        cvText = StringVar()
        cvText.set("Values:")
        cvLabel = Label(tabCluster, textvariable = cvText)
        cvLabel.pack()
        clusterValues = StringVar()
        clusterValues.set("Select an option")
        cvFiles = options
        cvDropDown = OptionMenu(tabCluster, clusterValues, *cvFiles, command = getcValues)
        cvDropDown.pack()
    else:
        global cvLabel2
        cvLabel2.pack_forget()
        global cvDropDown2
        if cvDropDown2 != None : cvDropDown2.destroy() #cvDropDown.pack_forget()
        cvText2 = StringVar()
        cvText2.set("Values:")
        cvLabel2 = Label(tabCluster2, textvariable = cvText2)
        cvLabel2.pack()
        clusterValues2 = StringVar()
        clusterValues2.set("Select an option")
        cvFiles2 = options
        cvDropDown2 = OptionMenu(tabCluster2, clusterValues2, *cvFiles2, command = getcValues)
        cvDropDown2.pack()
    return

def getcValues(choice):
    global cValues
    cValues = choice
    print cValues
    return

def getcPriority(choice):
    if choice == "Select an option" or choice == " ":
        return 
    global clusterPriority
    clusterPriority = str(choice) + "cluster"
    print "Cluster priority: " + clusterPriority
    return


""" Displays aggregate values based on choice """
def displayAggValues(choice):
    if choice == " " or choice == "Select an option":
        return " "
    name = ("sample_class_1.csv" if uploadText.get() == "Upload a list of students"
            else uploadText.get())   
    csvReader = csv.reader(open(name, 'rb'), delimiter=',')
    options = [" "]
    value = 0
    for row in csvReader:
        for column in row:
            if column == choice:
                value += row.index(column)
                break
        options.append(row[value])
    options = list(set(options))
    #if choice in options : options.remove(choice)
    #global avLabel
    #avLabel.pack_forget()
    #global avDropDown
    #if avDropDown != None : avDropDown.pack_forget()
    #avText = StringVar()
    #avText.set("Values:")
    #avLabel = Label(tabAggregate, textvariable = avText)
    #avLabel.pack()
    #aggValues = StringVar() 
    #aggValues.set("Select an option")
    #avFiles = options
    #avDropDown = OptionMenu(tabAggregate, aggValues, *avFiles)
    #avDropDown.pack()
    return


""" Display the distribute values based on choice """
def displayDisValues(choice):
    if choice == " " or choice == "Select an option":
        return " "
    name = ("sample_class_1.csv" if uploadText.get() == "Upload a list of students"
            else uploadText.get())   
    csvReader = csv.reader(open(name, 'rb'), delimiter=',')
    options = [" "]
    value = 0
    for row in csvReader:
        for column in row:
            if column == choice:
                value += row.index(column)
                break
        options.append(row[value])
    options = list(set(options))
    if choice in options : options.remove(choice)
    
    if load == "":
        global dvLabel
        dvLabel.pack_forget()
        global dvDropDown
        if dvDropDown != None : dvDropDown.pack_forget()
        dvText = StringVar()
        dvText.set("Values:")
        dvLabel = Label(tabDistribute, textvariable = dvText)
        dvLabel.pack()
        disValues = StringVar()
        disValues.set("Select an option")
        dvFiles = options
        dvDropDown = OptionMenu(tabDistribute, disValues, *dvFiles, command = getdValues)
        dvDropDown.pack()
    
    else:
        global dvLabel2
        dvLabel2.pack_forget()
        global dvDropDown2
        if dvDropDown2 != None : dvDropDown2.pack_forget()
        dvText2 = StringVar()
        dvText2.set("Values:")
        dvLabel2 = Label(tabDistribute2, textvariable = dvText2)
        dvLabel2.pack() 
        disValues2 = StringVar()
        disValues2.set("Select an option")
        dvFiles2 = options
        dvDropDown2 = OptionMenu(tabDistribute2, disValues2, *dvFiles2, command = getdValues)
        dvDropDown2.pack()

    return

def getdValues(choice):
    global dValues
    dValues = choice
    print dValues
    return

def getdPriority(choice):
    if choice == "Select an option" or choice == " ":
        return	
    global distributePriority
    distributePriority = str(choice) + "distribute"
    print "Distribute priority: " + distributePriority
    return	
                

########## USER UPLOADS A LIST OF STUDENTS ##########    
""" Retrieves the name of the student list file.
    Precondition: Comma separated values (.csv) file
"""
def uploadFile():
    name = rulefile if rulefile != "" else "test_groups.txt"  
    path = askopenfilename()
    d, f = os.path.split(path)
    os.chdir(d)
    path2 = str(path).rindex("/") + 1
    path3 = str(path[path2:]).strip()
    if ".csv" not in path3:
        tkMessageBox.showinfo("Wait!", "Please make sure you are uploading "
                              + "a comma separated value (.csv) file.")
        return
    uploadText.set(path3)
    uploadText2.set(path3)
    x = fileinput.input(name, inplace=1) 
    for line in x:
        line = (line.replace(line, "classlist : " + path3)
                if "classlist" in line else line) 
        print line
    x.close()
    clusterMenu.set(loadCluster())   #TESTING TESTING TESTING
    return

    
########## GET USER INPUT FOR STUDENT_IDENTIFIER ##########    
""" Student Identifier """
def studentIdentifier():
    choice = idMenu2.get() if load != "" else idMenu.get()
    if choice == " " or choice == "Select an option":
        tkMessageBox.showinfo("Wait!", "Please select an option for"
                              + "'Student Identifier'.")
        return
    name = rulefile if rulefile != "" else "test_groups.txt"
    x = fileinput.input(name, inplace=1) 
    for line in x:
        line = (line.replace(line, "student_identifier : " + choice)
                if "student_identifier" in line else line) 
        print line
    x.close()
    removeLines()
    print "STUDENT IDENTIFIER : " + choice + " in " + rulefile
    return
    

########## GET USER INPUT FOR GROUP SIZE ##########    
""" In case students do not divide evenly, some groups will have either a- or a+ students. """
def specialGroups():
    choice = studFiles.get() if load == "" else studFiles2.get()
    number = yourName.get().strip() if load == "" else yourName2.get().strip()
    if number == '' or number.isdigit() == False:
        number = str(4)
        tkMessageBox.showinfo("Wait!", "Please enter a numerical value"
                              + " for 'Number of students per group'.")
        return
    name = rulefile if rulefile != "" else "test_groups.txt"
    choice = number + "-" if choice == "One less student" else number + "+"        
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = (line.replace(line, "group_size : " + choice)
                if "group_size" in line else line) 
        print line
    x.close()
    removeLines()
    print "SPECIAL GROUPS " + number + choice + " in " + rulefile
    return
    

########## GET USER INPUT FOR CLUSTER ##########
""" Cluster students. """
def cluster():
    choice = clusterMenu2.get() if load != "" else clusterMenu.get()
    #priority = cpMenu2.get() if load != "" else cpMenu.get()
    #print "CLUSTER " + priority
    name = rulefile if rulefile != "" else "test_groups.txt"
    val = cValues 
    print clusterValues2.get()
    print clusterValues.get()
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = line.replace(line, "") if "cluster" in line else line
        print line
    x.close()
    if choice != " " and choice != "Select an option":
        with open(name, "a") as x:
            x.write("\n- cluster : " + choice + "\n"
                    + "  values : " + val)
    removeLines()
    print "CLUSTER " + choice + " values: " + val + " in " + rulefile
    return
    

########## GET USER INPUT FOR AGGREGATE ##########    
""" Aggregate students. """
def aggregate():
    choice = aggMenu2.get() if load != "" else aggMenu.get()
    #priority = apMenu2.get() if load != "" else apMenu.get()
    #print "AGG " + priority
    name = rulefile if rulefile != "" else "test_groups.txt"
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = line.replace(line, "") if "aggregate" in line else line
        print line
    x.close()
    if choice != " " and choice != "Select an option":
        with open(name, "a") as x:
            x.write("\n- aggregate : " + choice)
    removeLines()
    print "AGGREGATE " + choice + " in " + rulefile
    return

def getaPriority(choice):
    if choice == "Select an option" or choice == " ":
        return	
    global aggeregatePriority
    aggregatePriority = str(choice) + "aggregate "
    print "Aggregate priority: " + aggregatePriority
    return



######### GET USER INPUT FOR DISTRIBUTE ##########
""" Distrubute students. """    
def distribute():
    choice = disMenu2.get() if load != "" else disMenu.get()
    #priority = dpMenu2.get() if load != "" else dpMenu.get()
    #print "DIS " + priority
    name = rulefile if rulefile != "" else "test_groups.txt"
    val = dValues
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = line.replace(line, "") if "distribute" in line else line
        print line
    x.close()
    if choice != " " and choice != "Select an option":
        with open(name, "a") as x:
            x.write("\n- distribute : " + choice + "\n"
                    + "  values : " + val)
    removeLines()
    print "DISTRIBUTE " + choice + " values : " + val + " in " + rulefile
    return


########## CREATE NEW RULE FILE ##########    
""" Create new rule file for new project.
    If file already exists, user may choose to overwite.
"""
def write():
    if projectName.get().strip() is "":
        tkMessageBox.showinfo("Wait!","Please enter a name for your project.")
        return
    name = projectName.get().strip() + ".txt"
    if os.path.isfile(name):
        result = tkMessageBox.askquestion("Confirmation",
                        "A file with the name " + "'" + name 
                        + "'" + " already exists." + "\n" 
                        + "Would you like to overwrite it?",
                        icon='warning')
        if result == "no":
            return
        if result == "yes":
            open(name, 'w').close()
    try:
        file = open(name,'a+')   
        file.close()
        with open(name, 'r+') as s:        
            s.write("#Project Name : " + name + "\n"
                    + "classlist : " + "\n"
                    + "student_identifier : " + "\n"
                    + "group_size : " + "\n")
        projectText.set(name)
    except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0) # quit Python
    global rulefile
    rulefile = name
    bar.add(tab1)
    bar.add(tabCluster)
    bar.add(tabAggregate)
    bar.add(tabDistribute)
    bar.add(tabBalance)
    bar.add(tabTolerance)
    bar.delete("Name your Project")
    tkMessageBox.showinfo("Confirmation",
                          "Rule file '" + name + "' was sucessfully " 
                          + "created and added to the folder.")
    return


########## REMOVE UNECESSARY ITEMS IN THE RULEFILE ##########
""" Remove unecessary lines containing 'values' """
def removeValues():
    name = rulefile if rulefile != "" else "test_groups.txt"
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = line.replace(line, "") if "values" in line else line
        print line
    x.close()
    removeLines()
    return


""" Remove empty lines in the text file """
def removeLines():
    name = rulefile if rulefile != "" else "test_groups.txt" 
    x = fileinput.input(name, inplace=1) 
    for line in x:
        line = line.rstrip()
        if line != "":
            print line
    x.close()
    return


########## SET BALANCE VALUE ##########
""" Balance certain values """
def balance():
    choice = balanceMenu2.get() if load != "" else balanceMenu.get()
    name = rulefile if rulefile != "" else "test_groups.txt"
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = line.replace(line, "") if "balance" in line else line
        print line
    x.close()
    if choice != " " and choice != "Select an option":
        with open(name, "a") as x:
            x.write("\n- balance : " + choice)
    removeLines()
    print "BALANCE " + choice + " in " + rulefile
    return


########## ADD TOLERANCE LEVEL ##########
""" Add tolerance level
    Precondition : Integer or float
"""
def tolerance():
    choice = toleranceValue2.get() if load != "" else toleranceValue.get()
    name = rulefile if rulefile != "" else "test_groups.txt"
    x = fileinput.input(name, inplace=1)
    for line in x:
        line = line.replace(line, "") if "tol" in line else line
        print line
    x.close()
    if choice.strip() != "":
        with open(name, "a") as x:
            x.write("\n#- tol : " + choice)
    removeLines()
    print "TOLERANCE " + choice + " in " + rulefile
    return


########## SAVE USER INPUT ##########
""" Saves the current user input. """
def save():
    print "SAVE " + rulefile
    removeValues()
    studentIdentifier()
    specialGroups()
    cluster()
    aggregate()
    distribute()
    balance()
    tolerance()
    tkMessageBox.showinfo("SAVED", "Your input has been saved to "
                              + "'" + rulefile + "'" + ".\n\nIf you wish to use it"
                              + " later on, load the file under 'Existing Project'"
                              + " on the home screen." )
    return

########## RUN GROUPENG ##########
""" Run GroupEng. This is the final step.  """
def groupEng():
    result = tkMessageBox.askquestion("Confirmation",
                        "Please make sure that "
                        + "you have finalized all of your input." + "\n" 
                        + "Proceed with group creation?",
                        icon='warning')
    if result == "no":
        return
    save()
    if len(sys.argv) > 1:
        try:
            groups, status, outdir = controller.run(sys.argv[1])
            if not status:
                print('Could not completely meet all rules')
        except Exception as e:
            print(e)
    else:
        if rulefile == "":
            return
        #name = ("student_groups.txt" if rulefile == ""
        #        else rulefile)
        name = rulefile
        #name = "student_groups.txt"
        path = str(os.getcwd())
        path = path + '/' + name 
        d, f = os.path.split(path)
        os.chdir(d)
        try:
            groups, status, outdir = controller.run(f)
        except Exception as e:
            showerror('GroupEng Error', '{0}'.format(e))
        
        if status:
            showinfo("GroupEng", "GroupEng Run Succesful\n Output in: {0}".format(outdir))

            bar.add(tabResults) #Display groups

        else:
            showinfo("GroupEng", "GroupEng Ran Correctly but not all rules could be met\n"
                     "Output in: {0}".format(outdir))

            bar.add(tabResults)



########## NEW PROJECT ##########
""" Begins a new project by creating a new rule file (.txt)
    that is named by the user
"""
def new():
    bar.add(tab00)
    bar.delete("Welcome to GroupEng")
    return

########## LOAD EXISTING PROJECT ##########
""" Load an existing rule file.
    Precondition: Must be in text (.txt) format.
"""
def existingProject(): 
    path = askopenfilename()
    d, f = os.path.split(path)
    os.chdir(d)
    path2 = str(path).rindex("/") + 1
    path3 = str(path[path2:]).strip()
    if ".txt" not in path3:
        tkMessageBox.showinfo("Wait!", "Please make sure your file is "
                              + "in text (.txt) format.")
        return
    if os.stat(path3) [6] == 0:
        tkMessageBox.showinfo("Wait!", "Please make sure you are not "
                              + "uploading an empty file.")
        return
    global rulefile
    rulefile = path3
    bar.add(tab3)
    bar.add(tabCluster2)
    bar.add(tabAggregate2)
    bar.add(tabDistribute2)
    bar.add(tabBalance2)
    bar.add(tabTolerance2)
    bar.delete("Welcome to GroupEng")
    global load 
    load = "LOADED"
    uploadText2.set(loadClasslist())
    yourName2.delete(0, END)
    #yourName2.insert(0, loadGroupSize())
    idMenu2.set(loadIdentifier())
    studFiles2.set(loadSpecGroups())
    #change group size display				# CHANGE GROUP SIZE DISPLAY
    clusterMenu2.set(loadCluster())
    clusterValues2.set(loadClusterValues())
    aggMenu2.set(loadAggregate())
    disMenu2.set(loadDistribute())
    disValues2.set(loadDistributeValues())
    balanceMenu2.set(loadBalance())
    tkMessageBox.showinfo("Bravo!", "Your project has been successfully "
                              + "loaded.")
    return

""" Display the contents of a loaded classlist. """
def loadClasslist():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open (name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif ("classlist" in line and "#" not in line and
                line.replace("classlist : ", "", 1).strip() != ""):
                return line.replace("classlist : ", "", 1)
    return "<No file selected>"

""" Display the loaded student identifier. """
def loadIdentifier():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open (name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif ("student_identifier" in line and "#" not in line and
                line.replace("student_identifier : ", "", 1).strip() != ""):
                return line.replace("student_identifier : ", "", 1)
    return "Select an option"

""" Display the loaded group size. """
def loadGroupSize():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open (name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif "group_size" in line and "#" not in line:
                global load_group_size
                load_group_size += line.replace("group_size : ", "", 1)
    if "+" in load_group_size:
        return load_group_size.replace("+", "", 1)
    elif "-" in load_group_size:
        return load_group_size.replace("-", "", 1)
    else:
        return 

""" Display the loaded choice for special groups. """
def loadSpecGroups():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif "+" in line and "#" not in line:
                return "One extra student"
            elif "-" in line and "#" not in line:
                return "One less student"
    return "Select an option"

""" Display the loaded cluster choice """
def loadCluster():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif ("cluster" in line and "#" not in line and
                line.replace("- cluster : ", "", 1).strip() != ""):
                return line.replace("- cluster : ", "", 1)
    return "Select an option"

""" Display the loaded cluster values """ 
def loadClusterValues():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as x:
        for line in x:
            if "#" in line:
                continue
            elif ("cluster" in line and "#" not in line):
                print next(x).replace("values : ", "", 1)
                return next(x).replace("values : ", "", 1)
    return "Select an option"

""" Display the loaded aggregate choice """
def loadAggregate():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif ("aggregate" in line and "#" not in line and
                line.replace("- aggregate : ", "", 1).strip() != ""):
                return line.replace("- aggregate : ", "", 1)
    return "Select an option"

""" Display the loaded distribute choice """
def loadDistribute():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            if ("distribute" in line and "#" not in line and
                line.replace("- distribute : ", "", 1).strip() != ""):
                return line.replace("- distribute : ", "", 1)
    return "Select an option"

""" Display the loaded distribute values """
def loadDistributeValues():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as x:
        for line in x:
            if "#" in line:
                continue
            elif ("distribute" in line and "#" not in line):
                return next(x).replace("values : ", "", 1)
    return "Select an option"


""" Display the loaded balance choice """
def loadBalance():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif ("balance" in line and "#" not in line and
                line.replace("- balance : ", "", 1).strip() != ""):
                return line.replace("- balance : ", "", 1)            
    return "Select an option"

""" Display the loaded tolerance level """
def loadTolerance():
    name = rulefile if rulefile != "" else "test_groups.txt"
    with open(name, "r") as test:
        for line in test:
            if "#" in line:
                continue
            elif ("tol" in line and "#" not in line and
                line.replace("- tol : ", "", 1).strip() != ""):
                return line.replace("- tol : ", "", 1)            
    return 


"""  Determine the order of execution for cluster(), aggregate(),
     and distribute() based on their selected priorities.
"""
def sortFunctions():
    while (clusterPriority, aggregatePriority, distributePriority != 0):
        global functionList
        functionList.append(clusterPriority)
        functionList.append(aggregatePriority)
        functionList.append(distributePriority)
        global functionList2
        functionList2 = sorted(functionList)
        for i in functionList2:
            "".join([x for x in i if not x.isdigit()])
            vars() [i] = i
        x = [cluster, aggregate, distribute]
        break
    
    return





app = Tk()
app.title("GroupEng")
app.geometry("550x600+200+200")
sb = Scrollbar(app)
sb.pack(side="right", fill="y")

bar = TabBar(app)

####################  INTRO SCREEN ####################
""" Intro Screen """
tab0 = Tab(app, "Welcome to GroupEng")
buttonProject = Button(tab0, text = "New Project", width = 20, command = new)
buttonProject.pack(side =  'top', padx = 15)


### New Project Name ###
tab00 = Tab(app, "Name your Project")
""" Name of the project """
projectText = StringVar()
projectText.set("Name of your project:")
project1 = Label(tab00, textvariable = projectText)
project1.pack(expand = 1)

theName = StringVar(None)
projectName = Entry(tab00, textvariable = theName)
projectName.pack(expand = 1)

""" New rule file """
buttonNew = Button(tab00, text = "Continue", width = 20, command = write)
buttonNew.pack(side =  'top', padx = 15, pady = 15)


### Load Rule File ###
"""Existing Project """
buttonLoad = Button(tab0, text = "Existing Project", width = 20, command = existingProject)
buttonLoad.pack(side =  'top', padx = 15, pady = 15)



####################  TAB ONE (New Project) ####################
tab1 = Tab(app, "Basic Information")

""" Upload file """
uploadText = StringVar()
uploadText.set("Upload a list of students")
upload1 = Label(tab1, textvariable = uploadText, height = 3)
upload1.pack()

""" Uploaded File """
uploadText = StringVar()
uploadText.set("<No file selected>")
upload1 = Label(tab1, textvariable = uploadText, height = 3)
upload1.pack()

button0 = Button(tab1, text = "Browse", width = 20, command = uploadFile)
button0.pack(side =  'top', padx = 5, pady = 5)


""" Student Identifier """
idText = StringVar()
idText.set("Student Identifier: ")
idLabel = Label(tab1, textvariable = idText, height = 3)
idLabel.pack()

idMenu = StringVar()
idMenu.set("Select an option")
idFiles = display()
idDropDown = OptionMenu(tab1, idMenu, *idFiles)
idDropDown.pack(padx = 15)


""" Number of students per group """
labelText = StringVar()
labelText.set("Number of students per group:")
label1 = Label(tab1, textvariable = labelText, height = 4)
label1.pack()

custName = StringVar(None)
yourName = Entry(tab1, textvariable =custName)
yourName.pack()


""" Special Case: groups do not divide evenly """
labelText2 = StringVar()
labelText2.set("Some groups may not divide evenly." + "\n" + "\n" + "In that case, these groups will have:")
label2 = Label(tab1, textvariable = labelText2, height = 6)
label2.pack()

studFiles = StringVar()
studFiles.set("Select an option")
files = ["One extra student", "One less student"]
studDropDown = OptionMenu(tab1, studFiles, *files)
studDropDown.pack(padx = 15)

""" Save User Input """
buttonSave = Button(tab1, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tab1, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15)




####################  TAB 2 (New Project) ####################
tabCluster = Tab(app, "Cluster")
""" Cluster certain groups """
clusterText = StringVar()
clusterText.set("Cluster students based on:")
clusterLabel = Label(tabCluster, textvariable = clusterText, height = 3)
clusterLabel.pack()

clusterMenu = StringVar()
clusterMenu.set("Select an option")
clusterFiles = display()
clusterDropDown = OptionMenu(tabCluster, clusterMenu, *clusterFiles, command = displayValues)
clusterDropDown.pack(padx = 15)

cvText = StringVar()
cvText.set("Values:")
cvLabel = Label(tabCluster, textvariable = cvText)
cvLabel.pack()

clusterValues = StringVar()
clusterValues.set("Select an option")
cvFiles = ["value1","value2"]
cvDropDown = OptionMenu(tabCluster, clusterValues, *cvFiles)
cvDropDown.pack()

cpText = StringVar()
cpText.set("Priority:")
cpTextEntry = Label(tabCluster, textvariable = cpText)
cpTextEntry.pack()

cpMenu = StringVar()
cpMenu.set("Select an option")
cpfiles = [" ", 1, 2, 3]
cpDropDown = OptionMenu(tabCluster, cpMenu, *cpfiles, command = getcPriority)
cpDropDown.pack(padx = 15)

""" Save User Input """
buttonSave = Button(tabCluster, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabCluster, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabAggregate = Tab(app, "Aggregate")
"""Put students on the same project choice together."""
aggText = StringVar()
aggText.set("Aggregate students based on:")
aggLabel = Label(tabAggregate, textvariable = aggText, height = 3)
aggLabel.pack()

aggMenu = StringVar()
aggMenu.set("Select an option")
aggFiles = display()
aggDropDown = OptionMenu(tabAggregate, aggMenu, *aggFiles, command = displayAggValues)
aggDropDown.pack(padx = 15)

apText = StringVar()
apText.set("Priority:")
apTextEntry = Label(tabAggregate, textvariable = apText)
apTextEntry.pack()

apMenu = StringVar()
apMenu.set("Select an option")
apfiles = [" ", 1, 2, 3]
apDropDown = OptionMenu(tabAggregate, apMenu, *apfiles, command = getaPriority)
apDropDown.pack(padx = 15)

#### To change ###
#avText = StringVar()
#avText.set("Values:")
#avLabel = Label(tabAggregate, textvariable = avText)
#avLabel.pack()

#aggValues = StringVar()
#aggValues.set("Select an option")
#avFiles = ["value1","value2"]
#avDropDown = OptionMenu(tabAggregate, aggValues, *avFiles)
#avDropDown.pack()

""" Save User Input """
buttonSave = Button(tabAggregate, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabAggregate, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabDistribute = Tab(app, "Distribute")
""" Distribute certain groups """
disText = StringVar()
disText.set("Distribute students based on:")
disLabel = Label(tabDistribute, textvariable = disText, height = 3)
disLabel.pack()

disMenu = StringVar()
disMenu.set("Select an option")
disFiles = display()
disDropDown = OptionMenu(tabDistribute, disMenu, *disFiles, command = displayDisValues)
disDropDown.pack(padx = 15)

#### To change ####
dvText = StringVar()
dvText.set("Values:")
dvLabel = Label(tabDistribute, textvariable = dvText)
dvLabel.pack()

disValues = StringVar()
disValues.set("Select an option")
dvFiles = ["value1","value2"]
dvDropDown = OptionMenu(tabDistribute, disValues, *dvFiles)
dvDropDown.pack()

dpText = StringVar()
dpText.set("Priority:")
dpTextEntry = Label(tabDistribute, textvariable = dpText)
dpTextEntry.pack()

dpMenu = StringVar()
dpMenu.set("Select an option")
dpfiles = [" ", 1, 2, 3]
dpDropDown = OptionMenu(tabDistribute, dpMenu, *dpfiles, command = getdPriority)
dpDropDown.pack(padx = 15)


""" Save User Input """
buttonSave = Button(tabDistribute, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabDistribute, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)



############### TAB BALANCE (New Project) #########################
tabBalance = Tab(app, "Balance")
balanceText = StringVar()
balanceText.set("What would you like to balance?")
balanceLabel = Label(tabBalance, textvariable = balanceText)
balanceLabel.pack()

balanceMenu = StringVar()
balanceMenu.set("Select an option")
balanceFiles = display()
balanceDropDown = OptionMenu(tabBalance, balanceMenu, *balanceFiles)
balanceDropDown.pack()

""" Save User Input """
buttonSave = Button(tabBalance, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabBalance, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)





####################  TAB 3 (Existing Project) ####################
tab3 = Tab(app, "Basic Info")
""" Upload file """
uploadText2 = StringVar()
uploadText2.set("Upload a list of students")
upload1 = Label(tab3, textvariable = uploadText2, height = 3)
upload1.pack()


""" Uploaded File """
uploadText2 = StringVar()
uploadText2.set(loadClasslist())
upload1 = Label(tab3, textvariable = uploadText2, height = 3)
upload1.pack()

button0 = Button(tab3, text = "Change", width = 20, command = uploadFile)
button0.pack(side =  'top', padx = 5, pady = 5)

""" Student Identifier """
idText2 = StringVar()
idText2.set("Student Identifier: ")
idLabel2 = Label(tab3, textvariable = idText2, height = 3)
idLabel2.pack()

idMenu2 = StringVar()
idMenu2.set(loadIdentifier())
idFiles2 = display()
idDropDown = OptionMenu(tab3, idMenu2, *idFiles2)
idDropDown.pack(padx = 15)

""" Number of students per group """
labelText2 = StringVar()
labelText2.set("Number of students per group:")
label1 = Label(tab3, textvariable = labelText2, height = 4)
label1.pack()

custName2 = StringVar(None)
yourName2 = Entry(tab3, textvariable =custName2)
#yourName.insert(0, loadGroupSize())
yourName2.pack()

""" In case groups do not divide evenly """
labelText2 = StringVar()
labelText2.set("Some groups may not divide evenly." + "\n" + "\n"
               + "In that case, these groups will have:")
label2 = Label(tab3, textvariable = labelText2, height = 6)
label2.pack()

studFiles2 = StringVar()
studFiles2.set(loadSpecGroups())
files2 = ["One extra student", "One less student"]
studDropDown = OptionMenu(tab3, studFiles2, *files2)
studDropDown.pack(padx = 15)

""" Save User Input """
buttonSave = Button(tab3, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tab3, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15)




####################  TAB 4 (Existing Project) ####################
tabCluster2 = Tab(app, "Cluster2")
""" Cluster certain groups """
clusterText2 = StringVar()
clusterText2.set("Cluster students based on:")
clusterLabel2 = Label(tabCluster2, textvariable = clusterText2, height = 3)
clusterLabel2.pack()

clusterMenu2 = StringVar()
clusterMenu2.set(loadCluster())
clusterFiles2 = display()
clusterDropDown2 = OptionMenu(tabCluster2, clusterMenu2, *clusterFiles2, command = displayValues)
clusterDropDown2.pack(padx = 15)

cvText2 = StringVar()
cvText2.set("Values:")
cvLabel2 = Label(tabCluster2, textvariable = cvText2)
cvLabel2.pack()

clusterValues2 = StringVar()
clusterValues2.set(loadClusterValues())
cvFiles2 = ["value1", "value2"]
cvDropDown2 = OptionMenu(tabCluster2, clusterValues2, *cvFiles2)
cvDropDown2.pack()

cpText2 = StringVar()
cpText2.set("Priority:")
cpTextEntry2 = Label(tabCluster2, textvariable = cpText2)
cpTextEntry2.pack()

cpMenu2 = StringVar()
cpMenu2.set("Select an option")
cpfiles2 = [" ", 1, 2, 3]
cpDropDown2 = OptionMenu(tabCluster2, cpMenu2, *cpfiles2, command = getcPriority)
cpDropDown2.pack(padx = 15)

""" Save User Input """
buttonSave = Button(tabCluster2, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabCluster2, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabAggregate2 = Tab(app, "Aggregate2")
"""Put students on the same project choice together."""
aggText2 = StringVar()
aggText2.set("Aggregate students based on:")
aggLabel2 = Label(tabAggregate2, textvariable = aggText2, height = 3)
aggLabel2.pack()

aggMenu2 = StringVar()
aggMenu2.set(loadAggregate())
aggFiles = display()
aggDropDown = OptionMenu(tabAggregate2, aggMenu2, *aggFiles)
aggDropDown.pack(padx = 15)

#### To change ###
#avText2 = StringVar()
#avText2.set("Values:")
#avLabel2 = Label(tabAggregate2, textvariable = avText2)
#avLabel2.pack()

#aggValues2 = StringVar()
#aggValues2.set("Select an option")
#avFiles2 = ["value1","value2"]
#avDropDown2 = OptionMenu(tabAggregate2, aggValues2, *avFiles2)
#avDropDown2.pack()

apText2 = StringVar()
apText2.set("Priority:")
apTextEntry2 = Label(tabAggregate2, textvariable = apText2)
apTextEntry2.pack()

apMenu2 = StringVar()
apMenu2.set("Select an option")
apfiles2 = [" ", 1, 2, 3]
apDropDown2 = OptionMenu(tabAggregate2, apMenu2, *apfiles2, command = getaPriority)
apDropDown2.pack(padx = 15)

""" Save User Input """
buttonSave = Button(tabAggregate2, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabAggregate2, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabDistribute2 = Tab(app, "Distribute2")
""" Distribute certain groups """
disText2 = StringVar()
disText2.set("Distribute students based on:")
disLabel2 = Label(tabDistribute2, textvariable = disText2, height = 3)
disLabel2.pack()

disMenu2 = StringVar()
disMenu2.set(loadDistribute())
disFiles2 = display()
disDropDown2 = OptionMenu(tabDistribute2, disMenu2, *disFiles2, command = displayDisValues)
disDropDown2.pack(padx = 15)

#### To change ####
dvText2 = StringVar()
dvText2.set("Values:")
dvLabel2 = Label(tabDistribute2, textvariable = dvText)
dvLabel2.pack()

disValues2 = StringVar()
disValues2.set(loadDistributeValues())
dvFiles2 = ["value1","value2"]
dvDropDown2 = OptionMenu(tabDistribute2, disValues2, *dvFiles2)
dvDropDown2.pack()

dpText2 = StringVar()
dpText2.set("Priority:")
dpTextEntry2 = Label(tabDistribute2, textvariable = dpText2)
dpTextEntry2.pack()

dpMenu2 = StringVar()
dpMenu2.set("Select an option")
dpfiles2 = [" ", 1, 2, 3]
dpDropDown2 = OptionMenu(tabDistribute2, dpMenu2, *dpfiles2, command = getdPriority)
dpDropDown2.pack(padx = 15)

""" Save User Input """
buttonSave = Button(tabDistribute2, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabDistribute2, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)

tabBalance2 = Tab(app, "Balance2")
balanceText2 = StringVar()
balanceText2.set("What would you like to balance?")
balanceLabel2 = Label(tabBalance2, textvariable = balanceText2)
balanceLabel2.pack()

balanceMenu2 = StringVar()
balanceMenu2.set(loadBalance())
balanceFiles2 = display()
balanceDropDown2 = OptionMenu(tabBalance2, balanceMenu2, *balanceFiles2)
balanceDropDown2.pack()

""" Save User Input """
buttonSave = Button(tabBalance2, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabBalance2, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabTolerance = Tab(app, "Tolerance")

toleranceText = StringVar()
toleranceText.set("Tolerance:")
toleranceLabel = Label(tabTolerance, textvariable = toleranceText)
toleranceLabel.pack(expand = 1)

tValue = StringVar(None)
toleranceValue = Entry(tabTolerance, textvariable = tValue)
toleranceValue.pack(expand = 1)

""" Save User Input """
buttonSave = Button(tabTolerance, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabTolerance, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabTolerance2 = Tab(app, "Tolerance2")
toleranceText2 = StringVar()
toleranceText2.set("Tolerance:")
toleranceLabel2 = Label(tabTolerance2, textvariable = toleranceText2)
toleranceLabel2.pack(expand = 1)

tValue2 = StringVar(None)
toleranceValue2 = Entry(tabTolerance2, textvariable = tValue2)
toleranceValue2.pack(expand = 1)

""" Save User Input """
buttonSave = Button(tabTolerance2, text = "Save", width = 15, command = save)
buttonSave.pack(side = 'left', padx = 15, pady = 30)

""" Create Groups """
""" Precondition: All fields must be complete """
button1 = Button(tabTolerance2, text = "Create Groups", width = 15, command = groupEng)
button1.pack(side = 'right', padx = 15, pady = 30)


tabResults = Tab(app, "Results")
#frame = Frame(tabResults)
scrollbar = Scrollbar(tabResults, orient=VERTICAL)
listbox = Listbox(tabResults, height=30, width=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listbox.pack(side=LEFT, fill=BOTH, expand=1)

listbox.insert(END, "Student Groups")
f = open(os.path.join("groups_true_2014-08-27_22-09-07", "true_groups.txt"), "r")
for line in f:
    listbox.insert(END, line)
f.close()



bar.add(tab0)

bar.config(bd=2, relief=RIDGE)	

bar.show()
app.mainloop()
#baseFile()
