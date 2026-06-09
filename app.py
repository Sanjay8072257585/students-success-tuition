from flask import Flask, render_template, redirect, url_for, request, session, send_file
import pandas as pd

from config import Config
from models import db, Enquiry

app = Flask(__name__)

# Secret Key
app.secret_key = "sstc2026"

# Load Configuration
app.config.from_object(Config)

# Initialize Database
db.init_app(app)

# Create Database Tables
with app.app_context():
    db.create_all()


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# ABOUT PAGE
# =========================
@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# COURSES PAGE
# =========================
@app.route("/courses")
def courses():
    return render_template("courses.html")


# =========================
# CONTACT PAGE
# =========================
@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================
# ENQUIRY PAGE
# =========================
@app.route("/enquiry", methods=["GET", "POST"])
def enquiry():

    if request.method == "POST":

        new_enquiry = Enquiry(
            student_name=request.form["student_name"],
            phone=request.form["phone"],
            class_name=request.form["class_name"],
            course=request.form["course"],
            message=request.form["message"]
        )

        db.session.add(new_enquiry)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("enquiry.html")


# =========================
# ADMIN LOGIN
# =========================
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    error = None

    if request.method == "POST":

        password = request.form["password"]

        if password == "admin123":
            session["admin"] = True
            return redirect(url_for("admin"))
        else:
            error = "Invalid Password"

    return render_template(
        "admin_login.html",
        error=error
    )


# =========================
# ADMIN LOGOUT
# =========================
@app.route("/logout")
def logout():

    session.pop("admin", None)

    return redirect(url_for("home"))


# =========================
# ADMIN DASHBOARD
# =========================
@app.route("/admin")
def admin():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    search = request.args.get("search", "")

    if search:
        enquiries = Enquiry.query.filter(
            Enquiry.student_name.contains(search)
        ).all()
    else:
        enquiries = Enquiry.query.all()

    return render_template(
        "admin.html",
        enquiries=enquiries
    )


# =========================
# DELETE ENQUIRY
# =========================
@app.route("/delete-enquiry/<int:id>")
def delete_enquiry(id):

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    enquiry = Enquiry.query.get_or_404(id)

    db.session.delete(enquiry)
    db.session.commit()

    return redirect(url_for("admin"))


# =========================
# DOWNLOAD EXCEL
# =========================
@app.route("/download-excel")
def download_excel():

    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    enquiries = Enquiry.query.all()

    data = []

    for enquiry in enquiries:
        data.append({
            "ID": enquiry.id,
            "Student Name": enquiry.student_name,
            "Phone": enquiry.phone,
            "Class": enquiry.class_name,
            "Course": enquiry.course,
            "Message": enquiry.message
        })

    df = pd.DataFrame(data)

    file_name = "enquiries.xlsx"

    df.to_excel(file_name, index=False)

    return send_file(
        file_name,
        as_attachment=True
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)