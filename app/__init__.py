# Team fourCoffeePeanuts: Ryan Wang (PM), Eliza Knapp, Yaying Liang Li, Jesse Xie
# SoftDev
# P00 -- Move Slowly and Fix Things

# setup
from os import urandom
from flask import Flask, render_template, request, redirect, session # flask imports
import sqlite3   #enable control of an sqlite database

app = Flask(__name__) #creates flask object

app.secret_key = urandom(32)

DB_FILE="walnutLatte.db"

db = sqlite3.connect(DB_FILE, check_same_thread=False) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

create = "CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, stories TEXT) " # create users table
c.execute((create))
create = "CREATE TABLE IF NOT EXISTS stories (name TEXT, latestUpdate TEXT, fullStory TEXT) " # create stories table
c.execute((create))

logged_in_user = ""

# renders the main page
@app.route("/")
def main_page():
    global logged_in_user
    if session.get(logged_in_user):
        return redirect("/dashboard")
    return render_template("main_page.html")

# create account site
@app.route("/create_account")
def create_account():
    if session.get(logged_in_user):
        return redirect("/dashboard")
    return render_template("login_create.html", create=True)

# handles submitting of create account
@app.route("/submit_create_account", methods=['GET', 'POST'])
def submit_create_account():
    global logged_in_user
    if session.get(logged_in_user):
        return redirect("/dashboard")
    try:
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            same_password = request.form.get("same_password")
            #get data from form
            c.execute("SELECT * FROM users")
            usersTable = c.fetchall()
            #fetch user table data from db file
            if username == '':
                return render_template("login_create.html", create=True, error="Your username cannot be blank")
            c.execute("SELECT * FROM users WHERE username = (?)", (username,))
            userFromDB = c.fetchall()
            # print(f"\n\nuserFromDB: {userFromDB}\n\n")
            if (len(userFromDB) > 0): #check if username is already in the users database
                return render_template("login_create.html", create=True, error="That username has already been taken")
                # if it is, return this username has been taken error
            elif password != same_password: # if it is not, check if the passwords match
                return render_template("login_create.html", create=True, error="The passwords do not match")
                # if they do not, return passwords do not match error
            elif password == '':
                return render_template("login_create.html", create=True, error="Your password cannot be blank")
            else:
                info = [username,password,""]
                addAccount = f"INSERT INTO users VALUES(?,?,?)" # if they do, add the entry to the database
                c.execute(addAccount,info) #add user data to table
                db.commit() #save changes

                # log them in right after creating account
                # finally!!! (so annoying before)
                c.execute("SELECT * FROM users WHERE username = (?)", (username,))
                userFromDB = c.fetchall()
                if (len(userFromDB) > 0): #check if username is in the users database
                    if (userFromDB[0][1] == password): #check if password is correct
                        logged_in_user = username
                        session[username] = password #add session
                        return redirect("/dashboard") #if everything works, log the user in successfully

    except:
        return render_template("login_create.html", create=True, error="Error!") # overall error catch

# login page
@app.route("/login")
def login():
    if session.get(logged_in_user):
        return redirect("/dashboard")
    return render_template("login_create.html", create=False)

# handles submitting of login
@app.route("/submit_login", methods=['GET', 'POST'])
def submit_login():
    global logged_in_user
    if session.get(logged_in_user):
        return redirect("/dashboard")
    try:
        if request.method == "POST":
            user = request.form.get("username") #get data from form
            passwd = request.form.get("password")

            c.execute("SELECT * FROM users WHERE username = (?)", (user,))
            userFromDB = c.fetchall()
            if (len(userFromDB) > 0): #check if user is in the users database
                if (userFromDB[0][1] == passwd): #check if password is correct
                    logged_in_user = user
                    session[user] = passwd #add session
                    return redirect("/dashboard") #if everything works, log the user in successfully
                else: #user exists, but password is wrong
                    return render_template("login_create.html", create=False, error="The password is incorrect") #call error fxn; indicate passwd is incorrect
            return render_template("login_create.html", create=False, error="That user does not exist") #call error fxn; indicate username is incorrect
        #only return this after checking all the usernames & confirming it doesn't exist

    except:
        return render_template("login_create.html", create=True, error="Error!")
        #overall catch for working site

#logout page
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    global logged_in_user
    if logged_in_user in session:
        session.pop(logged_in_user)
        logged_in_user = ""
    return render_template('main_page.html')

@app.route("/dashboard")
def dashboard():
    if not session.get(logged_in_user):
        # if session doesn't have the correct login info, i.e. you are not signed in
        return render_template('main_page.html')

    c.execute("SELECT stories FROM users WHERE username = (?)", (logged_in_user,))
    # this is only to create userStorieslist
    userStories = c.fetchall()
    # this list stores the titles of stories that user added/contributed
    # [title1, title2, title3]
    userStoriesList = list(userStories[0][0].split(","))

    # this is the number of titles
    num_stories = len(userStoriesList)
    # previously if userStoriesList == [''], num_stories == 1
    # this corrects that
    if (num_stories == 1) and (userStoriesList[0] == ''):
        num_stories = 0

    stories_list = []
    for story in userStoriesList:
        c.execute("SELECT * FROM stories where name = (?)", (story,))
        row = c.fetchall()
        stories_list.append(row)
    # to be clear the format of stories_list is as follows
    # [
    #     [(title1, latest1, fullstory1)],  # these are OF THE USER
    #     [(title2, latest2, fullstory2)],  # these are OF THE USER
    #     [(title3, latest3, fullstory3)],  # these are OF THE USER
    # ]
    # if empty it will look like [[]]

    #print(f"userStoriesList: {userStoriesList}\n")
    #print(f"num_stories: {num_stories}\n")
    #print(f"stories_list: {stories_list}\n")

    # this list stores the user,pass,titles info
    # and displays for debugging purposes
    c.execute("SELECT * FROM users")
    users_list = [line for line in c]

    # this list stores the titles,latest,full info
    # and displays for debugging purposes
    c.execute("SELECT * FROM stories")
    db_stories_list = [line for line in c]

    return render_template(
        "dashboard.html",
        username=logged_in_user,         # so we can see username when we log in
        num_stories=num_stories,         # num of stories the user has added/contributed to
        stories_list=stories_list,       # shows the tables user has added/contributed to
        db_stories_list=db_stories_list, # shows title,latest,full for debugging
        users_list=users_list,           # shows user,pass,titles for debugging
        )

@app.route("/create_story")
def create_story():
    if not session.get(logged_in_user):
        # if session doesn't have the correct login info, i.e. you are not signed in
        return render_template('main_page.html')
    return render_template("create_story.html")

@app.route("/submit_create_story", methods=['GET', 'POST'])
def submit_create_story():
    global logged_in_user
    if not session.get(logged_in_user):
        # if session doesn't have the correct login info, i.e. you are not signed in
        return render_template('main_page.html')
    # add the stuff to database
    if request.method == "POST":
        # current problem: it's not a post method but i don't know why

        # stores the info into handy variables to put into a tuple,
        # to insert into the stories stories in the DB
        title = request.form.get("title").strip() #remove whitespace at beginning and end
        story = request.form.get("story")
        latest_update = request.form.get("story")

        # check if the title is taken
        c.execute("SELECT * FROM stories WHERE lower(name) = (?)", (title.lower(),)) # case insensitive
        titleRepeats = c.fetchall()

        if (len(titleRepeats) > 0):
            return render_template("create_story.html", error="The name of the story is already taken", story=story)

        # adds the story info (title, story text) to the stories table in walnutLatte.db
        data_tuple = (title, latest_update, story)
        insert = """INSERT INTO stories
        (name, latestUpdate, fullStory)
        VALUES (?, ?, ?);"""
        c.execute(insert, data_tuple)

        # adds created story to stories column in users table
        c.execute("SELECT stories FROM users WHERE username = (?)", (logged_in_user,))
        storiesList = c.fetchall()
        if (storiesList[0][0] == ""):
            amendedStoriesList = (title)
        else:
            amendedStoriesList = (storiesList[0][0] + "," + title)
        editStoriesList = "UPDATE users SET stories = (?) WHERE username = (?)"
        c.execute(editStoriesList,(amendedStoriesList,logged_in_user))
        db.commit()

    # then go back to dashboard
    # TO DO: dashboard should now render the new story added to
    return redirect("/dashboard")

@app.route("/full_story", methods=['GET', 'POST'])
def full_story():
    global logged_in_user
    if not session.get(logged_in_user):
        return render_template('main_page.html')
    if request.method == "POST":
        # print("here")
        story_text = request.form.get("full_story")
        story_title = request.form.get("story_title")
        return render_template("full_story.html", title=story_title, story=story_text)
    else:
        return render_template("full_story.html", story="There seems to be a problem rendering the story")


def flat_clean(c_fetch_all_list):
    # c_fetch_all_list is a list of tuples, each tuple representing the stories of each user
    # the first element of each tuple is a comma-separated str of titles
    ''' returns a "flattened" set with no empty strings '''
    title_str = ""
    for line_tuple in c_fetch_all_list:
        title_str += line_tuple[0] + ","
    flat_list = title_str.split(",")
    # remove empty strings
    flat_list = [title for title in flat_list if title]
    # remove duplicates
    return list(set(flat_list))


def untouched():
    ''' returns a list of tuples of stories that the user has not added/contributed '''
    c.execute("SELECT stories FROM users WHERE username == (?)", (logged_in_user,))
    flat_logged_titles = flat_clean(c.fetchall()) #list of all stories that user has contributed to

    logged_title_str = "(" + ", ".join("'" + str(title) + "'" for title in flat_logged_titles) + ")"
    # this will look something like ('coffee', 'peanut') which is the format necessary for logged_title_str
    execute_str = f"SELECT * FROM stories WHERE name NOT IN {logged_title_str}"

    return c.execute(execute_str).fetchall() #list of tuples (name, latest, full) of all stories that were not touched by user 


@app.route("/see_stories")
def see_stories():
    global logged_in_user
    if not session.get(logged_in_user):
        return render_template('main_page.html')

    storiesList = untouched() 
    return render_template("see_stories.html", storiesList=storiesList)

@app.route("/search_see_stories", methods=['GET','POST'])
def search_see_stories():
    # put stories that match search criteria here
    if request.method == "POST":
        # search_stories must only include untouched stories
        untouched_titles = flat_clean(untouched())
        untouched_title_str = "(" + ", ".join("'" + str(title) + "'" for title in untouched_titles) + ")"

        # search_stories also needs to follow the search criterion
        searchWord = request.form.get("search") # get searchWord

        execute_str = f"SELECT * FROM stories WHERE name LIKE '%{searchWord}%' AND name IN {untouched_title_str}"
        searched_stories = c.execute(execute_str).fetchall()
        print(searched_stories)

        return render_template("see_stories.html", storiesList=searched_stories)
    else:
        return redirect("/dashboard")

@app.route("/edit_story", methods=['GET', 'POST'])
def edit_story():
    global logged_in_user
    if not session.get(logged_in_user):
        return render_template('main_page.html')
    if request.method == "POST":
        # print("here")
        story_title = request.form.get("story_title")
        story_preview = request.form.get("preview")
        c.execute("SELECT stories FROM users WHERE username = (?)", (logged_in_user,))
        # this is only to create userStorieslist
        userStories = c.fetchall()
        # this list stores the titles of stories that user added/contributed
        # [title1, title2, title3]
        userStoriesList = list(userStories[0][0].split(","))
        if userStoriesList.count(story_title) > 0:

            # if user has contributed already, and redirect to dashboard
            return redirect("/dashboard") # redirect to dashboard if user has contributed already
        return render_template("edit_story.html", title=story_title, story_preview=story_preview)
    else:
        return redirect("/dashboard")


@app.route("/submit_edit_story", methods=['GET', 'POST'])
def submit_edit_story():
    global logged_in_user
    if not session.get(logged_in_user):
        return render_template('main_page.html')
    if request.method == "POST":
        title = request.form.get("story_title")
        update = request.form.get("story")

        c.execute("SELECT * FROM stories WHERE name = (?)", (title,))
        story_row = c.fetchall() #gets the row with the title

        # replace latestUpdate
        # replace fullStory
        new_full_story = story_row[0][2] + update
        new_latest_update = update
        c.execute("UPDATE stories SET latestUpdate = (?), fullStory = (?) WHERE name = (?)", (new_latest_update, new_full_story, title))

        #finally, it has to add the title to the user's list
        c.execute("SELECT stories FROM users WHERE username = (?)",(logged_in_user,))
        all_stories = c.fetchall()[0][0]
        if (all_stories == ""):
            new_all_stories = (title)
        else:
            new_all_stories = (all_stories + "," + title)
        c.execute("UPDATE users SET stories = (?) WHERE username = (?)", (new_all_stories, logged_in_user))
        db.commit()

        return redirect("/dashboard") # now you go back to dashboard

    return redirect("/edit_story", error="something went wrong")


if __name__ == "__main__":
    app.debug = True
    app.run()
