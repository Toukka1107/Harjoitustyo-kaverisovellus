from flask import Flask, render_template, request, redirect, session, abort
from users import login, signup, edit_profile, get_user_id, get_user_by_username, get_profile_by_user_id, get_username, check_username
from messages import add_message, all_messages, add_comment
from friends import send_request, add_friends, delete_friend_request, get_friend_request, get_all_friend_requests, get_all_friends, check_friend_request, check_friendship, delete_friend

def create_routes(app):
    @app.route("/")
    def index():
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login")

        messages = all_messages()
        for message in messages:
            message['friend'] = check_friendship(user_id, message['user_id'])

        return render_template("index.html", messages=messages)

    @app.route("/send", methods=["POST"])
    def send():
        subject = request.form.get("subject")
        message_content = request.form.get("message")
        user_id = session.get("user_id")
        errors = []

        if len(subject) > 20:
            errors.append("Otsikko ei saa olla yli 20 merkkiä")
        if len(message_content) > 800:
            errors.append("Viesti ei saa olla yli 800 merkkiä")

        if errors:
            messages = all_messages()
            for message in messages:
                message['friend'] = check_friendship(user_id, message['user_id'])
            return render_template("index.html", errors=errors, messages=messages)

        if user_id and subject and message_content:
            add_message(user_id, subject, message_content)

        return redirect("/")
    
    @app.route("/comment", methods=["POST"])
    def comment():
        comment_content = request.form.get("comment")
        user_id = session.get("user_id")
        message_id = request.form.get("message_id")
        errors = []

        if len(comment_content) > 800:
            messages = all_messages()
            for message in messages:
                message['friend'] = check_friendship(user_id, message['user_id'])
            errors.append("Kommentti ei saa olla yli 800 merkkiä")
            return render_template("index.html", errors=errors, messages=messages)

        if user_id and comment_content:
            add_comment(user_id, message_id, comment_content)

        return redirect("/")
    
    @app.route("/profile/<username>")
    def profile(username):
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login")

        user_result = get_user_by_username(username)
        if not user_result:
            return abort(403, "Käyttäjää ei löydy")

        profile_result = get_profile_by_user_id(user_result)
        friends = check_friendship(user_id, user_result)
        friend_request = check_friend_request(user_id, user_result)

        return render_template(
            "profile.html", 
            username=username,
            profile=profile_result, 
            friends=friends, 
            friend_request=friend_request, 
            user={"id": user_result})

    @app.route("/profile/<username>/edit", methods=["GET", "POST"])
    def edit_profile_route(username):
        user_id = session.get("user_id")
        if not user_id:
            abort(403, description="Käyttäjä ei ole kirjautunut sisään")

        profile_result = get_profile_by_user_id(user_id)
        if not profile_result:
            return render_template("profile_edit.html", error="Profiilia ei löydy", profile=None)

        if request.method == "POST":
            age = request.form.get("age")
            hobbies = request.form.get("hobbies")
            about_me = request.form.get("about_me")
            avatar = request.form.get("avatar") + ".png"
            errors = []

            if int(age) < 16:
                errors.append("Sinun tulee olla vähintään 16-vuotias")
                    
            if int(age) < 0 or int(age) > 120:
                errors.append("Syötä validi ikä")
            
            if len(hobbies) > 200:
                errors.append("'Harrastukset' - maksimipituus ylitetty")
            
            if len(about_me) > 800:
                errors.append("'Minusta' - maksimipituus ylitetty")
            
            if errors:
                return render_template("profile_edit.html", profile=profile_result, errors=errors)
            else:
                edit_profile(user_id, age, hobbies, about_me, avatar)
                return redirect(f"/profile/{username}")

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
            password_check = request.form.get("password_check")
            age = request.form.get("age")
            hobbies = request.form.get("hobbies")
            about_me = request.form.get("about_me")
            avatar = request.form.get("avatar") + ".png"
            errors = []

            if check_username(username):
                errors.append("Käyttäjätunnus on jo käytössä")

            if len(username) < 4 or len(username) > 20:
                errors.append("Käyttäjätunnuksen pitää olla 4-20 merkkiä")
            
            if len(password) < 8 or len(password) > 24:
                errors.append("Salasanan pitää olla 8-24 merkkiä")
            
            if password != password_check:
                errors.append("Salasanat eivät täsmää")
            
            if int(age) < 16:
                errors.append("Sinun tulee olla vähintään 16 luodaksesi tunnus")
            
            if int(age) < 0 or int(age) > 120:
                errors.append("Syötä validi ikä")
            
            if len(hobbies) > 200:
                errors.append("'Harrastukset' - maksimipituus ylitetty")
            
            if len(about_me) > 800:
                errors.append("'Minusta' - maksimipituus ylitetty")
            
            if errors:
                return render_template("signup.html", errors=errors)

            else: 
                signup(username, password, age, hobbies, about_me, avatar)
                session["username"] = username
                session["user_id"] = get_user_id()
                return redirect("/")


        return render_template("signup.html")

    @app.route("/friends")
    def friends_route():
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login")
        
        requests = get_all_friend_requests(user_id)
        friends = get_all_friends(user_id)

        return render_template("friends.html", requests=requests, friends=friends)
        
    @app.route("/send_friend_request/<friend_id>", methods=["POST"])
    def send_friend_request(friend_id):
        user_id = session.get("user_id")
        profile_username = get_username(friend_id)
        if not user_id:
            return redirect("/login")

        if not friend_id:
            return redirect("/profile/{{ session['username'] }}", error="Virheellinen kaveripyyntö")

        if send_request(user_id, friend_id):
            return redirect(f"/profile/{profile_username}")
        else:
            return render_template("profile.html", error="Kaveripyyntöä ei voitu lähettää")
        
    @app.route("/end_friendship/<friend_id>", methods=["POST"])
    def end_friendship(friend_id):
        user_id = session.get("user_id")
        profile_username = get_username(friend_id)
        if not user_id:
            return redirect("/login")

        if not friend_id:
            return redirect("/profile/{{ session['username'] }}", error="Virheellinen kavereista poisto")

        if delete_friend(user_id, friend_id):
            return redirect(f"/profile/{profile_username}")
        else:
            return render_template("profile.html", error="Käyttäjää ei voitu poistaa kavereista")

    @app.route("/accept_friend_request/<request_username>", methods=["POST"])
    def accept_friend_request(request_username):
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login")

        friend_id = get_user_by_username(request_username)
        if not friend_id:
            return render_template("friends.html", error="Käyttäjää ei löydy")

        add_friends(user_id, friend_id)
        return redirect("/friends")


    @app.route("/decline_friend_request/<request_username>", methods=["POST"])
    def decline_friend_request(request_username):
        user_id = session.get("user_id")
        if not user_id:
            return redirect("/login")
        
        friend_id = get_user_by_username(request_username)
        delete_friend_request(friend_id, user_id)
        return redirect("/friends")
