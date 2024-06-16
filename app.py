from itsdangerous import URLSafeTimedSerializer
from fastapi.encoders import jsonable_encoder
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from functools import wraps
from flask import (
    render_template,
    redirect,
    request,
    url_for,
    session,
    jsonify,
    Flask,
    flash,
)
import re
import os


app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123456@localhost/clinicdb"
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

with app.app_context():
    db.Model.metadata.reflect(db.engine)


class Doctor(db.Model):
    __table__ = db.metadata.tables["doctor"]


class User(db.Model):
    __table__ = db.metadata.tables["user"]


class Patient(db.Model):
    __table__ = db.metadata.tables["patient"]


class Appointment(db.Model):
    __table__ = db.metadata.tables["appointments"]


class Medicine(db.Model):
    __table__ = db.metadata.tables["medicines"]


class Speciality(db.Model):
    __table__ = db.metadata.tables["speciality"]


class Insurance(db.Model):
    __table__ = db.metadata.tables["insurance"]


app.config["MAIL_SERVER"] = "smtp-mail.outlook.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "usalclinic@hotmail.com"
app.config["MAIL_PASSWORD"] = "Uc_123456"
mail = Mail(app)

s = URLSafeTimedSerializer(app.secret_key)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("You need to log in first.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/forgotpassword", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(email, salt="password-reset-salt")
            reset_url = url_for("reset_password", token=token, _external=True)
            msg = Message(
                "Password Reset Request",
                sender="usalclinic@hotmail.com",
                recipients=[email],
            )
            msg.body = f"Please click the link to reset your password: {reset_url}"
            mail.send(msg)
            flash(
                "An email has been sent with instructions to reset your password.",
                "success",
            )
            return redirect(url_for("login"))
        else:
            flash("Email not found. Please check your email address.", "error")
            return redirect(url_for("forgot_password"))
    return render_template("forgot_password.html")


@app.route("/resetpassword/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = s.loads(token, salt="password-reset-salt", max_age=3600)
    except:
        flash("The password reset link is invalid or has expired.", "error")
        return redirect(url_for("forgot_password"))

    if request.method == "POST":
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("reset_password", token=token))

        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, "error")
            return redirect(url_for("reset_password", token=token))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User.query.filter_by(email=email).first()
        user.password = hashed_password
        db.session.commit()

        flash("Your password has been updated!", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html")


def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char in "!@#$%^&*()-_=+{}[]|:;<>?,./" for char in password):
        return False, "Password must contain at least one special character."
    return True, "Password is valid."


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
        if not user or not bcrypt.check_password_hash(user.password, password):
            flash("Username or password incorrect. Please try again.", "error")
            return redirect(url_for("login"))

        session["user_id"] = user.id
        session["username"] = user.username
        return redirect(url_for("homepage"))

    return render_template("login.html")


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False, "Invalid email format."
    return True, "Email is valid."


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash(
                "Username already exists. Please choose a different username.", "error"
            )
            return redirect(url_for("signup"))

        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("Email already exists. Please choose a different email.", "error")
            return redirect(url_for("signup"))

        is_valid, message = validate_email(email)
        if not is_valid:
            flash(message, "error")
            return redirect(url_for("signup"))

        is_valid, message = validate_password(password)
        if not is_valid:
            flash(message, "error")
            return redirect(url_for("signup"))

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully. You can now log in.", "success")
        return redirect(url_for("login"))

    return render_template("signup.html")


@app.route("/add_doctor", methods=["POST"])
def add_doctor():
    specialities = Speciality.query.all()
    if request.method == "POST":
        full_name = request.form["name"]
        phone = request.form["contact_nb"]
        emal = request.form["email"]
        specialit = request.form["speciality"]
        addess = request.form["address"]
        date_birth = request.form["dte_of_birth"]

        new_doctor = Doctor(
            name=full_name,
            contact_number=phone,
            email=emal,
            address=addess,
            speciality=specialit,
            date_of_birth=date_birth,
        )
        db.session.add(new_doctor)
        db.session.commit()

        doctors = Doctor.query.all()
        return render_template("doctor.html", dr=doctors, specialities=specialities)
    else:
        doctors = Doctor.query.all()
        return render_template("doctor.html", dr=doctors, specialities=specialities)


@app.route("/doctor", methods=["GET"])
@login_required
def doctor():
    specialities = Speciality.query.all()
    if request.method == "GET":
        doctors = Doctor.query.all()
        return render_template("doctor.html", dr=doctors, specialities=specialities)


@app.route("/delete_dr/<int:id>", methods=["POST"])
@login_required
def dlte_dr(id):
    if request.method == "POST":
        doctor = Doctor.query.get_or_404(id)
        db.session.delete(doctor)
        db.session.commit()
        doctors = Doctor.query.all()
        return render_template("doctor.html", dr=doctors)


@app.route("/update_dr_button/<int:id>", methods=["GET"])
@login_required
def updt_dr_btn(id):
    specialities = Speciality.query.all()
    if request.method == "GET":
        doctor = Doctor.query.get_or_404(id)
        return render_template("update_dr.html", x=doctor, specialities=specialities)


@app.route("/update_doctor/<int:id>", methods=["POST"])
@login_required
def updt_doctor(id):
    if request.method == "POST":
        doctor = Doctor.query.get_or_404(id)

        doctor.name = request.form["name"]
        doctor.contact_number = request.form["contact_nb"]
        doctor.email = request.form["email"]
        doctor.speciality = request.form["speciality"]
        doctor.address = request.form["address"]
        doctor.date_of_birth = request.form["dte_of_birth"]

        db.session.commit()

        doctors = Doctor.query.all()
        return render_template("doctor.html", dr=doctors)


@app.route("/patient", methods=["GET"])
@login_required
def patient():
    if request.method == "GET":
        patients = Patient.query.all()
        return render_template("patient.html", pt=patients)


@app.route("/add_patient", methods=["POST"])
def add_patient():
    if request.method == "POST":

        full_name = request.form["Name"]
        gndr = request.form["Gender"]
        bld = request.form["bld_type"]
        rlgn = request.form["Religion"]
        date_birth = request.form["dte_birth"]
        nation = request.form["nationality"]
        adres = request.form["Address"]
        phn_nb = request.form["phn_nb"]
        emal = request.form["email"]
        prfn = request.form["Profession"]
        g_nme = request.form["Garantor_name"]

        new_patient = Patient(
            name=full_name,
            gender=gndr,
            blood_type=bld,
            religion=rlgn,
            date_of_birth=date_birth,
            nationality=nation,
            address=adres,
            phone_number=phn_nb,
            email=emal,
            profession=prfn,
            garantor_name=g_nme,
        )
        db.session.add(new_patient)
        db.session.commit()

        patients = Patient.query.all()
        return render_template("patient.html", pt=patients)
    else:
        patients = Patient.query.all()
        return render_template("patient.html", pt=patients)


@app.route("/delete_pt/<int:id>", methods=["POST"])
@login_required
def dlte_pt(id):
    try:
        patient = Patient.query.get_or_404(id)
        related_appointments = Appointment.query.filter_by(patient_id=id).all()

        if related_appointments:
            return redirect(url_for("patient"))

        db.session.delete(patient)
        db.session.commit()
    except Exception as e:
        db.session.rollback()

    patients = Patient.query.all()
    return render_template("patient.html", pt=patients)


@app.route("/update_pt_button/<int:id>", methods=["GET"])
@login_required
def updt_pt_btn(id):
    if request.method == "GET":
        patient = Patient.query.get_or_404(id)
        return render_template("update_pt.html", p=patient)


@app.route("/update_patient/<int:id>", methods=["POST"])
@login_required
def updt_patient(id):
    if request.method == "POST":
        patient = Patient.query.get_or_404(id)

        patient.name = request.form["Name"]
        patient.gender = request.form["Gender"]
        patient.blood_type = request.form["bld_type"]
        patient.religion = request.form["Religion"]
        patient.date_of_birth = request.form["dte_birth"]
        patient.nationality = request.form["nationality"]
        patient.address = request.form["Address"]
        patient.phone_number = request.form["phn_nb"]
        patient.email = request.form["email"]
        patient.profession = request.form["Profession"]
        patient.garantor_name = request.form["Garantor_name"]

        db.session.commit()

        patients = Patient.query.all()
        return render_template("patient.html", pt=patients)


@app.route("/appointment", methods=["GET"])
@login_required
def appointment():
    if request.method == "GET":
        patients = Patient.query.all()
        doctors = Doctor.query.all()
        appointment = Appointment.query.all()
        return render_template(
            "appointment.html", dr=doctors, appt=appointment, pts=patients
        )


@app.route("/add_appt", methods=["POST", "GET"])
@login_required
def add_appt():
    if request.method == "POST":
        patients_id = request.form["patients_id"]
        patients_name = request.form["patients_name"]
        patients_phone_nb = request.form["patients_phone_nb"]
        patients_email = request.form["patients_email"]
        Doctor_ID = request.form["Doctor_ID"]
        doctors_name = request.form["doctors_name"]
        dr_phone_nb = request.form["dr_phone_nb"]
        date = request.form["date"]

        new_appointment = Appointment(
            patient_id=patients_id,
            patient_name=patients_name,
            patient_contact_number=patients_phone_nb,
            patient_email=patients_email,
            doctor_id=Doctor_ID,
            doctor_name=doctors_name,
            doctor_contact_number=dr_phone_nb,
            appointment_date=date,
        )
        db.session.add(new_appointment)
        db.session.commit()

        patients = Patient.query.all()
        doctors = Doctor.query.all()
        appointment = Appointment.query.all()
        return render_template(
            "appointment.html", dr=doctors, appt=appointment, pts=patients
        )


@app.route("/add_appt_on_pt/<int:id>", methods=["POST", "GET"])
@login_required
def add_appt_onPT(id):
    if request.method == "GET":
        patient = Patient.query.get_or_404(id)
        patients = Patient.query.all()
        doctors = Doctor.query.all()
        appointment = Appointment.query.all()
        return render_template(
            "appointment.html", pt=patient, dr=doctors, appt=appointment, pts=patients
        )


@app.route("/delete_appt/<int:id>", methods=["POST"])
@login_required
def dlte_appt(id):
    if request.method == "POST":
        appointment = Appointment.query.get_or_404(id)
        db.session.delete(appointment)
        db.session.commit()

        patients = Patient.query.all()
        doctors = Doctor.query.all()
        appointments = Appointment.query.all()
        return render_template(
            "appointment.html", appt=appointments, dr=doctors, pts=patients
        )


@app.route("/update_appt_button/<int:id>", methods=["GET"])
@login_required
def updt_appt_btn(id):
    if request.method == "GET":
        appointment = Appointment.query.get_or_404(id)
        doctors = Doctor.query.all()
        patients = Patient.query.all()
        return render_template(
            "update_appt.html", a=appointment, dr=doctors, pts=patients
        )


@app.route("/update_appt/<int:id>", methods=["POST", "GET"])
@login_required
def updt_appt(id):
    if request.method == "POST":
        appointment = Appointment.query.get_or_404(id)

        appointment.patient_id = request.form["patients_id"]
        appointment.patient_name = request.form["patients_name"]
        appointment.patient_contact_number = request.form["patients_phone_nb"]
        appointment.patient_email = request.form["patients_email"]
        appointment.doctor_id = request.form["Doctor_ID"]
        appointment.doctor_name = request.form["doctors_name"]
        appointment.doctor_contact_number = request.form["dr_phone_nb"]
        appointment.appointment_date = request.form["date"]

        db.session.commit()

        patients = Patient.query.all()
        doctors = Doctor.query.all()
        appointment = Appointment.query.all()
        return render_template(
            "appointment.html", dr=doctors, appt=appointment, pts=patients
        )


@app.route("/home")
@login_required
def homepage():
    logged_in_user = session.get("username")
    doctors_count = Doctor.query.count()
    patients_count = Patient.query.count()
    appointments_count = Appointment.query.count()
    users_count = User.query.count()
    return render_template(
        "homePage.html",
        doctors_count=doctors_count,
        patients_count=patients_count,
        appointments_count=appointments_count,
        logged_in_user=logged_in_user,
        users_count=users_count,
    )


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))


@app.route("/api/insurance_rend", methods=["GET"])
def get_insurance():
    return render_template("insurance.html")


@app.route("/api/medicines_rend", methods=["GET"])
def get_medicines():
    return render_template("medicines.html")


@app.route("/api/specialities_rend", methods=["GET"])
def get_specialities():
    return render_template("speciality.html")


@app.route("/api/all_medicines", methods=["GET"])
def get_all_medicines():
    medicines = Medicine.query.all()
    return jsonable_encoder(medicines)


@app.route("/api/medicines/<int:id>", methods=["GET"])
def get_medicine(id):
    med = Medicine.query.get_or_404(id)
    return jsonable_encoder(med)


@app.route("/api/add_medicines", methods=["POST"])
def add_medicine():
    new_medicine = Medicine(
        medicine_name=request.json["medicine_name"],
        manufacturer=request.json["manufacturer"],
        price=request.json["price"],
        expiration_date=request.json["expiration_date"],
    )
    db.session.add(new_medicine)
    db.session.commit()
    return (jsonable_encoder(new_medicine), 201)


@app.route("/api/delete_medicines/<int:id>", methods=["DELETE"])
def delete_medicine(id):
    medicine = Medicine.query.get_or_404(id)
    db.session.delete(medicine)
    db.session.commit()
    return jsonify({"message": "delete success"}), 200


@app.route("/api/update_medicines/<int:id>", methods=["PUT"])
def update_medicine(id):
    medicine = Medicine.query.get_or_404(id)
    medicine.medicine_name = request.json["medicine_name"]
    medicine.manufacturer = request.json["manufacturer"]
    medicine.price = request.json["price"]
    medicine.expiration_date = request.json["expiration_date"]
    db.session.commit()
    return jsonify({"message": "update success"}), 200


@app.route("/api/all_specialities", methods=["GET"])
def get_all_specialities():
    specialities = Speciality.query.all()
    return jsonable_encoder(specialities)


@app.route("/api/specialities/<int:id>", methods=["GET"])
def get_speciality(id):
    spec = Speciality.query.get_or_404(id)
    return jsonable_encoder(spec)


@app.route("/api/add_specialities", methods=["POST"])
def add_speciality():
    new_speciality = Speciality(
        speciality_name=request.json["speciality_name"],
        description=request.json["description"],
    )
    db.session.add(new_speciality)
    db.session.commit()
    return jsonable_encoder(new_speciality), 201


@app.route("/api/delete_specialities/<int:id>", methods=["DELETE"])
def delete_speciality(id):
    speciality = Speciality.query.get_or_404(id)
    db.session.delete(speciality)
    db.session.commit()
    return jsonify({"message": "delete success"}), 200


@app.route("/api/update_specialities/<int:id>", methods=["PUT"])
def update_speciality(id):
    speciality = Speciality.query.get_or_404(id)
    speciality.speciality_name = request.json["speciality_name"]
    speciality.description = request.json["description"]
    db.session.commit()
    return jsonify({"message": "update success"}), 200


@app.route("/api/all_insurances", methods=["GET"])
def get_all_insurances():
    insurances = Insurance.query.all()
    return jsonable_encoder(insurances)


@app.route("/api/insurance/<int:id>", methods=["GET"])
def get_ins(id):
    ins = Insurance.query.get_or_404(id)
    return jsonable_encoder(ins)


@app.route("/api/add_insurances", methods=["POST"])
def add_insurance():
    new_insurance = Insurance(
        insurance_name=request.json["insurance_name"],
        coverage_details=request.json["coverage_details"],
        contact_number=request.json["contact_number"],
        address=request.json["address"],
    )
    db.session.add(new_insurance)
    db.session.commit()
    return jsonable_encoder(new_insurance), 201


@app.route("/api/delete_insurances/<int:id>", methods=["DELETE"])
def delete_insurance(id):
    insurance = Insurance.query.get_or_404(id)
    db.session.delete(insurance)
    db.session.commit()
    return jsonify({"message": "delete success"}), 200


@app.route("/api/update_insurances/<int:id>", methods=["PUT"])
def update_insurance(id):
    insurance = Insurance.query.get_or_404(id)
    insurance.insurance_name = request.json["insurance_name"]
    insurance.coverage_details = request.json["coverage_details"]
    insurance.contact_number = request.json["contact_number"]
    insurance.address = request.json["address"]
    db.session.commit()
    return jsonify({"message": "update success"}), 200


if __name__ == "__main__":
    app.run(debug=True)
