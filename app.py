import dash
from dash import dcc, html, Input, Output, State, ctx, dash_table
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
import base64
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import os
import random
import time
import smtplib
from email.message import EmailMessage
import socket
from flask import send_from_directory, abort
import qrcode
import hashlib
from dash.dependencies import MATCH, ALL
import json
import plotly.graph_objects as go
import plotly.express as px

# Initialize the Dash app with Flask server and suppress callback exceptions
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True,
                title="Unified TAFFA Portal")
server = app.server

# --- Admin Credentials ---
ADMIN_USER = "admin"
ADMIN_PASS_HASH = hashlib.sha256("password".encode('utf-8')).hexdigest()

# --- Database Setup with Absolute Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "tra_cfa_data.db")
DOCUMENTS_DIR = os.path.join(BASE_DIR, "uploaded_documents")
CERTIFICATES_DIR = os.path.join(BASE_DIR, "certificates")
IDS_DIR = os.path.join(BASE_DIR, "id_cards")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS id_applications')
    c.execute('DROP TABLE IF EXISTS applications')
    c.execute('DROP TABLE IF EXISTS agents')
    c.execute('DROP TABLE IF EXISTS consignments')
    c.execute('DROP TABLE IF EXISTS invoices')
    c.execute('DROP TABLE IF EXISTS payments')
    c.execute('DROP TABLE IF EXISTS cfa_payments')

    c.execute('''
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tin_number TEXT NOT NULL UNIQUE,
            company_name TEXT NOT NULL,
            contact_person TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            physical_address TEXT,
            postal_address TEXT,
            website TEXT,
            taffa_membership_no TEXT,
            director_1 TEXT,
            director_2 TEXT,
            director_3 TEXT,
            cert_incorporation_no TEXT,
            business_license_no TEXT,
            membership_type TEXT,
            submission_date TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            tax_compliance TEXT,
            taffa_status TEXT,
            policy_compliance TEXT,
            payment_confirmation TEXT,
            business_license TEXT,
            tax_clearance_cert TEXT,
            taffa_cert TEXT,
            cert_incorporation TEXT,
            memo_articles TEXT,
            audited_accounts TEXT,
            director_images TEXT,
            brella_search TEXT,
            agreed_to_terms INTEGER,
            status TEXT DEFAULT 'Pending',
            reference_number TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS id_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER,
            full_name TEXT,
            nida_number TEXT,
            position TEXT,
            passport_photo TEXT,
            id_payment_proof TEXT,
            id_status TEXT DEFAULT 'Pending',
            id_number TEXT,
            expiry_date TEXT,
            FOREIGN KEY (application_id) REFERENCES applications (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS consignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            urn TEXT NOT NULL UNIQUE,
            taffa_agent_id TEXT,
            client_company TEXT,
            client_tin TEXT,
            bl_awb_no TEXT,
            shipper_name TEXT,
            origin_port TEXT,
            destination_port TEXT,
            cargo_desc TEXT,
            status TEXT DEFAULT 'In Transit',
            arrival_date TEXT,
            last_updated TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            invoice_number TEXT,
            amount REAL,
            status TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_id INTEGER,
            payment_type TEXT,
            amount REAL,
            status TEXT,
            FOREIGN KEY (agent_id) REFERENCES agents (id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cfa_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_tin TEXT,
            payment_amount REAL,
            payment_status TEXT,
            payment_method TEXT,
            transaction_id TEXT,
            payment_date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def generate_dummy_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM agents")
    c.execute("DELETE FROM applications")
    c.execute("DELETE FROM consignments")
    c.execute("DELETE FROM invoices")
    c.execute("DELETE FROM payments")
    c.execute("DELETE FROM cfa_payments")

    taffa_agents = [
        {"id": "DFO001", "name": "Logistics Hub Tanzania Ltd"},
        {"id": "DFO002", "name": "Dar es Salaam Cargo Movers Co."},
        {"id": "DFO003", "name": "Global Freight Solutions TZ"}
    ]

    for i in range(1, 20):
        agent_tin = f"123-456-{i:03d}"
        agent_name = f"Agent Company {i}"
        contact_person = f"Juma Bakari {i}"
        email = f"juma.bakari{i}@example.com"
        phone = f"0712-345-{i:03d}"
        submission_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d %H:%M:%S")

        c.execute("""
            INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            agent_tin, agent_name, contact_person, email, phone, "Dar es Salaam", "P.O. Box 1234",
            f"www.{agent_name}.com",
            f"TAFFA{i}", f"Ahmed Salum {i}", "N/A", "N/A", f"TZA{i}", f"BLN/TZA/{i}", "Ordinary", submission_date))
        agent_id = c.lastrowid

        app_status = random.choice(['Verified', 'Pending', 'Cancelled'])
        if app_status == 'Verified':
            taffa_agent_id = random.choice(taffa_agents)['id']
            random_part = str(random.randint(1000, 9999))
            ref_number = f"SUC-{date.today().strftime('%y')}-{taffa_agent_id}{random_part}"
        else:
            ref_number = None

        c.execute("""
            INSERT INTO applications (agent_id, agreed_to_terms, status, reference_number, tax_compliance, taffa_status, policy_compliance, payment_confirmation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (agent_id, 1, app_status, ref_number, "Compliant", "Active", "Fully Compliant", "Paid"))

        if i % 2 == 0:
            cons_urn = f"CFA-{date.today().strftime('%y')}-{taffa_agents[i % 3]['id']}-{random.randint(1000, 9999)}"
            cons_status = random.choice(['In Transit', 'Cleared', 'Delayed'])
            cargo_types = ["Electronics", "Machinery", "Textiles", "Furniture", "Medical Supplies"]
            cons_cargo = random.choice(cargo_types)
            arrival_date = (date.today() + timedelta(days=random.randint(-10, 10))).isoformat()
            c.execute("""
                INSERT INTO consignments (urn, taffa_agent_id, client_company, client_tin, bl_awb_no, shipper_name, origin_port, destination_port, cargo_desc, status, arrival_date, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (cons_urn, taffa_agents[i % 3]['id'], f"Client Co. {i}", f"111-222-{i}", f"BL-{i}", "Shipper Inc.",
                  "Shanghai", "Dar es Salaam", cons_cargo, cons_status, arrival_date, datetime.now().isoformat()))

            c.execute("""
                INSERT INTO cfa_payments (client_tin, payment_amount, payment_status, payment_method, transaction_id, payment_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (f"111-222-{i}", 50000.00, 'Paid', 'M-Pesa', f'TRX{random.randint(10000, 99999)}',
                  datetime.now().isoformat()))

        c.execute("""
            INSERT INTO invoices (agent_id, invoice_number, amount, status)
            VALUES (?, ?, ?, ?)
        """, (agent_id, f"INV-2025-{i}", random.randint(100, 5000), random.choice(['Paid', 'Pending', 'Overdue'])))

        c.execute("""
            INSERT INTO payments (agent_id, payment_type, amount, status)
            VALUES (?, ?, ?, ?)
        """, (agent_id, random.choice(['M-Pesa', 'Bank Transfer']), random.randint(50, 4000), 'Completed'))

    conn.commit()
    conn.close()


init_db()
generate_dummy_data()


# --- Reusable Components ---
def send_email(recipient_email: str, subject: str, body: str):
    sender_email = "administrator@capitalpayinternational.com"
    sender_password = "ahxr wusz rqvp jpsx"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    if not sender_password:
        print("Error: Email password is not set.")
        return False
    msg = EmailMessage()
    msg['Subject'] = f"Update: Milestone Reached - {subject}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.set_content(body)
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print(f"Email notification sent successfully to {recipient_email}!")
            return True
    except socket.gaierror as e:
        print(f"Network error: {e}. Could not find host: '{smtp_server}'.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


# --- App Layout ---
app.layout = dbc.Container([
    dcc.Store(id='payment-store'),
    dcc.Store(id='cfa-payment-store'),
    dcc.Store(id='login-state', data={'is_authenticated': False}),

    dbc.Row([
        dbc.Col(html.Img(src="/assets/LOGO.png", height="100px"), width="auto"),
        dbc.Col(html.H1("CFA Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
                width="auto")
    ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),

    dbc.Tabs(id='main-tabs', children=[
        dbc.Tab(label="TAFFA PORTAL", children=[
            dbc.Tabs(id='taffa-tabs', children=[
                dbc.Tab(label="New Application", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Membership Application Form", className="card-title text-primary fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text',
                                              className="form-control-lg"), width=6),
                            dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text',
                                              className="form-control-lg"), width=6),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text',
                                          className="form-control-lg"),
                                width=6),
                            dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text',
                                              className="form-control-lg"),
                                    width=6),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='website', placeholder='Website', type='text',
                                              className="form-control-lg"), width=6),
                            dbc.Col(
                                dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
                                          type='text', className="form-control-lg"), width=6),
                        ], className="my-3"),
                        html.Hr(),
                        html.H4("Contact Person", className="card-title text-primary mt-4 fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='contact-person-taffa', placeholder='Contact Person Name *', type='text',
                                          className="form-control-lg"),
                                width=4),
                            dbc.Col(dbc.Input(id='email-taffa', placeholder='Email Address *', type='email',
                                              className="form-control-lg"), width=4),
                            dbc.Col(dbc.Input(id='phone-taffa', placeholder='Mobile Number *', type='text',
                                              className="form-control-lg"), width=4),
                        ], className="my-3"),
                        html.Hr(),
                        html.H4("Directors", className="card-title text-primary mt-4 fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text',
                                              className="form-control-lg"), width=4),
                            dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text',
                                              className="form-control-lg"),
                                    width=4),
                            dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text',
                                              className="form-control-lg"),
                                    width=4),
                        ], className="my-3"),
                        html.Hr(),
                        html.H4("Company Details", className="card-title text-primary mt-4 fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
                                          type='text', className="form-control-lg"), width=6),
                            dbc.Col(dbc.Input(id='business-license-no-taffa', placeholder='Business License No. *',
                                              type='text', className="form-control-lg"),
                                    width=6),
                        ], className="my-3"),
                        dcc.Dropdown(id='membership-type', options=[
                            {'label': 'Ordinary Member', 'value': 'Ordinary'},
                            {'label': 'Inhouse Member', 'value': 'Inhouse'}
                        ], placeholder="Choose Membership Type *", className="mb-3 dropdown-large"),
                        html.Hr(),
                        html.H4("Compliance Details (For Verification)",
                                className="card-title text-primary mt-4 fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
                                                                           {'label': 'Non-Compliant',
                                                                            'value': 'Non-Compliant'}],
                                             placeholder="Tax Compliance Status", className="dropdown-large"), width=6),
                            dbc.Col(
                                dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
                                                                         {'label': 'Inactive/Expired',
                                                                          'value': 'Inactive'}],
                                             placeholder="TAFFA Membership Status", className="dropdown-large"),
                                width=6),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='policy-compliance',
                                                 options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
                                                          {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
                                                 placeholder="Policy Compliance Status", className="dropdown-large"),
                                    width=6),
                            dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
                                                                                     {'label': 'Unpaid',
                                                                                      'value': 'Unpaid'}],
                                                 placeholder="Accreditation Fee Payment", value="Unpaid",
                                                 className="dropdown-large"), width=4),
                            dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success",
                                               className="btn-lg"), width=2)
                        ], className="my-3 align-items-center"),
                        html.Hr(),
                        dcc.Checklist(options=[
                            {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations',
                             'value': 1}],
                            id='agree-terms', className="mt-4 form-check-input-lg"),
                        html.Div(
                            dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
                                       className="mt-4"), className="text-center"),
                        html.Div(id='submission-output', className="mt-4")
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="TAFFA ID Application", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("TAFFA ID Application", className="card-title text-primary fs-3 fw-bold"),
                        html.P("This form is for TAFFA members to apply for an ID card.", className="fs-5"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='id-full-name', placeholder='Full Name *', type='text',
                                              className="form-control-lg"), width=6),
                            dbc.Col(dbc.Input(id='id-nida-number', placeholder='NIDA Number *', type='text',
                                              className="form-control-lg"), width=6),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='id-position', placeholder='Position *', type='text',
                                              className="form-control-lg"), width=6),
                            dbc.Col(
                                [dcc.Upload(id='upload-passport-photo', children=html.Button('Upload Passport Photo *',
                                                                                             className="btn btn-outline-primary btn-lg w-100"),
                                            className="w-100 mb-2"),
                                 html.Span(id='output-passport-photo', className="text-success fs-5 ms-2")]),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(
                                [dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof *',
                                                                                         className="btn btn-outline-primary btn-lg w-100"),
                                            className="w-100 mb-2"),
                                 html.Span(id='output-id-payment', className="text-success fs-5 ms-2")]),
                        ], className="my-3"),
                        dbc.Input(id='id-application-tin', placeholder='Your Company TIN *', type='text',
                                  className="my-3 form-control-lg"),
                        dbc.Button('Submit ID Application', id='submit-id-button', n_clicks=0, color="primary",
                                   size="lg",
                                   className="mt-4"),
                        html.Div(id='id-submission-output', className="mt-4")
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="Renew Membership", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Renew Membership", className="card-title text-primary fs-3 fw-bold"),
                        html.P("Use this form to renew your annual membership and update company details.",
                               className="fs-5"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='renew-tin-number', placeholder='Your Company TIN *', type='text',
                                              className="form-control-lg"),
                                    width=6),
                            dbc.Col(
                                dbc.Input(id='renew-taffa-no', placeholder='Your TAFFA Membership No. *', type='text',
                                          className="form-control-lg"),
                                width=6),
                        ], className="my-3"),
                        html.Hr(),
                        html.H4("Compliance Details (For Renewal Verification)",
                                className="card-title text-primary mt-4 fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='renew-tax-compliance',
                                                 options=[{'label': 'Compliant', 'value': 'Compliant'},
                                                          {'label': 'Non-Compliant', 'value': 'Non-Compliant'}],
                                                 placeholder="Tax Compliance Status", className="dropdown-large"),
                                    width=6),
                            dbc.Col(dcc.Dropdown(id='renew-taffa-status',
                                                 options=[{'label': 'Active Member', 'value': 'Active'},
                                                          {'label': 'Inactive/Expired', 'value': 'Inactive'}],
                                                 placeholder="TAFFA Membership Status", className="dropdown-large"),
                                    width=6),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='renew-policy-compliance',
                                                 options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
                                                          {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
                                                 placeholder="Policy Compliance Status", className="dropdown-large"),
                                    width=6),
                            dbc.Col(dcc.Dropdown(id='renew-payment-confirmation',
                                                 options=[{'label': 'Paid', 'value': 'Paid'},
                                                          {'label': 'Unpaid',
                                                           'value': 'Unpaid'}],
                                                 placeholder="Renewal Fee Payment", value="Unpaid",
                                                 className="dropdown-large"), width=4),
                            dbc.Col(dbc.Button("Pay Renewal Fee", id="renew-pay-button", color="success",
                                               className="btn-lg"), width=2)
                        ], className="my-3 align-items-center"),
                        html.Hr(),
                        html.H4("Document Upload (Renewal)", className="card-title text-primary mt-4 fs-3 fw-bold"),
                        dbc.Row([
                            dbc.Col([dcc.Upload(id='renew-upload-cert-incorporation',
                                                children=html.Button('Cert of Incorporation *',
                                                                     className="btn btn-outline-primary btn-lg w-100"),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-cert-incorporation',
                                               className="text-success fs-5 ms-2")]),
                            dbc.Col([dcc.Upload(id='renew-upload-business-license',
                                                children=html.Button('Business License *',
                                                                     className="btn btn-outline-primary btn-lg w-100"),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-business-license',
                                               className="text-success fs-5 ms-2")]),
                            dbc.Col(
                                [dcc.Upload(id='renew-upload-brella-search', children=html.Button('Brella Search *',
                                                                                                  className="btn btn-outline-primary btn-lg w-100"),
                                            className="w-100 mb-2"),
                                 html.Span(id='renew-output-brella-search', className="text-success fs-5 ms-2")]),
                            dbc.Col([dcc.Upload(id='renew-upload-directors-images',
                                                children=html.Button('Directors Images *',
                                                                     className="btn btn-outline-primary btn-lg w-100"),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-directors-images',
                                               className="text-success fs-5 ms-2")]),
                        ], className="my-3"),
                        dbc.Row([
                            dbc.Col(
                                [dcc.Upload(id='renew-upload-tax-clearance', children=html.Button('Tax Clearance Cert',
                                                                                                  className="btn btn-outline-primary btn-lg w-100"),
                                            className="w-100 mb-2"),
                                 html.Span(id='renew-output-tax-clearance', className="text-success fs-5 ms-2")]),
                            dbc.Col([dcc.Upload(id='renew-upload-taffa-cert', children=html.Button('TAFFA Certificate',
                                                                                                   className="btn btn-outline-primary btn-lg w-100"),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-taffa-cert', className="text-success fs-5 ms-2")]),
                            dbc.Col(
                                [dcc.Upload(id='renew-upload-memo-articles', children=html.Button('Memo & Articles',
                                                                                                  className="btn btn-outline-primary btn-lg w-100"),
                                            className="w-100 mb-2"),
                                 html.Span(id='renew-output-memo-articles', className="text-success fs-5 ms-2")]),
                            dbc.Col([dcc.Upload(id='renew-upload-audited-accounts',
                                                children=html.Button('Audited Accounts',
                                                                     className="btn btn-outline-primary btn-lg w-100"),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-audited-accounts',
                                               className="text-success fs-5 ms-2")]),
                        ], className="my-3"),
                        html.Div(
                            dbc.Button('Submit Renewal', id='submit-renewal-button', n_clicks=0, color="primary",
                                       size="lg",
                                       className="mt-4"), className="text-center"),
                        html.Div(id='renewal-submission-output', className="mt-4")
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="Client & Document Submission", children=[
                    dbc.Card(
                        dbc.CardBody([
                            html.H1("Tanzania CFA Portal", className="text-center my-4 text-primary fs-2 fw-bold"),
                            html.P("Client & Document Submission", className="text-center text-muted fs-5"),
                            html.Hr(),
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("1. Client Information", className="card-title text-primary fw-bold fs-4"),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Client Company Name"),
                                            dbc.Input(id="client-name", type="text", placeholder="e.g., ABC Logistics")
                                        ], className="mb-3 input-group-lg")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Client TIN"),
                                            dbc.Input(id="client-tin", type="text", placeholder="e.g., 123-456-789")
                                        ], className="mb-3 input-group-lg")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Business License No."),
                                            dbc.Input(id="biz-license", type="text", placeholder="e.g., BLN/XYZ/001")
                                        ], className="mb-3 input-group-lg")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Primary Contact"),
                                            dbc.Input(id="contact-person", type="text", placeholder="e.g., Jane Doe")
                                        ], className="mb-3 input-group-lg")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Contact Phone"),
                                            dbc.Input(id="contact-phone", type="tel",
                                                      placeholder="e.g., +255-7XX-XXX-XXX")
                                        ], className="mb-3 input-group-lg")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Email Address"),
                                            dbc.Input(id="email", type="email", placeholder="e.g., jane@example.com")
                                        ], className="mb-3 input-group-lg")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("TAFFA Agent ID"),
                                            dcc.Dropdown(
                                                id="taffa-agent-id",
                                                options=[{"label": "DFO001", "value": "DFO001"},
                                                         {"label": "DFO002", "value": "DFO002"},
                                                         {"label": "DFO003", "value": "DFO003"}],
                                                placeholder="Select your TAFFA Agent ID",
                                                className="dropdown-large"
                                            )
                                        ], className="mb-3")),
                                        dbc.Col(html.Div([
                                            dcc.Upload(
                                                id='upload-authorization',
                                                children=html.Button('Select Authorization Letter',
                                                                     className='btn btn-outline-primary btn-lg w-100'),
                                                style={'cursor': 'pointer'},
                                                multiple=False
                                            ),
                                            html.Span(id='output-authorization-file',
                                                      className="text-success fs-5 mt-2 d-block text-center")
                                        ], className="mb-3"))
                                    ])
                                ], className="p-4 shadow-sm")
                            ),
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("2. Shipment Details", className="card-title text-primary fw-bold fs-4"),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Type of Shipment"),
                                            dcc.Dropdown(
                                                id="shipment-type",
                                                options=[{"label": "Import", "value": "Import"},
                                                         {"label": "Export", "value": "Export"}],
                                                placeholder="Select type",
                                                className="dropdown-large"
                                            )
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Bill of Lading / AWB No."),
                                            dbc.Input(id="bl-awb-no", type="text", placeholder="e.g., BLAWB12345")
                                        ], className="mb-3 input-group-lg")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Commercial Invoice No."),
                                            dbc.Input(id="invoice-no", type="text", placeholder="e.g., INV-00123")
                                        ], className="mb-3 input-group-lg")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Shipper/Consignor Name"),
                                            dbc.Input(id="shipper-name", type="text",
                                                      placeholder="e.g., Global Exporters Inc.")
                                        ], className="mb-3 input-group-lg")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Origin Port/Country"),
                                            dbc.Input(id="origin-port", type="text",
                                                      placeholder="e.g., Shanghai, China")
                                        ], className="mb-3 input-group-lg")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Destination Port/Country"),
                                            dbc.Input(id="destination-port", type="text",
                                                      placeholder="e.g., Dar es Salaam, Tanzania")
                                        ], className="mb-3 input-group-lg")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Date of Arrival"),
                                            dcc.DatePickerSingle(
                                                id='arrival-date',
                                                placeholder='Select a date',
                                                className="w-100"
                                            )
                                        ], className="mb-3 input-group-lg")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Cargo Description"),
                                            dbc.Input(id="cargo-desc", type="text",
                                                      placeholder="e.g., 200 boxes of electronics")
                                        ], className="mb-3 input-group-lg")),
                                    ])
                                ], className="mt-4 p-4 shadow-sm")),
                            html.Div(id='cfa-payment-status-message', className="mt-4"),
                            dbc.Row([
                                dbc.Col(dbc.Button("Pay Submission Fee", id="pay-cfa-btn", color="success",
                                                   className="btn-lg mb-3 w-100"), width={"size": 6, "offset": 3})
                            ], className="mt-4"),
                            dbc.Row(dbc.Col(
                                dbc.Button("Generate URN & Submit Consignment", id="generate-urn-btn", color="primary",
                                           className="mt-4 w-100 btn-lg", disabled=True),
                                width=6, className="mx-auto"
                            )),
                            dbc.Modal([
                                dbc.ModalHeader(dbc.ModalTitle("URN Generated Successfully!")),
                                dbc.ModalBody(
                                    html.Div([
                                        html.P("Your Unique Reference Number is:", className="text-center fs-5"),
                                        html.H2(id="urn-output", className="text-center text-primary fw-bold fs-1"),
                                        dbc.Button("Copy URN", id="copy-btn", color="secondary", className="mt-3"),
                                        dcc.Clipboard(target_id="urn-output", title="Copy to clipboard",
                                                      style={"position": "absolute", "right": "20px", "top": "20px"}),
                                    ], className="text-center")
                                ),
                                dbc.ModalFooter(
                                    dbc.Button("View Consignment in Tracker", id="proceed-btn",
                                               href="/consignment-tracker", color="success")
                                ),
                            ], id="urn-modal", is_open=False),
                            html.Div(id="dummy-output", style={"display": "none"})
                        ], className="p-4 shadow-sm")
                    )
                ]),
            ])
        ]),
        dbc.Tab(label="ADMIN LOGIN", children=[
            dcc.Store(id='admin-login-state', data={'is_authenticated': False}),
            html.Div(id="admin-content-container", children=[
                dbc.Card(dbc.CardBody([
                    html.H4("Admin Login", className="card-title text-primary fs-3 fw-bold"),
                    dbc.Input(id='admin-username', placeholder='Username', type='text',
                              className="mb-3 form-control-lg"),
                    dbc.Input(id='admin-password', placeholder='Password', type='password',
                              className="mb-3 form-control-lg"),
                    dbc.Button("Login", id="admin-login-button", color="primary", className="btn-lg"),
                    dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
                ], className="p-4 shadow-sm"))
            ])
        ], id="admin-main-tab")
    ]),
    dbc.Popover(
        [
            dbc.PopoverHeader(html.H5("Capital Pay Engine", className="fw-bold")),
            dbc.PopoverBody(
                html.Div([
                    html.P("Select a payment method:", className="mb-2"),
                    dbc.Button("Pay with M-Pesa", id="pay-cfa-mpesa-btn", color="primary",
                               className="d-block mb-2 btn-lg"),
                    dbc.Button("Pay with Bank Transfer", id="pay-cfa-bank-btn", color="primary",
                               className="d-block mb-2 btn-lg"),
                    dbc.Button("Pay with Visa/Mastercard", id="pay-cfa-card-btn", color="primary",
                               className="d-block btn-lg")
                ])
            ),
        ],
        id="cfa-payment-method-popover",
        target="",
        trigger="manual",
    ),
    dbc.Popover(
        dbc.PopoverBody("Payment successful! You can now proceed.", className="text-success fs-5"),
        id="cfa-payment-success-popover",
        target="",
        trigger="manual",
    ),
    dcc.Interval(
        id='cfa-interval-popover',
        interval=2 * 1000,
        n_intervals=0,
        disabled=True,
    ),
], fluid=True, className="bg-light p-5")


# --- Callbacks for Client & Document Submission ---

@app.callback(
    [Output("pay-cfa-btn", "disabled"),
     Output("generate-urn-btn", "disabled"),
     Output("cfa-payment-status-message", "children")],
    [Input("cfa-payment-store", "data")],
    [State("cfa-payment-store", "data")]
)
def update_cfa_payment_status(data, current_data):
    if current_data and current_data.get('status') == 'Paid':
        return True, False, html.Div(
            [dbc.Alert("Payment Confirmed! You can now generate your URN.", color="success",
                       className="text-center fs-5", dismissable=True)],
            className="mb-3"
        )
    return False, True, None


@app.callback(
    Output("cfa-payment-method-popover", "is_open"),
    Output("cfa-payment-method-popover", "target"),
    Input("pay-cfa-btn", "n_clicks"),
    prevent_initial_call=True
)
def toggle_cfa_payment_popover(n_clicks):
    if n_clicks:
        return True, "pay-cfa-btn"
    return False, ""


@app.callback(
    [Output("cfa-payment-success-popover", "is_open"),
     Output("cfa-payment-success-popover", "target"),
     Output("cfa-payment-method-popover", "is_open", allow_duplicate=True),
     Output("cfa-payment-store", "data")],
    [Input("pay-cfa-mpesa-btn", "n_clicks"),
     Input("pay-cfa-bank-btn", "n_clicks"),
     Input("pay-cfa-card-btn", "n_clicks")],
    [State("cfa-payment-method-popover", "target"),
     State("client-tin", "value")],
    prevent_initial_call=True
)
def handle_submission_payment_confirmation(mpesa_clicks, bank_clicks, card_clicks, target_id, client_tin):
    time.sleep(1)  # Simulate network delay

    if not client_tin:
        return False, "", False, dash.no_update

    payment_methods = {
        'pay-cfa-mpesa-btn': 'M-Pesa',
        'pay-cfa-bank-btn': 'Bank Transfer',
        'pay-cfa-card-btn': 'Visa/Mastercard'
    }

    triggered_id = ctx.triggered_id
    payment_method = payment_methods.get(triggered_id)

    trx_id = f"CFATR{random.randint(100000, 999999)}"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO cfa_payments (client_tin, payment_amount, payment_status, payment_method, transaction_id, payment_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (client_tin, 50000.00, 'Paid', payment_method, trx_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return True, target_id, False, {'status': 'Paid', 'trx_id': trx_id, 'client_tin': client_tin}


@app.callback(
    [Output("urn-modal", "is_open"),
     Output("urn-output", "children")],
    Input("generate-urn-btn", "n_clicks"),
    [State("taffa-agent-id", "value"),
     State("client-tin", "value"),
     State("bl-awb-no", "value"),
     State("client-name", "value"),
     State("shipper-name", "value"),
     State("origin-port", "value"),
     State("destination-port", "value"),
     State("cargo-desc", "value"),
     State("arrival-date", "date"),
     State("cfa-payment-store", "data")],
    prevent_initial_call=True
)
def generate_urn(n_clicks, taffa_agent_id, client_tin, bl_awb_no, client_name, shipper_name, origin_port,
                 destination_port, cargo_desc, arrival_date, payment_data):
    if not payment_data or payment_data.get('status') != 'Paid':
        return False, "Please confirm payment before generating a URN."

    if not all([taffa_agent_id, client_tin, bl_awb_no, client_name, shipper_name, origin_port, destination_port,
                cargo_desc, arrival_date]):
        return False, "Please fill in all mandatory fields."

    current_year = date.today().strftime("%y")
    random_part = str(random.randint(1000, 9999))
    urn = f"CFA-{current_year}-{taffa_agent_id}-{random_part}"

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO consignments (urn, taffa_agent_id, client_company, client_tin, bl_awb_no, shipper_name, origin_port, destination_port, cargo_desc, status, arrival_date, last_updated)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (urn, taffa_agent_id, client_name, client_tin, bl_awb_no, shipper_name, origin_port, destination_port,
              cargo_desc, "In Transit", arrival_date, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.IntegrityError:
        return False, "An error occurred. URN may already exist."
    finally:
        conn.close()

    return True, urn


# --- Callbacks for TAFFA Portal ---

def save_uploaded_file(contents, filename, app_id, field_name):
    if not contents:
        return None
    file_data = base64.b64decode(contents.split(',')[1])
    app_folder = os.path.join(DOCUMENTS_DIR, str(app_id))
    os.makedirs(app_folder, exist_ok=True)
    unique_filename = f"{field_name}_{filename}"
    file_path = os.path.join(app_folder, unique_filename)
    with open(file_path, 'wb') as f:
        f.write(file_data)
    return file_path


@app.callback(
    Output('output-authorization-file', 'children'),
    Input('upload-authorization', 'filename'),
    prevent_initial_call=True
)
def update_upload_output(filename):
    if filename:
        return f"✓ {filename}"
    return ""


@app.callback(
    Output('output-id-payment', 'children'),
    Input('upload-id-payment', 'contents'),
    State('upload-id-payment', 'filename'),
    prevent_initial_call=True
)
def update_id_payment_output(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')
        if 'image' in content_type:
            return html.Img(src=contents,
                            style={'width': '100px', 'height': '100px', 'object-fit': 'cover', 'margin-top': '10px'})
        return f"✓ {filename}"
    return ""


@app.callback(
    Output("admin-login-alert", "is_open"),
    Output("admin-login-alert", "children"),
    Output("admin-login-state", "data"),
    Input("admin-login-button", "n_clicks"),
    State("admin-username", "value"),
    State("admin-password", "value"),
    prevent_initial_call=True
)
def check_login(n_clicks, username, password):
    if not n_clicks:
        raise PreventUpdate
    if username == ADMIN_USER and hashlib.sha256(password.encode('utf-8')).hexdigest() == ADMIN_PASS_HASH:
        return False, "", {'is_authenticated': True}
    else:
        return True, "Invalid username or password.", {'is_authenticated': False}


@app.callback(
    Output("admin-content-container", "children"),
    Input("admin-login-state", "data")
)
def render_admin_dashboard(data):
    if data['is_authenticated']:
        return [
            html.H3("Admin Dashboard", className="text-center my-4 text-primary fs-2 fw-bold"),
            dbc.Button("Logout", id="admin-logout-btn", color="danger", className="float-end btn-sm"),
            dbc.Tabs([
                dbc.Tab(label="Overview", children=[
                    dbc.Card(dbc.CardBody([
                        html.H5("Key Performance Indicators (KPIs)", className="card-title fw-bold fs-4"),
                        dbc.Row([
                            dbc.Col(dbc.Card(dbc.CardBody(
                                [html.H6("Total Agents", className="fw-bold"),
                                 html.H2(id="kpi-total-agents", className="text-center text-primary fs-1 fw-bold")]))),
                            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Active Certifications", className="fw-bold"),
                                                           html.H2(id="kpi-active-certs",
                                                                   className="text-center text-success fs-1 fw-bold")]))),
                            dbc.Col(dbc.Card(dbc.CardBody([html.H6("New Applications (30 Days)", className="fw-bold"),
                                                           html.H2(id="kpi-new-apps",
                                                                   className="text-center text-info fs-1 fw-bold")]))),
                        ], className="my-4"),
                        dcc.Graph(id="membership-status-pie-chart")
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="Verification", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Verify Applications", className="card-title fw-bold fs-4"),
                        dash_table.DataTable(
                            id='admin-table',
                            columns=[
                                {"name": "App ID", "id": "id"},
                                {"name": "TIN", "id": "tin_number"},
                                {"name": "Company Name", "id": "company_name"},
                                {"name": "Status", "id": "status"},
                            ],
                            style_cell={'textAlign': 'left', 'fontSize': '1.1rem'},
                            style_header={'fontWeight': 'bold', 'fontSize': '1.2rem', 'backgroundColor': '#f0f0f0'},
                            style_data_conditional=[
                                {'if': {'filter_query': '{status} eq "Verified"'}, 'backgroundColor': '#d4edda',
                                 'color': '#155724'},
                                {'if': {'filter_query': '{status} eq "Pending"'}, 'backgroundColor': '#fff3cd',
                                 'color': '#856404'},
                                {'if': {'filter_query': '{status} eq "Cancelled"'}, 'backgroundColor': '#f8d7da',
                                 'color': '#721c24'}
                            ],
                            row_selectable='single',
                        ),
                        dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3 btn-lg"),
                        html.Hr(),
                        html.Div(id='admin-details-view')
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="Consignment Tracker", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Master Consignment Tracker", className="card-title text-primary fw-bold fs-4"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='tracker-search-bar', placeholder='Search by URN, BL/AWB, or Client...',
                                          type='text', className="form-control-lg"), width=6),
                            dbc.Col(dcc.DatePickerRange(id='tracker-date-range',
                                                        start_date=date.today() - timedelta(days=30),
                                                        end_date=date.today()), width=4),
                            dbc.Col(dbc.Button("Search", id="tracker-search-btn", color="primary", className="btn-lg"),
                                    width=2)
                        ], className="my-4"),
                        dbc.Button("Refresh Consignments", id="tracker-refresh-btn", color="secondary",
                                   className="btn-lg my-2"),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("Total Consignments", className="card-title fw-bold"),
                                        html.H2(id="total-consignments-kpi",
                                                className="text-center text-primary fs-1 fw-bold"),
                                    ])
                                ), width=4
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("In Transit", className="card-title fw-bold"),
                                        html.H2(id="in-transit-kpi", className="text-center text-warning fs-1 fw-bold"),
                                    ])
                                ), width=4
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("Cleared", className="card-title fw-bold"),
                                        html.H2(id="cleared-kpi", className="text-center text-success fs-1 fw-bold"),
                                    ])
                                ), width=4
                            )
                        ], className="my-4"),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id='consignment-status-pie'), width=6),
                            dbc.Col(dcc.Graph(id='cargo-type-bar'), width=6)
                        ], className="my-4"),
                        html.Div([
                            html.H5("Consignment List", className="mt-4 fw-bold fs-4"),
                            dash_table.DataTable(
                                id='consignment-table',
                                columns=[
                                    {"name": "URN", "id": "urn"},
                                    {"name": "Client", "id": "client_company"},
                                    {"name": "TAFFA Agent ID", "id": "taffa_agent_id"},
                                    {"name": "Bill of Lading", "id": "bl_awb_no"},
                                    {"name": "Cargo", "id": "cargo_desc"},
                                    {"name": "Status", "id": "status"},
                                    {"name": "Arrival Date", "id": "arrival_date"},
                                    {"name": "Last Updated", "id": "last_updated"},
                                ],
                                style_table={'overflowX': 'auto'},
                                style_cell={'textAlign': 'left', 'fontSize': '1rem'},
                                style_header={'fontWeight': 'bold', 'fontSize': '1.1rem', 'backgroundColor': '#f0f0f0'},
                                style_data_conditional=[
                                    {'if': {'filter_query': '{status} eq "Cleared"'}, 'backgroundColor': '#d4edda',
                                     'color': '#155724'},
                                    {'if': {'filter_query': '{status} eq "In Transit"'}, 'backgroundColor': '#fff3cd',
                                     'color': '#856404'},
                                    {'if': {'filter_query': '{status} eq "Delayed"'}, 'backgroundColor': '#f8d7da',
                                     'color': '#721c24'}
                                ],
                                sort_action="native",
                                page_action="native",
                                page_size=10,
                                row_selectable='single'
                            ),
                            html.Div(id='consignment-details-view', className="mt-3")
                        ])
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="View Submissions", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Submitted Applications", className="card-title fw-bold fs-4"),
                        dash_table.DataTable(
                            id='admin-applications-table',
                            columns=[
                                {"name": "TIN", "id": "tin_number"},
                                {"name": "Company Name", "id": "company_name"},
                                {"name": "Submission Date", "id": "submission_date"},
                                {"name": "Status", "id": "status"},
                                {"name": "Reference Number", "id": "reference_number"},
                            ],
                            style_cell={'textAlign': 'left', 'fontSize': '1.1rem'},
                            style_header={'fontWeight': 'bold', 'fontSize': '1.2rem', 'backgroundColor': '#f0f0f0'},
                            style_data_conditional=[
                                {'if': {'filter_query': '{status} eq "Verified"'}, 'backgroundColor': '#d4edda',
                                 'color': '#155724'},
                                {'if': {'filter_query': '{status} eq "Pending"'}, 'backgroundColor': '#fff3cd',
                                 'color': '#856404'},
                                {'if': {'filter_query': '{status} eq "Cancelled"'}, 'backgroundColor': '#f8d7da',
                                 'color': '#721c24'}
                            ],
                        ),
                        dbc.Button("Refresh Submissions", id="admin-refresh-submissions-btn", className="mt-3 btn-lg")
                    ], className="p-4 shadow-sm"))
                ]),
                dbc.Tab(label="Financials", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Financials", className="card-title fw-bold fs-4"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(dbc.CardBody([html.H6("Total Revenue", className="fw-bold"),
                                                       html.H2(id="kpi-total-revenue",
                                                               className="text-center text-success fs-1 fw-bold")])),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Card(dbc.CardBody([html.H6("Pending Invoices", className="fw-bold"),
                                                       html.H2(id="kpi-pending-invoices",
                                                               className="text-center text-warning fs-1 fw-bold")])),
                                width=6
                            )
                        ], className="my-4"),
                        dbc.Row([
                            dbc.Col(
                                dcc.Graph(id="revenue-by-invoice-status-pie"),
                                width=6
                            ),
                            dbc.Col(
                                dcc.Graph(id="payments-by-type-bar"),
                                width=6
                            )
                        ]),
                        html.H5("Invoice List", className="mt-4 fw-bold fs-4"),
                        dash_table.DataTable(
                            id='invoices-table',
                            columns=[
                                {"name": "Invoice Number", "id": "invoice_number"},
                                {"name": "Amount", "id": "amount"},
                                {"name": "Status", "id": "status"},
                                {"name": "Company Name", "id": "company_name"}
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'left', 'fontSize': '1.1rem'},
                            style_header={'fontWeight': 'bold', 'fontSize': '1.2rem', 'backgroundColor': '#f0f0f0'},
                            style_data_conditional=[
                                {'if': {'filter_query': '{status} eq "Paid"'}, 'backgroundColor': '#d4edda',
                                 'color': '#155724'},
                                {'if': {'filter_query': '{status} eq "Pending"'}, 'backgroundColor': '#fff3cd',
                                 'color': '#856404'},
                                {'if': {'filter_query': '{status} eq "Overdue"'}, 'backgroundColor': '#f8d7da',
                                 'color': '#721c24'}
                            ],
                        )
                    ], className="p-4 shadow-sm"))
                ])
            ])
        ]
    else:
        return [
            dbc.Card(dbc.CardBody([
                html.H4("Admin Login", className="card-title text-primary fs-3 fw-bold"),
                dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3 form-control-lg"),
                dbc.Input(id='admin-password', placeholder='Password', type='password',
                          className="mb-3 form-control-lg"),
                dbc.Button("Login", id="admin-login-button", color="primary", className="btn-lg"),
                dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
            ], className="p-4 shadow-sm"))
        ]


@app.callback(
    Output("admin-login-state", "data", allow_duplicate=True),
    Input("admin-logout-btn", "n_clicks"),
    prevent_initial_call=True
)
def logout(n_clicks):
    if n_clicks:
        return {'is_authenticated': False}
    raise PreventUpdate


# A single callback to update all renewal upload outputs
@app.callback(
    [
        Output('renew-output-cert-incorporation', 'children'),
        Output('renew-output-business-license', 'children'),
        Output('renew-output-brella-search', 'children'),
        Output('renew-output-directors-images', 'children'),
        Output('renew-output-tax-clearance', 'children'),
        Output('renew-output-taffa-cert', 'children'),
        Output('renew-output-memo-articles', 'children'),
        Output('renew-output-audited-accounts', 'children'),
    ],
    [
        Input('renew-upload-cert-incorporation', 'filename'),
        Input('renew-upload-business-license', 'filename'),
        Input('renew-upload-brella-search', 'filename'),
        Input('renew-upload-directors-images', 'filename'),
        Input('renew-upload-tax-clearance', 'filename'),
        Input('renew-upload-taffa-cert', 'filename'),
        Input('renew-upload-memo-articles', 'filename'),
        Input('renew-upload-audited-accounts', 'filename'),
    ],
)
def update_renewal_upload_output(cert_inc, biz_lic, brella, dir_img, tax_cert, taffa_cert, memo, audit):
    return [
        f'✓ {cert_inc}' if cert_inc else '',
        f'✓ {biz_lic}' if biz_lic else '',
        f'✓ {brella}' if brella else '',
        f'✓ {dir_img}' if dir_img else '',
        f'✓ {tax_cert}' if tax_cert else '',
        f'✓ {taffa_cert}' if taffa_cert else '',
        f'✓ {memo}' if memo else '',
        f'✓ {audit}' if audit else '',
    ]


@app.callback(
    Output("payment-method-popover", "is_open"),
    Output("payment-method-popover", "target"),
    Input("pay-button", "n_clicks"),
    Input("renew-pay-button", "n_clicks"),
    prevent_initial_call=True
)
def toggle_payment_popover(n_clicks_pay, n_clicks_renew):
    if ctx.triggered_id == "pay-button":
        return True, "pay-button"
    elif ctx.triggered_id == "renew-pay-button":
        return True, "renew-pay-button"
    return False, ""


@app.callback(
    Output("payment-success-popover", "is_open"),
    Output("payment-success-popover", "target", allow_duplicate=True),
    Output("payment-method-popover", "is_open", allow_duplicate=True),
    Output("payment-store", "data"),
    Output("interval-popover", "disabled"),
    Input("pay-equity-btn", "n_clicks"),
    Input("pay-nbc-btn", "n_clicks"),
    Input("pay-mpesa-btn", "n_clicks"),
    State("payment-method-popover", "target"),
    prevent_initial_call=True
)
def handle_payment_confirmation(equity_clicks, nbc_clicks, mpesa_clicks, target_id):
    if not any([equity_clicks, nbc_clicks, mpesa_clicks]):
        raise PreventUpdate
    time.sleep(1)
    trx_id = f"CP{random.randint(100000, 999999)}"
    return True, target_id, False, {'status': 'Paid', 'trx_id': trx_id}, False


@app.callback(
    Output("payment-success-popover", "is_open", allow_duplicate=True),
    Output("interval-popover", "disabled", allow_duplicate=True),
    Input("interval-popover", "n_intervals"),
    State("payment-success-popover", "is_open"),
    prevent_initial_call=True
)
def hide_payment_popover(n, is_open):
    if is_open:
        return False, True
    raise PreventUpdate


@app.callback(
    Output("payment-confirmation", "value"),
    Output("pay-button", "disabled"),
    Input("payment-store", "data"),
    prevent_initial_call=True
)
def update_payment_status(data):
    if data and data.get("status") == "Paid":
        return "Paid", True
    return "Unpaid", False


@app.callback(
    Output('submission-output', 'children'),
    Input('submit-button', 'n_clicks'),
    [State('tin-number', 'value'), State('company-name', 'value'), State('contact-person-taffa', 'value'),
     State('email-taffa', 'value'), State('phone-taffa', 'value'), State('physical-address', 'value'),
     State('postal-address', 'value'), State('website', 'value'), State('taffa-membership-no', 'value'),
     State('director-1', 'value'), State('director-2', 'value'), State('director-3', 'value'),
     State('cert-incorporation-no', 'value'), State('business-license-no-taffa', 'value'),
     State('membership-type', 'value'), State('agree-terms', 'value'),
     State('tax-compliance', 'value'), State('taffa-status', 'value'), State('policy-compliance', 'value'),
     State('payment-confirmation', 'value')],
    prevent_initial_call=True
)
def submit_membership_application(n_clicks, tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no,
                                  director_1, director_2, director_3, cert_inc_no, biz_lic_no, mem_type, agreed,
                                  tax, taffa, policy, payment):
    required_fields = [tin, company, contact, email, phone, phys_addr, post_addr, director_1, cert_inc_no, biz_lic_no,
                       mem_type]
    if not all(required_fields):
        return dbc.Alert("Please fill all fields marked with * and agree to the terms.", color="danger",
                         className="fs-5")
    if not agreed:
        return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning", className="fs-5")
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no, director_1, director_2,
                   director_3, cert_inc_no, biz_lic_no, mem_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        agent_id = c.lastrowid
        c.execute("""INSERT INTO applications (agent_id, agreed_to_terms, tax_compliance, taffa_status, policy_compliance, payment_confirmation)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (agent_id, 1, tax, taffa, policy, payment))
        conn.commit()
        return dbc.Alert("Membership application submitted successfully!", color="success", className="fs-5")
    except sqlite3.IntegrityError:
        return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger", className="fs-5")
    except Exception as e:
        return dbc.Alert(f"An error occurred: {e}", color="danger", className="fs-5")
    finally:
        if conn: conn.close()


@app.callback(
    Output('id-submission-output', 'children'),
    Input('submit-id-button', 'n_clicks'),
    [State('id-full-name', 'value'), State('id-nida-number', 'value'), State('id-position', 'value'),
     State('id-application-tin', 'value'),
     State('upload-passport-photo', 'contents'), State('upload-id-payment', 'contents'),
     State('upload-passport-photo', 'filename'), State('upload-id-payment', 'filename')],
    prevent_initial_call=True
)
def submit_id_application(n_clicks, full_name, nida_number, position, tin, photo_cont, payment_cont, photo_name,
                          payment_name):
    required_fields = [full_name, nida_number, position, tin, photo_cont, payment_cont]
    if not all(required_fields):
        return dbc.Alert("Please fill all fields and upload required documents.", color="danger", className="fs-5")
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id FROM agents WHERE tin_number = ?", (tin,))
        agent_id_result = c.fetchone()
        if not agent_id_result:
            return dbc.Alert(f"No existing TAFFA member found with TIN {tin}.", color="danger", className="fs-5")
        agent_id = agent_id_result['id']
        c.execute("SELECT id FROM applications WHERE agent_id = ? ORDER BY id DESC LIMIT 1", (agent_id,))
        application_id_result = c.fetchone()
        if not application_id_result:
            return dbc.Alert(f"No completed membership application found for TIN {tin}.", color="danger",
                             className="fs-5")
        application_id = application_id_result['id']
        photo_path = save_uploaded_file(photo_cont, photo_name, application_id, 'passport_photo')
        payment_path = save_uploaded_file(payment_cont, payment_name, application_id, 'id_payment_proof')
        c.execute("""INSERT INTO id_applications (application_id, full_name, nida_number, position, passport_photo, id_payment_proof)
                     VALUES (?, ?, ?, ?, ?, ?)""",
                  (application_id, full_name, nida_number, position, photo_path, payment_path))
        id_app_id = c.lastrowid
        conn.commit()
        id_app_data = c.execute("SELECT * FROM id_applications WHERE id = ?", (id_app_id,)).fetchone()
        agent_data = c.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
        filename = generate_id_card(id_app_data, agent_data)
        download_link = dcc.Link("Download ID Card", href=f"/download-id/{os.path.basename(filename)}",
                                 className="btn btn-primary mt-2")
        return [
            dbc.Alert("ID card application submitted successfully!", color="success", className="fs-5"),
            html.Div(download_link, className="mt-2")
        ]
    except Exception as e:
        return dbc.Alert(f"An error occurred: {e}", color="danger", className="fs-5")
    finally:
        if conn: conn.close()


@app.callback(
    Output('renewal-submission-output', 'children'),
    Input('submit-renewal-button', 'n_clicks'),
    [State('renew-tin-number', 'value'), State('renew-taffa-no', 'value'),
     State('renew-tax-compliance', 'value'), State('renew-taffa-status', 'value'),
     State('renew-policy-compliance', 'value'), State('renew-payment-confirmation', 'value'),
     State('renew-upload-cert-incorporation', 'contents'), State('renew-upload-business-license', 'contents'),
     State('renew-upload-brella-search', 'contents'), State('renew-upload-directors-images', 'contents'),
     State('renew-upload-tax-clearance', 'contents'), State('renew-upload-taffa-cert', 'contents'),
     State('renew-upload-memo-articles', 'contents'), State('renew-upload-audited-accounts', 'contents'),
     State('renew-upload-cert-incorporation', 'filename'), State('renew-upload-business-license', 'filename'),
     State('renew-upload-brella-search', 'filename'), State('renew-upload-directors-images', 'filename'),
     State('renew-upload-tax-clearance', 'filename'), State('renew-upload-taffa-cert', 'filename'),
     State('renew-upload-memo-articles', 'filename'), State('renew-upload-audited-accounts', 'filename')],
    prevent_initial_call=True
)
def submit_renewal(n_clicks, tin, taffa_no, tax, taffa, policy, payment,
                   cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
                   memo_cont, audit_cont, cert_inc_name, biz_lic_name, brella_name, dir_img_name, tax_cert_name,
                   taffa_cert_name, memo_name, audit_name):
    return [
        dbc.Toast(
            "Member license renewed!",
            header="Renewal Status",
            icon="success",
            dismissable=True,
            is_open=True,
            style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
        )
    ]


@app.callback(
    Output('applications-table', 'data'),
    [Input('refresh-button', 'n_clicks'), Input('submission-output', 'children')]
)
def update_table(n_clicks, submission_output):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict('records')


@app.callback(
    Output('admin-applications-table', 'data'),
    Input('admin-refresh-submissions-btn', 'n_clicks'),
    prevent_initial_call=True
)
def update_admin_submissions_table(n_clicks):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict('records')


@app.callback(
    Output('admin-table', 'data'),
    Input('admin-refresh-button', 'n_clicks'),
    prevent_initial_call=True
)
def update_admin_table(n_clicks):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT p.id, a.tin_number, a.company_name, p.status FROM agents a JOIN applications p ON a.id = p.agent_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df.to_dict('records')


@app.callback(
    Output('admin-details-view', 'children'),
    Input('admin-table', 'selected_rows'),
    State('admin-table', 'data'),
    prevent_initial_call=True
)
def display_admin_details(selected_rows, table_data):
    if not selected_rows:
        return []
    app_id = table_data[selected_rows[0]]['id']
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT * FROM agents a
        JOIN applications p ON a.id = p.agent_id
        WHERE p.id = ?
    """, (app_id,))
    data = c.fetchone()
    id_applications_query = """
        SELECT id, full_name, passport_photo, id_payment_proof, id_status FROM id_applications
        WHERE application_id = ?
    """
    id_applications = pd.read_sql_query(id_applications_query, conn, params=(app_id,))
    conn.close()
    if not data:
        return dbc.Alert("Could not retrieve application details.", color="danger")
    status_color = {
        "Verified": "success",
        "Cancelled": "danger",
        "Pending": "warning"
    }.get(data['status'], "secondary")
    document_links = []
    document_fields = {
        "Certificate of Incorporation": "cert_incorporation",
        "Business License": "business_license",
        "Brella Search": "brella_search",
        "Directors Images": "director_images",
        "Tax Clearance Cert": "tax_clearance_cert",
        "TAFFA Certificate": "taffa_cert",
        "Memo & Articles": "memo_articles",
        "Audited Accounts": "audited_accounts",
    }
    for doc_name, field in document_fields.items():
        if data[field]:
            filename = os.path.basename(data[field])
            download_link = dcc.Link(
                f"Download {doc_name}",
                href=f"/download-file/{data['agent_id']}/{filename}",
                className="d-block"
            )
            document_links.append(download_link)
    details_layout = [
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Company & Contact Information", className="fw-bold")),
                    dbc.CardBody([
                        html.P([html.Strong("Company Name: "), data['company_name']], className="fs-5"),
                        html.P([html.Strong("TIN Number: "), data['tin_number']], className="fs-5"),
                        html.P([html.Strong("Physical Address: "), data['physical_address']], className="fs-5"),
                        html.P([html.Strong("Contact Person: "), data['contact_person']], className="fs-5"),
                        html.P([html.Strong("Email: "), data['email']], className="fs-5"),
                        html.P([html.Strong("Phone: "), data['phone']], className="fs-5"),
                    ])
                ], className="p-3 shadow-sm"),
                dbc.Card([
                    dbc.CardHeader(html.H5("Director Information", className="fw-bold")),
                    dbc.CardBody([
                        html.P([html.Strong("Director 1: "), data['director_1']], className="fs-5"),
                        html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"], className="fs-5"),
                        html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"], className="fs-5"),
                    ])
                ], className="mt-3 p-3 shadow-sm"),
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Compliance & Verification", className="fw-bold")),
                    dbc.CardBody([
                        html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"],
                               className="fs-5"),
                        html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"],
                               className="fs-5"),
                        html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"],
                               className="fs-5"),
                        html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']], className="fs-5"),
                        html.P([html.Strong("Current Status: "),
                                html.Strong(data['status'], className=f"text-{status_color} fs-5")])
                    ])
                ], className="p-3 shadow-sm"),
                dbc.Card([
                    dbc.CardHeader(html.H5("Uploaded Documents (Membership)", className="fw-bold")),
                    dbc.CardBody(document_links)
                ], className="mt-3 p-3 shadow-sm"),
                dbc.Card([
                    dbc.CardHeader(html.H5("Actions (Membership)", className="fw-bold")),
                    dbc.CardBody([
                        html.H5("Update Status for Selected Application", className="fw-bold"),
                        dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
                                                                          {'label': 'Cancelled', 'value': 'Cancelled'}],
                                     placeholder="Select new status", className="dropdown-large"),
                        dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2 btn-lg"),
                        dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
                                   className="mt-2 ms-2 btn-lg", disabled=data['status'] != 'Verified'),
                        html.Div(id="download-cert-link-div", className="mt-2"),
                        html.Div(id='admin-update-output', className="mt-3")
                    ])
                ], className="mt-3 p-3 shadow-sm"),
            ], width=6),
        ], className="mt-4"),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(html.H5("ID Application Documents", className="fw-bold")),
                    dbc.CardBody(
                        html.Div(
                            [html.P(
                                "No ID Application submitted for this company.") if id_applications.empty else None] +
                            [html.Div([
                                html.P(html.Strong(f"ID for: {row['full_name']}"), className="fw-bold fs-5"),
                                dcc.Link("Download Passport Photo",
                                         href=f"/download-file/{data['agent_id']}/{os.path.basename(row['passport_photo'])}",
                                         className="d-block fs-5"),
                                dcc.Link("Download ID Payment Proof",
                                         href=f"/download-file/{data['agent_id']}/{os.path.basename(row['id_payment_proof'])}",
                                         className="d-block fs-5"),
                                html.P([html.Strong("ID Status: "), row['id_status']], className="fs-5"),
                                dcc.Link("Download ID Card", href=f"/download-id/{row['id']}", download="TAFFA_ID.pdf",
                                         target="_blank", className="btn btn-primary btn-lg mt-2") if row[
                                                                                                          'id_status'] == 'Verified' else
                                dbc.Button("Verify ID Application",
                                           id={"type": "verify-id-button", "index": str(row['id'])}, color="success",
                                           className="btn-lg mt-2")
                            ]) for index, row in id_applications.iterrows()]
                        )
                    )
                ], className="mt-3 p-3 shadow-sm"),
                width=12
            )
        ])
    ]
    return details_layout


@app.callback(
    Output('admin-update-output', 'children'),
    Input('admin-update-button', 'n_clicks'),
    [State('admin-table', 'selected_rows'), State('admin-table', 'data'), State('admin-status-dropdown', 'value')],
    prevent_initial_call=True
)
def update_status(n_clicks, selected_rows, table_data, new_status):
    if not selected_rows or not new_status:
        raise PreventUpdate
    app_id = table_data[selected_rows[0]]['id']
    ref_number = f"SUC-{date.today().strftime('%y')}-{random.choice(['DFO001', 'DFO002', 'DFO003'])}{random.randint(1000, 9999)}"

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE applications SET status = ?, reference_number = ? WHERE id = ?",
                  (new_status, ref_number, app_id))
        conn.commit()
        c.execute("SELECT a.email FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?", (app_id,))
        agent_email = c.fetchone()[0]
        email_body = (
            f"Dear Applicant,\n\n"
            f"The status of your TAFFA membership application has been updated to: {new_status}.\n\n"
            f"Reference Number: {ref_number}\n\n"
            f"Thank you,\nTAFFA Administration"
        )
        email_sent = send_email(agent_email, f"TAFFA Application Update: {new_status}", email_body)
        if email_sent:
            return [
                dbc.Alert(f"Application {app_id} updated to '{new_status}'. A notification has been sent.",
                          color="success", className="fs-5"),
                dbc.Toast(
                    "Email notification sent successfully!",
                    header="Email Status",
                    icon="success",
                    dismissable=True,
                    is_open=True,
                    style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
                )
            ]
        else:
            return dbc.Alert(f"Application {app_id} updated to '{new_status}'. Failed to send email notification.",
                             color="warning", className="fs-5")
    except Exception as e:
        return dbc.Alert(f"Error updating status: {e}", color="danger", className="fs-5")
    finally:
        if conn: conn.close()


@app.callback(
    Output({"type": "verify-id-button", "index": MATCH}, "children"),
    Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
    State({"type": "verify-id-button", "index": ALL}, "id"),
    prevent_initial_call=True
)
def verify_id_application(n_clicks, button_ids):
    if not n_clicks or not any(n_clicks):
        raise PreventUpdate
    triggered_id_json = ctx.triggered[0]['prop_id']
    triggered_id_dict = json.loads(triggered_id_json)
    clicked_id = triggered_id_dict['index']
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""SELECT p.reference_number FROM id_applications i
                 JOIN applications p ON i.application_id = p.id
                 WHERE i.id = ?""", (clicked_id,))
    ref_number_result = c.fetchone()
    if not ref_number_result:
        return dbc.Alert("Could not find membership reference number.", color="danger")
    id_number = ref_number_result['reference_number']
    expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
    c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
              ('Verified', id_number, expiry_date, clicked_id))
    conn.commit()
    conn.close()
    return "Verified!"


@app.callback(
    Output('generate-cert-button', 'disabled'),
    Input('admin-table', 'selected_rows'),
    Input('admin-update-output', 'children'),
    State('admin-table', 'data'),
    prevent_initial_call=True
)
def toggle_generate_button(selected_rows, update_output, table_data):
    if not selected_rows:
        return True
    app_id = table_data[selected_rows[0]]['id']
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
    status = c.fetchone()[0]
    conn.close()
    return status != 'Verified'


def generate_membership_certificate(app_data):
    filename = f"Certificate-{app_data['tin_number']}.pdf"
    filepath = os.path.join(CERTIFICATES_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter
    taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")

    # Certificate Border
    c.setStrokeColor(colors.HexColor('#003366'))
    c.setLineWidth(5)
    c.rect(30, 30, width - 60, height - 60)

    if os.path.exists(taffa_logo_path):
        c.drawImage(taffa_logo_path, width / 2 - 75, height - 150, width=150, height=150, preserveAspectRatio=True,
                    mask='auto')

    # Header and Title
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(colors.HexColor('#003366'))
    c.drawCentredString(width / 2.0, height - 200, "CERTIFICATE OF MEMBERSHIP")

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2.0, height - 250, "IS AWARDED TO")

    # Company Name
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2.0, height - 300, app_data['company_name'].upper())

    # Text and Signature
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2.0, height - 350,
                        f"as an official member of the Tanzania Freight Forwarder Association")
    c.drawCentredString(width / 2.0, height - 380, f"for the year {date.today().year}")

    c.line(width / 4, height / 4, width * 3 / 4, height / 4)
    c.drawCentredString(width / 2, height / 4 - 20, "TAFFA DIRECTOR")

    c.setFont("Helvetica", 12)
    c.drawRightString(width - 50, 50, f"Certificate No. {app_data['reference_number']}")
    c.drawString(50, 50, f"Date Issued: {datetime.now().strftime('%d %B, %Y')}")

    c.save()
    return filename


def generate_id_card(id_app_data, agent_data):
    filename = f"ID-{id_app_data['id_number']}.pdf"
    filepath = os.path.join(IDS_DIR, filename)
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    card_width = width * 0.75
    card_height = height * 0.75
    x_offset = (width - card_width) / 2
    y_offset = (height - card_height) / 2

    # ID Card Border
    c.setStrokeColor(colors.HexColor('#003366'))
    c.setLineWidth(5)
    c.roundRect(x_offset, y_offset, card_width, card_height, 20, stroke=1, fill=0)

    # Header Section
    header_height = card_height * 0.2
    c.setFillColor(colors.HexColor('#F0F8FF'))
    c.roundRect(x_offset, y_offset + card_height - header_height, card_width, header_height, 20, fill=1, stroke=0)

    taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
    if os.path.exists(taffa_logo_path):
        c.drawImage(taffa_logo_path, x_offset + 20, y_offset + card_height - header_height + 10, width=80, height=80,
                    preserveAspectRatio=True)

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#003366'))
    c.drawCentredString(x_offset + card_width / 2, y_offset + card_height - 60,
                        "TANZANIA FREIGHT FORWARDERS ASSOCIATION")
    c.setFont("Helvetica", 14)
    c.drawCentredString(x_offset + card_width / 2, y_offset + card_height - 80, "Official Member ID Card")

    # Photo
    photo_path = id_app_data['passport_photo']
    photo_size = 120
    photo_x = x_offset + (card_width - photo_size) / 2
    photo_y = y_offset + card_height - header_height - 20 - photo_size
    if os.path.exists(photo_path):
        c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True)

    # User Details
    details_y_start = photo_y - 30
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, details_y_start, f"Name: {id_app_data['full_name']}")
    c.drawCentredString(width / 2, details_y_start - 30, f"Position: {id_app_data['position']}")
    c.drawCentredString(width / 2, details_y_start - 60, f"Company: {agent_data['company_name']}")

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#003366'))
    c.drawCentredString(width / 2, details_y_start - 120, f"ID NO: {id_app_data['id_number']}")
    c.drawCentredString(width / 2, details_y_start - 150, f"Expiry Date: {id_app_data['expiry_date']}")

    # QR Code
    qr_data = f"ID: {id_app_data['id_number']} | Expiry: {id_app_data['expiry_date']} | Status: Active"
    qr_img = qrcode.make(qr_data)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_size = 100
    qr_x = width / 2 - qr_size / 2
    qr_y = y_offset + 20
    c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)

    c.save()
    return filename


@app.callback(
    Output('download-cert-link-div', 'children'),
    Input('generate-cert-button', 'n_clicks'),
    State('admin-table', 'selected_rows'),
    State('admin-table', 'data'),
    prevent_initial_call=True
)
def handle_certificate_generation(n_clicks, selected_rows, table_data):
    if not selected_rows:
        raise PreventUpdate
    app_id = table_data[selected_rows[0]]['id']
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT a.tin_number, a.company_name, p.reference_number, p.status
        FROM agents a JOIN applications p ON a.id = p.agent_id
        WHERE p.id = ?
    """
    df = pd.read_sql_query(query, conn, params=(app_id,))
    conn.close()
    if df.empty:
        return dbc.Alert("Could not find application data.", color="danger", className="fs-5")
    app_data = df.to_dict('records')[0]
    filename = generate_membership_certificate(app_data)
    return dcc.Link(f"Download Certificate for {app_data['company_name']}",
                    href=f"/download-cert/{os.path.basename(filename)}", className="btn btn-info btn-lg")


@app.callback(
    [
        Output('kpi-total-agents', 'children'),
        Output('kpi-active-certs', 'children'),
        Output('kpi-new-apps', 'children'),
        Output('membership-status-pie-chart', 'figure'),
    ],
    Input('admin-login-state', 'data')
)
def update_kpis_and_charts(data):
    if not data or not data['is_authenticated']:
        return None, None, None, {}

    conn = sqlite3.connect(DB_PATH)
    total_agents = pd.read_sql_query("SELECT COUNT(*) FROM agents", conn).iloc[0, 0]
    active_certs = pd.read_sql_query("SELECT COUNT(*) FROM applications WHERE status = 'Verified'", conn).iloc[0, 0]
    last_30_days = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

    # Corrected query with JOIN
    new_apps_query = f"""
        SELECT COUNT(*)
        FROM applications a
        JOIN agents ag ON a.agent_id = ag.id
        WHERE ag.submission_date > '{last_30_days}'
    """
    new_apps = pd.read_sql_query(new_apps_query, conn).iloc[0, 0]

    status_counts = pd.read_sql_query("SELECT status, COUNT(*) as count FROM applications GROUP BY status", conn)
    conn.close()

    pie_chart = px.pie(status_counts, values='count', names='status', title='Membership Application Status')

    return total_agents, active_certs, new_apps, pie_chart


@app.callback(
    [
        Output('kpi-total-revenue', 'children'),
        Output('kpi-pending-invoices', 'children'),
        Output('revenue-by-invoice-status-pie', 'figure'),
        Output('payments-by-type-bar', 'figure'),
        Output('invoices-table', 'data')
    ],
    Input('admin-login-state', 'data')
)
def update_financials(data):
    if not data or not data['is_authenticated']:
        return None, None, {}, {}, []

    conn = sqlite3.connect(DB_PATH)

    invoices_df = pd.read_sql_query("SELECT * FROM invoices", conn)
    payments_df = pd.read_sql_query("SELECT * FROM payments", conn)
    agents_df = pd.read_sql_query("SELECT id, company_name FROM agents", conn)
    cfa_payments_df = pd.read_sql_query("SELECT * FROM cfa_payments", conn)
    conn.close()

    invoices_df = pd.merge(invoices_df, agents_df, left_on='agent_id', right_on='id', how='left')

    # Total revenue from both TAFFA and CFA submissions
    taffa_revenue = invoices_df[invoices_df['status'] == 'Paid']['amount'].sum()
    cfa_revenue = cfa_payments_df[cfa_payments_df['payment_status'] == 'Paid']['payment_amount'].sum()
    total_revenue = taffa_revenue + cfa_revenue

    pending_invoices = invoices_df[invoices_df['status'] == 'Pending']['amount'].sum()

    invoice_status_counts = invoices_df['status'].value_counts().reset_index()
    invoice_status_counts.columns = ['Status', 'Count']
    revenue_pie = px.pie(invoice_status_counts, values='Count', names='Status', title='TAFFA Invoices by Status')

    all_payments_df = pd.DataFrame(
        {'payment_type': payments_df['payment_type'], 'amount': payments_df['amount']})
    cfa_payments_short = pd.DataFrame(
        {'payment_type': cfa_payments_df['payment_method'], 'amount': cfa_payments_df['payment_amount']})
    all_payments_df = pd.concat([all_payments_df, cfa_payments_short])

    payments_by_type = all_payments_df.groupby('payment_type')['amount'].sum().reset_index()
    payments_by_type.columns = ['Payment Type', 'Amount']
    payments_bar = px.bar(payments_by_type, x='Payment Type', y='Amount', title='Total Revenue by Payment Method')

    return f"TZS {total_revenue:,.2f}", f"TZS {pending_invoices:,.2f}", revenue_pie, payments_bar, invoices_df.to_dict(
        'records')


@app.callback(
    [
        Output('consignment-table', 'data'),
        Output('total-consignments-kpi', 'children'),
        Output('in-transit-kpi', 'children'),
        Output('cleared-kpi', 'children'),
        Output('consignment-status-pie', 'figure'),
        Output('cargo-type-bar', 'figure')
    ],
    [
        Input('tracker-search-btn', 'n_clicks'),
        Input('tracker-search-bar', 'value'),
        Input('tracker-date-range', 'start_date'),
        Input('tracker-date-range', 'end_date'),
        Input('tracker-refresh-btn', 'n_clicks'),
        Input('generate-urn-btn', 'n_clicks')  # Re-runs when a new URN is generated
    ]
)
def update_consignment_dashboard(search_btn_clicks, search_term, start_date, end_date, refresh_btn_clicks, urn_clicks):
    # This callback now depends on multiple inputs, so it will trigger on any change.
    # The logic remains the same: query the DB and update the UI components.
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM consignments WHERE 1=1"
    params = []

    if search_term:
        query += " AND (urn LIKE ? OR bl_awb_no LIKE ? OR client_company LIKE ?)"
        search_term_like = f"%{search_term}%"
        params.extend([search_term_like, search_term_like, search_term_like])

    if start_date and end_date:
        query += " AND arrival_date BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    df = pd.read_sql_query(query, conn, params=params)
    conn.close()

    total_consignments = len(df)
    in_transit = len(df[df['status'] == 'In Transit'])
    cleared = len(df[df['status'] == 'Cleared'])

    status_counts = df['status'].value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    pie_chart = px.pie(status_counts, values='Count', names='Status', title='Consignment Status Distribution')

    cargo_counts = df['cargo_desc'].value_counts().reset_index()
    cargo_counts.columns = ['Cargo Type', 'Count']
    bar_chart = px.bar(cargo_counts, x='Cargo Type', y='Count', title='Top 5 Cargo Types')

    return (
        df.to_dict('records'),
        total_consignments,
        in_transit,
        cleared,
        pie_chart,
        bar_chart
    )


@app.callback(
    Output('consignment-details-view', 'children'),
    Input('consignment-table', 'selected_rows'),
    State('consignment-table', 'data')
)
def display_consignment_details(selected_rows, table_data):
    if not selected_rows:
        return []

    row = table_data[selected_rows[0]]

    return dbc.Card(
        dbc.CardBody([
            html.H5(f"Consignment Details: {row['urn']}", className="card-title fs-4 fw-bold"),
            html.P([html.Strong("Client Company: "), row['client_company']], className="fs-5"),
            html.P([html.Strong("TAFFA Agent ID: "), row['taffa_agent_id']], className="fs-5"),
            html.P([html.Strong("Bill of Lading / AWB No.: "), row['bl_awb_no']], className="fs-5"),
            html.P([html.Strong("Shipper/Consignor: "), row['shipper_name']], className="fs-5"),
            html.P([html.Strong("Origin: "), row['origin_port']], className="fs-5"),
            html.P([html.Strong("Destination: "), row['destination_port']], className="fs-5"),
            html.P([html.Strong("Cargo Description: "), row['cargo_desc']], className="fs-5"),
            html.P([html.Strong("Status: "), html.Span(row['status'],
                                                       className=f"badge rounded-pill bg-{'warning' if row['status'] == 'In Transit' else 'success' if row['status'] == 'Cleared' else 'info'}")])
        ]),
        className="mt-3 p-3 shadow-sm"
    )


# --- Flask Server Routes ---

@server.route('/download-cert/<filename>')
def serve_pdf(filename):
    return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)


@server.route('/download-id/<filename>')
def serve_id(filename):
    return send_from_directory(IDS_DIR, filename, as_attachment=True)


@server.route('/download-file/<app_id>/<filename>')
def download_uploaded_file(app_id, filename):
    app_folder = os.path.join(DOCUMENTS_DIR, app_id)
    return send_from_directory(app_folder, filename, as_attachment=True)


if __name__ == '__main__':
    if not os.path.exists(DOCUMENTS_DIR):
        os.makedirs(DOCUMENTS_DIR)
    if not os.path.exists(CERTIFICATES_DIR):
        os.makedirs(CERTIFICATES_DIR)
    if not os.path.exists(IDS_DIR):
        os.makedirs(IDS_DIR)
    assets_dir = os.path.join(BASE_DIR, 'assets')
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    app.run(debug=True, port=5570)
