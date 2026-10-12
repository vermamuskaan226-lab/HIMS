# ============================================================
# HIMS BACKEND - Database, validation, business logic
# Frontend/UI is in frontend.py
# ============================================================

from pathlib import Path # Operating system with path 
import sqlite3 # for database
import uuid # unique id generator 
from datetime import datetime, date # date and time 
import pandas as pd # extraction , cleaning , visualization ,....

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "hims.db"

# DATABASE
# ============================================================

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id TEXT PRIMARY KEY,
            doctor_name TEXT NOT NULL,
            department TEXT NOT NULL,
            specialty TEXT,
            room TEXT,
            password TEXT DEFAULT '1234'
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            fullname TEXT,
            dob TEXT,
            age INTEGER,
            gender TEXT,
            marital_status TEXT,
            mobile TEXT,
            email TEXT,
            aadhaar TEXT,
            address TEXT,
            area TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            blood_group TEXT,
            emergency_name TEXT,
            emergency_number TEXT,
            symptoms TEXT,
            symptom_duration TEXT,
            current_condition TEXT,
            allergies TEXT,
            previous_surgery TEXT,
            family_history TEXT,
            has_insurance TEXT,
            insurance_provider TEXT,
            policy_number TEXT,
            insurance_validity TEXT,
            department TEXT,
            preferred_doctor TEXT,
            appointment_date TEXT,
            appointment_time TEXT,
            created_at TEXT
        )
    """)

    doctors = [
        ("RAK001", "Dr. Rakesh", "Cardiology", "Cardiologist", "Room 101", "1234"),
        ("MAD001", "Dr. Madan", "Physiology", "Physician", "Room 102", "1234"),
        ("PRI001", "Dr. Priya", "Dermatology", "Dermatologist", "Room 103", "1234"),
        ("ANI001", "Dr. Anil", "Neurology", "Neurologist", "Room 104", "1234"),
    ]

    for doctor in doctors:
        cur.execute("""
            INSERT OR IGNORE INTO doctors
            (doctor_id, doctor_name, department, specialty, room, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, doctor)

    conn.commit()
    conn.close()


def get_doctor(doctor_id):
    conn = db()
    row = conn.execute(
        "SELECT * FROM doctors WHERE UPPER(doctor_id)=UPPER(?)",
        (doctor_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def get_doctors():
    conn = db()
    rows = conn.execute(
        "SELECT doctor_id, doctor_name, department FROM doctors ORDER BY doctor_name"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_patient_df(doctor_id=None, today_only=False, upcoming=False):
    conn = db()
    today = datetime.now().strftime("%Y-%m-%d")

    if doctor_id:
        if today_only:
            query = """
                SELECT * FROM patients
                WHERE UPPER(preferred_doctor)=UPPER(?)
                  AND appointment_date=?
                ORDER BY appointment_time
            """
            rows = conn.execute(query, (doctor_id, today)).fetchall()
        elif upcoming:
            query = """
                SELECT * FROM patients
                WHERE UPPER(preferred_doctor)=UPPER(?)
                  AND appointment_date>=?
                ORDER BY appointment_date, appointment_time
            """
            rows = conn.execute(query, (doctor_id, today)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM patients
                WHERE UPPER(preferred_doctor)=UPPER(?)
                ORDER BY appointment_date DESC, appointment_time DESC
            """, (doctor_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM patients
            ORDER BY appointment_date DESC, appointment_time DESC
        """).fetchall()

    conn.close()
    return pd.DataFrame([dict(r) for r in rows])


# ============================================================

# IF / ELSE VALIDATION — NO REGEX
# ============================================================

def valid_date(value):
    if value == "":
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d") # inside try because when error comes interpretor will not stop 
        return True
    except ValueError:
        return False # hiding error on webpage


def valid_time(value):
    if value == "":
        return False
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False


def validate(field, value):
    value = str(value).strip()

    if field in ["fullname", "emergency_name", "city", "state"]:
        if value == "":
            return False, "This field cannot be empty."
        elif not value.replace(" ", "").isalpha():
            return False, "Use letters and spaces only."

    elif field == "dob":
        if not valid_date(value):
            return False, "Enter a valid date in YYYY-MM-DD format."

    elif field == "age":
        if not value.isdigit():
            return False, "Age must contain numbers only."
        elif int(value) < 1 or int(value) > 120:
            return False, "Age must be between 1 and 120."

    elif field == "gender":
        if value.lower() not in ["male", "female", "other", "m", "f", "o"]:
            return False, "Choose Male, Female or Other."

    elif field == "marital_status":
        if value.lower() not in [
            "single", "married", "divorced", "widowed", "separated"
        ]:
            return False, "Enter a valid marital status."

    elif field in ["mobile", "emergency_number"]:
        if len(value) != 10:
            return False, "Number must contain exactly 10 digits."
        elif not value.isdigit():
            return False, "Number must contain digits only."
        elif value[0] not in "6789":
            return False, "Enter a valid Indian mobile number."

    elif field == "email":
        if value.count("@") != 1:
            return False, "Enter a valid email address."
        parts = value.split("@")
        if parts[0] == "" or parts[1] == "":
            return False, "Enter a valid email address."
        elif "." not in parts[1]:
            return False, "Email domain must contain a dot."
        elif parts[1].startswith(".") or parts[1].endswith("."):
            return False, "Enter a valid email address."

    elif field == "aadhaar":
        if len(value) != 12:
            return False, "Aadhaar must contain exactly 12 digits."
        elif not value.isdigit():
            return False, "Aadhaar must contain digits only."

    elif field == "pincode":
        if len(value) != 6:
            return False, "Pincode must contain exactly 6 digits."
        elif not value.isdigit():
            return False, "Pincode must contain digits only."

    elif field == "blood_group":
        if value.upper() not in [
            "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
        ]:
            return False, "Enter a valid blood group."

    elif field == "has_insurance":
        if value.lower() not in ["yes", "no"]:
            return False, "Choose Yes or No."

    elif field == "insurance_validity":
        if not valid_date(value):
            return False, "Enter a valid date in YYYY-MM-DD format."

    elif field == "preferred_doctor":
        doctor = get_doctor(value.upper())
        if not doctor:
            return False, "Doctor ID not found."

    elif field == "appointment_date":
        if not valid_date(value):
            return False, "Enter a valid date in YYYY-MM-DD format."

    elif field == "appointment_time":
        if not valid_time(value):
            return False, "Use HH:MM format, for example 14:30."

    elif field in [
        "address", "area", "symptoms", "symptom_duration",
        "current_condition", "department"
    ]:
        if value == "":
            return False, "This field cannot be empty."

    return True, ""


def assign_department(symptoms):
    text = symptoms.lower()

    if "chest" in text or "heart" in text:
        return "Cardiology"
    elif "bone" in text or "fracture" in text:
        return "Orthopedics"
    elif "skin" in text or "rash" in text:
        return "Dermatology"
    elif "eye" in text or "vision" in text:
        return "Ophthalmology"
    elif "brain" in text or "headache" in text:
        return "Neurology"
    else:
        return "General Medicine"


# ============================================================
# PATIENT CHATBOT
# ============================================================

QUESTIONS = [
    ("fullname", "What is your full name?"),
    ("dob", "What is your date of birth?"),
    ("age", "What is your age?"),
    ("gender", "What is your gender?"),
    ("marital_status", "What is your marital status?"),
    ("mobile", "What is your 10-digit mobile number?"),
    ("email", "What is your email address?"),
    ("aadhaar", "What is your 12-digit Aadhaar number?"),
    ("address", "What is your house number / street?"),
    ("area", "What is your area / locality?"),
    ("city", "What city do you live in?"),
    ("state", "What state do you live in?"),
    ("pincode", "What is your 6-digit pincode?"),
    ("blood_group", "What is your blood group?"),
    ("emergency_name", "Who is your emergency contact?"),
    ("emergency_number", "What is the emergency contact number?"),
    ("symptoms", "Please describe your symptoms."),
    ("symptom_duration", "How long have you had these symptoms?"),
    ("current_condition", "Describe your current medical condition."),
    ("allergies", "Do you have any allergies? Type No if none."),
    ("previous_surgery", "Any previous surgery? Type No if none."),
    ("family_history", "Enter family medical history, or type No."),
    ("has_insurance", "Do you have health insurance?"),
    ("insurance_provider", "What is your insurance provider?"),
    ("policy_number", "What is your insurance policy number?"),
    ("insurance_validity", "What is the policy expiry date?"),
    ("department", "Which department do you prefer?"),
    ("preferred_doctor", "Which doctor would you like to consult?"),
    ("appointment_date", "What appointment date do you need?"),
    ("appointment_time", "What appointment time do you need?"),
]


def save_patient(data):
    patient_id = (
        "PAT"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + uuid.uuid4().hex[:4].upper()
    )

    auto_department = assign_department(data.get("symptoms", ""))
    department = data.get("department") or auto_department

    conn = db()
    conn.execute("""
        INSERT INTO patients (
            patient_id, fullname, dob, age, gender, marital_status,
            mobile, email, aadhaar, address, area, city, state, pincode,
            blood_group, emergency_name, emergency_number, symptoms,
            symptom_duration, current_condition, allergies, previous_surgery,
            family_history, has_insurance, insurance_provider, policy_number,
            insurance_validity, department, preferred_doctor,
            appointment_date, appointment_time, created_at
        )
        VALUES (
            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
    """, (
        patient_id,
        data.get("fullname"),
        data.get("dob"),
        int(data.get("age")),
        data.get("gender"),
        data.get("marital_status"),
        data.get("mobile"),
        data.get("email"),
        data.get("aadhaar"),
        data.get("address"),
        data.get("area"),
        data.get("city"),
        data.get("state"),
        data.get("pincode"),
        data.get("blood_group"),
        data.get("emergency_name"),
        data.get("emergency_number"),
        data.get("symptoms"),
        data.get("symptom_duration"),
        data.get("current_condition"),
        data.get("allergies"),
        data.get("previous_surgery"),
        data.get("family_history"),
        data.get("has_insurance"),
        data.get("insurance_provider"),
        data.get("policy_number"),
        data.get("insurance_validity"),
        department,
        data.get("preferred_doctor"),
        data.get("appointment_date"),
        data.get("appointment_time"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ))
    conn.commit()
    conn.close()

    return patient_id, auto_department, department


def reset_chat():
    for key in [
        "chat_step", "chat_data", "chat_done",
        "chat_patient_id", "chat_department"
    ]:
        st.session_state.pop(key, None)




# Backend initialization is intentionally safe to call from the frontend.
def initialize():
    init_db()

if __name__ == "__main__":
    initialize()
