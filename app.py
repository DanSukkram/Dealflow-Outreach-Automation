import streamlit as st
import pandas as pd
import smtplib
import time
import re
from datetime import datetime
from io import BytesIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ------------------------------------------------------
# Page setup
# ------------------------------------------------------

st.set_page_config(
    page_title="DealFlow Outreach Automation",
    page_icon="✉️",
    layout="wide"
)


# ------------------------------------------------------
# DealFlow-style CSS
# ------------------------------------------------------

st.markdown(
    """
    <style>
        :root {
            --df-navy: #081f33;
            --df-navy-2: #0d2f4f;
            --df-blue: #123d64;
            --df-gold: #c8a45d;
            --df-gold-soft: #f4ead1;
            --df-bg: #f7f6f1;
            --df-card: #ffffff;
            --df-border: #ded8ca;
            --df-text: #102033;
            --df-muted: #64748b;
            --df-green: #15803d;
            --df-red: #b91c1c;
            --df-amber: #b45309;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(200, 164, 93, 0.12), transparent 34%),
                linear-gradient(180deg, #fbfaf6 0%, var(--df-bg) 100%);
            color: var(--df-text);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 1.4rem;
            padding-bottom: 2.2rem;
        }

        h1, h2, h3 {
            color: var(--df-navy) !important;
            letter-spacing: -0.02em;
        }

        p, label, span, div {
            color: var(--df-text);
            font-size: 14px;
        }

        .hero-card {
            background: linear-gradient(135deg, var(--df-navy) 0%, var(--df-blue) 72%, #174b78 100%);
            border: 1px solid rgba(200, 164, 93, 0.42);
            border-radius: 22px;
            padding: 30px;
            margin-bottom: 18px;
            box-shadow: 0 18px 45px rgba(8, 31, 51, 0.14);
            position: relative;
            overflow: hidden;
        }

        .hero-card:after {
            content: "";
            position: absolute;
            right: -80px;
            top: -90px;
            width: 250px;
            height: 250px;
            border-radius: 50%;
            background: rgba(200, 164, 93, 0.16);
        }

        .hero-eyebrow {
            color: var(--df-gold);
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.16em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .hero-title {
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 10px;
            color: #ffffff;
            line-height: 1.1;
        }

        .hero-subtitle {
            font-size: 15px;
            color: #dbe7f2;
            max-width: 820px;
            line-height: 1.65;
        }

        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 18px;
        }

        .pill {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(200, 164, 93, 0.35);
            padding: 7px 12px;
            border-radius: 999px;
            font-size: 12px;
            color: #f7ecd2;
            font-weight: 650;
        }

        .carousel-shell {
            background: var(--df-card);
            border: 1px solid var(--df-border);
            border-radius: 22px;
            padding: 26px;
            margin: 16px 0;
            box-shadow: 0 14px 38px rgba(8, 31, 51, 0.08);
            min-height: 570px;
        }

        .page-head {
            border-bottom: 1px solid #ebe4d6;
            padding-bottom: 16px;
            margin-bottom: 20px;
        }

        .step-label {
            display: inline-block;
            background: var(--df-gold-soft);
            color: #7c5c18;
            border: 1px solid rgba(200, 164, 93, 0.45);
            padding: 5px 11px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            margin-bottom: 10px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 760;
            color: var(--df-navy);
            margin-bottom: 4px;
        }

        .section-desc {
            font-size: 14px;
            color: var(--df-muted);
            line-height: 1.55;
            max-width: 850px;
        }

        .small-card {
            background: #fffdf8;
            border: 1px solid #e7dfcf;
            border-radius: 16px;
            padding: 16px;
            height: 100%;
        }

        .metric-number {
            font-size: 26px;
            font-weight: 800;
            color: var(--df-navy);
        }

        .metric-label {
            font-size: 12px;
            color: var(--df-muted);
        }

        .success-box,
        .warning-box,
        .error-box,
        .info-box {
            border-radius: 14px;
            padding: 13px 15px;
            font-size: 13px;
            margin: 11px 0;
            border: 1px solid transparent;
        }

        .success-box {
            background: #ecfdf3;
            border-color: #bbf7d0;
            color: #166534;
        }

        .warning-box {
            background: #fffbeb;
            border-color: #fde68a;
            color: #92400e;
        }

        .error-box {
            background: #fef2f2;
            border-color: #fecaca;
            color: #991b1b;
        }

        .info-box {
            background: #eff6ff;
            border-color: #bfdbfe;
            color: #1e40af;
        }

        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: var(--df-text) !important;
            border: 1px solid #d8d2c5 !important;
            border-radius: 12px !important;
        }

        .stFileUploader {
            background: #fffdf8;
            border: 1px dashed var(--df-gold);
            border-radius: 16px;
            padding: 18px;
        }

        .stButton > button {
            background: var(--df-navy) !important;
            color: white !important;
            border-radius: 12px !important;
            border: 1px solid var(--df-navy) !important;
            padding: 0.65rem 1.05rem !important;
            font-weight: 700 !important;
            transition: 0.15s ease-in-out;
        }

        .stButton > button:hover {
            background: var(--df-blue) !important;
            border-color: var(--df-blue) !important;
            transform: translateY(-1px);
        }

        .stButton > button:disabled {
            background: #cbd5e1 !important;
            border-color: #cbd5e1 !important;
            color: #64748b !important;
        }

        .stDownloadButton > button {
            background: var(--df-gold) !important;
            color: var(--df-navy) !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 800 !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 14px;
            border: 1px solid #e2dccf;
            overflow: hidden;
        }

        .progress-wrap {
            display: flex;
            gap: 8px;
            margin: 14px 0 18px 0;
            align-items: center;
        }

        .progress-step {
            flex: 1;
            height: 7px;
            border-radius: 99px;
            background: #e6dfd1;
            overflow: hidden;
        }

        .progress-step-active {
            background: linear-gradient(90deg, var(--df-gold), #e4c977);
        }

        .progress-labels {
            display: flex;
            justify-content: space-between;
            gap: 8px;
            margin-top: -6px;
            margin-bottom: 16px;
        }

        .progress-label {
            flex: 1;
            font-size: 11px;
            color: #64748b;
            text-align: center;
        }

        .progress-label-current {
            color: var(--df-navy);
            font-weight: 800;
        }

        .nav-card {
            background: #fffdf8;
            border: 1px solid #e7dfcf;
            border-radius: 16px;
            padding: 14px 16px;
            margin-top: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# Session state
# ------------------------------------------------------

PAGES = [
    "Credentials",
    "Upload",
    "Filter",
    "Template",
    "Controls",
    "Preview",
    "Confirm",
]

if "page" not in st.session_state:
    st.session_state.page = 0

if "df_base" not in st.session_state:
    st.session_state.df_base = None

if "df_working" not in st.session_state:
    st.session_state.df_working = None

if "selected_sheet_names" not in st.session_state:
    st.session_state.selected_sheet_names = []

if "deduped_count" not in st.session_state:
    st.session_state.deduped_count = 0

if "used_placeholders" not in st.session_state:
    st.session_state.used_placeholders = []

if "missing_personalization_df" not in st.session_state:
    st.session_state.missing_personalization_df = pd.DataFrame()


# ------------------------------------------------------
# Generic helpers
# ------------------------------------------------------

def get_secret_value(key):
    try:
        return st.secrets[key]
    except Exception:
        return None


def go_next():
    if st.session_state.page < len(PAGES) - 1:
        st.session_state.page += 1
        st.rerun()


def go_back():
    if st.session_state.page > 0:
        st.session_state.page -= 1
        st.rerun()


def render_progress():
    st.markdown('<div class="progress-wrap">', unsafe_allow_html=True)
    cols = st.columns(len(PAGES))
    for i, col in enumerate(cols):
        cls = "progress-step progress-step-active" if i <= st.session_state.page else "progress-step"
        with col:
            st.markdown(f'<div class="{cls}"></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    cols = st.columns(len(PAGES))
    for i, col in enumerate(cols):
        label_cls = "progress-label progress-label-current" if i == st.session_state.page else "progress-label"
        with col:
            st.markdown(f'<div class="{label_cls}">{i + 1}. {PAGES[i]}</div>', unsafe_allow_html=True)


def render_nav(next_enabled=True, next_label="Next →", back_enabled=True):
    st.markdown('<div class="nav-card">', unsafe_allow_html=True)
    left, middle, right = st.columns([1, 2, 1])

    with left:
        if st.button("← Back", disabled=(not back_enabled or st.session_state.page == 0), use_container_width=True):
            go_back()

    with middle:
        st.markdown(
            f"""
            <div style="text-align:center; padding-top:10px; color:#64748b; font-size:13px;">
                Page {st.session_state.page + 1} of {len(PAGES)} · {PAGES[st.session_state.page]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with right:
        if st.button(next_label, disabled=(not next_enabled or st.session_state.page == len(PAGES) - 1), use_container_width=True):
            go_next()

    st.markdown('</div>', unsafe_allow_html=True)


def render_page_header(step_number, title, description):
    st.markdown(
        f"""
        <div class="page-head">
            <div class="step-label">Step {step_number}</div>
            <div class="section-title">{title}</div>
            <div class="section-desc">{description}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_metric(number, label):
    st.markdown(
        f"""
        <div class="small-card">
            <div class="metric-number">{number}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def clean_text(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def normalize_header(value):
    return clean_text(value).lower().replace("\n", " ").strip()


def is_valid_email(email):
    if not isinstance(email, str):
        return False

    email = email.strip()
    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(email_pattern, email) is not None


def parse_email_list(email_text):
    if not email_text:
        return []

    email_text = str(email_text).replace(";", ",")

    return [
        email.strip()
        for email in email_text.split(",")
        if email.strip()
    ]


def extract_placeholders(text):
    if not text:
        return []

    return sorted(set(re.findall(r"\{([A-Za-z0-9_]+)\}", text)))


def validate_placeholders(subject_template, body_template, available_columns):
    subject_placeholders = extract_placeholders(subject_template)
    body_placeholders = extract_placeholders(body_template)

    all_placeholders = sorted(set(subject_placeholders + body_placeholders))
    available_columns_set = set(available_columns)

    unknown_placeholders = [
        placeholder for placeholder in all_placeholders
        if placeholder not in available_columns_set
    ]

    return all_placeholders, unknown_placeholders


def get_missing_personalization_summary(df, placeholders):
    summary = []

    for placeholder in placeholders:
        if placeholder not in df.columns:
            continue

        missing_count = df[placeholder].apply(
            lambda value: clean_text(value) == ""
        ).sum()

        if missing_count > 0:
            summary.append(
                {
                    "placeholder": placeholder,
                    "missing_rows": int(missing_count),
                    "total_rows": int(len(df))
                }
            )

    return pd.DataFrame(summary)


def derive_greeting_name(contact_name):
    name = clean_text(contact_name)

    if not name:
        return ""

    name = re.sub(
        r"^(mr\.?|mrs\.?|ms\.?|miss|dr\.?|prof\.?)\s+",
        "",
        name,
        flags=re.IGNORECASE
    ).strip()

    parts = [part for part in name.split() if part]

    if not parts:
        return ""

    return parts[-1]


def detect_standard_header_row(raw_df):
    for index, row in raw_df.iterrows():
        headers = [normalize_header(value) for value in row.tolist()]

        has_company = any(
            header in ["company", "company name", "company's name"]
            for header in headers
        )

        has_email = any(header == "email" for header in headers)

        has_contact = any(
            header in [
                "name",
                "contact name",
                "contact name - tier 1",
                "contact name tier 1",
                "2nd pic",
                "contact name - tier 2",
                "contact name tier 2",
                "pic"
            ]
            for header in headers
        )

        if has_company and has_email and has_contact:
            return index

    return None


def find_first_matching_column(headers, accepted_headers):
    normalized_headers = [normalize_header(header) for header in headers]

    for accepted_header in accepted_headers:
        accepted_header = accepted_header.lower().strip()

        for index, header in enumerate(normalized_headers):
            if header == accepted_header:
                return index

    return None


def find_column_containing(headers, accepted_keywords):
    normalized_headers = [normalize_header(header) for header in headers]

    for keyword in accepted_keywords:
        keyword = keyword.lower().strip()

        for index, header in enumerate(normalized_headers):
            if keyword in header:
                return index

    return None


def get_tier_from_contact_header(contact_header, contact_number):
    header = normalize_header(contact_header)

    if "tier 1" in header:
        return "Tier 1"

    if "tier 2" in header:
        return "Tier 2"

    if "tier 3" in header:
        return "Tier 3"

    if "2nd" in header or "second" in header:
        return "Tier 2"

    if "3rd" in header or "third" in header:
        return "Tier 3"

    return f"Tier {contact_number}"


def validate_standard_sourcing_format(raw_df, sheet_name):
    issues = []

    header_row_index = detect_standard_header_row(raw_df)

    if header_row_index is None:
        issues.append(
            f"{sheet_name}: Could not detect the standard header row. Make sure the sheet has Company / Company Name, contact name fields, and Email columns."
        )
        return issues

    headers = [clean_text(value) for value in raw_df.iloc[header_row_index].tolist()]
    normalized_headers = [normalize_header(header) for header in headers]

    company_col_index = find_first_matching_column(
        headers,
        ["Company", "Company Name", "Company's Name"]
    )

    if company_col_index is None:
        issues.append(f"{sheet_name}: Missing company column. Use 'Company' or 'Company Name'.")

    email_col_indexes = [
        index for index, header in enumerate(normalized_headers)
        if header == "email"
    ]

    if not email_col_indexes:
        issues.append(f"{sheet_name}: No Email columns found. Email columns must be named exactly 'Email'.")

    accepted_contact_headers = [
        "name",
        "contact name",
        "contact name - tier 1",
        "contact name tier 1",
        "contact name - tier 2",
        "contact name tier 2",
        "contact name - tier 3",
        "contact name tier 3",
        "2nd pic",
        "3rd pic",
        "pic"
    ]

    accepted_title_headers = [
        "position",
        "title",
        "designation",
        "role",
        "job title"
    ]

    for email_col_index in email_col_indexes:
        if email_col_index < 2:
            issues.append(
                f"{sheet_name}: An Email column is too far left. Each Email column must have contact name and position/title before it."
            )
            continue

        contact_header = normalize_header(headers[email_col_index - 2])
        title_header = normalize_header(headers[email_col_index - 1])

        contact_ok = (
            contact_header in accepted_contact_headers
            or "contact name" in contact_header
            or "pic" in contact_header
        )

        title_ok = title_header in accepted_title_headers

        if not contact_ok:
            issues.append(
                f"{sheet_name}: The column two places before Email should be contact name, but found '{headers[email_col_index - 2]}'."
            )

        if not title_ok:
            issues.append(
                f"{sheet_name}: The column directly before Email should be Position or Title, but found '{headers[email_col_index - 1]}'."
            )

    return issues


def flatten_standard_sourcing_sheet(raw_df, sheet_name):
    header_row_index = detect_standard_header_row(raw_df)

    if header_row_index is None:
        return pd.DataFrame()

    headers = [clean_text(value) for value in raw_df.iloc[header_row_index].tolist()]
    normalized_headers = [normalize_header(header) for header in headers]

    data_df = raw_df.iloc[header_row_index + 1:].copy()

    company_col_index = find_first_matching_column(headers, ["Company", "Company Name", "Company's Name"])
    linkedin_col_index = find_first_matching_column(headers, ["Linkedin", "LinkedIn", "Company LinkedIn"])
    type_col_index = find_first_matching_column(headers, ["Type", "Sector", "Industry"])
    website_col_index = find_first_matching_column(headers, ["Website", "Company Website"])
    country_col_index = find_first_matching_column(headers, ["Country", "Location", "Market"])
    revenue_col_index = find_column_containing(headers, ["revenue"])
    source_status_col_index = find_first_matching_column(headers, ["Status"])
    ownership_col_index = find_first_matching_column(headers, ["Ownership / Shareholders", "Ownership", "Shareholders"])
    target_classification_col_index = find_first_matching_column(headers, ["Target classification", "Target Classification", "Classification"])
    note_col_index = find_first_matching_column(headers, ["Note", "Notes"])
    greeting_name_col_index = find_first_matching_column(headers, ["Greeting Name", "Greeting", "First Name", "Preferred Name"])

    email_col_indexes = [
        index for index, header in enumerate(normalized_headers)
        if header == "email"
    ]

    recipients = []

    for raw_index, row in data_df.iterrows():
        company_name = clean_text(row.iloc[company_col_index]) if company_col_index is not None else ""

        if not company_name:
            continue

        company_linkedin = clean_text(row.iloc[linkedin_col_index]) if linkedin_col_index is not None else ""
        company_type = clean_text(row.iloc[type_col_index]) if type_col_index is not None else ""
        website = clean_text(row.iloc[website_col_index]) if website_col_index is not None else ""
        country = clean_text(row.iloc[country_col_index]) if country_col_index is not None else ""
        revenue = clean_text(row.iloc[revenue_col_index]) if revenue_col_index is not None else ""
        source_status = clean_text(row.iloc[source_status_col_index]) if source_status_col_index is not None else ""
        ownership = clean_text(row.iloc[ownership_col_index]) if ownership_col_index is not None else ""
        target_classification = clean_text(row.iloc[target_classification_col_index]) if target_classification_col_index is not None else ""
        note = clean_text(row.iloc[note_col_index]) if note_col_index is not None else ""

        contact_number = 0

        for email_col_index in email_col_indexes:
            email = clean_text(row.iloc[email_col_index])

            if not email:
                continue

            contact_number += 1

            contact_name_col_index = email_col_index - 2
            title_col_index = email_col_index - 1

            contact_name = ""
            title = ""
            tier = f"Tier {contact_number}"

            if contact_name_col_index >= 0:
                contact_name = clean_text(row.iloc[contact_name_col_index])
                tier = get_tier_from_contact_header(headers[contact_name_col_index], contact_number)

            if title_col_index >= 0:
                title = clean_text(row.iloc[title_col_index])

            manual_greeting_name = ""
            if greeting_name_col_index is not None and contact_number == 1:
                manual_greeting_name = clean_text(row.iloc[greeting_name_col_index])

            greeting_name = manual_greeting_name if manual_greeting_name else derive_greeting_name(contact_name)

            recipients.append(
                {
                    "source_sheet": sheet_name,
                    "source_excel_row": raw_index + 1,
                    "company_name": company_name,
                    "contact_name": contact_name,
                    "greeting_name": greeting_name,
                    "title": title,
                    "email": email,
                    "tier": tier,
                    "company_linkedin": company_linkedin,
                    "type": company_type,
                    "website": website,
                    "country": country,
                    "revenue": revenue,
                    "source_status": source_status,
                    "ownership_shareholders": ownership,
                    "target_classification": target_classification,
                    "note": note,
                    "status": "",
                    "sent_at": "",
                    "error_message": ""
                }
            )

    return pd.DataFrame(recipients)


def personalize_text(template, row):
    personalized = template

    for column in row.index:
        placeholder = "{" + str(column) + "}"
        value = row[column]

        if pd.isna(value):
            value = ""

        personalized = personalized.replace(placeholder, str(value).strip())

    personalized = personalized.replace("Dear ,", "Dear there,")
    personalized = personalized.replace("Dear nan,", "Dear there,")

    if "{contact_name}" in personalized:
        personalized = personalized.replace("{contact_name}", "there")

    if "{greeting_name}" in personalized:
        personalized = personalized.replace("{greeting_name}", "there")

    return personalized


def send_email(
    to_email,
    subject,
    body,
    sender_name,
    sender_email,
    sender_password,
    smtp_server,
    smtp_port,
    cc_emails=None
):
    if cc_emails is None:
        cc_emails = []

    message = MIMEMultipart()

    if sender_name:
        message["From"] = f"{sender_name} <{sender_email}>"
    else:
        message["From"] = sender_email

    message["To"] = to_email
    message["Subject"] = subject

    if cc_emails:
        message["Cc"] = ", ".join(cc_emails)

    message.attach(MIMEText(body, "plain"))

    all_recipients = [to_email] + cc_emails

    with smtplib.SMTP(smtp_server, int(smtp_port)) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(
            from_addr=sender_email,
            to_addrs=all_recipients,
            msg=message.as_string()
        )


def convert_df_to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Outreach Results")

    return output.getvalue()


# ------------------------------------------------------
# Hero
# ------------------------------------------------------

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-eyebrow">DealFlow Internal Tool</div>
        <div class="hero-title">Outreach Automation Workspace</div>
        <div class="hero-subtitle">
            A controlled email workflow for standardized sourcing sheets. Move page by page, review recipients,
            validate templates, send preview emails, and execute outreach with clear confirmation steps.
        </div>
        <div class="pill-row">
            <div class="pill">Sourcing Workbook Upload</div>
            <div class="pill">Multiple Contacts Per Company</div>
            <div class="pill">Tier Filtering</div>
            <div class="pill">Template Validation</div>
            <div class="pill">Preview Email</div>
            <div class="pill">Status Tracking</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

render_progress()

st.markdown('<div class="carousel-shell">', unsafe_allow_html=True)


# ------------------------------------------------------
# Page 0: Credentials
# ------------------------------------------------------

if st.session_state.page == 0:
    render_page_header(
        "1",
        "Sender Credentials",
        "Enter the sender email credentials and optional CC recipients. Once completed, move to the next page."
    )

    APP_PASSWORD = get_secret_value("APP_PASSWORD")

    if APP_PASSWORD:
        access_code = st.text_input(
            "Internal access code",
            type="password",
            placeholder="Enter team access code",
            key="access_code"
        )

        if access_code != APP_PASSWORD:
            st.markdown(
                '<div class="warning-box">Enter the correct internal access code to continue.</div>',
                unsafe_allow_html=True
            )
            render_nav(next_enabled=False, back_enabled=False)
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        st.markdown('<div class="success-box">Access confirmed.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="warning-box">
            Use an app password where possible. Gmail requires a Google App Password.
            For Outlook or Microsoft 365, SMTP access must be enabled for the mailbox.
        </div>
        """,
        unsafe_allow_html=True
    )

    cred_col1, cred_col2 = st.columns(2)

    with cred_col1:
        email_provider = st.selectbox(
            "Email provider",
            ["Gmail", "Outlook / Microsoft 365", "Custom SMTP"],
            key="email_provider"
        )

    with cred_col2:
        sender_name = st.text_input(
            "Sender name",
            value=st.session_state.get("sender_name", "Dan"),
            key="sender_name"
        )

    if st.session_state.email_provider == "Gmail":
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
    elif st.session_state.email_provider == "Outlook / Microsoft 365":
        smtp_server = "smtp.office365.com"
        smtp_port = 587
    else:
        custom_col1, custom_col2 = st.columns(2)
        with custom_col1:
            smtp_server = st.text_input("SMTP server", placeholder="smtp.example.com", key="custom_smtp_server")
        with custom_col2:
            smtp_port = st.number_input("SMTP port", min_value=1, max_value=9999, value=587, key="custom_smtp_port")

    st.session_state.smtp_server = smtp_server
    st.session_state.smtp_port = smtp_port

    login_col1, login_col2 = st.columns(2)

    with login_col1:
        sender_email = st.text_input(
            "Sender email address",
            placeholder="example@dealflow.sg",
            key="sender_email"
        )

    with login_col2:
        sender_password = st.text_input(
            "Email app password",
            type="password",
            help="Use an app password, not your normal email password.",
            key="sender_password"
        )

    cc_input = st.text_area(
        "CC recipients, optional",
        placeholder="person1@dealflow.sg, person2@dealflow.sg",
        help="Separate multiple CC emails with commas or semicolons.",
        height=90,
        key="cc_input"
    )

    cc_emails = parse_email_list(cc_input)
    st.session_state.cc_emails = cc_emails

    with st.expander("View SMTP and CC settings"):
        st.write("**SMTP server:**", smtp_server)
        st.write("**SMTP port:**", smtp_port)
        st.write("**CC:**", ", ".join(cc_emails) if cc_emails else "None")

    credentials_ready = bool(smtp_server and smtp_port and sender_email and sender_password)

    if credentials_ready:
        st.markdown('<div class="success-box">Credentials entered. Continue to workbook upload.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box">Enter all required sender credentials before continuing.</div>', unsafe_allow_html=True)

    render_nav(next_enabled=credentials_ready, back_enabled=False)


# ------------------------------------------------------
# Page 1: Upload
# ------------------------------------------------------

elif st.session_state.page == 1:
    render_page_header(
        "2",
        "Upload Standardized Sourcing Workbook",
        "Upload your Excel workbook, select sheets, validate the format, and normalize all contacts into recipient rows."
    )

    uploaded_file = st.file_uploader(
        "Upload your outreach Excel file",
        type=["xlsx"],
        key="uploaded_file"
    )

    if not uploaded_file:
        st.markdown(
            """
            <div class="warning-box">
                Waiting for Excel upload. Required structure includes <b>Company</b>, <b>Name</b>, <b>Position</b>, <b>Email</b>,
                and optional second contact fields such as <b>2nd PiC</b>, <b>Position</b>, and <b>Email</b>.
            </div>
            """,
            unsafe_allow_html=True
        )
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    try:
        file_bytes = uploaded_file.getvalue()
        excel_file = pd.ExcelFile(BytesIO(file_bytes))
        sheet_names = excel_file.sheet_names
    except Exception as error:
        st.markdown(f'<div class="error-box">Something went wrong while reading the workbook: {error}</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    selected_sheet_names = st.multiselect(
        "Select sheets to process",
        options=sheet_names,
        default=[sheet_names[0]] if sheet_names else [],
        key="selected_sheet_names_widget"
    )

    if not selected_sheet_names:
        st.markdown('<div class="warning-box">Select at least one sheet to process.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    all_recipients = []
    sheet_summary = []
    all_format_issues = []

    for selected_sheet_name in selected_sheet_names:
        raw_df = pd.read_excel(
            BytesIO(file_bytes),
            sheet_name=selected_sheet_name,
            header=None,
            dtype=object
        )

        format_issues = validate_standard_sourcing_format(raw_df, selected_sheet_name)

        if format_issues:
            all_format_issues.extend(format_issues)
            recipients_df = pd.DataFrame()
        else:
            recipients_df = flatten_standard_sourcing_sheet(raw_df, selected_sheet_name)

        if not recipients_df.empty:
            all_recipients.append(recipients_df)

        sheet_summary.append(
            {
                "sheet_name": selected_sheet_name,
                "recipients_found": len(recipients_df),
                "valid_emails": recipients_df["email"].apply(is_valid_email).sum() if not recipients_df.empty else 0
            }
        )

    st.subheader("Format Validation")

    if all_format_issues:
        for issue in all_format_issues:
            st.error(issue)

        st.markdown(
            '<div class="error-box">Format validation failed. No emails will be sent until the selected sheets match the standardized sourcing format.</div>',
            unsafe_allow_html=True
        )
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="success-box">Format validation passed.</div>', unsafe_allow_html=True)

    summary_df = pd.DataFrame(sheet_summary)

    st.subheader("Sheet Processing Summary")
    st.dataframe(summary_df, use_container_width=True)

    if not all_recipients:
        st.markdown(
            '<div class="error-box">No usable recipients were found. Make sure the selected sheet has company rows and at least one filled Email column.</div>',
            unsafe_allow_html=True
        )
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    df = pd.concat(all_recipients, ignore_index=True)

    before_dedup_count = len(df)
    df = df.drop_duplicates(subset=["email"], keep="first").reset_index(drop=True)
    deduped_count = before_dedup_count - len(df)

    valid_email_count = df["email"].apply(is_valid_email).sum()
    invalid_email_count = len(df) - valid_email_count
    unique_company_count = df["company_name"].nunique()

    st.session_state.df_base = df.copy()
    st.session_state.df_working = df.copy()
    st.session_state.selected_sheet_names = selected_sheet_names
    st.session_state.deduped_count = deduped_count

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        render_metric(len(df), "Total recipient rows")
    with metric_col2:
        render_metric(valid_email_count, "Valid emails")
    with metric_col3:
        render_metric(unique_company_count, "Unique companies")
    with metric_col4:
        render_metric(deduped_count, "Duplicate emails removed")

    if invalid_email_count > 0:
        st.markdown(
            f'<div class="warning-box">{invalid_email_count} recipient rows have invalid-looking emails and can be skipped during sending.</div>',
            unsafe_allow_html=True
        )

    st.subheader("Normalized Outreach Recipients")
    st.dataframe(df, use_container_width=True)

    render_nav(next_enabled=True)


# ------------------------------------------------------
# Page 2: Filter
# ------------------------------------------------------

elif st.session_state.page == 2:
    render_page_header(
        "3",
        "Recipient Filtering",
        "Choose which contact tiers should be included in this sending batch."
    )

    if st.session_state.df_base is None:
        st.markdown('<div class="error-box">No workbook has been processed yet. Go back and upload a workbook first.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    df_base = st.session_state.df_base.copy()

    available_tiers = sorted([tier for tier in df_base["tier"].dropna().unique().tolist() if clean_text(tier)])

    selected_tiers = st.multiselect(
        "Select tiers to include",
        options=available_tiers,
        default=available_tiers,
        help="For example, select only Tier 1 if you want to avoid emailing Tier 2 contacts in the same batch.",
        key="selected_tiers"
    )

    if not selected_tiers:
        st.markdown('<div class="error-box">Select at least one tier before continuing.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    df_working = df_base[df_base["tier"].isin(selected_tiers)].reset_index(drop=True)

    if df_working.empty:
        st.markdown('<div class="error-box">No recipients remain after tier filtering.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.session_state.df_working = df_working

    tier_summary = df_working["tier"].value_counts().reset_index()
    tier_summary.columns = ["tier", "recipient_count"]

    st.subheader("Tier Filter Summary")
    st.dataframe(tier_summary, use_container_width=True)

    st.markdown(
        f'<div class="success-box">Tier filtering applied. {len(df_working)} recipients remain in the current batch.</div>',
        unsafe_allow_html=True
    )

    st.subheader("Recipients After Filtering")
    st.dataframe(df_working, use_container_width=True)

    render_nav(next_enabled=True)


# ------------------------------------------------------
# Page 3: Template
# ------------------------------------------------------

elif st.session_state.page == 3:
    render_page_header(
        "4",
        "Create Email Template",
        "Use placeholders from the normalized recipient table. The app will validate placeholders before sending."
    )

    df = st.session_state.df_working

    if df is None or df.empty:
        st.markdown('<div class="error-box">No recipients are available. Go back and complete upload/filtering first.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    template_col1, template_col2 = st.columns([1, 1])

    with template_col1:
        subject_template = st.text_input(
            "Subject template",
            value=st.session_state.get("subject_template", "Introductory Discussion with {company_name}"),
            key="subject_template"
        )

        st.markdown(
            """
            <div class="small-card">
                <b>Available placeholders</b><br><br>
                <code>{company_name}</code><br>
                <code>{contact_name}</code><br>
                <code>{greeting_name}</code><br>
                <code>{title}</code><br>
                <code>{email}</code><br>
                <code>{tier}</code><br>
                <code>{company_linkedin}</code><br>
                <code>{type}</code><br>
                <code>{website}</code><br>
                <code>{country}</code><br>
                <code>{revenue}</code><br>
                <code>{source_status}</code><br>
                <code>{ownership_shareholders}</code><br>
                <code>{target_classification}</code><br>
                <code>{note}</code><br>
                <code>{source_sheet}</code>
            </div>
            """,
            unsafe_allow_html=True
        )

    with template_col2:
        body_template = st.text_area(
            "Body template",
            value=st.session_state.get(
                "body_template",
                """Dear {greeting_name},

I hope you are doing well.

I am reaching out from DealFlow.sg regarding a potential strategic partnership opportunity involving {company_name}.

We are currently supporting a leading international group exploring expansion opportunities across Southeast Asia, and would be keen to explore whether there may be room for an introductory discussion.

Best regards,
Dan"""
            ),
            height=330,
            key="body_template"
        )

    used_placeholders, unknown_placeholders = validate_placeholders(
        subject_template,
        body_template,
        df.columns.tolist()
    )

    st.session_state.used_placeholders = used_placeholders

    st.subheader("Template Validation")

    if unknown_placeholders:
        st.markdown(
            f"""
            <div class="error-box">
                Unknown placeholder(s) detected: <b>{", ".join(["{" + p + "}" for p in unknown_placeholders])}</b>.<br>
                These placeholders do not exist in the normalized recipient table. Fix them before continuing.
            </div>
            """,
            unsafe_allow_html=True
        )
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="success-box">Template placeholder validation passed.</div>', unsafe_allow_html=True)

    if used_placeholders:
        st.write("**Placeholders used:**", ", ".join(["{" + p + "}" for p in used_placeholders]))
    else:
        st.markdown('<div class="warning-box">No personalization placeholders were detected in the subject or body.</div>', unsafe_allow_html=True)

    missing_personalization_df = get_missing_personalization_summary(df, used_placeholders)
    st.session_state.missing_personalization_df = missing_personalization_df

    if not missing_personalization_df.empty:
        st.markdown(
            """
            <div class="warning-box">
                Some recipients are missing values for placeholders used in your template.
                The app will still allow sending, but review this carefully.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.dataframe(missing_personalization_df, use_container_width=True)
    else:
        st.markdown('<div class="success-box">No missing personalization values detected for the placeholders used.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="info-box">
            <b>Greeting name note:</b> The app creates <code>{greeting_name}</code> from <code>{contact_name}</code>.
            By default, it uses the last word of the contact name. If this is not suitable, use <code>{contact_name}</code> instead.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_nav(next_enabled=True)


# ------------------------------------------------------
# Page 4: Controls
# ------------------------------------------------------

elif st.session_state.page == 4:
    render_page_header(
        "5",
        "Sending Controls",
        "Set batch size and delay to keep sending controlled and reduce accidental mass outreach."
    )

    df = st.session_state.df_working

    if df is None or df.empty:
        st.markdown('<div class="error-box">No recipients are available. Go back and complete upload/filtering first.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    control_col1, control_col2, control_col3 = st.columns(3)

    with control_col1:
        send_delay = st.number_input(
            "Delay between emails, in seconds",
            min_value=0,
            max_value=120,
            value=st.session_state.get("send_delay", 5),
            key="send_delay"
        )

    with control_col2:
        max_emails = st.number_input(
            "Maximum emails to send in this batch",
            min_value=1,
            max_value=500,
            value=st.session_state.get("max_emails", min(20, max(1, len(df)))),
            key="max_emails"
        )

    with control_col3:
        send_only_valid = st.checkbox(
            "Send only to valid-looking recipient emails",
            value=st.session_state.get("send_only_valid", True),
            key="send_only_valid"
        )

    st.markdown(
        """
        <div class="warning-box">
            Recommended: send one test email to yourself first. Then send small batches before scaling.
        </div>
        """,
        unsafe_allow_html=True
    )

    render_nav(next_enabled=True)


# ------------------------------------------------------
# Page 5: Preview
# ------------------------------------------------------

elif st.session_state.page == 5:
    render_page_header(
        "6",
        "Preview Personalized Email",
        "Check exactly what one recipient will receive. You can also send the preview to yourself before batch sending."
    )

    df = st.session_state.df_working

    if df is None or df.empty:
        st.markdown('<div class="error-box">No recipients are available. Go back and complete upload/filtering first.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    cc_emails = st.session_state.get("cc_emails", [])

    preview_col1, preview_col2 = st.columns([0.35, 0.65])

    with preview_col1:
        preview_row_number = st.number_input(
            "Choose recipient row to preview",
            min_value=0,
            max_value=len(df) - 1,
            value=min(st.session_state.get("preview_row_number", 0), len(df) - 1),
            key="preview_row_number"
        )

        preview_row = df.iloc[preview_row_number]
        cc_preview_text = ", ".join(cc_emails) if cc_emails else "None"

        st.markdown(
            f"""
            <div class="small-card">
                <b>Preview Recipient</b><br><br>
                To: {preview_row["email"]}<br>
                CC: {cc_preview_text}<br>
                Company: {preview_row["company_name"]}<br>
                Contact: {preview_row["contact_name"]}<br>
                Greeting Name: {preview_row["greeting_name"]}<br>
                Title: {preview_row["title"]}<br>
                Tier: {preview_row["tier"]}<br>
                Source Sheet: {preview_row["source_sheet"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    with preview_col2:
        preview_subject = personalize_text(st.session_state.subject_template, preview_row)
        preview_body = personalize_text(st.session_state.body_template, preview_row)

        st.write("**Subject:**", preview_subject)
        st.write("**CC:**", ", ".join(cc_emails) if cc_emails else "None")

        st.text_area("Preview body", preview_body, height=300)

        include_cc_in_preview = st.checkbox(
            "Include CC recipients when sending preview to myself",
            value=False,
            help="Recommended to leave this off so you do not accidentally notify CC recipients during testing.",
            key="include_cc_in_preview"
        )

        if st.button("Send Preview Email to Myself"):
            try:
                preview_test_subject = "[PREVIEW] " + preview_subject

                preview_test_body = (
                    "PREVIEW EMAIL ONLY\n"
                    "This email was sent to yourself for review before batch sending.\n\n"
                    f"Original intended recipient: {preview_row['email']}\n"
                    f"Original company: {preview_row['company_name']}\n"
                    f"Original contact: {preview_row['contact_name']}\n\n"
                    "------------------------------\n\n"
                    + preview_body
                )

                preview_cc_emails = cc_emails if include_cc_in_preview else []

                send_email(
                    to_email=st.session_state.sender_email,
                    subject=preview_test_subject,
                    body=preview_test_body,
                    sender_name=st.session_state.sender_name,
                    sender_email=st.session_state.sender_email,
                    sender_password=st.session_state.sender_password,
                    smtp_server=st.session_state.smtp_server,
                    smtp_port=st.session_state.smtp_port,
                    cc_emails=preview_cc_emails
                )

                st.success(f"Preview email sent to {st.session_state.sender_email}.")

            except Exception as error:
                st.error(f"Failed to send preview email: {error}")

    render_nav(next_enabled=True)


# ------------------------------------------------------
# Page 6: Confirm + Send
# ------------------------------------------------------

elif st.session_state.page == 6:
    render_page_header(
        "7",
        "Final Confirmation and Send",
        "Review the final sending summary, confirm, then send the outreach batch."
    )

    df = st.session_state.df_working

    if df is None or df.empty:
        st.markdown('<div class="error-box">No recipients are available. Go back and complete upload/filtering first.</div>', unsafe_allow_html=True)
        render_nav(next_enabled=False)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    cc_emails = st.session_state.get("cc_emails", [])
    eligible_valid_count = df["email"].apply(is_valid_email).sum()
    invalid_count_after_filter = len(df) - eligible_valid_count

    if st.session_state.get("send_only_valid", True):
        estimated_sendable_count = min(st.session_state.max_emails, eligible_valid_count)
    else:
        estimated_sendable_count = min(st.session_state.max_emails, len(df))

    summary_col1, summary_col2, summary_col3 = st.columns(3)

    with summary_col1:
        render_metric(len(df), "Recipients after tier filter")
    with summary_col2:
        render_metric(estimated_sendable_count, "Estimated emails this batch")
    with summary_col3:
        render_metric(len(cc_emails), "CC recipients")

    summary_details_col1, summary_details_col2 = st.columns(2)

    with summary_details_col1:
        selected_tiers = st.session_state.get("selected_tiers", [])
        selected_sheets = st.session_state.get("selected_sheet_names", [])

        st.markdown(
            f"""
            <div class="small-card">
                <b>Sending Summary</b><br><br>
                Sender: {st.session_state.sender_email}<br>
                Selected sheets: {", ".join(selected_sheets)}<br>
                Selected tiers: {", ".join(selected_tiers)}<br>
                Total recipients after filtering: {len(df)}<br>
                Valid-looking recipient emails: {eligible_valid_count}<br>
                Invalid-looking recipient emails: {invalid_count_after_filter}<br>
                Maximum emails this batch: {st.session_state.max_emails}<br>
                Delay between emails: {st.session_state.send_delay} seconds
            </div>
            """,
            unsafe_allow_html=True
        )

    with summary_details_col2:
        cc_summary_text = ", ".join(cc_emails) if cc_emails else "None"
        used_placeholders = st.session_state.get("used_placeholders", [])
        missing_personalization_df = st.session_state.get("missing_personalization_df", pd.DataFrame())

        st.markdown(
            f"""
            <div class="small-card">
                <b>Template Summary</b><br><br>
                Subject: {st.session_state.subject_template}<br>
                CC: {cc_summary_text}<br>
                Placeholders used: {", ".join(["{" + p + "}" for p in used_placeholders]) if used_placeholders else "None"}<br>
                Missing personalization fields: {len(missing_personalization_df)} field(s)<br>
                Duplicate emails removed: {st.session_state.deduped_count}<br>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="warning-box">
            Once you click send, real emails will be sent from the sender account entered in Step 1.
            Make sure the recipients, selected tiers, CC list, and template are correct.
        </div>
        """,
        unsafe_allow_html=True
    )

    confirm_send = st.checkbox(
        "I confirm that I have reviewed the final summary, recipients, CC list, selected tiers, and email template.",
        key="confirm_send"
    )

    if st.button("Send Outreach Emails", disabled=not confirm_send):
        sent_count = 0
        failed_count = 0
        skipped_count = 0

        progress_bar = st.progress(0)
        status_message = st.empty()

        total_rows = len(df)

        for index, row in df.iterrows():
            if sent_count >= st.session_state.max_emails:
                break

            email = clean_text(row.get("email", ""))

            if st.session_state.send_only_valid and not is_valid_email(email):
                df.at[index, "status"] = "Skipped"
                df.at[index, "error_message"] = "Invalid recipient email format"
                skipped_count += 1
                continue

            try:
                subject = personalize_text(st.session_state.subject_template, row)
                body = personalize_text(st.session_state.body_template, row)

                send_email(
                    to_email=email,
                    subject=subject,
                    body=body,
                    sender_name=st.session_state.sender_name,
                    sender_email=st.session_state.sender_email,
                    sender_password=st.session_state.sender_password,
                    smtp_server=st.session_state.smtp_server,
                    smtp_port=st.session_state.smtp_port,
                    cc_emails=cc_emails
                )

                df.at[index, "status"] = "Sent"
                df.at[index, "sent_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                df.at[index, "error_message"] = ""

                sent_count += 1

                status_message.success(f"Sent email to {email}")
                progress_bar.progress(min((index + 1) / total_rows, 1.0))

                time.sleep(st.session_state.send_delay)

            except Exception as error:
                df.at[index, "status"] = "Failed"
                df.at[index, "error_message"] = str(error)

                failed_count += 1

                status_message.error(f"Failed to send email to {email}: {error}")

        st.session_state.df_working = df

        st.markdown(
            f"""
            <div class="success-box">
                Sending completed. Sent: <b>{sent_count}</b>, Failed: <b>{failed_count}</b>, Skipped: <b>{skipped_count}</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            render_metric(sent_count, "Sent")
        with result_col2:
            render_metric(failed_count, "Failed")
        with result_col3:
            render_metric(skipped_count, "Skipped")

        st.subheader("Updated Outreach Results")
        st.dataframe(df, use_container_width=True)

        excel_data = convert_df_to_excel(df)

        st.download_button(
            label="Download Updated Outreach Results",
            data=excel_data,
            file_name="updated_outreach_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    render_nav(next_enabled=False, next_label="Done", back_enabled=True)


st.markdown('</div>', unsafe_allow_html=True)