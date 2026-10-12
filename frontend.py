# ============================================================
# HIMS FRONTEND - Streamlit UI
# Backend/database/business logic is in backend.py
# ============================================================

from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import backend

st.set_page_config(
    page_title="HIMS | Doctor Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "hims.db"

# Backend function aliases (UI behavior remains unchanged)
db = backend.db
get_doctor = backend.get_doctor
get_doctors = backend.get_doctors
get_patient_df = backend.get_patient_df
validate = backend.validate
assign_department = backend.assign_department
QUESTIONS = backend.QUESTIONS
save_patient = backend.save_patient
reset_chat = backend.reset_chat

# PROFESSIONAL UI
# ============================================================

st.markdown("""
<style>
/* ---------- Global ---------- */
.stApp {
    background: #f5f7fb;
    color: #172033;
}
.block-container {
    max-width: 1450px;
    padding: 1.6rem 2.3rem 3rem;
}
#MainMenu, footer {visibility:hidden;}

h1, h2, h3, h4 {
    color: #172033 !important;
    letter-spacing: -0.35px;
}
p, label, .stCaption {
    color: #687389;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e9f1;
}
section[data-testid="stSidebar"] > div {
    padding: 1.2rem 1rem;
}
.sidebar-brand {
    display:flex;
    align-items:center;
    gap:12px;
    padding:8px 6px 18px;
}
.sidebar-logo {
    width:44px;
    height:44px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(135deg,#5b5fe9,#8b43e9);
    color:white;
    font-size:21px;
    font-weight:800;
    box-shadow:0 8px 20px rgba(91,95,233,.22);
}
.sidebar-title {
    font-size:17px;
    font-weight:800;
    color:#172033;
}
.sidebar-sub {
    font-size:10px;
    color:#8b94a7;
    margin-top:2px;
}
.sidebar-section {
    font-size:10px;
    font-weight:800;
    color:#9aa2b3;
    letter-spacing:1.1px;
    margin:17px 5px 7px;
}

/* ---------- Buttons ---------- */
.stButton > button {
    border-radius:10px;
    min-height:42px;
    font-weight:700;
    border:1px solid #e1e5ee;
    background:#ffffff;
    color:#4e5870;
    transition:.15s ease;
}
.stButton > button:hover {
    border-color:#6b6fe9;
    color:#5559df;
}
.stButton > button[kind="primary"] {
    background:linear-gradient(135deg,#5c61eb,#8b43e9) !important;
    color:#ffffff !important;
    border:0 !important;
    box-shadow:0 8px 18px rgba(94,88,232,.20);
}

/* ---------- Hero ---------- */
.hero {
    background:linear-gradient(135deg,#171c35 0%,#28225a 55%,#5530a3 100%);
    border-radius:20px;
    padding:28px 31px;
    color:white;
    box-shadow:0 14px 32px rgba(34,29,83,.16);
    margin-bottom:20px;
}
.hero-kicker {
    color:#b9bcff;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.5px;
    text-transform:uppercase;
}
.hero h1 {
    color:white !important;
    font-size:32px;
    margin:7px 0 5px;
}
.hero p {
    color:#d9daf1;
    font-size:14px;
    margin:0;
}

/* ---------- Section headers ---------- */
.section-head {
    display:flex;
    align-items:end;
    justify-content:space-between;
    margin:21px 0 10px;
}
.section-title {
    font-size:19px;
    font-weight:800;
    color:#1a2235;
}
.section-subtitle {
    color:#8b94a7;
    font-size:11px;
    margin-top:3px;
}

/* ---------- KPI ---------- */
.kpi-card {
    background:#ffffff;
    border:1px solid #e4e8f0;
    border-radius:15px;
    padding:17px 18px;
    min-height:116px;
    box-shadow:0 5px 18px rgba(24,35,58,.045);
}
.kpi-top {
    display:flex;
    justify-content:space-between;
    align-items:center;
}
.kpi-label {
    color:#788297;
    font-size:11px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:.65px;
}
.kpi-icon {
    width:30px;
    height:30px;
    border-radius:9px;
    display:grid;
    place-items:center;
    background:#f0f0ff;
    color:#5e62e9;
}
.kpi-value {
    font-size:27px;
    font-weight:850;
    color:#182034;
    margin-top:8px;
}
.kpi-note {
    color:#9aa2b2;
    font-size:10px;
    margin-top:2px;
}

/* ---------- Cards ---------- */
.card {
    background:#ffffff;
    border:1px solid #e4e8f0;
    border-radius:16px;
    padding:19px;
    box-shadow:0 5px 18px rgba(24,35,58,.045);
}
.card-title {
    color:#20283a;
    font-size:15px;
    font-weight:800;
    margin-bottom:3px;
}
.card-subtitle {
    color:#8c95a8;
    font-size:11px;
}

/* ---------- Queue ---------- */
.queue-card {
    background:#ffffff;
    border:1px solid #e4e8f0;
    border-left:4px solid #6a6ee9;
    border-radius:13px;
    padding:13px 15px;
    margin:7px 0;
    box-shadow:0 3px 12px rgba(24,35,58,.035);
}
.queue-time {
    color:#5b5fe5;
    font-size:12px;
    font-weight:800;
}
.queue-name {
    color:#1d2537;
    font-size:14px;
    font-weight:800;
}
.queue-meta {
    color:#7d879a;
    font-size:10px;
}
.symptom-chip {
    display:inline-block;
    background:#f2f3ff;
    color:#5c61dd;
    border-radius:20px;
    padding:4px 8px;
    font-size:9px;
    font-weight:700;
}

/* ---------- Chat ---------- */
.chat-shell {
    background:#ffffff;
    border:1px solid #e3e7ef;
    border-radius:18px;
    box-shadow:0 7px 24px rgba(25,34,55,.06);
    padding:20px;
}
.bot-message {
    background:#f1f2ff;
    border:1px solid #e1e2ff;
    color:#363c55;
    border-radius:12px 12px 12px 3px;
    padding:12px 14px;
    font-size:13px;
    line-height:1.5;
    margin-bottom:12px;
}
.step-label {
    color:#7d86a0;
    font-size:10px;
    font-weight:800;
    letter-spacing:1px;
}
.progress-text {
    color:#7d86a0;
    font-size:10px;
}

/* ---------- Login ---------- */
.login-card {
    max-width:520px;
    margin:50px auto 0;
    background:#ffffff;
    border:1px solid #e3e7ef;
    border-radius:20px;
    padding:30px;
    box-shadow:0 12px 35px rgba(24,34,57,.08);
}
.login-logo {
    width:60px;
    height:60px;
    border-radius:17px;
    display:grid;
    place-items:center;
    margin:0 auto 13px;
    background:linear-gradient(135deg,#5c61eb,#8b43e9);
    color:#ffffff;
    font-size:27px;
    font-weight:900;
}

/* ---------- Status ---------- */
.status-online {
    display:inline-flex;
    align-items:center;
    gap:7px;
    color:#218866;
    background:#ecfaf4;
    border:1px solid #d5f2e5;
    border-radius:20px;
    padding:6px 10px;
    font-size:10px;
    font-weight:700;
}
.status-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:#22b982;
}

/* ---------- Inputs / Controls ---------- */
/* Explicit foreground/background colors are required because Streamlit/BaseWeb
   can inherit the app theme and make entered values look invisible. */
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stTimeInput input,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] input,
[data-baseweb="select"] [role="combobox"] {
    color: #182034 !important;
    -webkit-text-fill-color: #182034 !important;
    background-color: #ffffff !important;
    caret-color: #5559df !important;
    border-radius: 9px !important;
}

.stTextInput > div,
.stTextArea > div,
.stDateInput > div,
.stTimeInput > div,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #dce1ea !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-baseweb="input"] input::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
    color: #8b94a7 !important;
    -webkit-text-fill-color: #8b94a7 !important;
    opacity: 1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus,
.stTimeInput input:focus,
[data-baseweb="input"] input:focus,
[data-baseweb="textarea"] textarea:focus {
    color: #182034 !important;
    -webkit-text-fill-color: #182034 !important;
    border-color: #777ae9 !important;
    box-shadow: 0 0 0 3px rgba(119,122,233,.10) !important;
    outline: none !important;
}

/* Selectbox, radio and checkbox labels/options */
[data-baseweb="select"] *,
[data-baseweb="popover"] *,
[role="option"],
[role="listbox"] *,
.stRadio label,
.stRadio label p,
.stCheckbox label,
.stCheckbox label p {
    color: #182034 !important;
}

[data-baseweb="select"] [role="combobox"] {
    color: #182034 !important;
    -webkit-text-fill-color: #182034 !important;
}

/* Buttons: keep text visible in every Streamlit button state */
.stButton > button,
.stDownloadButton > button,
button[kind] {
    color: #4e5870 !important;
    -webkit-text-fill-color: #4e5870 !important;
    background-color: #ffffff !important;
}

.stButton > button[kind="primary"],
button[kind="primary"] {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button:hover {
    color: #5559df !important;
    -webkit-text-fill-color: #5559df !important;
}

/* Browser autofill */
.stTextInput input:-webkit-autofill,
.stTextInput input:-webkit-autofill:hover,
.stTextInput input:-webkit-autofill:focus,
.stTextInput input:-webkit-autofill:active {
    -webkit-text-fill-color: #182034 !important;
    -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important;
    box-shadow: 0 0 0 1000px #ffffff inset !important;
}

/* ---------- Tables ---------- */
[data-testid="stDataFrame"] {
    border:1px solid #e3e7ef;
    border-radius:12px;
    overflow:hidden;
}

/* ---------- Hide empty top gap ---------- */
div[data-testid="stVerticalBlock"] > div:has(> div.stMarkdown) {
    max-width:100%;
}
</style>
""", unsafe_allow_html=True)


# ============================================================

def chatbot_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Patient Services</div>
        <h1>Patient Registration</h1>
        <p>Complete your HIMS registration through a guided, validated conversation.</p>
    </div>
    """, unsafe_allow_html=True)

    if "chat_step" not in st.session_state:
        st.session_state.chat_step = 0
        st.session_state.chat_data = {}
        st.session_state.chat_done = False

    if st.session_state.chat_done:
        st.success("Registration completed successfully.")

        st.markdown("""
        <div class="card">
            <div class="card-title">Registration Complete</div>
            <div class="card-subtitle">Your patient information has been saved in HIMS.</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Patient ID", st.session_state.chat_patient_id)
        c2.metric("Department", st.session_state.chat_department)
        c3.metric("Status", "Registered")

        st.markdown("### Registration Summary")
        summary = st.session_state.chat_data.copy()
        hidden = ["aadhaar", "policy_number"]
        safe_summary = {
            k.replace("_", " ").title(): (
                "••••" + str(v)[-4:] if k in hidden and v else v
            )
            for k, v in summary.items()
        }
        st.dataframe(
            pd.DataFrame(list(safe_summary.items()), columns=["Field", "Value"]),
            use_container_width=True,
            hide_index=True,
        )

        if st.button("＋ Register Another Patient", type="primary"):
            reset_chat()
            st.rerun()
        return

    step = st.session_state.chat_step
    total = len(QUESTIONS)
    field, question = QUESTIONS[step]

    left, main, right = st.columns([0.8, 2.6, 0.8])

    with main:
        st.markdown(
            f'<div class="chat-shell">'
            f'<div class="step-label">PATIENT INTAKE · STEP {step + 1} OF {total}</div>'
            f'<div style="margin-top:10px;">'
            f'<div class="bot-message">🤖 <b>HIMS Assistant</b><br>{question}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        st.progress((step + 1) / total)

        # Input controls
        if field == "gender":
            answer = st.radio(
                "Your answer",
                ["Male", "Female", "Other"],
                horizontal=True,
                key=f"input_{field}",
            )
        elif field == "marital_status":
            answer = st.selectbox(
                "Your answer",
                ["Single", "Married", "Divorced", "Widowed", "Separated"],
                key=f"input_{field}",
            )
        elif field == "has_insurance":
            answer = st.radio(
                "Your answer", ["Yes", "No"],
                horizontal=True, key=f"input_{field}"
            )
        elif field == "blood_group":
            answer = st.selectbox(
                "Your answer",
                ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                key=f"input_{field}",
            )
        elif field == "preferred_doctor":
            doctor_list = get_doctors()
            options = [
                f"{d['doctor_id']} — {d['doctor_name']} ({d['department']})"
                for d in doctor_list
            ]
            selected = st.selectbox(
                "Choose doctor", options, key=f"input_{field}"
            )
            answer = selected.split(" — ")[0]
        elif field == "department":
            answer = st.selectbox(
                "Preferred department",
                [
                    "General Medicine", "Cardiology", "Orthopedics",
                    "Dermatology", "Ophthalmology", "Neurology", "Physiology"
                ],
                key=f"input_{field}",
            )
        elif field in ["dob", "insurance_validity", "appointment_date"]:
            selected_date = st.date_input(
                "Your answer", value=date.today(), key=f"input_{field}"
            )
            answer = selected_date.strftime("%Y-%m-%d")
        elif field == "appointment_time":
            selected_time = st.time_input(
                "Your answer", value=datetime.now().time(), key=f"input_{field}"
            )
            answer = selected_time.strftime("%H:%M")
        elif field in [
            "symptoms", "current_condition", "allergies",
            "previous_surgery", "family_history", "address"
        ]:
            answer = st.text_area(
                "Your answer", key=f"input_{field}", height=100
            )
        else:
            answer = st.text_input(
                "Your answer", key=f"input_{field}",
                placeholder="Type your answer here..."
            )

        if field == "has_insurance" and str(answer).lower() == "no":
            st.caption("Insurance details will be skipped.")

        if st.button("Continue  →", type="primary", use_container_width=True):
            ok, message = validate(field, answer)

            if not ok:
                st.error(message)
                return

            st.session_state.chat_data[field] = str(answer).strip()

            # Conditional insurance flow
            if field == "has_insurance" and str(answer).lower() == "no":
                st.session_state.chat_data["insurance_provider"] = ""
                st.session_state.chat_data["policy_number"] = ""
                st.session_state.chat_data["insurance_validity"] = ""
                st.session_state.chat_step += 4
            else:
                st.session_state.chat_step += 1

            if st.session_state.chat_step >= total:
                patient_id, auto_department, department = save_patient(
                    st.session_state.chat_data
                )
                st.session_state.chat_patient_id = patient_id
                st.session_state.chat_department = department
                st.session_state.chat_done = True

            st.rerun()


# ============================================================

# LOGIN
# ============================================================

def login_page():
    st.markdown("""
    <div class="login-card">
        <div class="login-logo">✚</div>
        <h2 style="text-align:center;">Doctor Portal</h2>
        <p style="text-align:center;">
            Sign in to view your patient queue and clinical dashboard.
        </p>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.4, 1])

    with center:
        st.markdown("<br>", unsafe_allow_html=True)

        doctor_id = st.text_input(
            "Doctor ID",
            placeholder="Example: RAK001",
            key="login_doctor",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password",
            key="login_password",
        )

        if st.button("Sign In  →", type="primary", use_container_width=True):
            doctor = get_doctor(doctor_id.strip().upper())

            if doctor and password == doctor["password"]:
                st.session_state.logged_in = True
                st.session_state.doctor_id = doctor["doctor_id"]
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid Doctor ID or password.")

        st.caption("Demo credentials: RAK001 / 1234")


# ============================================================
# DOCTOR DASHBOARD
# ============================================================

def kpi(label, value, icon, note):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def dashboard_page():
    doctor_id = st.session_state.doctor_id
    doctor = get_doctor(doctor_id)

    today = datetime.now().strftime("%Y-%m-%d")

    assigned = get_patient_df(doctor_id=doctor_id)
    today_df = get_patient_df(doctor_id=doctor_id, today_only=True)
    upcoming_df = get_patient_df(doctor_id=doctor_id, upcoming=True)

    st.markdown(f"""
    <div class="hero">
        <div class="hero-kicker">Doctor Workspace · {doctor['doctor_id']}</div>
        <h1>Good day, {doctor['doctor_name']} 👋</h1>
        <p>{doctor['specialty']} · {doctor['department']} · {doctor['room']} · {today}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("Today's Queue", len(today_df), "👥", "Patients scheduled today")
    with c2:
        kpi("Total Assigned", len(assigned), "📋", "Patients assigned to you")
    with c3:
        if not assigned.empty and "age" in assigned:
            avg_age = assigned["age"].dropna().mean()
            value = f"{avg_age:.1f}" if pd.notna(avg_age) else "—"
        else:
            value = "—"
        kpi("Average Age", value, "◌", "Years across assigned patients")
    with c4:
        if not assigned.empty:
            insured = assigned["has_insurance"].fillna("").astype(str).str.lower().eq("yes").sum()
            rate = (insured / len(assigned)) * 100
            value = f"{rate:.0f}%"
        else:
            value = "0%"
        kpi("Insurance Rate", value, "✓", "Among assigned patients")

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Today's Patient Queue</div>
            <div class="section-subtitle">Patients currently scheduled to see you today</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if today_df.empty:
        st.markdown("""
        <div class="card">
            <div class="card-title">No patients scheduled today</div>
            <div class="card-subtitle">Your queue is currently clear.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, patient in today_df.iterrows():
            with st.container():
                a, b, c, d = st.columns([1, 2.3, 2.3, 1.3])

                with a:
                    st.markdown(
                        f'<div class="queue-time">🕐 {patient["appointment_time"]}</div>',
                        unsafe_allow_html=True,
                    )
                with b:
                    st.markdown(
                        f'<div class="queue-name">{patient["fullname"]}</div>'
                        f'<div class="queue-meta">{patient["patient_id"]} · '
                        f'{patient["age"]} yrs · {patient["gender"]}</div>',
                        unsafe_allow_html=True,
                    )
                with c:
                    symptom = str(patient["symptoms"] or "Not provided")
                    st.markdown(
                        f'<span class="symptom-chip">{symptom[:70]}</span>',
                        unsafe_allow_html=True,
                    )
                with d:
                    st.caption(str(patient["department"] or doctor["department"]))

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Clinical Overview</div>
            <div class="section-subtitle">Demographics and patient distribution</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown(
            '<div class="card"><div class="card-title">Patients by Gender</div>'
            '<div class="card-subtitle">Your assigned patient population</div></div>',
            unsafe_allow_html=True,
        )
        if not assigned.empty:
            gender = (
                assigned["gender"].fillna("Unknown")
                .replace({"m": "Male", "f": "Female", "o": "Other"})
                .value_counts()
                .reset_index()
            )
            gender.columns = ["Gender", "Patients"]
            fig = px.bar(
                gender, x="Gender", y="Patients",
                text="Patients",
                template="plotly_white",
            )
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=15, b=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_traces(
                marker_color="#6468e8",
                textposition="outside",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No assigned patient data yet.")

    with chart2:
        st.markdown(
            '<div class="card"><div class="card-title">Patient Departments</div>'
            '<div class="card-subtitle">Department distribution</div></div>',
            unsafe_allow_html=True,
        )
        if not assigned.empty:
            dept = assigned["department"].fillna("Unknown").value_counts().reset_index()
            dept.columns = ["Department", "Patients"]
            fig = px.bar(
                dept, x="Patients", y="Department",
                orientation="h",
                text="Patients",
                template="plotly_white",
            )
            fig.update_layout(
                height=300,
                margin=dict(l=10, r=10, t=15, b=10),
                showlegend=False,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
            )
            fig.update_traces(
                marker_color="#9a55e8",
                textposition="outside",
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No department data yet.")

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Upcoming Appointments</div>
            <div class="section-subtitle">Next patients in your schedule</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if upcoming_df.empty:
        st.info("No upcoming appointments.")
    else:
        display_cols = [
            "appointment_date", "appointment_time", "patient_id",
            "fullname", "age", "gender", "symptoms"
        ]
        display_cols = [c for c in display_cols if c in upcoming_df.columns]
        st.dataframe(
            upcoming_df[display_cols].head(25),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Patient Details</div>
            <div class="section-subtitle">Open a complete record for an assigned patient</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if assigned.empty:
        st.info("No patients are assigned to this Doctor ID.")
        return

    selected = st.selectbox(
        "Select patient",
        assigned["patient_id"].tolist(),
        format_func=lambda x: (
            f"{x}  ·  "
            f"{assigned.loc[assigned['patient_id'] == x, 'fullname'].iloc[0]}"
        ),
    )

    patient = assigned[assigned["patient_id"] == selected].iloc[0]

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Patient", str(patient["fullname"]))
    d2.metric("Age", str(patient["age"]))
    d3.metric("Gender", str(patient["gender"]))
    d4.metric("Blood Group", str(patient["blood_group"]))

    left, right = st.columns(2)

    with left:
        with st.container(border=True):
            st.markdown("**Contact & Appointment**")
            st.write(f"📱 **Mobile:** {patient['mobile']}")
            st.write(f"✉️ **Email:** {patient['email']}")
            st.write(
                f"📅 **Appointment:** "
                f"{patient['appointment_date']} {patient['appointment_time']}"
            )
            st.write(
                f"📍 **Location:** "
                f"{patient['city']}, {patient['state']}"
            )

    with right:
        with st.container(border=True):
            st.markdown("**Clinical Information**")
            st.write(f"🩺 **Symptoms:** {patient['symptoms']}")
            st.write(f"⏱️ **Duration:** {patient['symptom_duration']}")
            st.write(f"⚕️ **Current Condition:** {patient['current_condition']}")
            st.write(f"⚠️ **Allergies:** {patient['allergies']}")

    with st.expander("View Complete Patient Record"):
        details = patient.to_frame("Value")
        st.dataframe(details, use_container_width=True)


# ============================================================
# HOME
# ============================================================

def home_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Hospital Information Management System</div>
        <h1>HIMS Clinical Portal</h1>
        <p>Patient registration and doctor-side patient management in one application.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="card">
            <div class="card-title">🤖 Patient Registration</div>
            <div class="card-subtitle">
                A guided chatbot collects patient information and validates
                every response before saving it to HIMS.
            </div>
            <br>
            <b>Includes</b><br>
            • Personal information<br>
            • Contact information<br>
            • Symptoms and medical history<br>
            • Insurance details<br>
            • Doctor and appointment selection
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Patient Registration  →", type="primary",
                     use_container_width=True):
            st.session_state.page = "Patient Registration"
            st.rerun()

    with b:
        st.markdown("""
        <div class="card">
            <div class="card-title">👨‍⚕️ Doctor Portal</div>
            <div class="card-subtitle">
                Doctors log in with their Doctor ID and see only the patients
                scheduled for their own clinic queue.
            </div>
            <br>
            <b>Dashboard includes</b><br>
            • Today's patient queue<br>
            • Upcoming appointments<br>
            • Patient demographics<br>
            • Clinical details<br>
            • Complete patient records
        </div>
        """, unsafe_allow_html=True)

        if st.button("Doctor Login  →", use_container_width=True):
            st.session_state.page = "Doctor Login"
            st.rerun()

    st.markdown("""
    <div style="margin-top:24px;text-align:center;color:#98a1b2;font-size:11px;">
        HIMS · Streamlit · Patient Intake + Doctor Workspace
    </div>
    """, unsafe_allow_html=True)


# ============================================================

# APP STATE + NAVIGATION
# ============================================================

backend.initialize()

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">✚</div>
        <div>
            <div class="sidebar-title">HIMS</div>
            <div class="sidebar-sub">Clinical Management Portal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">MAIN MENU</div>',
                unsafe_allow_html=True)

    if st.button("⌂  Home", use_container_width=True):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("🤖  Patient Registration", use_container_width=True):
        st.session_state.page = "Patient Registration"
        st.rerun()

    if st.session_state.logged_in:
        if st.button("▣  Doctor Dashboard", use_container_width=True):
            st.session_state.page = "Dashboard"
            st.rerun()

        st.markdown('<div class="sidebar-section">SIGNED IN</div>',
                    unsafe_allow_html=True)

        doctor = get_doctor(st.session_state.doctor_id)

        st.markdown(f"""
        <div class="card" style="padding:13px;">
            <b style="font-size:13px;">{doctor['doctor_name']}</b><br>
            <span style="font-size:10px;color:#7d879a;">
                {doctor['doctor_id']} · {doctor['department']}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("↪  Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.pop("doctor_id", None)
            st.session_state.page = "Home"
            st.rerun()

    else:
        if st.button("👨‍⚕️  Doctor Login", use_container_width=True):
            st.session_state.page = "Doctor Login"
            st.rerun()

    st.markdown('<div class="sidebar-section">SYSTEM STATUS</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="status-online"><span class="status-dot"></span>'
        ' HIMS database ready</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section">DEMO DOCTORS</div>',
                unsafe_allow_html=True)
    st.code("RAK001\nMAD001\nPRI001\nANI001", language="text")
    st.caption("Demo password: 1234")


page = st.session_state.page

if page == "Home":
    home_page()

elif page == "Patient Registration":
    chatbot_page()

elif page == "Doctor Login":
    login_page()

elif page == "Dashboard":
    if st.session_state.logged_in:
        dashboard_page()
    else:
        st.session_state.page = "Doctor Login"
        st.rerun()
