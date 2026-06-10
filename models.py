from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    student_name = db.Column(db.String(100))
    parent_name = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    class_name = db.Column(db.String(50))

    school_name = db.Column(db.String(150))

    course = db.Column(db.String(100))

    message = db.Column(db.Text)

    def __repr__(self):
        return f"<Enquiry {self.student_name}>"