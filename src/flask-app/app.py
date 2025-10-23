#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.get("/")
def home():
    """Render a simple profile form."""
    # Prefill from query args if present (optional UX)
    form = {
        "name": request.args.get("name", ""),
        "email": request.args.get("email", ""),
        "role": request.args.get("role", ""),
        "bio": request.args.get("bio", ""),
        "subscribe": request.args.get("subscribe", "") == "on",
    }
    return render_template("index.html", title="Profile Form", form=form, error=None)


@app.post("/submit")
def submit():
    """Handle form submission and redirect to landing page."""
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    role = request.form.get("role", "").strip()
    bio = request.form.get("bio", "").strip()
    subscribe = request.form.get("subscribe")  # 'on' if checked

    if not name:
        form = dict(request.form)
        form["subscribe"] = bool(request.form.get("subscribe"))
        return render_template(
            "index.html",
            title="Profile Form",
            form=form,
            error="Name is required",
        ), 400

    # PRG pattern: redirect with query string to avoid form resubmission
    return redirect(
        url_for(
            "welcome",
            name=name,
            email=email,
            role=role,
            bio=bio,
            subscribe="on" if subscribe else "",
        )
    )


@app.get("/welcome")
def welcome():
    """Landing page that displays submitted information."""
    data = {
        "name": request.args.get("name", ""),
        "email": request.args.get("email", ""),
        "role": request.args.get("role", ""),
        "bio": request.args.get("bio", ""),
        "subscribe": request.args.get("subscribe") == "on",
    }
    return render_template("welcome.html", title="Welcome", **data)


if __name__ == "__main__":
    app.run(debug=True)
