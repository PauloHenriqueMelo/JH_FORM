"""
Geriatric History Taking Form
Jewish General Hospital - Geriatric Clinic
Pre-admission intake form for elderly patients
"""

import streamlit as st
from datetime import datetime, date
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# Page configuration
st.set_page_config(
    page_title="Geriatric Clinic - Patient Intake Form",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for elderly-friendly design
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1000px;
    }

    /* Large fonts throughout */
    html, body, [class*="css"] {
        font-size: 20px !important;
        font-family: Arial, sans-serif !important;
    }

    /* Headers */
    h1 {
        font-size: 42px !important;
        font-weight: bold !important;
        color: #1a365d !important;
        margin-bottom: 1rem !important;
    }

    h2 {
        font-size: 36px !important;
        font-weight: bold !important;
        color: #2c5282 !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 3px solid #2c5282 !important;
    }

    h3 {
        font-size: 28px !important;
        font-weight: bold !important;
        color: #2d3748 !important;
        margin-top: 1.5rem !important;
    }

    /* Labels and text */
    label {
        font-size: 24px !important;
        font-weight: 600 !important;
        color: #1a202c !important;
    }

    p, span, div {
        font-size: 22px !important;
        line-height: 1.6 !important;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        font-size: 24px !important;
        padding: 15px !important;
        border: 3px solid #4a5568 !important;
        border-radius: 10px !important;
    }

    .stTextArea > div > div > textarea {
        font-size: 22px !important;
        padding: 15px !important;
        border: 3px solid #4a5568 !important;
        border-radius: 10px !important;
    }

    .stSelectbox > div > div {
        font-size: 24px !important;
    }

    .stDateInput > div > div > input {
        font-size: 24px !important;
        padding: 15px !important;
    }

    /* Radio buttons and checkboxes - LARGE */
    .stRadio > div {
        gap: 15px !important;
    }

    .stRadio > div > label {
        font-size: 24px !important;
        padding: 20px 30px !important;
        background-color: #f7fafc !important;
        border: 3px solid #cbd5e0 !important;
        border-radius: 15px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        align-items: center !important;
        min-height: 70px !important;
    }

    .stRadio > div > label:hover {
        background-color: #e2e8f0 !important;
        border-color: #2c5282 !important;
    }

    .stCheckbox > label {
        font-size: 24px !important;
        padding: 15px !important;
    }

    /* Buttons - LARGE and prominent */
    .stButton > button {
        font-size: 28px !important;
        font-weight: bold !important;
        padding: 20px 50px !important;
        border-radius: 15px !important;
        min-height: 80px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        transform: scale(1.02) !important;
    }

    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: #2c5282 !important;
        height: 20px !important;
        border-radius: 10px !important;
    }

    /* Section dividers */
    hr {
        border: none !important;
        height: 4px !important;
        background-color: #e2e8f0 !important;
        margin: 2rem 0 !important;
    }

    /* Success/info messages */
    .stSuccess, .stInfo, .stWarning {
        font-size: 24px !important;
        padding: 20px !important;
        border-radius: 15px !important;
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        font-size: 26px !important;
        font-weight: bold !important;
    }

    /* Number input */
    .stNumberInput > div > div > input {
        font-size: 24px !important;
        padding: 15px !important;
    }

    /* Question boxes */
    .question-box {
        background-color: #f7fafc;
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 6px solid #2c5282;
    }

    /* Yes/No button styling */
    div[data-testid="stHorizontalBlock"] > div {
        padding: 5px !important;
    }

    /* Hide hamburger menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom button classes */
    .yes-button button {
        background-color: #276749 !important;
        color: white !important;
    }

    .no-button button {
        background-color: #c53030 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize all session state variables"""
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 0

    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'demographics': {},
            'symptoms': {},
            'cognitive': {},
            'medications': {},
            'adl': {},
            'iadl': {},
            'medical_history': {}
        }

    if 'form_completed' not in st.session_state:
        st.session_state.form_completed = False


def create_yes_no_question(question_text, key, help_text=None):
    """Create a large Yes/No question with big buttons"""
    st.markdown(f"### {question_text}")
    if help_text:
        st.markdown(f"*{help_text}*")

    col1, col2, col3 = st.columns([1, 1, 1])

    current_value = st.session_state.form_data.get(key, None)

    with col1:
        if st.button("YES", key=f"{key}_yes", use_container_width=True,
                     type="primary" if current_value == "Yes" else "secondary"):
            return "Yes"

    with col2:
        if st.button("NO", key=f"{key}_no", use_container_width=True,
                     type="primary" if current_value == "No" else "secondary"):
            return "No"

    with col3:
        if st.button("NOT SURE", key=f"{key}_unsure", use_container_width=True,
                     type="primary" if current_value == "Not Sure" else "secondary"):
            return "Not Sure"

    return current_value


def render_progress_bar():
    """Render progress indicator"""
    sections = [
        "Personal Information",
        "Current Symptoms",
        "Memory and Thinking",
        "Medications",
        "Daily Activities (Basic)",
        "Daily Activities (Complex)",
        "Medical History",
        "Review and Submit"
    ]

    progress = (st.session_state.current_section) / (len(sections) - 1)

    st.markdown("---")
    st.markdown(f"### Section {st.session_state.current_section + 1} of {len(sections)}: {sections[st.session_state.current_section]}")
    st.progress(progress)
    st.markdown("---")


def section_demographics():
    """Section 1: Patient Demographics"""
    st.header("Personal Information")
    st.markdown("Please provide your basic information. All fields are important for your care.")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First Name",
            value=st.session_state.form_data['demographics'].get('first_name', ''),
            key="first_name"
        )

        date_of_birth = st.date_input(
            "Date of Birth",
            value=st.session_state.form_data['demographics'].get('date_of_birth', date(1950, 1, 1)),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            key="dob"
        )

        phone = st.text_input(
            "Phone Number",
            value=st.session_state.form_data['demographics'].get('phone', ''),
            key="phone"
        )

    with col2:
        last_name = st.text_input(
            "Last Name",
            value=st.session_state.form_data['demographics'].get('last_name', ''),
            key="last_name"
        )

        sex = st.radio(
            "Sex",
            options=["Male", "Female", "Other", "Prefer not to say"],
            index=["Male", "Female", "Other", "Prefer not to say"].index(
                st.session_state.form_data['demographics'].get('sex', 'Male')
            ) if st.session_state.form_data['demographics'].get('sex') else 0,
            key="sex",
            horizontal=True
        )

        health_card = st.text_input(
            "Health Card Number (RAMQ)",
            value=st.session_state.form_data['demographics'].get('health_card', ''),
            key="health_card"
        )

    st.markdown("### Emergency Contact")

    col3, col4 = st.columns(2)

    with col3:
        emergency_name = st.text_input(
            "Emergency Contact Name",
            value=st.session_state.form_data['demographics'].get('emergency_name', ''),
            key="emergency_name"
        )

        emergency_relation = st.selectbox(
            "Relationship",
            options=["Spouse", "Child", "Sibling", "Friend", "Other"],
            index=["Spouse", "Child", "Sibling", "Friend", "Other"].index(
                st.session_state.form_data['demographics'].get('emergency_relation', 'Spouse')
            ) if st.session_state.form_data['demographics'].get('emergency_relation') else 0,
            key="emergency_relation"
        )

    with col4:
        emergency_phone = st.text_input(
            "Emergency Contact Phone",
            value=st.session_state.form_data['demographics'].get('emergency_phone', ''),
            key="emergency_phone"
        )

        preferred_language = st.selectbox(
            "Preferred Language",
            options=["English", "French", "Other"],
            index=["English", "French", "Other"].index(
                st.session_state.form_data['demographics'].get('preferred_language', 'English')
            ) if st.session_state.form_data['demographics'].get('preferred_language') else 0,
            key="preferred_language"
        )

    # Save to session state
    st.session_state.form_data['demographics'] = {
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': date_of_birth,
        'sex': sex,
        'phone': phone,
        'health_card': health_card,
        'emergency_name': emergency_name,
        'emergency_relation': emergency_relation,
        'emergency_phone': emergency_phone,
        'preferred_language': preferred_language
    }


def section_symptoms():
    """Section 2: Current Symptoms Assessment"""
    st.header("Current Symptoms")
    st.markdown("Please tell us about any symptoms you are experiencing. Select YES or NO for each question.")

    symptoms_questions = [
        ("pain", "Are you currently experiencing any PAIN?", "This includes headaches, joint pain, muscle pain, or any other discomfort"),
        ("dizziness", "Do you feel DIZZY or lightheaded?", "Feeling unsteady or like the room is spinning"),
        ("fatigue", "Do you feel unusually TIRED or weak?", "More tired than usual, lack of energy"),
        ("breathing", "Do you have difficulty BREATHING?", "Shortness of breath, wheezing, or chest tightness"),
        ("sleep", "Do you have trouble SLEEPING?", "Difficulty falling asleep, staying asleep, or sleeping too much"),
        ("appetite", "Have you noticed changes in your APPETITE?", "Eating more or less than usual"),
        ("vision", "Do you have problems with your VISION?", "Blurry vision, difficulty reading, or seeing things"),
        ("hearing", "Do you have problems with your HEARING?", "Difficulty hearing conversations or sounds"),
        ("balance", "Do you have problems with BALANCE or walking?", "Feeling unsteady, using a cane or walker"),
        ("falls", "Have you had any FALLS in the past 6 months?", "Falling down, tripping, or losing balance"),
    ]

    symptoms_data = {}

    for key, question, help_text in symptoms_questions:
        st.markdown("---")

        current_value = st.session_state.form_data['symptoms'].get(key, None)

        st.markdown(f"### {question}")
        st.markdown(f"*{help_text}*")

        col1, col2, col3 = st.columns(3)

        with col1:
            yes_selected = current_value == "Yes"
            if st.button("YES", key=f"symptom_{key}_yes", use_container_width=True,
                        type="primary" if yes_selected else "secondary"):
                symptoms_data[key] = "Yes"
                st.session_state.form_data['symptoms'][key] = "Yes"
                st.rerun()

        with col2:
            no_selected = current_value == "No"
            if st.button("NO", key=f"symptom_{key}_no", use_container_width=True,
                        type="primary" if no_selected else "secondary"):
                symptoms_data[key] = "No"
                st.session_state.form_data['symptoms'][key] = "No"
                st.rerun()

        with col3:
            unsure_selected = current_value == "Not Sure"
            if st.button("NOT SURE", key=f"symptom_{key}_unsure", use_container_width=True,
                        type="primary" if unsure_selected else "secondary"):
                symptoms_data[key] = "Not Sure"
                st.session_state.form_data['symptoms'][key] = "Not Sure"
                st.rerun()

        # Show current selection
        if current_value:
            st.info(f"Your answer: **{current_value}**")

        # Follow-up for positive responses
        if current_value == "Yes" and key == "pain":
            st.markdown("#### Where is your pain?")
            pain_location = st.text_area(
                "Please describe where you feel pain:",
                value=st.session_state.form_data['symptoms'].get('pain_location', ''),
                key="pain_location",
                height=100
            )
            st.session_state.form_data['symptoms']['pain_location'] = pain_location

            pain_level = st.slider(
                "How severe is your pain? (0 = No pain, 10 = Worst pain)",
                min_value=0, max_value=10,
                value=st.session_state.form_data['symptoms'].get('pain_level', 5),
                key="pain_level"
            )
            st.session_state.form_data['symptoms']['pain_level'] = pain_level

        if current_value == "Yes" and key == "falls":
            falls_count = st.number_input(
                "How many times have you fallen?",
                min_value=1, max_value=50,
                value=st.session_state.form_data['symptoms'].get('falls_count', 1),
                key="falls_count"
            )
            st.session_state.form_data['symptoms']['falls_count'] = falls_count

    # Additional symptoms
    st.markdown("---")
    st.markdown("### Any other symptoms or concerns?")
    other_symptoms = st.text_area(
        "Please describe any other symptoms not mentioned above:",
        value=st.session_state.form_data['symptoms'].get('other_symptoms', ''),
        key="other_symptoms",
        height=150
    )
    st.session_state.form_data['symptoms']['other_symptoms'] = other_symptoms


def section_cognitive():
    """Section 3: Cognitive Function Assessment (Simplified MMSE-style)"""
    st.header("Memory and Thinking")
    st.markdown("These questions help us understand your memory and thinking. Please answer as best as you can. It is okay if you are not sure.")

    # Orientation Questions
    st.markdown("### About Today")

    col1, col2 = st.columns(2)

    with col1:
        today_date = st.date_input(
            "What is today's date?",
            value=st.session_state.form_data['cognitive'].get('today_date', date.today()),
            key="today_date"
        )
        st.session_state.form_data['cognitive']['today_date'] = today_date

        day_of_week = st.selectbox(
            "What day of the week is it?",
            options=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "I'm not sure"],
            index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "I'm not sure"].index(
                st.session_state.form_data['cognitive'].get('day_of_week', "I'm not sure")
            ) if st.session_state.form_data['cognitive'].get('day_of_week') else 7,
            key="day_of_week"
        )
        st.session_state.form_data['cognitive']['day_of_week'] = day_of_week

    with col2:
        season = st.selectbox(
            "What season is it?",
            options=["Spring", "Summer", "Fall", "Winter", "I'm not sure"],
            index=["Spring", "Summer", "Fall", "Winter", "I'm not sure"].index(
                st.session_state.form_data['cognitive'].get('season', "I'm not sure")
            ) if st.session_state.form_data['cognitive'].get('season') else 4,
            key="season"
        )
        st.session_state.form_data['cognitive']['season'] = season

        current_year = st.number_input(
            "What year is it?",
            min_value=2000, max_value=2030,
            value=st.session_state.form_data['cognitive'].get('current_year', 2024),
            key="current_year"
        )
        st.session_state.form_data['cognitive']['current_year'] = current_year

    # Location
    st.markdown("### About This Place")

    location = st.text_input(
        "What is the name of this hospital?",
        value=st.session_state.form_data['cognitive'].get('hospital_name', ''),
        key="hospital_name"
    )
    st.session_state.form_data['cognitive']['hospital_name'] = location

    city = st.text_input(
        "What city are we in?",
        value=st.session_state.form_data['cognitive'].get('city', ''),
        key="city"
    )
    st.session_state.form_data['cognitive']['city'] = city

    # Memory concerns - self-reported
    st.markdown("---")
    st.markdown("### Memory Concerns")

    memory_questions = [
        ("forget_names", "Do you often forget names of people you know?"),
        ("forget_appointments", "Do you forget appointments or important dates?"),
        ("lose_items", "Do you frequently misplace items (keys, glasses, etc.)?"),
        ("repeat_questions", "Has anyone told you that you repeat questions or stories?"),
        ("difficulty_decisions", "Do you find it harder to make decisions than before?"),
        ("get_lost", "Do you ever get lost in familiar places?"),
    ]

    for key, question in memory_questions:
        st.markdown("---")
        current_value = st.session_state.form_data['cognitive'].get(key, None)

        st.markdown(f"### {question}")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("YES", key=f"cog_{key}_yes", use_container_width=True,
                        type="primary" if current_value == "Yes" else "secondary"):
                st.session_state.form_data['cognitive'][key] = "Yes"
                st.rerun()

        with col2:
            if st.button("NO", key=f"cog_{key}_no", use_container_width=True,
                        type="primary" if current_value == "No" else "secondary"):
                st.session_state.form_data['cognitive'][key] = "No"
                st.rerun()

        with col3:
            if st.button("SOMETIMES", key=f"cog_{key}_sometimes", use_container_width=True,
                        type="primary" if current_value == "Sometimes" else "secondary"):
                st.session_state.form_data['cognitive'][key] = "Sometimes"
                st.rerun()

        if current_value:
            st.info(f"Your answer: **{current_value}**")

    # Additional concerns
    st.markdown("---")
    memory_concerns = st.text_area(
        "Do you have any other concerns about your memory or thinking?",
        value=st.session_state.form_data['cognitive'].get('other_concerns', ''),
        key="memory_other_concerns",
        height=150
    )
    st.session_state.form_data['cognitive']['other_concerns'] = memory_concerns


def section_medications():
    """Section 4: Medications"""
    st.header("Medications")
    st.markdown("Please list all medications you are currently taking, including prescriptions, over-the-counter medicines, vitamins, and supplements.")

    # Ask if taking any medications
    st.markdown("### Are you currently taking any medications?")

    taking_meds = st.session_state.form_data['medications'].get('taking_medications', None)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES, I take medications", key="meds_yes", use_container_width=True,
                    type="primary" if taking_meds == "Yes" else "secondary"):
            st.session_state.form_data['medications']['taking_medications'] = "Yes"
            st.rerun()

    with col2:
        if st.button("NO, I don't take any medications", key="meds_no", use_container_width=True,
                    type="primary" if taking_meds == "No" else "secondary"):
            st.session_state.form_data['medications']['taking_medications'] = "No"
            st.rerun()

    if taking_meds == "Yes":
        st.markdown("---")
        st.markdown("### Please list your medications")
        st.markdown("*Include the name, dose if known, and how often you take it*")

        # Number of medications
        num_meds = st.number_input(
            "How many different medications do you take?",
            min_value=1, max_value=30,
            value=st.session_state.form_data['medications'].get('num_medications', 1),
            key="num_medications"
        )
        st.session_state.form_data['medications']['num_medications'] = num_meds

        # Medication entries
        medications_list = st.session_state.form_data['medications'].get('medications_list', [])

        # Ensure list is correct length
        while len(medications_list) < num_meds:
            medications_list.append({'name': '', 'dose': '', 'frequency': ''})

        for i in range(num_meds):
            st.markdown(f"#### Medication {i + 1}")
            col1, col2, col3 = st.columns([2, 1, 1])

            with col1:
                med_name = st.text_input(
                    f"Medication Name",
                    value=medications_list[i].get('name', '') if i < len(medications_list) else '',
                    key=f"med_name_{i}"
                )

            with col2:
                med_dose = st.text_input(
                    f"Dose (if known)",
                    value=medications_list[i].get('dose', '') if i < len(medications_list) else '',
                    key=f"med_dose_{i}",
                    placeholder="e.g., 10mg"
                )

            with col3:
                med_freq = st.selectbox(
                    f"How often?",
                    options=["Once daily", "Twice daily", "Three times daily", "As needed", "Weekly", "Other"],
                    key=f"med_freq_{i}"
                )

            if i < len(medications_list):
                medications_list[i] = {'name': med_name, 'dose': med_dose, 'frequency': med_freq}
            else:
                medications_list.append({'name': med_name, 'dose': med_dose, 'frequency': med_freq})

        st.session_state.form_data['medications']['medications_list'] = medications_list[:num_meds]

        # Medication management
        st.markdown("---")
        st.markdown("### Medication Management")

        st.markdown("#### Do you need help managing your medications?")
        help_meds = st.session_state.form_data['medications'].get('needs_help', None)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("YES", key="help_meds_yes", use_container_width=True,
                        type="primary" if help_meds == "Yes" else "secondary"):
                st.session_state.form_data['medications']['needs_help'] = "Yes"
                st.rerun()

        with col2:
            if st.button("NO", key="help_meds_no", use_container_width=True,
                        type="primary" if help_meds == "No" else "secondary"):
                st.session_state.form_data['medications']['needs_help'] = "No"
                st.rerun()

        if help_meds:
            st.info(f"Your answer: **{help_meds}**")

        # Medication adherence
        st.markdown("#### Do you ever miss doses of your medications?")
        miss_doses = st.session_state.form_data['medications'].get('miss_doses', None)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("NEVER", key="miss_never", use_container_width=True,
                        type="primary" if miss_doses == "Never" else "secondary"):
                st.session_state.form_data['medications']['miss_doses'] = "Never"
                st.rerun()

        with col2:
            if st.button("SOMETIMES", key="miss_sometimes", use_container_width=True,
                        type="primary" if miss_doses == "Sometimes" else "secondary"):
                st.session_state.form_data['medications']['miss_doses'] = "Sometimes"
                st.rerun()

        with col3:
            if st.button("OFTEN", key="miss_often", use_container_width=True,
                        type="primary" if miss_doses == "Often" else "secondary"):
                st.session_state.form_data['medications']['miss_doses'] = "Often"
                st.rerun()

        if miss_doses:
            st.info(f"Your answer: **{miss_doses}**")

    # Allergies
    st.markdown("---")
    st.markdown("### Drug Allergies")

    st.markdown("#### Do you have any allergies to medications?")
    has_allergies = st.session_state.form_data['medications'].get('has_allergies', None)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES", key="allergy_yes", use_container_width=True,
                    type="primary" if has_allergies == "Yes" else "secondary"):
            st.session_state.form_data['medications']['has_allergies'] = "Yes"
            st.rerun()

    with col2:
        if st.button("NO", key="allergy_no", use_container_width=True,
                    type="primary" if has_allergies == "No" else "secondary"):
            st.session_state.form_data['medications']['has_allergies'] = "No"
            st.rerun()

    if has_allergies == "Yes":
        allergies = st.text_area(
            "Please list your medication allergies:",
            value=st.session_state.form_data['medications'].get('allergies_list', ''),
            key="allergies_list",
            height=100
        )
        st.session_state.form_data['medications']['allergies_list'] = allergies


def section_adl():
    """Section 5: Basic Activities of Daily Living (BADL/ADL)"""
    st.header("Daily Activities - Basic")
    st.markdown("These questions ask about your ability to perform basic daily activities. Please select the answer that best describes your current ability.")

    adl_activities = [
        ("bathing", "BATHING", "Taking a bath or shower"),
        ("dressing", "DRESSING", "Getting dressed and undressed"),
        ("toileting", "USING THE TOILET", "Getting to and using the toilet"),
        ("transferring", "MOVING AROUND", "Getting in and out of bed or chair"),
        ("continence", "BLADDER AND BOWEL CONTROL", "Controlling bladder and bowel"),
        ("feeding", "EATING", "Feeding yourself"),
    ]

    for key, activity, description in adl_activities:
        st.markdown("---")
        st.markdown(f"### {activity}")
        st.markdown(f"*{description}*")

        current_value = st.session_state.form_data['adl'].get(key, None)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("I can do this\nBY MYSELF", key=f"adl_{key}_independent", use_container_width=True,
                        type="primary" if current_value == "Independent" else "secondary"):
                st.session_state.form_data['adl'][key] = "Independent"
                st.rerun()

        with col2:
            if st.button("I need\nSOME HELP", key=f"adl_{key}_assistance", use_container_width=True,
                        type="primary" if current_value == "Needs Assistance" else "secondary"):
                st.session_state.form_data['adl'][key] = "Needs Assistance"
                st.rerun()

        with col3:
            if st.button("I need\nFULL HELP", key=f"adl_{key}_dependent", use_container_width=True,
                        type="primary" if current_value == "Dependent" else "secondary"):
                st.session_state.form_data['adl'][key] = "Dependent"
                st.rerun()

        if current_value:
            st.info(f"Your answer: **{current_value}**")

    # Mobility aids
    st.markdown("---")
    st.markdown("### Mobility Aids")
    st.markdown("#### Do you use any mobility aids?")

    uses_aids = st.session_state.form_data['adl'].get('uses_mobility_aids', None)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES", key="aids_yes", use_container_width=True,
                    type="primary" if uses_aids == "Yes" else "secondary"):
            st.session_state.form_data['adl']['uses_mobility_aids'] = "Yes"
            st.rerun()

    with col2:
        if st.button("NO", key="aids_no", use_container_width=True,
                    type="primary" if uses_aids == "No" else "secondary"):
            st.session_state.form_data['adl']['uses_mobility_aids'] = "No"
            st.rerun()

    if uses_aids == "Yes":
        mobility_aids = st.multiselect(
            "Which mobility aids do you use? (Select all that apply)",
            options=["Cane", "Walker", "Wheelchair", "Scooter", "Grab bars", "Other"],
            default=st.session_state.form_data['adl'].get('mobility_aids_list', []),
            key="mobility_aids_list"
        )
        st.session_state.form_data['adl']['mobility_aids_list'] = mobility_aids


def section_iadl():
    """Section 6: Instrumental Activities of Daily Living (IADL)"""
    st.header("Daily Activities - Complex")
    st.markdown("These questions ask about more complex daily activities. Please select the answer that best describes your current ability.")

    iadl_activities = [
        ("telephone", "USING THE TELEPHONE", "Making and receiving phone calls"),
        ("shopping", "SHOPPING", "Getting groceries and other items"),
        ("food_prep", "PREPARING FOOD", "Planning and cooking meals"),
        ("housekeeping", "HOUSEWORK", "Cleaning, laundry, and home maintenance"),
        ("laundry", "DOING LAUNDRY", "Washing and drying clothes"),
        ("transportation", "TRANSPORTATION", "Getting to places outside walking distance"),
        ("medications", "TAKING MEDICATIONS", "Taking the right medication at the right time"),
        ("finances", "MANAGING MONEY", "Paying bills and managing finances"),
    ]

    for key, activity, description in iadl_activities:
        st.markdown("---")
        st.markdown(f"### {activity}")
        st.markdown(f"*{description}*")

        current_value = st.session_state.form_data['iadl'].get(key, None)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("I can do this\nBY MYSELF", key=f"iadl_{key}_independent", use_container_width=True,
                        type="primary" if current_value == "Independent" else "secondary"):
                st.session_state.form_data['iadl'][key] = "Independent"
                st.rerun()

        with col2:
            if st.button("I need\nSOME HELP", key=f"iadl_{key}_assistance", use_container_width=True,
                        type="primary" if current_value == "Needs Assistance" else "secondary"):
                st.session_state.form_data['iadl'][key] = "Needs Assistance"
                st.rerun()

        with col3:
            if st.button("I CANNOT\ndo this", key=f"iadl_{key}_unable", use_container_width=True,
                        type="primary" if current_value == "Unable" else "secondary"):
                st.session_state.form_data['iadl'][key] = "Unable"
                st.rerun()

        if current_value:
            st.info(f"Your answer: **{current_value}**")

    # Living situation
    st.markdown("---")
    st.markdown("### Living Situation")

    living_situation = st.selectbox(
        "Where do you currently live?",
        options=[
            "Own home - alone",
            "Own home - with spouse/partner",
            "Own home - with family",
            "Apartment/Condo - alone",
            "Apartment/Condo - with others",
            "Retirement residence",
            "Assisted living facility",
            "Long-term care facility",
            "Other"
        ],
        index=0,
        key="living_situation"
    )
    st.session_state.form_data['iadl']['living_situation'] = living_situation

    # Caregiver
    st.markdown("---")
    st.markdown("### Support System")
    st.markdown("#### Do you have someone who helps you regularly?")

    has_caregiver = st.session_state.form_data['iadl'].get('has_caregiver', None)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES", key="caregiver_yes", use_container_width=True,
                    type="primary" if has_caregiver == "Yes" else "secondary"):
            st.session_state.form_data['iadl']['has_caregiver'] = "Yes"
            st.rerun()

    with col2:
        if st.button("NO", key="caregiver_no", use_container_width=True,
                    type="primary" if has_caregiver == "No" else "secondary"):
            st.session_state.form_data['iadl']['has_caregiver'] = "No"
            st.rerun()

    if has_caregiver == "Yes":
        caregiver_relation = st.text_input(
            "Who helps you? (relationship)",
            value=st.session_state.form_data['iadl'].get('caregiver_relation', ''),
            key="caregiver_relation"
        )
        st.session_state.form_data['iadl']['caregiver_relation'] = caregiver_relation


def section_medical_history():
    """Section 7: Medical History"""
    st.header("Medical History")
    st.markdown("Please tell us about your past and current medical conditions.")

    conditions = [
        ("heart_disease", "Heart Disease", "Heart attack, heart failure, irregular heartbeat"),
        ("high_blood_pressure", "High Blood Pressure", "Hypertension"),
        ("diabetes", "Diabetes", "Type 1 or Type 2 diabetes"),
        ("stroke", "Stroke or TIA", "Mini-stroke or transient ischemic attack"),
        ("cancer", "Cancer", "Any type of cancer, past or present"),
        ("arthritis", "Arthritis", "Joint pain, osteoarthritis, rheumatoid arthritis"),
        ("osteoporosis", "Osteoporosis", "Weak or brittle bones"),
        ("lung_disease", "Lung Disease", "COPD, emphysema, asthma"),
        ("kidney_disease", "Kidney Disease", "Chronic kidney disease"),
        ("depression", "Depression or Anxiety", "Mental health conditions"),
        ("dementia", "Memory Problems", "Dementia, Alzheimer's, or cognitive impairment"),
        ("parkinsons", "Parkinson's Disease", "Movement disorder"),
    ]

    st.markdown("### Do you have or have you had any of these conditions?")

    for key, condition, description in conditions:
        st.markdown("---")
        st.markdown(f"### {condition}")
        st.markdown(f"*{description}*")

        current_value = st.session_state.form_data['medical_history'].get(key, None)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("YES", key=f"med_{key}_yes", use_container_width=True,
                        type="primary" if current_value == "Yes" else "secondary"):
                st.session_state.form_data['medical_history'][key] = "Yes"
                st.rerun()

        with col2:
            if st.button("NO", key=f"med_{key}_no", use_container_width=True,
                        type="primary" if current_value == "No" else "secondary"):
                st.session_state.form_data['medical_history'][key] = "No"
                st.rerun()

        with col3:
            if st.button("NOT SURE", key=f"med_{key}_unsure", use_container_width=True,
                        type="primary" if current_value == "Not Sure" else "secondary"):
                st.session_state.form_data['medical_history'][key] = "Not Sure"
                st.rerun()

        if current_value:
            st.info(f"Your answer: **{current_value}**")

    # Surgeries
    st.markdown("---")
    st.markdown("### Past Surgeries")
    st.markdown("#### Have you had any surgeries?")

    had_surgeries = st.session_state.form_data['medical_history'].get('had_surgeries', None)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES", key="surgery_yes", use_container_width=True,
                    type="primary" if had_surgeries == "Yes" else "secondary"):
            st.session_state.form_data['medical_history']['had_surgeries'] = "Yes"
            st.rerun()

    with col2:
        if st.button("NO", key="surgery_no", use_container_width=True,
                    type="primary" if had_surgeries == "No" else "secondary"):
            st.session_state.form_data['medical_history']['had_surgeries'] = "No"
            st.rerun()

    if had_surgeries == "Yes":
        surgeries_list = st.text_area(
            "Please list your surgeries and approximate dates:",
            value=st.session_state.form_data['medical_history'].get('surgeries_list', ''),
            key="surgeries_list",
            height=150
        )
        st.session_state.form_data['medical_history']['surgeries_list'] = surgeries_list

    # Hospitalizations
    st.markdown("---")
    st.markdown("### Recent Hospitalizations")
    st.markdown("#### Have you been hospitalized in the past year?")

    hospitalized = st.session_state.form_data['medical_history'].get('hospitalized_past_year', None)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("YES", key="hosp_yes", use_container_width=True,
                    type="primary" if hospitalized == "Yes" else "secondary"):
            st.session_state.form_data['medical_history']['hospitalized_past_year'] = "Yes"
            st.rerun()

    with col2:
        if st.button("NO", key="hosp_no", use_container_width=True,
                    type="primary" if hospitalized == "No" else "secondary"):
            st.session_state.form_data['medical_history']['hospitalized_past_year'] = "No"
            st.rerun()

    if hospitalized == "Yes":
        hospitalization_reason = st.text_area(
            "Please describe the reason for hospitalization:",
            value=st.session_state.form_data['medical_history'].get('hospitalization_reason', ''),
            key="hospitalization_reason",
            height=100
        )
        st.session_state.form_data['medical_history']['hospitalization_reason'] = hospitalization_reason

    # Other conditions
    st.markdown("---")
    other_conditions = st.text_area(
        "Any other medical conditions not mentioned above?",
        value=st.session_state.form_data['medical_history'].get('other_conditions', ''),
        key="other_conditions",
        height=150
    )
    st.session_state.form_data['medical_history']['other_conditions'] = other_conditions


def section_review():
    """Section 8: Review and Submit"""
    st.header("Review Your Answers")
    st.markdown("Please review your information below. You can go back to any section to make changes.")

    # Demographics Summary
    with st.expander("Personal Information", expanded=True):
        demo = st.session_state.form_data['demographics']
        if demo:
            st.markdown(f"**Name:** {demo.get('first_name', '')} {demo.get('last_name', '')}")
            st.markdown(f"**Date of Birth:** {demo.get('date_of_birth', 'Not provided')}")
            st.markdown(f"**Sex:** {demo.get('sex', 'Not provided')}")
            st.markdown(f"**Phone:** {demo.get('phone', 'Not provided')}")
            st.markdown(f"**Health Card:** {demo.get('health_card', 'Not provided')}")
            st.markdown(f"**Emergency Contact:** {demo.get('emergency_name', 'Not provided')} ({demo.get('emergency_relation', '')})")

    # Symptoms Summary
    with st.expander("Current Symptoms"):
        symptoms = st.session_state.form_data['symptoms']
        positive_symptoms = [k for k, v in symptoms.items() if v == "Yes" and not k.endswith('_location') and not k.endswith('_level') and not k.endswith('_count') and k != 'other_symptoms']
        if positive_symptoms:
            st.markdown("**Reported symptoms:**")
            for s in positive_symptoms:
                st.markdown(f"- {s.replace('_', ' ').title()}")
        else:
            st.markdown("No significant symptoms reported")

    # Cognitive Summary
    with st.expander("Memory and Thinking"):
        cognitive = st.session_state.form_data['cognitive']
        concerns = [k for k, v in cognitive.items() if v == "Yes" or v == "Sometimes"]
        if concerns:
            st.markdown("**Areas of concern:**")
            for c in concerns:
                if c not in ['today_date', 'day_of_week', 'season', 'current_year', 'hospital_name', 'city', 'other_concerns']:
                    st.markdown(f"- {c.replace('_', ' ').title()}")

    # Medications Summary
    with st.expander("Medications"):
        meds = st.session_state.form_data['medications']
        if meds.get('taking_medications') == "Yes":
            med_list = meds.get('medications_list', [])
            if med_list:
                for m in med_list:
                    if m.get('name'):
                        st.markdown(f"- {m.get('name', '')} {m.get('dose', '')} ({m.get('frequency', '')})")
        else:
            st.markdown("No medications reported")

    # ADL Summary
    with st.expander("Daily Activities - Basic"):
        adl = st.session_state.form_data['adl']
        needs_help = [k for k, v in adl.items() if v in ["Needs Assistance", "Dependent"]]
        if needs_help:
            st.markdown("**Activities requiring assistance:**")
            for a in needs_help:
                st.markdown(f"- {a.replace('_', ' ').title()}: {adl[a]}")
        else:
            st.markdown("Independent in all basic activities")

    # IADL Summary
    with st.expander("Daily Activities - Complex"):
        iadl = st.session_state.form_data['iadl']
        needs_help = [k for k, v in iadl.items() if v in ["Needs Assistance", "Unable"]]
        if needs_help:
            st.markdown("**Activities requiring assistance:**")
            for a in needs_help:
                if a not in ['living_situation', 'has_caregiver', 'caregiver_relation']:
                    st.markdown(f"- {a.replace('_', ' ').title()}: {iadl[a]}")

    # Medical History Summary
    with st.expander("Medical History"):
        history = st.session_state.form_data['medical_history']
        conditions = [k for k, v in history.items() if v == "Yes" and not k.startswith('had_') and not k.startswith('hospitalized') and k != 'surgeries_list' and k != 'hospitalization_reason' and k != 'other_conditions']
        if conditions:
            st.markdown("**Reported conditions:**")
            for c in conditions:
                st.markdown(f"- {c.replace('_', ' ').title()}")

    st.markdown("---")
    st.markdown("### Confirmation")

    confirmation = st.checkbox(
        "I confirm that the information provided is accurate to the best of my knowledge.",
        key="confirmation"
    )

    if confirmation:
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("SUBMIT FORM", key="submit_form", use_container_width=True, type="primary"):
                st.session_state.form_completed = True
                st.rerun()

        with col2:
            pdf_buffer = generate_pdf_report()
            st.download_button(
                label="DOWNLOAD PDF",
                data=pdf_buffer,
                file_name=f"patient_intake_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )


def generate_pdf_report():
    """Generate PDF report of the form data"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a365d')
    )

    section_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#2c5282')
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )

    elements = []

    # Title
    elements.append(Paragraph("Geriatric Clinic - Patient Intake Form", title_style))
    elements.append(Paragraph("Jewish General Hospital", styles['Normal']))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Demographics
    elements.append(Paragraph("PATIENT INFORMATION", section_style))
    demo = st.session_state.form_data['demographics']
    demo_data = [
        ["Name:", f"{demo.get('first_name', '')} {demo.get('last_name', '')}"],
        ["Date of Birth:", str(demo.get('date_of_birth', ''))],
        ["Sex:", demo.get('sex', '')],
        ["Phone:", demo.get('phone', '')],
        ["Health Card:", demo.get('health_card', '')],
        ["Emergency Contact:", f"{demo.get('emergency_name', '')} ({demo.get('emergency_relation', '')})"],
        ["Emergency Phone:", demo.get('emergency_phone', '')],
        ["Preferred Language:", demo.get('preferred_language', '')],
    ]

    demo_table = Table(demo_data, colWidths=[2*inch, 4*inch])
    demo_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(demo_table)
    elements.append(Spacer(1, 15))

    # Symptoms
    elements.append(Paragraph("CURRENT SYMPTOMS", section_style))
    symptoms = st.session_state.form_data['symptoms']
    symptom_names = {
        'pain': 'Pain',
        'dizziness': 'Dizziness',
        'fatigue': 'Fatigue',
        'breathing': 'Breathing difficulty',
        'sleep': 'Sleep problems',
        'appetite': 'Appetite changes',
        'vision': 'Vision problems',
        'hearing': 'Hearing problems',
        'balance': 'Balance problems',
        'falls': 'Falls'
    }

    for key, name in symptom_names.items():
        if symptoms.get(key):
            elements.append(Paragraph(f"<b>{name}:</b> {symptoms.get(key, 'Not answered')}", normal_style))
            if key == 'pain' and symptoms.get('pain') == 'Yes':
                if symptoms.get('pain_location'):
                    elements.append(Paragraph(f"  - Location: {symptoms.get('pain_location')}", normal_style))
                if symptoms.get('pain_level'):
                    elements.append(Paragraph(f"  - Severity: {symptoms.get('pain_level')}/10", normal_style))

    if symptoms.get('other_symptoms'):
        elements.append(Paragraph(f"<b>Other symptoms:</b> {symptoms.get('other_symptoms')}", normal_style))

    elements.append(Spacer(1, 15))

    # Cognitive
    elements.append(Paragraph("COGNITIVE ASSESSMENT", section_style))
    cognitive = st.session_state.form_data['cognitive']

    cognitive_items = [
        ('forget_names', 'Forgets names'),
        ('forget_appointments', 'Forgets appointments'),
        ('lose_items', 'Misplaces items'),
        ('repeat_questions', 'Repeats questions'),
        ('difficulty_decisions', 'Difficulty with decisions'),
        ('get_lost', 'Gets lost in familiar places'),
    ]

    for key, name in cognitive_items:
        if cognitive.get(key):
            elements.append(Paragraph(f"<b>{name}:</b> {cognitive.get(key)}", normal_style))

    if cognitive.get('other_concerns'):
        elements.append(Paragraph(f"<b>Other concerns:</b> {cognitive.get('other_concerns')}", normal_style))

    elements.append(Spacer(1, 15))

    # Medications
    elements.append(Paragraph("MEDICATIONS", section_style))
    meds = st.session_state.form_data['medications']

    if meds.get('taking_medications') == "Yes":
        med_list = meds.get('medications_list', [])
        for m in med_list:
            if m.get('name'):
                elements.append(Paragraph(f"- {m.get('name', '')} {m.get('dose', '')} ({m.get('frequency', '')})", normal_style))

        if meds.get('needs_help'):
            elements.append(Paragraph(f"<b>Needs help with medications:</b> {meds.get('needs_help')}", normal_style))
        if meds.get('miss_doses'):
            elements.append(Paragraph(f"<b>Misses doses:</b> {meds.get('miss_doses')}", normal_style))
    else:
        elements.append(Paragraph("No medications reported", normal_style))

    if meds.get('has_allergies') == "Yes":
        elements.append(Paragraph(f"<b>Drug allergies:</b> {meds.get('allergies_list', 'Not specified')}", normal_style))

    elements.append(Spacer(1, 15))

    # ADL
    elements.append(Paragraph("BASIC ACTIVITIES OF DAILY LIVING (ADL)", section_style))
    adl = st.session_state.form_data['adl']

    adl_items = ['bathing', 'dressing', 'toileting', 'transferring', 'continence', 'feeding']
    for item in adl_items:
        if adl.get(item):
            elements.append(Paragraph(f"<b>{item.title()}:</b> {adl.get(item)}", normal_style))

    if adl.get('uses_mobility_aids') == "Yes":
        aids = adl.get('mobility_aids_list', [])
        elements.append(Paragraph(f"<b>Mobility aids:</b> {', '.join(aids)}", normal_style))

    elements.append(Spacer(1, 15))

    # IADL
    elements.append(Paragraph("INSTRUMENTAL ACTIVITIES OF DAILY LIVING (IADL)", section_style))
    iadl = st.session_state.form_data['iadl']

    iadl_items = ['telephone', 'shopping', 'food_prep', 'housekeeping', 'laundry', 'transportation', 'medications', 'finances']
    for item in iadl_items:
        if iadl.get(item):
            elements.append(Paragraph(f"<b>{item.replace('_', ' ').title()}:</b> {iadl.get(item)}", normal_style))

    if iadl.get('living_situation'):
        elements.append(Paragraph(f"<b>Living situation:</b> {iadl.get('living_situation')}", normal_style))
    if iadl.get('has_caregiver') == "Yes":
        elements.append(Paragraph(f"<b>Caregiver:</b> {iadl.get('caregiver_relation', 'Yes')}", normal_style))

    elements.append(Spacer(1, 15))

    # Medical History
    elements.append(Paragraph("MEDICAL HISTORY", section_style))
    history = st.session_state.form_data['medical_history']

    conditions = [
        ('heart_disease', 'Heart Disease'),
        ('high_blood_pressure', 'High Blood Pressure'),
        ('diabetes', 'Diabetes'),
        ('stroke', 'Stroke/TIA'),
        ('cancer', 'Cancer'),
        ('arthritis', 'Arthritis'),
        ('osteoporosis', 'Osteoporosis'),
        ('lung_disease', 'Lung Disease'),
        ('kidney_disease', 'Kidney Disease'),
        ('depression', 'Depression/Anxiety'),
        ('dementia', 'Memory Problems'),
        ('parkinsons', "Parkinson's Disease"),
    ]

    positive_conditions = [(name, history.get(key)) for key, name in conditions if history.get(key) == "Yes"]
    if positive_conditions:
        for name, _ in positive_conditions:
            elements.append(Paragraph(f"- {name}", normal_style))
    else:
        elements.append(Paragraph("No significant medical conditions reported", normal_style))

    if history.get('had_surgeries') == "Yes":
        elements.append(Paragraph(f"<b>Past surgeries:</b> {history.get('surgeries_list', 'Not specified')}", normal_style))

    if history.get('hospitalized_past_year') == "Yes":
        elements.append(Paragraph(f"<b>Recent hospitalization:</b> {history.get('hospitalization_reason', 'Not specified')}", normal_style))

    if history.get('other_conditions'):
        elements.append(Paragraph(f"<b>Other conditions:</b> {history.get('other_conditions')}", normal_style))

    # Footer
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("_" * 50, normal_style))
    elements.append(Paragraph(f"Form completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Paragraph("This form was completed electronically by the patient.", styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def render_navigation():
    """Render navigation buttons"""
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.session_state.current_section > 0:
            if st.button("BACK", key="nav_back", use_container_width=True):
                st.session_state.current_section -= 1
                st.rerun()

    with col3:
        if st.session_state.current_section < 7:
            if st.button("NEXT", key="nav_next", use_container_width=True, type="primary"):
                st.session_state.current_section += 1
                st.rerun()


def render_completion_page():
    """Render the form completion page"""
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="color: #276749; font-size: 48px;">Thank You!</h1>
        <p style="font-size: 28px; margin: 30px 0;">Your form has been submitted successfully.</p>
        <p style="font-size: 24px;">Please return the tablet to the receptionist.</p>
        <p style="font-size: 24px;">A healthcare professional will be with you shortly.</p>
    </div>
    """, unsafe_allow_html=True)

    # Allow starting a new form
    st.markdown("---")
    if st.button("START NEW FORM", key="new_form", use_container_width=True):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()


def main():
    """Main application function"""
    initialize_session_state()

    # Header
    st.title("Jewish General Hospital")
    st.markdown("### Geriatric Clinic - Patient Intake Form")

    if st.session_state.form_completed:
        render_completion_page()
        return

    # Progress bar
    render_progress_bar()

    # Render current section
    sections = [
        section_demographics,
        section_symptoms,
        section_cognitive,
        section_medications,
        section_adl,
        section_iadl,
        section_medical_history,
        section_review
    ]

    sections[st.session_state.current_section]()

    # Navigation
    render_navigation()

    # Help text
    st.markdown("---")
    st.markdown("*Need help? Please ask the receptionist for assistance.*")


if __name__ == "__main__":
    main()
