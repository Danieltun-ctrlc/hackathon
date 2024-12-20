from flask import Flask, render_template, request, redirect, url_for

from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length  # pip install email-validator
from flask_bootstrap import Bootstrap5  # pip install bootstrap-flask

log = False
login_userp = []
point = ''

app = Flask(__name__)
app.secret_key = "any-string-you-want-just-keep-it-secret"
bootstrap = Bootstrap5(app)


@app.route("/")
def home():
    return render_template('home.html', log=log, acc=login_userp)


@app.route("/requests", methods=["GET", 'POST'])
def requestp():
    with open("requests", ) as file:
        requestst = file.readlines()
        re_list = []
        for request_ in requestst:
            one = request_.split(",")
            print(one)
            if one[0] != "\n":
                if one[4][-1] == "\n":
                    one[4] = one[4][:-1]
                if one[2] == 't':
                    one[2] = True
                else:
                    one[2] = False
                one[0] = int(one[0])

                re_list.append(one)
    with open("users") as filet:
        con = filet.readlines()
        re_do = []
        for c in con:
            ind = c.split(",")
            if ind[0] != "\n":
                if ind[2][-1] == "\n":
                    ind[2] = ind[2][:-1]

                re_do.append(ind)

        print("helo")
        print(re_do)
        global point
        if len(login_userp) == 0:
            point = "login first"
        else:

            for do in re_do:
                if do[0] == login_userp[0]:
                    point = do[2]

    if request.method == 'POST':
        topic = request.form.get("topic")
        message = request.form.get("status")
        if not log:
            return render_template("requests.html", rp=re_list, log=log, acc=login_userp, po=point)
        else:

            with open("requests", ) as file:
                requestst = file.readlines()
                number = len(requestst) + 1
            with open('requests', 'a') as file2:

                file2.write(f"{number},{login_userp[0]},f,{topic},{message}" + "\n")

            return redirect(url_for("requestp"))
    else:

        return render_template("requests.html", rp=re_list, log=log, acc=login_userp, po=point)


@app.route("/re/<id>", methods=["GET", 'POST'])
def sub(id):
    if request.method == "POST":
        new = []
        if not log:
            pass
        else:
            with open("requests", ) as file_:
                content = file_.readlines()
                for value in content:
                    i = value.split(",")
                    if i[0] != "\n":
                        if i[4][-1] == "\n":
                            i[4] = i[4][:-1]
                        if i[0] == id:
                            i[2] = "t"
                        large = ",".join(i)
                        new.append(large)

            big_string = "\n".join(new)
            print(big_string)
            with open("requests", "w") as file_:
                file_.write(big_string)
            with open("users") as fileq:
                lists = []
                contents = fileq.readlines()
                for value in contents:
                    k = value.split(",")
                    if k[0] != "\n":
                        if k[2][-1] == '\n':
                            k[2] = k[2][:-1]
                        if login_userp[0] == k[0]:
                            k[2] = str(int(k[2]) + 10)
                        print(k)
                        final = ",".join(k)
                        lists.append(final)
            print(lists)

            big_string2 = "\n".join(lists)
            print(big_string2)
            with open("users", "w") as file_:
                file_.write(big_string2)

        return redirect(url_for('requestp'))


@app.route("/signup", methods=["GET", 'POST'])
def signing():
    if request.method == "POST":
        return render_template("signup.html")


@app.route("/sign", methods=["GET", 'POST'])
def sign_():
    already = False
    if request.method == "POST":

        user = request.form.get("username")
        password = (request.form.get("password"))
        emails = []
        with open("users") as file:
            contents = file.readlines()
            print(contents)
            for value in contents:
                j = value.split(",")
                print(j)
                emails.append(j[0])
            print(emails)
            if user in emails:
                already = True
                return render_template("signup.html", valid=already)
            else:
                with open('users', 'a') as file2:
                    file2.write("\n" + f"{user},{password},0")

                return redirect(url_for("login"))
    else:
        return render_template("signup.html", valid=already)


@app.route("/login", methods=["GET", 'POST'])
def login():
    if request.method == "POST":
        return render_template("login.html", passw=True, re=True)
    else:
        return render_template("login.html", passw=True, re=True)


@app.route("/logining", methods=["GET", 'POST'])
def logining_():
    if request.method == "POST":

        user = request.form.get("username")
        password = (request.form.get("password"))
        with open("users", ) as file_:
            final = []
            content = file_.readlines()
            for value in content:
                i = value.split(",")
                print(i)
                if i[0] != "\n":
                    if i[2][-1] == "\n":
                        i[2] = i[2][:-1]

                    final.append(i)
            print(final)
        for pair in final:
            if pair[0] == user:
                if pair[1] == password:
                    global log
                    log = True
                    global login_userp
                    login_userp = pair
                    print(login_userp)
                    return redirect(url_for("home"))
                else:
                    return render_template("login.html", passw=False, re=True)
        return render_template("login.html", passw=True, re=False)


with open("requests", ) as file:
    print(file.readlines())


@app.route("/events", methods=["GET", "POST"])
def event():
    with open("events", ) as file:
        event = file.readlines()
        re_list = []
        for request_ in event:
            one = request_.split(",")
            print(one)
            if one[0] != "\n":
                if one[2][-1] == "\n":
                    one[2] = one[2][:-1]

                re_list.append(one)
            print(re_list)
    if request.method == 'POST':
        topic = request.form.get("topic")
        message = request.form.get("status")
        if not log:
            return render_template("mem.html", rp=re_list, log=log, acc=login_userp)
        else:

            with open('events', 'a') as file2:

                file2.write(f"{login_userp[0]},{topic},{message}" + "\n")

            return redirect(url_for("event"))
    else:

        return render_template("mem.html", log=log, acc=login_userp, rp=re_list)


@app.route("/feature")
def feat():
    return render_template("ft.html", acc=login_userp, log=log)


@app.route("/Gifts")
def gift():
    with open("users") as filet:
        con = filet.readlines()
        re_do = []
        for c in con:
            ind = c.split(",")
            if ind[0] != "\n":
                if ind[2][-1] == "\n":
                    ind[2] = ind[2][:-1]

                re_do.append(ind)

        print("helo")
        print(re_do)
        global point
        if len(login_userp) == 0:
            point = "login first"
        else:

            for do in re_do:
                if do[0] == login_userp[0]:
                    point = do[2]
    return render_template("gifts.html", acc=login_userp, log=log, po=point)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
