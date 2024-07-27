from flask import Flask, render_template, request, redirect, session, abort
from users import login, signup, edit_profile, get_user_id, get_user_by_username, get_profile_by_user_id
from messages import message, all_messages

def create_routes(app):
    @app.route("/")
    def index():
        if "username" not in session:
            return redirect("/login")

        messages = all_messages()
        return render_template("index.html", messages=messages)

    @app.route("/send", methods=["POST"])
    def send():
        subject = request.form.get("subject")
        message_content = request.form.get("message")
        user_id = session.get("user_id")

        if len(subject) > 20 or len(message_content) > 200:
            return render_template("index.html", error="Otsikko ei saa olla yli 20 merkkiä")
        if len(subject) > 200:
            return render_template("index.html", error="Viesti ei saa olla yli 200 merkkiä")

        if user_id and subject and message_content:
            message(user_id, subject, message_content)

        return redirect("/")

    @app.route("/profile/<username>")
    def profile(username):
        user_result = get_user_by_username(username)
        if not user_result:
            abort(404, description="Käyttäjää ei ole olemassa")

        profile_result = get_profile_by_user_id(user_result.id)
        if not profile_result:
            abort(404, description="Profiilia ei ole")

        return render_template("profile.html", user=user_result, profile=profile_result)

    @app.route("/profile/<username>/edit", methods=["GET", "POST"])
    def edit_profile_route(username):
        if request.method == "POST":
            age = request.form.get("age")
            hobbies = request.form.get("hobbies")
            about_me = request.form.get("about_me")
            user_id = session.get("user_id")

            if user_id:
                if edit_profile(user_id, age, hobbies, about_me):
                    return redirect(f"/profile/{username}")
                else:
                    return render_template("profile_edit.html", error="Profiilin päivitys epäonnistui")

        user_id = session.get("user_id")
        if not user_id:
            abort(403, description="Käyttäjä ei ole kirjautunut sisään")

        profile_result = get_profile_by_user_id(user_id)
        if not profile_result:
            return render_template("profile_edit.html", error="Profiilia ei löydy", profile=None)

        return render_template("profile_edit.html", profile=profile_result)

    @app.route("/login", methods=["GET", "POST"])
    def login_route():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if login(username, password):
                session["username"] = username
                session["user_id"] = get_user_id()
                return redirect("/")

            return render_template("login.html", error="Väärä käyttäjätunnus tai salasana")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop("username", None)
        session.pop("user_id", None)
        return redirect("/")

    @app.route("/signup", methods=["GET", "POST"])
    def signup_route():
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            age = int(request.form.get("age"))
            hobbies = request.form.get("hobbies")
            about_me = request.form.get("about_me")

            if len(username) < 4 or len(username) > 20:
                return render_template("signup.html", error="Käyttäjätunnuksen pitää olla 4-20 merkkiä")

            if len(password) < 8 or len(password) > 24:
                return render_template("signup.html", error="Salasanan pitää olla 8-24 merkkiä")
                
            if password != password_check:
                return render_template("signup.html", error="Salasanat eivät täsmää")
            
            if 0 <= age < 16 :
                return render_template("signup.html", error="Sinun tulee olla vähintään 16 luodaksesi tunnus")
            
            if age < 0 or age > 120:
                return render_template("signup.html", error="Syötä validi ikä")

            if signup(username, password, age, hobbies, about_me):
                session["username"] = username
                session["user_id"] = get_user_id()
                return redirect("/")

            return render_template("signup.html", error="Rekisteröinti epäonnistui")

        return render_template("signup.html")
