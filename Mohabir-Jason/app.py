from flask import Flask, render_template, request, redirect, url_for, session
import hashlib
import csv
app = Flask(__name__)    #create Flask object

@app.route("/")
@app.route("/login", methods=["POST"])
def disp_loginpage():
    print "\n\n\n\n"
    print "::DIAG:: this flsk obj"
    print app
    print "::DIAG:: this request obj"
    print request
    print "::DIAG:: request.headers"
    print request.headers
    print "::DIAG:: request.method"
    print request.method
    print "::DIAG:: request.args"
    print request.args 
    print "::DIAG:: request.form"
    print request.form
    return render_template("login.html")

@app.route("/auth", methods=['POST'])
def authenticate():
    inputtedUser = request.form['username']
    inputtedPass = request.form['password']
    inputtedTask = request.form['task']

    if inputtedTask == "register":

        accountInfo = csv.reader(open("data/info.csv"))
        for i in accountInfo:
            if inputtedUser == i[0]:
                return render_template("fail.html",
                                       title = "Failed Login", 
                                       text = "This username is already registered!")

        hashPass = hashlib.sha1()
        hashPass.update(inputtedPass)
        newInfo = inputtedUser + "," + hashPass.hexdigest()
        newLine = open("data/info.csv","a")
        newLine.write(newInfo)
        newLine.close

        return render_template("success.html",
                               title = "Account Creation Successful",
                               text = "A new account has been created for the user: " + inputtedUser)

    if inputtedTask == "login":
        accountInfo = csv.reader(open("data/info.csv"))
        for i in accountInfo:
            if inputtedUser == i[0]:
                hashPass = hashlib.sha1()
                hashPass.update(inputtedPass)
                if i[1] == hashPass.hexdigest():
                    session["user"] = inputtedUser
                    return render_template("success.html", 
                                           title = "Welcome to the Promise Land",
                                           text = "You have logged in successfully. Welcome: " + inputtedUser)
                else:
                    return render_template("fail.html",
                                           title = "Failed Login",
                                           text = "Your username or password were incorrect")

@app.route("/jacabo")
def js():
    #redirect(url_for("js"))
    return redirect("http://xkcd.com")



if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()

print "We are at the end"
