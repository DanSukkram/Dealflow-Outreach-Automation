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
    page_title="Email Outreach Automation",
    page_icon="✉️",
    layout="wide"
)


# ------------------------------------------------------
# Custom CSS — DealFlow.sg inspired: dark navy + gold
# ------------------------------------------------------

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

        /* ── Base ── */
        .stApp {
            background: #080e1c;
            color: #e8e4da;
            font-family: 'DM Sans', sans-serif;
        }

        .block-container {
            max-width: 1080px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* ── Typography ── */
        h1, h2, h3, h4 {
            font-family: 'Cormorant Garamond', Georgia, serif !important;
            color: #f0ebe0 !important;
            letter-spacing: 0.01em;
        }

        p, label, span, div {
            color: #9da8b8;
            font-size: 13.5px;
            font-family: 'DM Sans', sans-serif;
        }

        /* ── Hero card ── */
        .hero-card {
            background: linear-gradient(135deg, #0d1628 0%, #111e35 100%);
            border: 1px solid #c9a84c33;
            border-top: 3px solid #c9a84c;
            border-radius: 4px;
            padding: 36px 40px;
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }

        .hero-card::before {
            content: '';
            position: absolute;
            top: -60px;
            right: -60px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, #c9a84c18 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-title {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 34px;
            font-weight: 700;
            color: #f0ebe0;
            margin-bottom: 10px;
            letter-spacing: 0.01em;
        }

        .hero-subtitle {
            font-size: 14px;
            color: #7a8a9e;
            max-width: 700px;
            line-height: 1.7;
        }

        /* ── Pills ── */
        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 20px;
        }

        .pill {
            background: transparent;
            border: 1px solid #c9a84c55;
            padding: 4px 12px;
            border-radius: 2px;
            font-size: 11px;
            color: #c9a84c;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            font-weight: 500;
        }

        /* ── Section cards ── */
        .section-card {
            background: #0d1628;
            border: 1px solid #1e2d47;
            border-left: 3px solid #c9a84c;
            border-radius: 4px;
            padding: 28px 32px;
            margin: 20px 0;
        }

        .small-card {
            background: #0a1220;
            border: 1px solid #1e2d47;
            border-radius: 4px;
            padding: 18px 20px;
            height: 100%;
            font-size: 13px;
            line-height: 1.7;
            color: #8a97a8;
        }

        .small-card b {
            color: #c9a84c;
            font-weight: 600;
            display: block;
            margin-bottom: 10px;
            font-size: 11px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        /* ── Step label ── */
        .step-label {
            display: inline-block;
            background: transparent;
            border: 1px solid #c9a84c;
            color: #c9a84c;
            padding: 2px 10px;
            border-radius: 2px;
            font-size: 10px;
            font-weight: 600;
            margin-bottom: 10px;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .section-title {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 22px;
            font-weight: 600;
            color: #f0ebe0 !important;
            margin-bottom: 4px;
        }

        .section-desc {
            font-size: 13px;
            color: #5a6a7e;
            margin-bottom: 18px;
            line-height: 1.6;
        }

        /* ── Metrics ── */
        .metric-number {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 36px;
            font-weight: 700;
            color: #c9a84c;
            line-height: 1;
            margin-bottom: 4px;
        }

        .metric-label {
            font-size: 11px;
            color: #4a5a6e;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* ── Alert boxes ── */
        .success-box,
        .warning-box,
        .error-box,
        .info-box {
            border-radius: 3px;
            padding: 11px 16px;
            font-size: 13px;
            margin: 12px 0;
            border: 1px solid transparent;
            font-family: 'DM Sans', sans-serif;
        }

        .success-box {
            background: #0a1e13;
            border-color: #1a4a2a;
            border-left: 3px solid #2a7a4a;
            color: #5dba82;
        }

        .warning-box {
            background: #1a130a;
            border-color: #3a2a0a;
            border-left: 3px solid #c9a84c;
            color: #b89040;
        }

        .error-box {
            background: #1a0a0a;
            border-color: #3a1515;
            border-left: 3px solid #8a2020;
            color: #c05050;
        }

        .info-box {
            background: #0a1020;
            border-color: #1a2540;
            border-left: 3px solid #2a5090;
            color: #5a88c0;
        }

        /* ── Inputs ── */
        .stTextInput input,
        .stTextArea textarea,
        .stNumberInput input {
            background-color: #0a1220 !important;
            color: #d0ccc0 !important;
            border: 1px solid #1e2d47 !important;
            border-radius: 3px !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 13.5px !important;
        }

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stNumberInput input:focus {
            border-color: #c9a84c88 !important;
            box-shadow: 0 0 0 2px #c9a84c15 !important;
        }

        .stSelectbox div[data-baseweb="select"] > div,
        .stMultiSelect div[data-baseweb="select"] > div {
            background-color: #0a1220 !important;
            color: #d0ccc0 !important;
            border: 1px solid #1e2d47 !important;
            border-radius: 3px !important;
        }

        /* ── File uploader ── */
        .stFileUploader {
            background: #0a1220;
            border: 1px dashed #2a3d5a;
            border-radius: 4px;
            padding: 16px;
        }

        /* ── Buttons ── */
        .stButton > button {
            background: transparent !important;
            color: #c9a84c !important;
            border: 1px solid #c9a84c !important;
            border-radius: 3px !important;
            padding: 0.55rem 1.2rem !important;
            font-weight: 500 !important;
            font-family: 'DM Sans', sans-serif !important;
            font-size: 13px !important;
            letter-spacing: 0.04em !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover {
            background: #c9a84c !important;
            color: #080e1c !important;
        }

        .stButton > button:disabled {
            border-color: #2a3a4a !important;
            color: #3a4a5a !important;
        }

        .stDownloadButton > button {
            background: transparent !important;
            color: #5dba82 !important;
            border: 1px solid #2a7a4a !important;
            border-radius: 3px !important;
            padding: 0.55rem 1.2rem !important;
            font-weight: 500 !important;
            font-family: 'DM Sans', sans-serif !important;
            letter-spacing: 0.04em !important;
        }

        .stDownloadButton > button:hover {
            background: #2a7a4a !important;
            color: #f0ebe0 !important;
        }

        /* ── Tables / Dataframes ── */
        div[data-testid="stDataFrame"] {
            border-radius: 3px;
            border: 1px solid #1e2d47;
            overflow: hidden;
        }

        /* ── Checkbox ── */
        .stCheckbox label {
            color: #8a97a8 !important;
            font-size: 13.5px !important;
        }

        /* ── Expander ── */
        .streamlit-expanderHeader {
            background: #0a1220 !important;
            color: #7a8a9e !important;
            border: 1px solid #1e2d47 !important;
            border-radius: 3px !important;
            font-size: 13px !important;
        }

        /* ── Subheader overrides ── */
        .stMarkdown h2, .stMarkdown h3 {
            font-family: 'Cormorant Garamond', Georgia, serif !important;
            color: #c9a84c !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            border-bottom: 1px solid #1e2d47;
            padding-bottom: 8px;
            margin-top: 20px !important;
        }

        /* ── Divider ── */
        hr {
            border-color: #1e2d47 !important;
        }

        /* ── Code blocks ── */
        code {
            background: #0a1220 !important;
            color: #c9a84c !important;
            border: 1px solid #1e2d47 !important;
            border-radius: 2px !important;
            padding: 1px 5px !important;
            font-size: 12px !important;
        }

        /* ── Multiselect tags ── */
        span[data-baseweb="tag"] {
            background: #1a2a1a !important;
            border: 1px solid #2a5a2a !important;
        }

        /* ── Progress bar ── */
        .stProgress > div > div {
            background: linear-gradient(90deg, #c9a84c, #e8c86a) !important;
            border-radius: 2px !important;
        }

        /* ── Number input arrows ── */
        .stNumberInput div[data-baseweb="input"] {
            background-color: #0a1220 !important;
        }

        /* ── Scrollbar ── */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #080e1c;
        }
        ::-webkit-scrollbar-thumb {
            background: #2a3d5a;
            border-radius: 3px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #c9a84c55;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# Optional Streamlit secrets
# ------------------------------------------------------

def get_secret_value(key):
    try:
        return st.secrets[key]
    except Exception:
        return None


# ------------------------------------------------------
# UI helper functions
# ------------------------------------------------------

def render_step(step_number, title, description):
    st.markdown(
        f"""
        <div class="step-label">Step {step_number}</div>
        <div class="section-title">{title}</div>
        <div class="section-desc">{description}</div>
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


# ------------------------------------------------------
# Data helper functions
# ------------------------------------------------------

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
    """
    Allows multiple CC emails.

    Accepted formats:
    person1@company.com, person2@company.com
    person1@company.com; person2@company.com
    person1@company.com
    """

    if not email_text:
        return []

    email_text = str(email_text).replace(";", ",")

    emails = [
        email.strip()
        for email in email_text.split(",")
        if email.strip()
    ]

    return emails


def extract_placeholders(text):
    """
    Extracts placeholders from a template.
    Example: 'Dear {contact_name}' -> ['contact_name']
    """

    if not text:
        return []

    return sorted(set(re.findall(r"\{([A-Za-z0-9_]+)\}", text)))


def validate_placeholders(subject_template, body_template, available_columns):
    """
    Checks whether all placeholders used in the templates exist as columns
    in the normalized recipient table.
    """

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
    """
    Counts how many rows are missing values for each placeholder used in the template.
    """

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
    """
    Creates a greeting_name from contact_name.

    This is a practical fallback:
    - If the contact name has multiple words, it uses the last word.
    - For many Vietnamese names, the last word is often the given name.
    - If this is not desired, users can add a manual Greeting Name column later,
      or use {contact_name} instead.
    """

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

    if contact_number == 1:
        return "Tier 1"

    if contact_number == 2:
        return "Tier 2"

    if contact_number == 3:
        return "Tier 3"

    return f"Tier {contact_number}"


def validate_standard_sourcing_format(raw_df, sheet_name):
    issues = []

    header_row_index = detect_standard_header_row(raw_df)

    if header_row_index is None:
        issues.append(
            f"{sheet_name}: Could not detect the standard header row. "
            "Make sure the sheet has Company / Company Name, contact name fields, and Email columns."
        )
        return issues

    headers = [clean_text(value) for value in raw_df.iloc[header_row_index].tolist()]
    normalized_headers = [normalize_header(header) for header in headers]

    company_col_index = find_first_matching_column(
        headers,
        ["Company", "Company Name", "Company's Name"]
    )

    if company_col_index is None:
        issues.append(
            f"{sheet_name}: Missing company column. Use 'Company' or 'Company Name'."
        )

    email_col_indexes = [
        index for index, header in enumerate(normalized_headers)
        if header == "email"
    ]

    if not email_col_indexes:
        issues.append(
            f"{sheet_name}: No Email columns found. Email columns must be named exactly 'Email'."
        )

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
                f"{sheet_name}: An Email column is too far left. "
                "Each Email column must have contact name and position/title before it."
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
                f"{sheet_name}: The column two places before Email should be contact name, "
                f"but found '{headers[email_col_index - 2]}'."
            )

        if not title_ok:
            issues.append(
                f"{sheet_name}: The column directly before Email should be Position or Title, "
                f"but found '{headers[email_col_index - 1]}'."
            )

    return issues


def flatten_standard_sourcing_sheet(raw_df, sheet_name):
    header_row_index = detect_standard_header_row(raw_df)

    if header_row_index is None:
        return pd.DataFrame()

    headers = [clean_text(value) for value in raw_df.iloc[header_row_index].tolist()]
    normalized_headers = [normalize_header(header) for header in headers]

    data_df = raw_df.iloc[header_row_index + 1:].copy()

    company_col_index = find_first_matching_column(
        headers,
        ["Company", "Company Name", "Company's Name"]
    )

    linkedin_col_index = find_first_matching_column(
        headers,
        ["Linkedin", "LinkedIn", "Company LinkedIn"]
    )

    type_col_index = find_first_matching_column(
        headers,
        ["Type", "Sector", "Industry"]
    )

    website_col_index = find_first_matching_column(
        headers,
        ["Website", "Company Website"]
    )

    country_col_index = find_first_matching_column(
        headers,
        ["Country", "Location", "Market"]
    )

    revenue_col_index = find_column_containing(
        headers,
        ["revenue"]
    )

    source_status_col_index = find_first_matching_column(
        headers,
        ["Status"]
    )

    ownership_col_index = find_first_matching_column(
        headers,
        ["Ownership / Shareholders", "Ownership", "Shareholders"]
    )

    target_classification_col_index = find_first_matching_column(
        headers,
        ["Target classification", "Target Classification", "Classification"]
    )

    note_col_index = find_first_matching_column(
        headers,
        ["Note", "Notes"]
    )

    greeting_name_col_index = find_first_matching_column(
        headers,
        ["Greeting Name", "Greeting", "First Name", "Preferred Name"]
    )

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
                tier = get_tier_from_contact_header(
                    headers[contact_name_col_index],
                    contact_number
                )

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
    """
    Sends one plain-text email.

    cc_emails can contain multiple CC recipients.
    """

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
        <div class="hero-title">Email Outreach Automation</div>
        <div class="hero-subtitle">
            Upload a workbook with company rows and multiple contact columns,
            convert each contact into an individual outreach recipient, send personalized emails, CC multiple recipients if needed,
            and download a status-tracked result file.
        </div>
        <div class="pill-row">
            <div class="pill">Standardized Sourcing Format</div>
            <div class="pill">Multiple Contacts Per Company</div>
            <div class="pill">Multiple CC Recipients</div>
            <div class="pill">Tier Filtering</div>
            <div class="pill">Template Validation</div>
            <div class="pill">Preview Test Email</div>
            <div class="pill">Status Tracking</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ------------------------------------------------------
# Optional access password
# ------------------------------------------------------

APP_PASSWORD = get_secret_value("APP_PASSWORD")

if APP_PASSWORD:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    render_step("0", "Internal Access", "Enter the team access code before using the outreach tool.")

    entered_app_password = st.text_input(
        "Internal access code",
        type="password",
        placeholder="Enter access code"
    )

    if entered_app_password != APP_PASSWORD:
        st.markdown(
            '<div class="warning-box">Please enter the correct internal access code to continue.</div>',
            unsafe_allow_html=True
        )
        st.stop()

    st.markdown(
        '<div class="success-box">Access confirmed. You may continue.</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 1: Sender credentials + CC
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "1",
    "Sender Email Credentials",
    "Choose your email provider, enter the sender credentials, and optionally CC one or more people."
)

st.markdown(
    """
    <div class="warning-box">
        Use an app password where possible. Gmail requires a Google App Password.
        For Outlook or Microsoft 365, SMTP access must be allowed for the mailbox.
    </div>
    """,
    unsafe_allow_html=True
)

cred_col1, cred_col2 = st.columns(2)

with cred_col1:
    email_provider = st.selectbox(
        "Email provider",
        ["Gmail", "Outlook / Microsoft 365", "Custom SMTP"]
    )

with cred_col2:
    sender_name = st.text_input(
        "Sender name",
        value="Dan"
    )

if email_provider == "Gmail":
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

elif email_provider == "Outlook / Microsoft 365":
    smtp_server = "smtp.office365.com"
    smtp_port = 587

else:
    custom_col1, custom_col2 = st.columns(2)

    with custom_col1:
        smtp_server = st.text_input(
            "SMTP server",
            value="",
            placeholder="smtp.example.com"
        )

    with custom_col2:
        smtp_port = st.number_input(
            "SMTP port",
            min_value=1,
            max_value=9999,
            value=587
        )

login_col1, login_col2 = st.columns(2)

with login_col1:
    sender_email = st.text_input(
        "Sender email address",
        placeholder="example@gmail.com"
    )

with login_col2:
    sender_password = st.text_input(
        "Email app password",
        type="password",
        help="Use an app password, not your normal email password."
    )

cc_input = st.text_area(
    "CC recipients, optional",
    placeholder="person1@company.com, person2@company.com, person3@company.com",
    help="You can enter multiple CC emails separated by commas or semicolons.",
    height=90
)

cc_emails = parse_email_list(cc_input)

with st.expander("View SMTP and CC settings being used"):
    st.write("**SMTP server:**", smtp_server)
    st.write("**SMTP port:**", smtp_port)

    if cc_emails:
        st.write("**Number of CC recipients:**", len(cc_emails))
        st.write("**CC:**", ", ".join(cc_emails))
    else:
        st.write("**CC:** None")

credentials_ready = bool(smtp_server and smtp_port and sender_email and sender_password)

if not credentials_ready:
    st.markdown(
        '<div class="warning-box">Enter all sender credentials before uploading your Excel file.</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown(
    '<div class="success-box">Sender credentials entered. You can now upload your Excel file.</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 2: Upload Excel workbook
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "2",
    "Upload Standardized Sourcing Workbook",
    "Upload a workbook using the standardized format: Company, Linkedin, Type, Website, Country, Revenue, Name, Position, Email, Status, 2nd PiC, Position, Email, and related notes."
)

uploaded_file = st.file_uploader(
    "Upload your outreach Excel file",
    type=["xlsx"]
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
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

try:
    file_bytes = uploaded_file.getvalue()
    excel_file = pd.ExcelFile(BytesIO(file_bytes))
    sheet_names = excel_file.sheet_names

except Exception as error:
    st.markdown(
        f'<div class="error-box">Something went wrong while reading the workbook: {error}</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

selected_sheet_names = st.multiselect(
    "Select sheets to process",
    options=sheet_names,
    default=[sheet_names[0]] if sheet_names else []
)

if not selected_sheet_names:
    st.markdown(
        '<div class="warning-box">Select at least one sheet to process.</div>',
        unsafe_allow_html=True
    )
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
        """
        <div class="error-box">
            Format validation failed. No emails will be sent until the selected sheets match the standardized sourcing format.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
else:
    st.markdown(
        '<div class="success-box">Format validation passed. The selected sheets follow the standardized sourcing format.</div>',
        unsafe_allow_html=True
    )

summary_df = pd.DataFrame(sheet_summary)

st.subheader("Sheet Processing Summary")
st.dataframe(summary_df, use_container_width=True)

if not all_recipients:
    st.markdown(
        """
        <div class="error-box">
            No usable recipients were found. Make sure the selected sheet has company rows and at least one filled Email column.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

df = pd.concat(all_recipients, ignore_index=True)

before_dedup_count = len(df)
df = df.drop_duplicates(subset=["email"], keep="first").reset_index(drop=True)
deduped_count = before_dedup_count - len(df)

valid_email_count = df["email"].apply(is_valid_email).sum()
invalid_email_count = len(df) - valid_email_count
unique_company_count = df["company_name"].nunique()

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

st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 3: Tier filtering
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "3",
    "Recipient Filtering",
    "Choose which contact tiers should be included in this sending batch."
)

available_tiers = sorted([tier for tier in df["tier"].dropna().unique().tolist() if clean_text(tier)])

selected_tiers = st.multiselect(
    "Select tiers to include",
    options=available_tiers,
    default=available_tiers,
    help="For example, select only Tier 1 if you want to avoid emailing Tier 2 contacts in the same batch."
)

if not selected_tiers:
    st.markdown(
        '<div class="error-box">Select at least one tier before continuing.</div>',
        unsafe_allow_html=True
    )
    st.stop()

df = df[df["tier"].isin(selected_tiers)].reset_index(drop=True)

if df.empty:
    st.markdown(
        '<div class="error-box">No recipients remain after tier filtering.</div>',
        unsafe_allow_html=True
    )
    st.stop()

tier_summary = df["tier"].value_counts().reset_index()
tier_summary.columns = ["tier", "recipient_count"]

st.subheader("Tier Filter Summary")
st.dataframe(tier_summary, use_container_width=True)

st.markdown(
    f'<div class="success-box">Tier filtering applied. {len(df)} recipients remain in the current batch.</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 4: Email template + validation
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "4",
    "Create Email Template",
    "Use placeholders from the normalized recipient table. The app will validate placeholders before sending."
)

template_col1, template_col2 = st.columns([1, 1])

with template_col1:
    subject_template = st.text_input(
        "Subject template",
        value="Placeholder Subject for {company_name}"
    )

    st.markdown(
        """
        <div class="small-card">
            <b>Available placeholders</b>
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
        value="""Dear {greeting_name},

This is a placeholder template for the email.
Please change it accordingly for your needs""",
        height=330
    )

used_placeholders, unknown_placeholders = validate_placeholders(
    subject_template,
    body_template,
    df.columns.tolist()
)

st.subheader("Template Validation")

if unknown_placeholders:
    st.markdown(
        f"""
        <div class="error-box">
            Unknown placeholder(s) detected: <b>{", ".join(["{" + p + "}" for p in unknown_placeholders])}</b>.<br>
            These placeholders do not exist in the normalized recipient table. Fix them before sending.
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

st.markdown(
    '<div class="success-box">Template placeholder validation passed.</div>',
    unsafe_allow_html=True
)

if used_placeholders:
    st.write("**Placeholders used in this template:**", ", ".join(["{" + p + "}" for p in used_placeholders]))
else:
    st.markdown(
        '<div class="warning-box">No personalization placeholders were detected in the subject or body.</div>',
        unsafe_allow_html=True
    )

missing_personalization_df = get_missing_personalization_summary(df, used_placeholders)

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
    st.markdown(
        '<div class="success-box">No missing personalization values detected for the placeholders used.</div>',
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="info-box">
        <b>Greeting name note:</b> The app creates <code>{greeting_name}</code> from <code>{contact_name}</code>.
        By default, it uses the last word of the contact name, which is often suitable for Vietnamese names.
        If this is not suitable, use <code>{contact_name}</code> instead.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 5: Sending controls
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "5",
    "Sending Controls",
    "Set batch size and delay to keep sending controlled and reduce accidental mass outreach."
)

control_col1, control_col2, control_col3 = st.columns(3)

with control_col1:
    send_delay = st.number_input(
        "Delay between emails, in seconds",
        min_value=0,
        max_value=120,
        value=5
    )

with control_col2:
    max_emails = st.number_input(
        "Maximum emails to send in this batch",
        min_value=1,
        max_value=500,
        value=min(20, max(1, len(df)))
    )

with control_col3:
    send_only_valid = st.checkbox(
        "Send only to valid-looking recipient emails",
        value=True
    )

st.markdown(
    """
    <div class="warning-box">
        Recommended: send one test email to yourself first. Then send small batches before scaling.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 6: Preview email + send preview to self
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "6",
    "Preview Personalized Email",
    "Check exactly what one recipient will receive. You can also send the preview to yourself before batch sending."
)

preview_col1, preview_col2 = st.columns([0.35, 0.65])

with preview_col1:
    preview_row_number = st.number_input(
        "Choose recipient row to preview",
        min_value=0,
        max_value=len(df) - 1,
        value=0
    )

    preview_row = df.iloc[preview_row_number]

    cc_preview_text = ", ".join(cc_emails) if cc_emails else "None"

    st.markdown(
        f"""
        <div class="small-card">
            <b>Preview Recipient</b>
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
    preview_subject = personalize_text(subject_template, preview_row)
    preview_body = personalize_text(body_template, preview_row)

    st.write("**Subject:**", preview_subject)

    if cc_emails:
        st.write("**CC:**", ", ".join(cc_emails))
    else:
        st.write("**CC:** None")

    st.text_area(
        "Preview body",
        preview_body,
        height=300
    )

    include_cc_in_preview = st.checkbox(
        "Include CC recipients when sending preview to myself",
        value=False,
        help="Recommended to leave this off so you do not accidentally notify CC recipients during testing."
    )

    send_preview_button = st.button("Send Preview Email to Myself")

    if send_preview_button:
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
                to_email=sender_email,
                subject=preview_test_subject,
                body=preview_test_body,
                sender_name=sender_name,
                sender_email=sender_email,
                sender_password=sender_password,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                cc_emails=preview_cc_emails
            )

            st.success(f"Preview email sent to {sender_email}.")

        except Exception as error:
            st.error(f"Failed to send preview email: {error}")

st.markdown('</div>', unsafe_allow_html=True)


# ------------------------------------------------------
# Step 7: Final confirmation summary + send emails
# ------------------------------------------------------

st.markdown('<div class="section-card">', unsafe_allow_html=True)
render_step(
    "7",
    "Final Confirmation and Send",
    "Review the final sending summary, confirm, then send the outreach batch."
)

eligible_valid_count = df["email"].apply(is_valid_email).sum()
invalid_count_after_filter = len(df) - eligible_valid_count

if send_only_valid:
    estimated_sendable_count = min(max_emails, eligible_valid_count)
else:
    estimated_sendable_count = min(max_emails, len(df))

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    render_metric(len(df), "Recipients after tier filter")

with summary_col2:
    render_metric(estimated_sendable_count, "Estimated emails this batch")

with summary_col3:
    render_metric(len(cc_emails), "CC recipients")

summary_details_col1, summary_details_col2 = st.columns(2)

with summary_details_col1:
    st.markdown(
        f"""
        <div class="small-card">
            <b>Sending Summary</b>
            Sender: {sender_email}<br>
            Selected sheets: {", ".join(selected_sheet_names)}<br>
            Selected tiers: {", ".join(selected_tiers)}<br>
            Total recipients after filtering: {len(df)}<br>
            Valid-looking recipient emails: {eligible_valid_count}<br>
            Invalid-looking recipient emails: {invalid_count_after_filter}<br>
            Maximum emails this batch: {max_emails}<br>
            Delay between emails: {send_delay} seconds
        </div>
        """,
        unsafe_allow_html=True
    )

with summary_details_col2:
    cc_summary_text = ", ".join(cc_emails) if cc_emails else "None"

    st.markdown(
        f"""
        <div class="small-card">
            <b>Template Summary</b>
            Subject: {subject_template}<br>
            CC: {cc_summary_text}<br>
            Placeholders used: {", ".join(["{" + p + "}" for p in used_placeholders]) if used_placeholders else "None"}<br>
            Missing personalization fields: {len(missing_personalization_df)} field(s)<br>
            Duplicate emails removed: {deduped_count}<br>
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
    "I confirm that I have reviewed the final summary, recipients, CC list, selected tiers, and email template."
)

send_button = st.button("Send Outreach Emails")

if send_button:
    if not confirm_send:
        st.markdown(
            '<div class="error-box">Please tick the confirmation checkbox before sending.</div>',
            unsafe_allow_html=True
        )
        st.stop()

    sent_count = 0
    failed_count = 0
    skipped_count = 0

    progress_bar = st.progress(0)
    status_message = st.empty()

    total_rows = len(df)

    for index, row in df.iterrows():
        if sent_count >= max_emails:
            break

        email = clean_text(row.get("email", ""))

        if send_only_valid and not is_valid_email(email):
            df.at[index, "status"] = "Skipped"
            df.at[index, "error_message"] = "Invalid recipient email format"
            skipped_count += 1
            continue

        try:
            subject = personalize_text(subject_template, row)
            body = personalize_text(body_template, row)

            send_email(
                to_email=email,
                subject=subject,
                body=body,
                sender_name=sender_name,
                sender_email=sender_email,
                sender_password=sender_password,
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                cc_emails=cc_emails
            )

            df.at[index, "status"] = "Sent"
            df.at[index, "sent_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.at[index, "error_message"] = ""

            sent_count += 1

            status_message.success(f"Sent email to {email}")
            progress_bar.progress(min((index + 1) / total_rows, 1.0))

            time.sleep(send_delay)

        except Exception as error:
            df.at[index, "status"] = "Failed"
            df.at[index, "error_message"] = str(error)

            failed_count += 1

            status_message.error(f"Failed to send email to {email}: {error}")

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

st.markdown('</div>', unsafe_allow_html=True)