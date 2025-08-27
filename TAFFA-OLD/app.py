# # # # # import dash
# # # # # from dash import dcc, html, Input, Output, State, ctx, dash_table
# # # # # import dash_bootstrap_components as dbc
# # # # # from dash.exceptions import PreventUpdate
# # # # # import sqlite3
# # # # # import pandas as pd
# # # # # from datetime import datetime, date
# # # # # import base64
# # # # # import io
# # # # # from reportlab.lib.pagesizes import letter
# # # # # from reportlab.pdfgen import canvas
# # # # # from reportlab.lib.utils import ImageReader
# # # # # from reportlab.lib import colors
# # # # # from PIL import Image
# # # # # import os
# # # # # import random
# # # # # import time
# # # # # import smtplib
# # # # # from email.message import EmailMessage
# # # # # import socket
# # # # # from flask import send_from_directory
# # # # # import qrcode
# # # # # import hashlib
# # # # #
# # # # # # Initialize the Dash app with Flask server and suppress callback exceptions
# # # # # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True,
# # # # #                 title="TAFFA Portal")
# # # # # server = app.server
# # # # #
# # # # # # --- Admin Credentials ---
# # # # # ADMIN_USER = "admin"
# # # # # ADMIN_PASS_HASH = hashlib.sha256("password".encode('utf-8')).hexdigest()  # Hash the password "password"
# # # # #
# # # # # # --- Database Setup with Absolute Path ---
# # # # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # # # # DB_PATH = os.path.join(BASE_DIR, "tra_cfa_data.db")
# # # # # DOCUMENTS_DIR = os.path.join(BASE_DIR, "uploaded_documents")
# # # # # CERTIFICATES_DIR = os.path.join(BASE_DIR, "certificates")
# # # # #
# # # # #
# # # # # def init_db():
# # # # #     conn = sqlite3.connect(DB_PATH)
# # # # #     c = conn.cursor()
# # # # #
# # # # #     # Drop tables to ensure a clean slate and prevent schema errors on re-runs
# # # # #     c.execute('DROP TABLE IF EXISTS applications')
# # # # #     c.execute('DROP TABLE IF EXISTS agents')
# # # # #     c.execute('DROP TABLE IF EXISTS taffa_id_applications')
# # # # #
# # # # #     # agents table updated to match the latest fields
# # # # #     c.execute('''
# # # # #         CREATE TABLE IF NOT EXISTS agents (
# # # # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # # # #             tin_number TEXT NOT NULL UNIQUE,
# # # # #             company_name TEXT NOT NULL,
# # # # #             contact_person TEXT NOT NULL,
# # # # #             email TEXT NOT NULL,
# # # # #             phone TEXT NOT NULL,
# # # # #             physical_address TEXT,
# # # # #             postal_address TEXT,
# # # # #             website TEXT,
# # # # #             taffa_membership_no TEXT,
# # # # #             director_1 TEXT,
# # # # #             director_2 TEXT,
# # # # #             director_3 TEXT,
# # # # #             cert_incorporation_no TEXT,
# # # # #             business_license_no TEXT,
# # # # #             membership_type TEXT,
# # # # #             submission_date TEXT NOT NULL
# # # # #         )
# # # # #     ''')
# # # # #     # applications table updated to store file paths as TEXT
# # # # #     c.execute('''
# # # # #         CREATE TABLE IF NOT EXISTS applications (
# # # # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # # # #             agent_id INTEGER,
# # # # #             tax_compliance TEXT,
# # # # #             taffa_status TEXT,
# # # # #             policy_compliance TEXT,
# # # # #             payment_confirmation TEXT,
# # # # #             business_license TEXT,
# # # # #             tax_clearance_cert TEXT,
# # # # #             taffa_cert TEXT,
# # # # #             cert_incorporation TEXT,
# # # # #             memo_articles TEXT,
# # # # #             audited_accounts TEXT,
# # # # #             director_images TEXT,
# # # # #             brella_search TEXT,
# # # # #             agreed_to_terms INTEGER,
# # # # #             merged_pdf_for_id TEXT,
# # # # #             id_payment_proof TEXT,
# # # # #             status TEXT DEFAULT 'Pending',
# # # # #             reference_number TEXT,
# # # # #             FOREIGN KEY (agent_id) REFERENCES agents (id)
# # # # #         )
# # # # #     ''')
# # # # #     conn.commit()
# # # # #     conn.close()
# # # # #
# # # # #
# # # # # init_db()
# # # # #
# # # # # # --- Logo Paths ---
# # # # # taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # # # # taffa_logo_src = "/assets/LOGO.png"
# # # # #
# # # # #
# # # # # # --- Reusable Components ---
# # # # # def logo_header(logo_src, text):
# # # # #     return dbc.Row([
# # # # #         dbc.Col(html.Img(src=logo_src, height="80px"), width="auto"),
# # # # #         dbc.Col(html.H5(text, className="align-self-center"))
# # # # #     ], className="mb-4 align-items-center justify-content-center")
# # # # #
# # # # #
# # # # # def send_email(recipient_email: str, subject: str, body: str):
# # # # #     """Sends an email notification."""
# # # # #     sender_email = "administrator@capitalpayinternational.com"
# # # # #     sender_password = "ahxr wusz rqvp jpsx"
# # # # #     smtp_server = "smtp.gmail.com"
# # # # #     smtp_port = 587
# # # # #
# # # # #     if not sender_password:
# # # # #         print("Error: Email password is not set.")
# # # # #         return False
# # # # #
# # # # #     msg = EmailMessage()
# # # # #     msg['Subject'] = f"Update: Milestone Reached - {subject}"
# # # # #     msg['From'] = sender_email
# # # # #     msg['To'] = recipient_email
# # # # #     msg.set_content(body)
# # # # #
# # # # #     try:
# # # # #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# # # # #             server.starttls()
# # # # #             server.login(sender_email, sender_password)
# # # # #             server.send_message(msg)
# # # # #             print(f"Email notification sent successfully to {recipient_email}!")
# # # # #             return True
# # # # #     except socket.gaierror as e:
# # # # #         print(f"Network error: {e}. Could not find host: '{smtp_server}'.")
# # # # #         return False
# # # # #     except Exception as e:
# # # # #         print(f"An unexpected error occurred: {e}")
# # # # #         return False
# # # # #
# # # # #
# # # # # # --- App Layout ---
# # # # # app.layout = dbc.Container([
# # # # #     dcc.Store(id='payment-store'),
# # # # #     dcc.Store(id='login-state', data={'is_authenticated': False}),
# # # # #     dbc.Row([
# # # # #         dbc.Col(html.Img(src="/assets/LOGO.png", height="100px"), width="auto"),
# # # # #         dbc.Col(html.H1("Customs Agent Accreditation Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
# # # # #                 width="auto")
# # # # #     ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),
# # # # #
# # # # #     dbc.Tabs(id='tabs', children=[
# # # # #         dbc.Tab(label="New/Renewal Membership", children=[
# # # # #             dbc.Card(dbc.CardBody([
# # # # #                 html.H4("Membership Application Form", className="card-title text-primary"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text'), width=6),
# # # # #                     dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text'), width=6),
# # # # #                 ], className="mb-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text'),
# # # # #                             width=6),
# # # # #                     dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text'), width=6),
# # # # #                 ], className="mb-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dbc.Input(id='website', placeholder='Website', type='text'), width=6),
# # # # #                     dbc.Col(dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
# # # # #                                       type='text'), width=6),
# # # # #                 ], className="mb-3"),
# # # # #                 html.Hr(),
# # # # #                 html.H4("Contact Person", className="card-title text-primary mt-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dbc.Input(id='contact-person', placeholder='Contact Person Name *', type='text'), width=4),
# # # # #                     dbc.Col(dbc.Input(id='email', placeholder='Email Address *', type='email'), width=4),
# # # # #                     dbc.Col(dbc.Input(id='phone', placeholder='Mobile Number *', type='text'), width=4),
# # # # #                 ], className="mb-3"),
# # # # #                 html.Hr(),
# # # # #                 html.H4("Directors", className="card-title text-primary mt-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text'), width=4),
# # # # #                     dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text'), width=4),
# # # # #                     dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text'), width=4),
# # # # #                 ], className="mb-3"),
# # # # #                 html.Hr(),
# # # # #                 html.H4("Company Details", className="card-title text-primary mt-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
# # # # #                                       type='text'), width=6),
# # # # #                     dbc.Col(dbc.Input(id='business-license-no', placeholder='Business License No. *', type='text'),
# # # # #                             width=6),
# # # # #                 ], className="mb-3"),
# # # # #                 dcc.Dropdown(id='membership-type', options=[
# # # # #                     {'label': 'Ordinary Member', 'value': 'Ordinary'},
# # # # #                     {'label': 'Inhouse Member', 'value': 'Inhouse'}
# # # # #                 ], placeholder="Choose Membership Type *", className="mb-3"),
# # # # #                 html.Hr(),
# # # # #                 html.H4("Compliance Details (For Verification)", className="card-title text-primary mt-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
# # # # #                                                                        {'label': 'Non-Compliant',
# # # # #                                                                         'value': 'Non-Compliant'}],
# # # # #                                          placeholder="Tax Compliance Status"), width=6),
# # # # #                     dbc.Col(dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
# # # # #                                                                      {'label': 'Inactive/Expired',
# # # # #                                                                       'value': 'Inactive'}],
# # # # #                                          placeholder="TAFFA Membership Status"), width=6),
# # # # #                 ], className="mb-3"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col(dcc.Dropdown(id='policy-compliance',
# # # # #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# # # # #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# # # # #                                          placeholder="Policy Compliance Status"), width=6),
# # # # #                     dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# # # # #                                                                              {'label': 'Unpaid', 'value': 'Unpaid'}],
# # # # #                                          placeholder="Accreditation Fee Payment", value="Unpaid"), width=4),
# # # # #                     dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success"), width=2)
# # # # #                 ], className="mb-3 align-items-center"),
# # # # #                 html.Hr(),
# # # # #                 html.H4("Document Upload (Membership)", className="card-title text-primary mt-4"),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col([dcc.Upload(id='upload-cert-incorporation', children=html.Button('Cert of Incorporation *'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-cert-incorporation')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-business-license', children=html.Button('Business License *'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-business-license')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-brella-search', children=html.Button('Brella Search *'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-brella-search')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-director-images', children=html.Button('Directors Images *'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-director-images')]),
# # # # #                 ]),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col([dcc.Upload(id='upload-tax-clearance', children=html.Button('Tax Clearance Cert'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-tax-clearance')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-taffa-cert', children=html.Button('TAFFA Certificate'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-taffa-cert')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-memo-articles', children=html.Button('Memo & Articles'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-memo-articles')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-audited-accounts', children=html.Button('Audited Accounts'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-audited-accounts')]),
# # # # #                 ]),
# # # # #                 html.Hr(),
# # # # #                 html.H4("TAFFA ID Application (Optional)", className="card-title text-primary mt-4"),
# # # # #                 html.P("If you are also applying for TAFFA IDs, please upload the required documents below."),
# # # # #                 html.Ul([
# # # # #                     html.Li(
# # # # #                         "Merged PDF with: Full names, NIDA number, position, physical address, passport photos (white background), and current TAFFA certificate."),
# # # # #                     html.Li("Proof of payment for the IDs.")
# # # # #                 ]),
# # # # #                 dbc.Row([
# # # # #                     dbc.Col([dcc.Upload(id='upload-merged-pdf', children=html.Button('Upload Merged PDF'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-merged-pdf')]),
# # # # #                     dbc.Col([dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof'),
# # # # #                                         className="w-100 mb-2"), html.Span(id='output-id-payment')]),
# # # # #                 ]),
# # # # #                 dcc.Checklist(options=[
# # # # #                     {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations', 'value': 1}],
# # # # #                     id='agree-terms', className="mt-4"),
# # # # #                 html.Div(dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
# # # # #                                     className="mt-4"), className="text-center"),
# # # # #                 html.Div(id='submission-output', className="mt-4")
# # # # #             ]))
# # # # #         ]),
# # # # #         dbc.Tab(label="View Submissions", children=[
# # # # #             dbc.Card(dbc.CardBody([
# # # # #                 html.H4("Submitted Applications", className="card-title"),
# # # # #                 dash_table.DataTable(
# # # # #                     id='applications-table',
# # # # #                     columns=[
# # # # #                         {"name": "TIN", "id": "tin_number"},
# # # # #                         {"name": "Company Name", "id": "company_name"},
# # # # #                         {"name": "Submission Date", "id": "submission_date"},
# # # # #                         {"name": "Status", "id": "status"},
# # # # #                         {"name": "Reference Number", "id": "reference_number"},
# # # # #                     ],
# # # # #                     style_cell={'textAlign': 'left'},
# # # # #                 ),
# # # # #                 dbc.Button("Refresh Data", id="refresh-button", className="mt-3")
# # # # #             ]))
# # # # #         ]),
# # # # #         # Admin Verification tab is now dynamic
# # # # #         dbc.Tab(label="Admin Verification", id='admin-tab-content', children=[
# # # # #             # This content will be dynamically rendered by a callback
# # # # #         ])
# # # # #     ]),
# # # # #     # --- Payment Popovers ---
# # # # #     dbc.Popover(
# # # # #         [
# # # # #             dbc.PopoverHeader("Capital Pay Engine"),
# # # # #             dbc.PopoverBody(
# # # # #                 html.Div([
# # # # #                     dbc.Button("Pay with Equity Bank", id="pay-equity-btn", color="primary", className="d-block mb-2"),
# # # # #                     dbc.Button("Pay with NBC Bank", id="pay-nbc-btn", color="primary", className="d-block mb-2"),
# # # # #                     dbc.Button("Pay with M-Pesa", id="pay-mpesa-btn", color="primary", className="d-block")
# # # # #                 ])
# # # # #             ),
# # # # #         ],
# # # # #         id="payment-method-popover",
# # # # #         target="pay-button",
# # # # #         trigger="click",
# # # # #     ),
# # # # #     dbc.Popover(
# # # # #         dbc.PopoverBody("Payment of 20,000 TZS successful!", className="text-success"),
# # # # #         id="payment-success-popover",
# # # # #         target="pay-button",
# # # # #         trigger="manual",
# # # # #     ),
# # # # #     dcc.Interval(
# # # # #         id='interval-popover',
# # # # #         interval=12 * 1000,
# # # # #         n_intervals=0,
# # # # #         disabled=True,
# # # # #     ),
# # # # # ], fluid=True)
# # # # #
# # # # # # --- Helper function for saving uploaded files ---
# # # # # def save_uploaded_file(contents, filename, app_id, field_name):
# # # # #     if not contents:
# # # # #         return None
# # # # #
# # # # #     file_data = base64.b64decode(contents.split(',')[1])
# # # # #     app_folder = os.path.join(DOCUMENTS_DIR, str(app_id))
# # # # #     os.makedirs(app_folder, exist_ok=True)
# # # # #     unique_filename = f"{field_name}_{filename}"
# # # # #     file_path = os.path.join(app_folder, unique_filename)
# # # # #
# # # # #     with open(file_path, 'wb') as f:
# # # # #         f.write(file_data)
# # # # #
# # # # #     return file_path
# # # # #
# # # # #
# # # # # # --- Callbacks ---
# # # # #
# # # # # # Admin Login Callback
# # # # # @app.callback(
# # # # #     Output('login-state', 'data'),
# # # # #     Output('admin-login-alert', 'children'),
# # # # #     Output('admin-login-alert', 'is_open'),
# # # # #     Input('admin-login-button', 'n_clicks'),
# # # # #     State('admin-username', 'value'),
# # # # #     State('admin-password', 'value'),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def check_login(n_clicks, username, password):
# # # # #     if not n_clicks:
# # # # #         raise PreventUpdate
# # # # #
# # # # #     if username == ADMIN_USER and hashlib.sha256(password.encode('utf-8')).hexdigest() == ADMIN_PASS_HASH:
# # # # #         return {'is_authenticated': True}, "", False
# # # # #     else:
# # # # #         return {'is_authenticated': False}, "Invalid username or password.", True
# # # # #
# # # # #
# # # # # # Dynamically render Admin Tab content
# # # # # @app.callback(
# # # # #     Output('admin-tab-content', 'children'),
# # # # #     Input('login-state', 'data')
# # # # # )
# # # # # def render_admin_tab_content(data):
# # # # #     if data['is_authenticated']:
# # # # #         return [
# # # # #             dbc.Card(dbc.CardBody([
# # # # #                 html.H4("Verify Applications", className="card-title"),
# # # # #                 dash_table.DataTable(
# # # # #                     id='admin-table',
# # # # #                     columns=[
# # # # #                         {"name": "App ID", "id": "id"},
# # # # #                         {"name": "TIN", "id": "tin_number"},
# # # # #                         {"name": "Company Name", "id": "company_name"},
# # # # #                         {"name": "Status", "id": "status"},
# # # # #                     ],
# # # # #                     style_cell={'textAlign': 'left'},
# # # # #                     row_selectable='single',
# # # # #                 ),
# # # # #                 dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3"),
# # # # #                 html.Hr(),
# # # # #                 html.Div(id='admin-details-view')
# # # # #             ]))
# # # # #         ]
# # # # #     else:
# # # # #         return [
# # # # #             dbc.Card(dbc.CardBody([
# # # # #                 html.H4("Admin Login", className="card-title"),
# # # # #                 dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
# # # # #                 dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
# # # # #                 dbc.Button("Login", id="admin-login-button", color="primary"),
# # # # #                 dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
# # # # #             ]))
# # # # #         ]
# # # # #
# # # # # # File upload status messages
# # # # # for short_name in ['cert-incorporation', 'business-license', 'brella-search', 'director-images', 'tax-clearance',
# # # # #                    'taffa-cert', 'memo-articles', 'audited-accounts', 'merged-pdf', 'id-payment']:
# # # # #     @app.callback(
# # # # #         Output(f'output-{short_name}', 'children'),
# # # # #         Input(f'upload-{short_name}', 'filename'),
# # # # #         prevent_initial_call=True
# # # # #     )
# # # # #     def update_upload_output(filename):
# # # # #         if filename: return f'✓ {filename}'
# # # # #         return ''
# # # # #
# # # # #
# # # # # # --- Payment Callbacks ---
# # # # # @app.callback(
# # # # #     Output("payment-store", "data"),
# # # # #     Output("payment-success-popover", "is_open"),
# # # # #     Output("interval-popover", "disabled"),
# # # # #     Output("payment-method-popover", "is_open"),
# # # # #     Input("pay-equity-btn", "n_clicks"),
# # # # #     Input("pay-nbc-btn", "n_clicks"),
# # # # #     Input("pay-mpesa-btn", "n_clicks"),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def handle_payment_confirmation(equity_clicks, nbc_clicks, mpesa_clicks):
# # # # #     if not any([equity_clicks, nbc_clicks, mpesa_clicks]):
# # # # #         raise PreventUpdate
# # # # #
# # # # #     time.sleep(1)
# # # # #     trx_id = f"CP{random.randint(100000, 999999)}"
# # # # #
# # # # #     return {'status': 'Paid', 'trx_id': trx_id}, True, False, False
# # # # #
# # # # #
# # # # # @app.callback(
# # # # #     Output("payment-success-popover", "is_open", allow_duplicate=True),
# # # # #     Output("interval-popover", "disabled", allow_duplicate=True),
# # # # #     Input("interval-popover", "n_intervals"),
# # # # #     State("payment-success-popover", "is_open"),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def hide_payment_popover(n, is_open):
# # # # #     if is_open:
# # # # #         return False, True
# # # # #     raise PreventUpdate
# # # # #
# # # # #
# # # # # @app.callback(
# # # # #     Output("payment-confirmation", "value"),
# # # # #     Output("pay-button", "disabled"),
# # # # #     Input("payment-store", "data"),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def update_payment_status(data):
# # # # #     if data and data.get("status") == "Paid":
# # # # #         return "Paid", True
# # # # #     return "Unpaid", False
# # # # #
# # # # #
# # # # # # --- Form Submission Callback ---
# # # # # @app.callback(
# # # # #     Output('submission-output', 'children'),
# # # # #     Input('submit-button', 'n_clicks'),
# # # # #     [State('tin-number', 'value'), State('company-name', 'value'), State('contact-person', 'value'),
# # # # #      State('email', 'value'), State('phone', 'value'), State('physical-address', 'value'),
# # # # #      State('postal-address', 'value'), State('website', 'value'), State('taffa-membership-no', 'value'),
# # # # #      State('director-1', 'value'), State('director-2', 'value'), State('director-3', 'value'),
# # # # #      State('cert-incorporation-no', 'value'), State('business-license-no', 'value'),
# # # # #      State('membership-type', 'value'), State('agree-terms', 'value'),
# # # # #      State('tax-compliance', 'value'), State('taffa-status', 'value'), State('policy-compliance', 'value'),
# # # # #      State('payment-confirmation', 'value'),
# # # # #      State('upload-cert-incorporation', 'contents'), State('upload-business-license', 'contents'),
# # # # #      State('upload-brella-search', 'contents'), State('upload-director-images', 'contents'),
# # # # #      State('upload-tax-clearance', 'contents'), State('upload-taffa-cert', 'contents'),
# # # # #      State('upload-memo-articles', 'contents'), State('upload-audited-accounts', 'contents'),
# # # # #      State('upload-merged-pdf', 'contents'), State('upload-id-payment', 'contents'),
# # # # #      State('upload-cert-incorporation', 'filename'), State('upload-business-license', 'filename'),
# # # # #      State('upload-brella-search', 'filename'), State('upload-director-images', 'filename'),
# # # # #      State('upload-tax-clearance', 'filename'), State('upload-taffa-cert', 'filename'),
# # # # #      State('upload-memo-articles', 'filename'), State('upload-audited-accounts', 'filename'),
# # # # #      State('upload-merged-pdf', 'filename'), State('upload-id-payment', 'filename')],
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def submit_membership_application(n_clicks, tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no,
# # # # #                                   director_1, director_2, director_3, cert_inc_no, biz_lic_no, mem_type, agreed,
# # # # #                                   tax, taffa, policy, payment,
# # # # #                                   cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont,
# # # # #                                   taffa_cert_cont,
# # # # #                                   memo_cont, audit_cont, merged_pdf_cont, id_payment_cont,
# # # # #                                   cert_inc_name, biz_lic_name, brella_name, dir_img_name, tax_cert_name,
# # # # #                                   taffa_cert_name,
# # # # #                                   memo_name, audit_name, merged_pdf_name, id_payment_name):
# # # # #     required_fields = [tin, company, contact, email, phone, phys_addr, post_addr, director_1, cert_inc_no, biz_lic_no,
# # # # #                        mem_type, cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont]
# # # # #     if not all(required_fields):
# # # # #         return dbc.Alert("Please fill all fields marked with * and upload the required documents.", color="danger")
# # # # #     if not agreed:
# # # # #         return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning")
# # # # #
# # # # #     try:
# # # # #         conn = sqlite3.connect(DB_PATH)
# # # # #         c = conn.cursor()
# # # # #
# # # # #         # Insert agent data first to get agent_id
# # # # #         c.execute("""INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
# # # # #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
# # # # #                   (tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no, director_1, director_2,
# # # # #                    director_3, cert_inc_no, biz_lic_no, mem_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
# # # # #         agent_id = c.lastrowid
# # # # #
# # # # #         # Save files to disk and get their paths
# # # # #         cert_inc_path = save_uploaded_file(cert_inc_cont, cert_inc_name, agent_id, 'cert_inc')
# # # # #         biz_lic_path = save_uploaded_file(biz_lic_cont, biz_lic_name, agent_id, 'biz_lic')
# # # # #         brella_path = save_uploaded_file(brella_cont, brella_name, agent_id, 'brella')
# # # # #         dir_img_path = save_uploaded_file(dir_img_cont, dir_img_name, agent_id, 'dir_img')
# # # # #         tax_cert_path = save_uploaded_file(tax_cert_cont, tax_cert_name, agent_id, 'tax_cert')
# # # # #         taffa_cert_path = save_uploaded_file(taffa_cert_cont, taffa_cert_name, agent_id, 'taffa_cert')
# # # # #         memo_path = save_uploaded_file(memo_cont, memo_name, agent_id, 'memo')
# # # # #         audit_path = save_uploaded_file(audit_cont, audit_name, agent_id, 'audit')
# # # # #         merged_pdf_path = save_uploaded_file(merged_pdf_cont, merged_pdf_name, agent_id, 'merged_pdf')
# # # # #         id_payment_path = save_uploaded_file(id_payment_cont, id_payment_name, agent_id, 'id_payment')
# # # # #
# # # # #         # Insert application data with file paths
# # # # #         c.execute("""INSERT INTO applications (agent_id, agreed_to_terms, tax_compliance, taffa_status, policy_compliance, payment_confirmation, cert_incorporation, business_license, brella_search, director_images, tax_clearance_cert, taffa_cert, memo_articles, audited_accounts, merged_pdf_for_id, id_payment_proof)
# # # # #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
# # # # #                   (agent_id, 1, tax, taffa, policy, payment,
# # # # #                    cert_inc_path, biz_lic_path, brella_path, dir_img_path,
# # # # #                    tax_cert_path, taffa_cert_path, memo_path, audit_path,
# # # # #                    merged_pdf_path, id_payment_path
# # # # #                    ))
# # # # #         conn.commit()
# # # # #         return dbc.Alert("Membership application submitted successfully!", color="success")
# # # # #     except sqlite3.IntegrityError:
# # # # #         return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger")
# # # # #     except Exception as e:
# # # # #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# # # # #     finally:
# # # # #         if conn: conn.close()
# # # # #
# # # # #
# # # # # # Refresh public applications table
# # # # # @app.callback(
# # # # #     Output('applications-table', 'data'),
# # # # #     [Input('refresh-button', 'n_clicks'), Input('submission-output', 'children')]
# # # # # )
# # # # # def update_table(n_clicks, submission_output):
# # # # #     conn = sqlite3.connect(DB_PATH)
# # # # #     query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
# # # # #     df = pd.read_sql_query(query, conn)
# # # # #     conn.close()
# # # # #     return df.to_dict('records')
# # # # #
# # # # #
# # # # # # --- Admin Panel Callbacks ---
# # # # # @app.callback(
# # # # #     Output('admin-table', 'data'),
# # # # #     Input('admin-refresh-button', 'n_clicks'),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def update_admin_table(n_clicks):
# # # # #     conn = sqlite3.connect(DB_PATH)
# # # # #     query = "SELECT p.id, a.tin_number, a.company_name, p.status FROM agents a JOIN applications p ON a.id = p.agent_id"
# # # # #     df = pd.read_sql_query(query, conn)
# # # # #     conn.close()
# # # # #     return df.to_dict('records')
# # # # #
# # # # #
# # # # # @app.callback(
# # # # #     Output('admin-details-view', 'children'),
# # # # #     Input('admin-table', 'selected_rows'),
# # # # #     State('admin-table', 'data'),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def display_admin_details(selected_rows, table_data):
# # # # #     if not selected_rows:
# # # # #         return []
# # # # #
# # # # #     app_id = table_data[selected_rows[0]]['id']
# # # # #     conn = sqlite3.connect(DB_PATH)
# # # # #     conn.row_factory = sqlite3.Row
# # # # #     c = conn.cursor()
# # # # #     c.execute("""
# # # # #         SELECT * FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?
# # # # #     """, (app_id,))
# # # # #     data = c.fetchone()
# # # # #     conn.close()
# # # # #
# # # # #     if not data:
# # # # #         return dbc.Alert("Could not retrieve application details.", color="danger")
# # # # #
# # # # #     status_color = {
# # # # #         "Verified": "success",
# # # # #         "Cancelled": "danger",
# # # # #         "Pending": "warning"
# # # # #     }.get(data['status'], "secondary")
# # # # #
# # # # #     # Generate document download links dynamically
# # # # #     document_links = []
# # # # #     document_fields = {
# # # # #         "Certificate of Incorporation": "cert_incorporation",
# # # # #         "Business License": "business_license",
# # # # #         "Brella Search": "brella_search",
# # # # #         "Directors Images": "director_images",
# # # # #         "Tax Clearance Cert": "tax_clearance_cert",
# # # # #         "TAFFA Certificate": "taffa_cert",
# # # # #         "Memo & Articles": "memo_articles",
# # # # #         "Audited Accounts": "audited_accounts",
# # # # #         "Merged PDF for ID": "merged_pdf_for_id",
# # # # #         "ID Payment Proof": "id_payment_proof"
# # # # #     }
# # # # #
# # # # #     for doc_name, field in document_fields.items():
# # # # #         if data[field]:
# # # # #             filename = os.path.basename(data[field])
# # # # #             download_link = dcc.Link(
# # # # #                 f"Download {doc_name}",
# # # # #                 href=f"/download-file/{str(app_id)}/{filename}",
# # # # #                 className="d-block"
# # # # #             )
# # # # #             document_links.append(download_link)
# # # # #
# # # # #     details_layout = [
# # # # #         dbc.Row([
# # # # #             dbc.Col([
# # # # #                 dbc.Card([
# # # # #                     dbc.CardHeader("Company & Contact Information"),
# # # # #                     dbc.CardBody([
# # # # #                         html.P([html.Strong("Company Name: "), data['company_name']]),
# # # # #                         html.P([html.Strong("TIN Number: "), data['tin_number']]),
# # # # #                         html.P([html.Strong("Physical Address: "), data['physical_address']]),
# # # # #                         html.P([html.Strong("Contact Person: "), data['contact_person']]),
# # # # #                         html.P([html.Strong("Email: "), data['email']]),
# # # # #                         html.P([html.Strong("Phone: "), data['phone']]),
# # # # #                     ])
# # # # #                 ]),
# # # # #                 dbc.Card([
# # # # #                     dbc.CardHeader("Director Information"),
# # # # #                     dbc.CardBody([
# # # # #                         html.P([html.Strong("Director 1: "), data['director_1']]),
# # # # #                         html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"]),
# # # # #                         html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"]),
# # # # #                     ])
# # # # #                 ], className="mt-3"),
# # # # #             ], width=6),
# # # # #             dbc.Col([
# # # # #                 dbc.Card([
# # # # #                     dbc.CardHeader("Compliance & Verification"),
# # # # #                     dbc.CardBody([
# # # # #                         html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"]),
# # # # #                         html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"]),
# # # # #                         html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"]),
# # # # #                         html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']]),
# # # # #                         html.P([html.Strong("Current Status: "),
# # # # #                                 html.Strong(data['status'], className=f"text-{status_color}")])
# # # # #                     ])
# # # # #                 ]),
# # # # #                 dbc.Card([
# # # # #                     dbc.CardHeader("Uploaded Documents"),
# # # # #                     dbc.CardBody(document_links)
# # # # #                 ], className="mt-3"),
# # # # #                 dbc.Card([
# # # # #                     dbc.CardHeader("Actions"),
# # # # #                     dbc.CardBody([
# # # # #                         html.H5("Update Status for Selected Application"),
# # # # #                         dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
# # # # #                                                                           {'label': 'Cancelled', 'value': 'Cancelled'}],
# # # # #                                      placeholder="Select new status"),
# # # # #                         dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2"),
# # # # #                         dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
# # # # #                                    className="mt-2 ms-2", disabled=data['status'] != 'Verified'),
# # # # #                         html.Div(id="download-cert-link-div", className="mt-2"),
# # # # #                         html.Div(id='admin-update-output', className="mt-3")
# # # # #                     ])
# # # # #                 ], className="mt-3"),
# # # # #             ], width=6),
# # # # #         ], className="mt-4")
# # # # #     ]
# # # # #     return details_layout
# # # # #
# # # # #
# # # # # @app.callback(
# # # # #     Output('admin-update-output', 'children'),
# # # # #     Input('admin-update-button', 'n_clicks'),
# # # # #     [State('admin-table', 'selected_rows'), State('admin-table', 'data'), State('admin-status-dropdown', 'value')],
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def update_status(n_clicks, selected_rows, table_data, new_status):
# # # # #     if not selected_rows or not new_status:
# # # # #         raise PreventUpdate
# # # # #
# # # # #     app_id = table_data[selected_rows[0]]['id']
# # # # #     ref_number = f"TAFFA-TRA-{random.randint(10000, 99999)}{'PASS' if new_status == 'Verified' else 'FAIL'}"
# # # # #
# # # # #     try:
# # # # #         conn = sqlite3.connect(DB_PATH)
# # # # #         c = conn.cursor()
# # # # #         c.execute("UPDATE applications SET status = ?, reference_number = ? WHERE id = ?",
# # # # #                   (new_status, ref_number, app_id))
# # # # #         conn.commit()
# # # # #
# # # # #         c.execute("SELECT a.email FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?", (app_id,))
# # # # #         agent_email = c.fetchone()[0]
# # # # #
# # # # #         email_body = (
# # # # #             f"Dear Applicant,\n\n"
# # # # #             f"The status of your TAFFA membership application has been updated to: {new_status}.\n\n"
# # # # #             f"Reference Number: {ref_number}\n\n"
# # # # #             f"Thank you,\nTAFFA Administration"
# # # # #         )
# # # # #
# # # # #         email_sent = send_email(agent_email, f"TAFFA Application Update: {new_status}", email_body)
# # # # #
# # # # #         if email_sent:
# # # # #             return [
# # # # #                 dbc.Alert(f"Application {app_id} updated to '{new_status}'. A notification has been sent.",
# # # # #                           color="success"),
# # # # #                 dbc.Toast(
# # # # #                     "Email notification sent successfully!",
# # # # #                     header="Email Status",
# # # # #                     icon="success",
# # # # #                     dismissable=True,
# # # # #                     is_open=True,
# # # # #                     style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# # # # #                 )
# # # # #             ]
# # # # #         else:
# # # # #             return dbc.Alert(f"Application {app_id} updated to '{new_status}'. Failed to send email notification.",
# # # # #                              color="warning")
# # # # #
# # # # #     except Exception as e:
# # # # #         return dbc.Alert(f"Error updating status: {e}", color="danger")
# # # # #     finally:
# # # # #         if conn: conn.close()
# # # # #
# # # # #
# # # # # @app.callback(
# # # # #     Output('generate-cert-button', 'disabled'),
# # # # #     Input('admin-table', 'selected_rows'),
# # # # #     Input('admin-update-output', 'children'),
# # # # #     State('admin-table', 'data'),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def toggle_generate_button(selected_rows, update_output, table_data):
# # # # #     if not selected_rows:
# # # # #         return True
# # # # #
# # # # #     app_id = table_data[selected_rows[0]]['id']
# # # # #     conn = sqlite3.connect(DB_PATH)
# # # # #     c = conn.cursor()
# # # # #     c.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
# # # # #     status = c.fetchone()[0]
# # # # #     conn.close()
# # # # #
# # # # #     return status != 'Verified'
# # # # #
# # # # #
# # # # # def generate_certificate(app_data):
# # # # #     filename = f"certificate_{app_data['tin_number']}.pdf"
# # # # #     filepath = os.path.join(CERTIFICATES_DIR, filename)
# # # # #     c = canvas.Canvas(filepath, pagesize=letter)
# # # # #     width, height = letter
# # # # #
# # # # #     c.setStrokeColor(colors.HexColor('#0d6efd'))
# # # # #     c.setLineWidth(5)
# # # # #     c.rect(10, 10, width - 20, height - 20)
# # # # #
# # # # #     # Use the same TAFFA logo from assets folder for both placements, pushed down
# # # # #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # # # #     if os.path.exists(taffa_logo_path):
# # # # #         c.drawImage(taffa_logo_path, width - 150, height - 100, width=100, preserveAspectRatio=True, mask='auto')
# # # # #         c.drawImage(taffa_logo_path, 50, height - 100, width=100, preserveAspectRatio=True, mask='auto')
# # # # #
# # # # #     c.setFont("Helvetica-Bold", 24)
# # # # #     c.setFillColor(colors.HexColor('#0d6efd'))
# # # # #     c.drawCentredString(width / 2.0, height - 120, "Certificate of Accreditation")
# # # # #
# # # # #     c.setFont("Helvetica", 12)
# # # # #     c.setFillColor(colors.black)
# # # # #     c.drawCentredString(width / 2.0, height - 150, "Issued by the Tanzania Freight Forwarders Association (TAFFA)")
# # # # #     c.drawCentredString(width / 2.0, height - 170, "in collaboration with the Tanzania Revenue Authority (TRA)")
# # # # #
# # # # #     c.setFont("Helvetica", 16)
# # # # #     c.drawCentredString(width / 2.0, height - 250, "This is to certify that:")
# # # # #
# # # # #     c.setFont("Helvetica-Bold", 24)
# # # # #     c.drawCentredString(width / 2.0, height - 290, app_data['company_name'].upper())
# # # # #
# # # # #     c.setFont("Helvetica", 14)
# # # # #     c.drawCentredString(width / 2.0, height - 320, f"with TIN: {app_data['tin_number']}")
# # # # #
# # # # #     c.drawString(100, height - 400, "has been successfully accredited as a Customs Clearing and")
# # # # #     c.drawString(100, height - 420, "Forwarding Agent.")
# # # # #
# # # # #     # New serial number and combined reference string for QR code data
# # # # #     serial_number = f"SN-{random.randint(1000, 9999)}"
# # # # #     combined_ref = f"{app_data['reference_number']}/{serial_number}"
# # # # #
# # # # #     c.drawString(100, height - 480, f"Reference Number: {combined_ref}")
# # # # #     c.drawString(100, height - 500, f"Date of Issue: {date.today().strftime('%B %d, %Y')}")
# # # # #
# # # # #     # Generate and draw QR code with verification status and combined reference
# # # # #     qr_data = f"{combined_ref} - Status: {app_data['status'].upper()}"
# # # # #     qr_img = qrcode.make(qr_data)
# # # # #     qr_buffer = io.BytesIO()
# # # # #     qr_img.save(qr_buffer, format='PNG')
# # # # #     qr_buffer.seek(0)
# # # # #     c.drawImage(ImageReader(qr_buffer), width - 150, 180, width=100, height=100)  # Moved up by 30 points for spacing
# # # # #
# # # # #     c.drawRightString(width - 100, 150, "Authorized Signature, TAFFA & TRA")
# # # # #
# # # # #     c.save()
# # # # #     return filename
# # # # #
# # # # #
# # # # # @app.callback(
# # # # #     Output('download-cert-link-div', 'children'),
# # # # #     Input('generate-cert-button', 'n_clicks'),
# # # # #     State('admin-table', 'selected_rows'),
# # # # #     State('admin-table', 'data'),
# # # # #     prevent_initial_call=True
# # # # # )
# # # # # def handle_certificate_generation(n_clicks, selected_rows, table_data):
# # # # #     if not selected_rows:
# # # # #         raise PreventUpdate
# # # # #
# # # # #     app_id = table_data[selected_rows[0]]['id']
# # # # #
# # # # #     conn = sqlite3.connect(DB_PATH)
# # # # #     query = """
# # # # #         SELECT a.tin_number, a.company_name, p.reference_number, p.status
# # # # #         FROM agents a JOIN applications p ON a.id = p.agent_id
# # # # #         WHERE p.id = ?
# # # # #     """
# # # # #     df = pd.read_sql_query(query, conn, params=(app_id,))
# # # # #     conn.close()
# # # # #
# # # # #     if df.empty:
# # # # #         return dbc.Alert("Could not find application data.", color="danger")
# # # # #
# # # # #     app_data = df.to_dict('records')[0]
# # # # #     filename = generate_certificate(app_data)
# # # # #
# # # # #     # Use the new Flask route for certificates
# # # # #     return dcc.Link(f"Download Certificate for {app_data['company_name']}",
# # # # #                     href=f"/download-cert/{os.path.basename(filename)}")
# # # # #
# # # # #
# # # # # # Flask route to serve the dynamically generated PDF from the certificates folder
# # # # # @server.route('/download-cert/<filename>')
# # # # # def serve_pdf(filename):
# # # # #     return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)
# # # # #
# # # # #
# # # # # # Flask route to serve the uploaded documents from the new folder
# # # # # @server.route('/download-file/<app_id>/<filename>')
# # # # # def download_uploaded_file(app_id, filename):
# # # # #     app_folder = os.path.join(DOCUMENTS_DIR, app_id)
# # # # #     return send_from_directory(app_folder, filename, as_attachment=True)
# # # # #
# # # # #
# # # # # if __name__ == '__main__':
# # # # #     # Ensure the necessary directories exist
# # # # #     if not os.path.exists(DOCUMENTS_DIR):
# # # # #         os.makedirs(DOCUMENTS_DIR)
# # # # #     if not os.path.exists(CERTIFICATES_DIR):
# # # # #         os.makedirs(CERTIFICATES_DIR)
# # # # #
# # # # #     assets_dir = os.path.join(BASE_DIR, 'assets')
# # # # #     if not os.path.exists(assets_dir):
# # # # #         os.makedirs(assets_dir)
# # # # #
# # # # #     app.run(debug=True, port=5078)
# # # #
# # # #
# # # # import dash
# # # # from dash import dcc, html, Input, Output, State, ctx, dash_table
# # # # import dash_bootstrap_components as dbc
# # # # from dash.exceptions import PreventUpdate
# # # # import sqlite3
# # # # import pandas as pd
# # # # from datetime import datetime, date, timedelta
# # # # import base64
# # # # import io
# # # # from reportlab.lib.pagesizes import letter, A4
# # # # from reportlab.pdfgen import canvas
# # # # from reportlab.lib.utils import ImageReader
# # # # from reportlab.lib import colors
# # # # from reportlab.lib.units import inch
# # # # from PIL import Image
# # # # import os
# # # # import random
# # # # import time
# # # # import smtplib
# # # # from email.message import EmailMessage
# # # # import socket
# # # # from flask import send_from_directory
# # # # import qrcode
# # # # import hashlib
# # # # from dash.dependencies import MATCH, ALL
# # # # import json
# # # #
# # # # # Initialize the Dash app with Flask server and suppress callback exceptions
# # # # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True,
# # # #                 title="TAFFA Portal")
# # # # server = app.server
# # # #
# # # # # --- Admin Credentials ---
# # # # ADMIN_USER = "admin"
# # # # ADMIN_PASS_HASH = hashlib.sha256("password".encode('utf-8')).hexdigest()
# # # #
# # # # # --- Database Setup with Absolute Path ---
# # # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # # # DB_PATH = os.path.join(BASE_DIR, "tra_cfa_data.db")
# # # # DOCUMENTS_DIR = os.path.join(BASE_DIR, "uploaded_documents")
# # # # CERTIFICATES_DIR = os.path.join(BASE_DIR, "certificates")
# # # # IDS_DIR = os.path.join(BASE_DIR, "id_cards")
# # # #
# # # #
# # # # def init_db():
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     c = conn.cursor()
# # # #
# # # #     # Drop tables to ensure a clean slate and prevent schema errors on re-runs
# # # #     c.execute('DROP TABLE IF EXISTS id_applications')
# # # #     c.execute('DROP TABLE IF EXISTS applications')
# # # #     c.execute('DROP TABLE IF EXISTS agents')
# # # #     c.execute('DROP TABLE IF EXISTS taffa_id_applications')
# # # #
# # # #     # agents table updated to match the latest fields
# # # #     c.execute('''
# # # #         CREATE TABLE IF NOT EXISTS agents (
# # # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # # #             tin_number TEXT NOT NULL UNIQUE,
# # # #             company_name TEXT NOT NULL,
# # # #             contact_person TEXT NOT NULL,
# # # #             email TEXT NOT NULL,
# # # #             phone TEXT NOT NULL,
# # # #             physical_address TEXT,
# # # #             postal_address TEXT,
# # # #             website TEXT,
# # # #             taffa_membership_no TEXT,
# # # #             director_1 TEXT,
# # # #             director_2 TEXT,
# # # #             director_3 TEXT,
# # # #             cert_incorporation_no TEXT,
# # # #             business_license_no TEXT,
# # # #             membership_type TEXT,
# # # #             submission_date TEXT NOT NULL
# # # #         )
# # # #     ''')
# # # #     # applications table updated to store file paths as TEXT
# # # #     c.execute('''
# # # #         CREATE TABLE IF NOT EXISTS applications (
# # # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # # #             agent_id INTEGER,
# # # #             tax_compliance TEXT,
# # # #             taffa_status TEXT,
# # # #             policy_compliance TEXT,
# # # #             payment_confirmation TEXT,
# # # #             business_license TEXT,
# # # #             tax_clearance_cert TEXT,
# # # #             taffa_cert TEXT,
# # # #             cert_incorporation TEXT,
# # # #             memo_articles TEXT,
# # # #             audited_accounts TEXT,
# # # #             director_images TEXT,
# # # #             brella_search TEXT,
# # # #             agreed_to_terms INTEGER,
# # # #             status TEXT DEFAULT 'Pending',
# # # #             reference_number TEXT,
# # # #             FOREIGN KEY (agent_id) REFERENCES agents (id)
# # # #         )
# # # #     ''')
# # # #     # New table for ID applications
# # # #     c.execute('''
# # # #         CREATE TABLE IF NOT EXISTS id_applications (
# # # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # # #             application_id INTEGER,
# # # #             full_name TEXT,
# # # #             nida_number TEXT,
# # # #             position TEXT,
# # # #             passport_photo TEXT,
# # # #             id_payment_proof TEXT,
# # # #             id_status TEXT DEFAULT 'Pending',
# # # #             id_number TEXT,
# # # #             expiry_date TEXT,
# # # #             FOREIGN KEY (application_id) REFERENCES applications (id)
# # # #         )
# # # #     ''')
# # # #
# # # #     conn.commit()
# # # #     conn.close()
# # # #
# # # #
# # # # init_db()
# # # #
# # # # # --- Logo Paths ---
# # # # taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # # # taffa_logo_src = "/assets/LOGO.png"
# # # #
# # # #
# # # # # --- Reusable Components ---
# # # # def logo_header(logo_src, text):
# # # #     return dbc.Row([
# # # #         dbc.Col(html.Img(src=logo_src, height="80px"), width="auto"),
# # # #         dbc.Col(html.H5(text, className="align-self-center"))
# # # #     ], className="mb-4 align-items-center justify-content-center")
# # # #
# # # #
# # # # def send_email(recipient_email: str, subject: str, body: str):
# # # #     """Sends an email notification."""
# # # #     sender_email = "administrator@capitalpayinternational.com"
# # # #     sender_password = "ahxr wusz rqvp jpsx"
# # # #     smtp_server = "smtp.gmail.com"
# # # #     smtp_port = 587
# # # #
# # # #     if not sender_password:
# # # #         print("Error: Email password is not set.")
# # # #         return False
# # # #
# # # #     msg = EmailMessage()
# # # #     msg['Subject'] = f"Update: Milestone Reached - {subject}"
# # # #     msg['From'] = sender_email
# # # #     msg['To'] = recipient_email
# # # #     msg.set_content(body)
# # # #
# # # #     try:
# # # #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# # # #             server.starttls()
# # # #             server.login(sender_email, sender_password)
# # # #             server.send_message(msg)
# # # #             print(f"Email notification sent successfully to {recipient_email}!")
# # # #             return True
# # # #     except socket.gaierror as e:
# # # #         print(f"Network error: {e}. Could not find host: '{smtp_server}'.")
# # # #         return False
# # # #     except Exception as e:
# # # #         print(f"An unexpected error occurred: {e}")
# # # #         return False
# # # #
# # # #
# # # # # --- App Layout ---
# # # # app.layout = dbc.Container([
# # # #     dcc.Store(id='payment-store'),
# # # #     dcc.Store(id='login-state', data={'is_authenticated': False}),
# # # #     dbc.Row([
# # # #         dbc.Col(html.Img(src="/assets/LOGO.png", height="100px"), width="auto"),
# # # #         dbc.Col(html.H1("Customs Agent Accreditation Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
# # # #                 width="auto")
# # # #     ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),
# # # #
# # # #     dbc.Tabs(id='tabs', children=[
# # # #         dbc.Tab(label="New Application", children=[
# # # #             dbc.Card(dbc.CardBody([
# # # #                 html.H4("Membership Application Form", className="card-title text-primary"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text'), width=6),
# # # #                     dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text'), width=6),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text'),
# # # #                             width=6),
# # # #                     dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text'), width=6),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='website', placeholder='Website', type='text'), width=6),
# # # #                     dbc.Col(dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
# # # #                                       type='text'), width=6),
# # # #                 ], className="mb-3"),
# # # #                 html.Hr(),
# # # #                 html.H4("Contact Person", className="card-title text-primary mt-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='contact-person', placeholder='Contact Person Name *', type='text'), width=4),
# # # #                     dbc.Col(dbc.Input(id='email', placeholder='Email Address *', type='email'), width=4),
# # # #                     dbc.Col(dbc.Input(id='phone', placeholder='Mobile Number *', type='text'), width=4),
# # # #                 ], className="mb-3"),
# # # #                 html.Hr(),
# # # #                 html.H4("Directors", className="card-title text-primary mt-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text'), width=4),
# # # #                     dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text'), width=4),
# # # #                     dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text'), width=4),
# # # #                 ], className="mb-3"),
# # # #                 html.Hr(),
# # # #                 html.H4("Company Details", className="card-title text-primary mt-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
# # # #                                       type='text'), width=6),
# # # #                     dbc.Col(dbc.Input(id='business-license-no', placeholder='Business License No. *', type='text'),
# # # #                             width=6),
# # # #                 ], className="mb-3"),
# # # #                 dcc.Dropdown(id='membership-type', options=[
# # # #                     {'label': 'Ordinary Member', 'value': 'Ordinary'},
# # # #                     {'label': 'Inhouse Member', 'value': 'Inhouse'}
# # # #                 ], placeholder="Choose Membership Type *", className="mb-3"),
# # # #                 html.Hr(),
# # # #                 html.H4("Compliance Details (For Verification)", className="card-title text-primary mt-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
# # # #                                                                        {'label': 'Non-Compliant',
# # # #                                                                         'value': 'Non-Compliant'}],
# # # #                                          placeholder="Tax Compliance Status"), width=6),
# # # #                     dbc.Col(dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
# # # #                                                                      {'label': 'Inactive/Expired',
# # # #                                                                       'value': 'Inactive'}],
# # # #                                          placeholder="TAFFA Membership Status"), width=6),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dcc.Dropdown(id='policy-compliance',
# # # #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# # # #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# # # #                                          placeholder="Policy Compliance Status"), width=6),
# # # #                     dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# # # #                                                                              {'label': 'Unpaid', 'value': 'Unpaid'}],
# # # #                                          placeholder="Accreditation Fee Payment", value="Unpaid"), width=4),
# # # #                     dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success"), width=2)
# # # #                 ], className="mb-3 align-items-center"),
# # # #                 html.Hr(),
# # # #                 dcc.Checklist(options=[
# # # #                     {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations', 'value': 1}],
# # # #                     id='agree-terms', className="mt-4"),
# # # #                 html.Div(dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
# # # #                                     className="mt-4"), className="text-center"),
# # # #                 html.Div(id='submission-output', className="mt-4")
# # # #             ]))
# # # #         ]),
# # # #         dbc.Tab(label="TAFFA ID Application", children=[
# # # #             dbc.Card(dbc.CardBody([
# # # #                 html.H4("TAFFA ID Application", className="card-title text-primary"),
# # # #                 html.P("This form is for TAFFA members to apply for an ID card."),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='id-full-name', placeholder='Full Name *', type='text'), width=6),
# # # #                     dbc.Col(dbc.Input(id='id-nida-number', placeholder='NIDA Number *', type='text'), width=6),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='id-position', placeholder='Position *', type='text'), width=6),
# # # #                     dbc.Col([dcc.Upload(id='upload-passport-photo', children=html.Button('Upload Passport Photo *'),
# # # #                                         className="w-100 mb-2"), html.Span(id='output-passport-photo')]),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col([dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof *'),
# # # #                                         className="w-100 mb-2"), html.Span(id='output-id-payment')]),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Input(id='id-application-tin', placeholder='Your Company TIN *', type='text', className="mb-3"),
# # # #                 dbc.Button('Submit ID Application', id='submit-id-button', n_clicks=0, color="primary", size="lg",
# # # #                            className="mt-4"),
# # # #                 html.Div(id='id-submission-output', className="mt-4")
# # # #             ]))
# # # #         ]),
# # # #         dbc.Tab(label="Renew Membership", children=[
# # # #             dbc.Card(dbc.CardBody([
# # # #                 html.H4("Renew Membership", className="card-title text-primary"),
# # # #                 html.P("Use this form to renew your annual membership and update company details."),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dbc.Input(id='renew-tin-number', placeholder='Your Company TIN *', type='text'), width=6),
# # # #                     dbc.Col(dbc.Input(id='renew-taffa-no', placeholder='Your TAFFA Membership No. *', type='text'),
# # # #                             width=6),
# # # #                 ], className="mb-3"),
# # # #                 html.Hr(),
# # # #                 html.H4("Compliance Details (For Renewal Verification)", className="card-title text-primary mt-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dcc.Dropdown(id='renew-tax-compliance',
# # # #                                          options=[{'label': 'Compliant', 'value': 'Compliant'},
# # # #                                                   {'label': 'Non-Compliant', 'value': 'Non-Compliant'}],
# # # #                                          placeholder="Tax Compliance Status"), width=6),
# # # #                     dbc.Col(dcc.Dropdown(id='renew-taffa-status',
# # # #                                          options=[{'label': 'Active Member', 'value': 'Active'},
# # # #                                                   {'label': 'Inactive/Expired', 'value': 'Inactive'}],
# # # #                                          placeholder="TAFFA Membership Status"), width=6),
# # # #                 ], className="mb-3"),
# # # #                 dbc.Row([
# # # #                     dbc.Col(dcc.Dropdown(id='renew-policy-compliance',
# # # #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# # # #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# # # #                                          placeholder="Policy Compliance Status"), width=6),
# # # #                     dbc.Col(dcc.Dropdown(id='renew-payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# # # #                                                                                    {'label': 'Unpaid',
# # # #                                                                                     'value': 'Unpaid'}],
# # # #                                          placeholder="Renewal Fee Payment", value="Unpaid"), width=4),
# # # #                     dbc.Col(dbc.Button("Pay Renewal Fee", id="renew-pay-button", color="success"), width=2)
# # # #                 ], className="mb-3 align-items-center"),
# # # #                 html.Hr(),
# # # #                 html.H4("Document Upload (Renewal)", className="card-title text-primary mt-4"),
# # # #                 dbc.Row([
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-cert-incorporation',
# # # #                                         children=html.Button('Cert of Incorporation *'), className="w-100 mb-2"),
# # # #                              html.Span(id='renew-output-cert-incorporation')]),
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-business-license', children=html.Button('Business License *'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-business-license')]),
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-brella-search', children=html.Button('Brella Search *'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-brella-search')]),
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-directors-images', children=html.Button('Directors Images *'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-directors-images')]),
# # # #                 ]),
# # # #                 dbc.Row([
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-tax-clearance', children=html.Button('Tax Clearance Cert'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-tax-clearance')]),
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-taffa-cert', children=html.Button('TAFFA Certificate'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-taffa-cert')]),
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-memo-articles', children=html.Button('Memo & Articles'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-memo-articles')]),
# # # #                     dbc.Col([dcc.Upload(id='renew-upload-audited-accounts', children=html.Button('Audited Accounts'),
# # # #                                         className="w-100 mb-2"), html.Span(id='renew-output-audited-accounts')]),
# # # #                 ]),
# # # #                 html.Div(
# # # #                     dbc.Button('Submit Renewal', id='submit-renewal-button', n_clicks=0, color="primary", size="lg",
# # # #                                className="mt-4"), className="text-center"),
# # # #                 html.Div(id='renewal-submission-output', className="mt-4")
# # # #             ]))
# # # #         ]),
# # # #         dbc.Tab(label="View Submissions", children=[
# # # #             dbc.Card(dbc.CardBody([
# # # #                 html.H4("Submitted Applications", className="card-title"),
# # # #                 dash_table.DataTable(
# # # #                     id='applications-table',
# # # #                     columns=[
# # # #                         {"name": "TIN", "id": "tin_number"},
# # # #                         {"name": "Company Name", "id": "company_name"},
# # # #                         {"name": "Submission Date", "id": "submission_date"},
# # # #                         {"name": "Status", "id": "status"},
# # # #                         {"name": "Reference Number", "id": "reference_number"},
# # # #                     ],
# # # #                     style_cell={'textAlign': 'left'},
# # # #                 ),
# # # #                 dbc.Button("Refresh Data", id="refresh-button", className="mt-3")
# # # #             ]))
# # # #         ]),
# # # #         dbc.Tab(label="Admin Verification", id='admin-tab-content')
# # # #     ]),
# # # #     dbc.Popover(
# # # #         [
# # # #             dbc.PopoverHeader("Capital Pay Engine"),
# # # #             dbc.PopoverBody(
# # # #                 html.Div([
# # # #                     dbc.Button("Pay with Equity Bank", id="pay-equity-btn", color="primary", className="d-block mb-2"),
# # # #                     dbc.Button("Pay with NBC Bank", id="pay-nbc-btn", color="primary", className="d-block mb-2"),
# # # #                     dbc.Button("Pay with M-Pesa", id="pay-mpesa-btn", color="primary", className="d-block")
# # # #                 ])
# # # #             ),
# # # #         ],
# # # #         id="payment-method-popover",
# # # #         target="",
# # # #         trigger="manual",
# # # #     ),
# # # #     dbc.Popover(
# # # #         dbc.PopoverBody("Payment of 20,000 TZS successful!", className="text-success"),
# # # #         id="payment-success-popover",
# # # #         target="",
# # # #         trigger="manual",
# # # #     ),
# # # #     dcc.Interval(
# # # #         id='interval-popover',
# # # #         interval=5 * 1000,
# # # #         n_intervals=0,
# # # #         disabled=True,
# # # #     ),
# # # # ], fluid=True)
# # # #
# # # #
# # # # def save_uploaded_file(contents, filename, app_id, field_name):
# # # #     if not contents:
# # # #         return None
# # # #
# # # #     file_data = base64.b64decode(contents.split(',')[1])
# # # #     app_folder = os.path.join(DOCUMENTS_DIR, str(app_id))
# # # #     os.makedirs(app_folder, exist_ok=True)
# # # #     unique_filename = f"{field_name}_{filename}"
# # # #     file_path = os.path.join(app_folder, unique_filename)
# # # #
# # # #     with open(file_path, 'wb') as f:
# # # #         f.write(file_data)
# # # #
# # # #     return file_path
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('login-state', 'data'),
# # # #     Output('admin-login-alert', 'children'),
# # # #     Output('admin-login-alert', 'is_open'),
# # # #     Input('admin-login-button', 'n_clicks'),
# # # #     State('admin-username', 'value'),
# # # #     State('admin-password', 'value'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def check_login(n_clicks, username, password):
# # # #     if not n_clicks:
# # # #         raise PreventUpdate
# # # #
# # # #     if username == ADMIN_USER and hashlib.sha256(password.encode('utf-8')).hexdigest() == ADMIN_PASS_HASH:
# # # #         return {'is_authenticated': True}, "", False
# # # #     else:
# # # #         return {'is_authenticated': False}, "Invalid username or password.", True
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('admin-tab-content', 'children'),
# # # #     Input('login-state', 'data')
# # # # )
# # # # def render_admin_tab_content(data):
# # # #     if data['is_authenticated']:
# # # #         return [
# # # #             dbc.Card(dbc.CardBody([
# # # #                 html.H4("Verify Applications", className="card-title"),
# # # #                 dash_table.DataTable(
# # # #                     id='admin-table',
# # # #                     columns=[
# # # #                         {"name": "App ID", "id": "id"},
# # # #                         {"name": "TIN", "id": "tin_number"},
# # # #                         {"name": "Company Name", "id": "company_name"},
# # # #                         {"name": "Status", "id": "status"},
# # # #                     ],
# # # #                     style_cell={'textAlign': 'left'},
# # # #                     row_selectable='single',
# # # #                 ),
# # # #                 dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3"),
# # # #                 html.Hr(),
# # # #                 html.Div(id='admin-details-view')
# # # #             ]))
# # # #         ]
# # # #     else:
# # # #         return [
# # # #             dbc.Card(dbc.CardBody([
# # # #                 html.H4("Admin Login", className="card-title"),
# # # #                 dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
# # # #                 dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
# # # #                 dbc.Button("Login", id="admin-login-button", color="primary"),
# # # #                 dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
# # # #             ]))
# # # #         ]
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('output-passport-photo', 'children'),
# # # #     Output('output-id-payment', 'children'),
# # # #     Input('upload-passport-photo', 'filename'),
# # # #     Input('upload-id-payment', 'filename'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def update_id_upload_output(photo_name, payment_name):
# # # #     return (
# # # #         f'✓ {photo_name}' if photo_name else '',
# # # #         f'✓ {payment_name}' if payment_name else '',
# # # #     )
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('renew-output-cert-incorporation', 'children'),
# # # #     Output('renew-output-business-license', 'children'),
# # # #     Output('renew-output-brella-search', 'children'),
# # # #     Output('renew-output-directors-images', 'children'),
# # # #     Output('renew-output-tax-clearance', 'children'),
# # # #     Output('renew-output-taffa-cert', 'children'),
# # # #     Output('renew-output-memo-articles', 'children'),
# # # #     Output('renew-output-audited-accounts', 'children'),
# # # #     Input('renew-upload-cert-incorporation', 'filename'),
# # # #     Input('renew-upload-business-license', 'filename'),
# # # #     Input('renew-upload-brella-search', 'filename'),
# # # #     Input('renew-upload-directors-images', 'filename'),
# # # #     Input('renew-upload-tax-clearance', 'filename'),
# # # #     Input('renew-upload-taffa-cert', 'filename'),
# # # #     Input('renew-upload-memo-articles', 'filename'),
# # # #     Input('renew-upload-audited-accounts', 'filename'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def update_renewal_upload_output(cert_inc, biz_lic, brella, dir_img, tax_cert, taffa_cert, memo, audit):
# # # #     return (
# # # #         f'✓ {cert_inc}' if cert_inc else '',
# # # #         f'✓ {biz_lic}' if biz_lic else '',
# # # #         f'✓ {brella}' if brella else '',
# # # #         f'✓ {dir_img}' if dir_img else '',
# # # #         f'✓ {tax_cert}' if tax_cert else '',
# # # #         f'✓ {taffa_cert}' if taffa_cert else '',
# # # #         f'✓ {memo}' if memo else '',
# # # #         f'✓ {audit}' if audit else '',
# # # #     )
# # # #
# # # #
# # # # @app.callback(
# # # #     Output("payment-method-popover", "is_open"),
# # # #     Output("payment-method-popover", "target"),
# # # #     Input("pay-button", "n_clicks"),
# # # #     Input("renew-pay-button", "n_clicks"),
# # # #     prevent_initial_call=True
# # # # )
# # # # def toggle_payment_popover(n_clicks_pay, n_clicks_renew):
# # # #     if ctx.triggered_id == "pay-button":
# # # #         return True, "pay-button"
# # # #     elif ctx.triggered_id == "renew-pay-button":
# # # #         return True, "renew-pay-button"
# # # #     return False, ""
# # # #
# # # #
# # # # @app.callback(
# # # #     Output("payment-success-popover", "is_open"),
# # # #     Output("payment-success-popover", "target", allow_duplicate=True),
# # # #     Output("payment-method-popover", "is_open", allow_duplicate=True),
# # # #     Output("payment-store", "data"),
# # # #     Output("interval-popover", "disabled"),
# # # #     Input("pay-equity-btn", "n_clicks"),
# # # #     Input("pay-nbc-btn", "n_clicks"),
# # # #     Input("pay-mpesa-btn", "n_clicks"),
# # # #     State("payment-method-popover", "target"),
# # # #     prevent_initial_call=True
# # # # )
# # # # def handle_payment_confirmation(equity_clicks, nbc_clicks, mpesa_clicks, target_id):
# # # #     if not any([equity_clicks, nbc_clicks, mpesa_clicks]):
# # # #         raise PreventUpdate
# # # #
# # # #     time.sleep(1)
# # # #     trx_id = f"CP{random.randint(100000, 999999)}"
# # # #
# # # #     return True, target_id, False, {'status': 'Paid', 'trx_id': trx_id}, False
# # # #
# # # #
# # # # @app.callback(
# # # #     Output("payment-success-popover", "is_open", allow_duplicate=True),
# # # #     Output("interval-popover", "disabled", allow_duplicate=True),
# # # #     Input("interval-popover", "n_intervals"),
# # # #     State("payment-success-popover", "is_open"),
# # # #     prevent_initial_call=True
# # # # )
# # # # def hide_payment_popover(n, is_open):
# # # #     if is_open:
# # # #         return False, True
# # # #     raise PreventUpdate
# # # #
# # # #
# # # # @app.callback(
# # # #     Output("payment-confirmation", "value"),
# # # #     Output("pay-button", "disabled"),
# # # #     Input("payment-store", "data"),
# # # #     prevent_initial_call=True
# # # # )
# # # # def update_payment_status(data):
# # # #     if data and data.get("status") == "Paid":
# # # #         return "Paid", True
# # # #     return "Unpaid", False
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('submission-output', 'children'),
# # # #     Input('submit-button', 'n_clicks'),
# # # #     [State('tin-number', 'value'), State('company-name', 'value'), State('contact-person', 'value'),
# # # #      State('email', 'value'), State('phone', 'value'), State('physical-address', 'value'),
# # # #      State('postal-address', 'value'), State('website', 'value'), State('taffa-membership-no', 'value'),
# # # #      State('director-1', 'value'), State('director-2', 'value'), State('director-3', 'value'),
# # # #      State('cert-incorporation-no', 'value'), State('business-license-no', 'value'),
# # # #      State('membership-type', 'value'), State('agree-terms', 'value'),
# # # #      State('tax-compliance', 'value'), State('taffa-status', 'value'), State('policy-compliance', 'value'),
# # # #      State('payment-confirmation', 'value')],
# # # #     prevent_initial_call=True
# # # # )
# # # # def submit_membership_application(n_clicks, tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no,
# # # #                                   director_1, director_2, director_3, cert_inc_no, biz_lic_no, mem_type, agreed,
# # # #                                   tax, taffa, policy, payment):
# # # #     required_fields = [tin, company, contact, email, phone, phys_addr, post_addr, director_1, cert_inc_no, biz_lic_no,
# # # #                        mem_type, agreed]
# # # #     if not all(required_fields):
# # # #         return dbc.Alert("Please fill all fields marked with * and upload the required documents.", color="danger")
# # # #     if not agreed:
# # # #         return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning")
# # # #
# # # #     try:
# # # #         conn = sqlite3.connect(DB_PATH)
# # # #         c = conn.cursor()
# # # #         c.execute("""INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
# # # #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
# # # #                   (tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no, director_1, director_2,
# # # #                    director_3, cert_inc_no, biz_lic_no, mem_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
# # # #         agent_id = c.lastrowid
# # # #
# # # #         c.execute("""INSERT INTO applications (agent_id, agreed_to_terms, tax_compliance, taffa_status, policy_compliance, payment_confirmation)
# # # #                      VALUES (?, ?, ?, ?, ?, ?)""",
# # # #                   (agent_id, 1, tax, taffa, policy, payment))
# # # #         conn.commit()
# # # #         return dbc.Alert("Membership application submitted successfully!", color="success")
# # # #     except sqlite3.IntegrityError:
# # # #         return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger")
# # # #     except Exception as e:
# # # #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# # # #     finally:
# # # #         if conn: conn.close()
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('id-submission-output', 'children'),
# # # #     Input('submit-id-button', 'n_clicks'),
# # # #     [State('id-full-name', 'value'), State('id-nida-number', 'value'), State('id-position', 'value'),
# # # #      State('id-application-tin', 'value'),
# # # #      State('upload-passport-photo', 'contents'), State('upload-id-payment', 'contents'),
# # # #      State('upload-passport-photo', 'filename'), State('upload-id-payment', 'filename')],
# # # #     prevent_initial_call=True
# # # # )
# # # # def submit_id_application(n_clicks, full_name, nida_number, position, tin, photo_cont, payment_cont, photo_name,
# # # #                           payment_name):
# # # #     required_fields = [full_name, nida_number, position, tin, photo_cont, payment_cont]
# # # #     if not all(required_fields):
# # # #         return dbc.Alert("Please fill all fields and upload required documents.", color="danger")
# # # #
# # # #     try:
# # # #         conn = sqlite3.connect(DB_PATH)
# # # #         conn.row_factory = sqlite3.Row
# # # #         c = conn.cursor()
# # # #
# # # #         c.execute("SELECT id FROM agents WHERE tin_number = ?", (tin,))
# # # #         agent_id_result = c.fetchone()
# # # #
# # # #         if not agent_id_result:
# # # #             return dbc.Alert(f"No existing TAFFA member found with TIN {tin}.", color="danger")
# # # #         agent_id = agent_id_result['id']
# # # #
# # # #         c.execute("SELECT id FROM applications WHERE agent_id = ? ORDER BY id DESC LIMIT 1", (agent_id,))
# # # #         application_id_result = c.fetchone()
# # # #
# # # #         if not application_id_result:
# # # #             return dbc.Alert(f"No completed membership application found for TIN {tin}.", color="danger")
# # # #         application_id = application_id_result['id']
# # # #
# # # #         photo_path = save_uploaded_file(photo_cont, photo_name, application_id, 'passport_photo')
# # # #         payment_path = save_uploaded_file(payment_cont, payment_name, application_id, 'id_payment_proof')
# # # #
# # # #         c.execute("""INSERT INTO id_applications (application_id, full_name, nida_number, position, passport_photo, id_payment_proof)
# # # #                      VALUES (?, ?, ?, ?, ?, ?)""",
# # # #                   (application_id, full_name, nida_number, position, photo_path, payment_path))
# # # #         id_app_id = c.lastrowid
# # # #         conn.commit()
# # # #
# # # #         id_app_data = c.execute("SELECT * FROM id_applications WHERE id = ?", (id_app_id,)).fetchone()
# # # #         agent_data = c.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
# # # #
# # # #         filename = generate_id_card(id_app_data, agent_data)
# # # #         download_link = dcc.Link("Download ID Card", href=f"/download-id/{os.path.basename(filename)}",
# # # #                                  className="btn btn-primary mt-2")
# # # #
# # # #         return [
# # # #             dbc.Alert("ID card application submitted successfully!", color="success"),
# # # #             html.Div(download_link, className="mt-2")
# # # #         ]
# # # #
# # # #     except Exception as e:
# # # #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# # # #     finally:
# # # #         if conn: conn.close()
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('renewal-submission-output', 'children'),
# # # #     Input('submit-renewal-button', 'n_clicks'),
# # # #     [State('renew-tin-number', 'value'), State('renew-taffa-no', 'value'),
# # # #      State('renew-tax-compliance', 'value'), State('renew-taffa-status', 'value'),
# # # #      State('renew-policy-compliance', 'value'), State('renew-payment-confirmation', 'value'),
# # # #      State('renew-upload-cert-incorporation', 'contents'), State('renew-upload-business-license', 'contents'),
# # # #      State('renew-upload-brella-search', 'contents'), State('renew-upload-directors-images', 'contents'),
# # # #      State('renew-upload-tax-clearance', 'contents'), State('renew-upload-taffa-cert', 'contents'),
# # # #      State('renew-upload-memo-articles', 'contents'), State('renew-upload-audited-accounts', 'contents'),
# # # #      State('renew-upload-cert-incorporation', 'filename'), State('renew-upload-business-license', 'filename'),
# # # #      State('renew-upload-brella-search', 'filename'), State('renew-upload-directors-images', 'filename'),
# # # #      State('renew-upload-tax-clearance', 'filename'), State('renew-upload-taffa-cert', 'filename'),
# # # #      State('renew-upload-memo-articles', 'filename'), State('renew-upload-audited-accounts', 'filename')],
# # # #     prevent_initial_call=True
# # # # )
# # # # def submit_renewal(n_clicks, tin, taffa_no, tax, taffa, policy, payment,
# # # #                    cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
# # # #                    memo_cont, audit_cont, cert_inc_name, biz_lic_name, brella_name, dir_img_name, tax_cert_name,
# # # #                    taffa_cert_name, memo_name, audit_name):
# # # #     required_uploads = [cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
# # # #                         memo_cont, audit_cont]
# # # #     if not all(required_uploads):
# # # #         return dbc.Alert("Please upload all required documents for renewal.", color="danger")
# # # #
# # # #     return [
# # # #         dbc.Toast(
# # # #             "Member license renewed!",
# # # #             header="Renewal Status",
# # # #             icon="success",
# # # #             dismissable=True,
# # # #             is_open=True,
# # # #             style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# # # #         )
# # # #     ]
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('applications-table', 'data'),
# # # #     [Input('refresh-button', 'n_clicks'), Input('submission-output', 'children')]
# # # # )
# # # # def update_table(n_clicks, submission_output):
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
# # # #     df = pd.read_sql_query(query, conn)
# # # #     conn.close()
# # # #     return df.to_dict('records')
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('admin-table', 'data'),
# # # #     Input('admin-refresh-button', 'n_clicks'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def update_admin_table(n_clicks):
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     query = "SELECT p.id, a.tin_number, a.company_name, p.status FROM agents a JOIN applications p ON a.id = p.agent_id"
# # # #     df = pd.read_sql_query(query, conn)
# # # #     conn.close()
# # # #     return df.to_dict('records')
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('admin-details-view', 'children'),
# # # #     Input('admin-table', 'selected_rows'),
# # # #     State('admin-table', 'data'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def display_admin_details(selected_rows, table_data):
# # # #     if not selected_rows:
# # # #         return []
# # # #
# # # #     app_id = table_data[selected_rows[0]]['id']
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     conn.row_factory = sqlite3.Row
# # # #     c = conn.cursor()
# # # #     c.execute("""
# # # #         SELECT * FROM agents a
# # # #         JOIN applications p ON a.id = p.agent_id
# # # #         WHERE p.id = ?
# # # #     """, (app_id,))
# # # #     data = c.fetchone()
# # # #
# # # #     id_applications_query = """
# # # #         SELECT id, full_name, passport_photo, id_payment_proof, id_status FROM id_applications
# # # #         WHERE application_id = ?
# # # #     """
# # # #     id_applications = pd.read_sql_query(id_applications_query, conn, params=(app_id,))
# # # #     conn.close()
# # # #
# # # #     if not data:
# # # #         return dbc.Alert("Could not retrieve application details.", color="danger")
# # # #
# # # #     status_color = {
# # # #         "Verified": "success",
# # # #         "Cancelled": "danger",
# # # #         "Pending": "warning"
# # # #     }.get(data['status'], "secondary")
# # # #
# # # #     document_links = []
# # # #     document_fields = {
# # # #         "Certificate of Incorporation": "cert_incorporation",
# # # #         "Business License": "business_license",
# # # #         "Brella Search": "brella_search",
# # # #         "Directors Images": "director_images",
# # # #         "Tax Clearance Cert": "tax_clearance_cert",
# # # #         "TAFFA Certificate": "taffa_cert",
# # # #         "Memo & Articles": "memo_articles",
# # # #         "Audited Accounts": "audited_accounts",
# # # #     }
# # # #
# # # #     for doc_name, field in document_fields.items():
# # # #         if data[field]:
# # # #             filename = os.path.basename(data[field])
# # # #             download_link = dcc.Link(
# # # #                 f"Download {doc_name}",
# # # #                 href=f"/download-file/{data['agent_id']}/{filename}",
# # # #                 className="d-block"
# # # #             )
# # # #             document_links.append(download_link)
# # # #
# # # #     details_layout = [
# # # #         dbc.Row([
# # # #             dbc.Col([
# # # #                 dbc.Card([
# # # #                     dbc.CardHeader("Company & Contact Information"),
# # # #                     dbc.CardBody([
# # # #                         html.P([html.Strong("Company Name: "), data['company_name']]),
# # # #                         html.P([html.Strong("TIN Number: "), data['tin_number']]),
# # # #                         html.P([html.Strong("Physical Address: "), data['physical_address']]),
# # # #                         html.P([html.Strong("Contact Person: "), data['contact_person']]),
# # # #                         html.P([html.Strong("Email: "), data['email']]),
# # # #                         html.P([html.Strong("Phone: "), data['phone']]),
# # # #                     ])
# # # #                 ]),
# # # #                 dbc.Card([
# # # #                     dbc.CardHeader("Director Information"),
# # # #                     dbc.CardBody([
# # # #                         html.P([html.Strong("Director 1: "), data['director_1']]),
# # # #                         html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"]),
# # # #                         html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"]),
# # # #                     ])
# # # #                 ], className="mt-3"),
# # # #             ], width=6),
# # # #             dbc.Col([
# # # #                 dbc.Card([
# # # #                     dbc.CardHeader("Compliance & Verification"),
# # # #                     dbc.CardBody([
# # # #                         html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"]),
# # # #                         html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"]),
# # # #                         html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"]),
# # # #                         html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']]),
# # # #                         html.P([html.Strong("Current Status: "),
# # # #                                 html.Strong(data['status'], className=f"text-{status_color}")])
# # # #                     ])
# # # #                 ]),
# # # #                 dbc.Card([
# # # #                     dbc.CardHeader("Uploaded Documents (Membership)"),
# # # #                     dbc.CardBody(document_links)
# # # #                 ], className="mt-3"),
# # # #                 dbc.Card([
# # # #                     dbc.CardHeader("Actions (Membership)"),
# # # #                     dbc.CardBody([
# # # #                         html.H5("Update Status for Selected Application"),
# # # #                         dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
# # # #                                                                           {'label': 'Cancelled', 'value': 'Cancelled'}],
# # # #                                      placeholder="Select new status"),
# # # #                         dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2"),
# # # #                         dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
# # # #                                    className="mt-2 ms-2", disabled=data['status'] != 'Verified'),
# # # #                         html.Div(id="download-cert-link-div", className="mt-2"),
# # # #                         html.Div(id='admin-update-output', className="mt-3")
# # # #                     ])
# # # #                 ], className="mt-3"),
# # # #             ], width=6),
# # # #         ], className="mt-4")
# # # #     ]
# # # #
# # # #     id_card_links = []
# # # #     if not id_applications.empty:
# # # #         id_card_details = [html.Hr(), html.H5("ID Card Applications", className="card-title")]
# # # #         for index, row in id_applications.iterrows():
# # # #             id_app_id = row['id']
# # # #             id_card_details.append(html.P(html.Strong(f"ID for: {row['full_name']}")))
# # # #             id_card_details.append(dcc.Link("Download Passport Photo",
# # # #                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['passport_photo'])}",
# # # #                                             className="d-block"))
# # # #             id_card_details.append(dcc.Link("Download ID Payment Proof",
# # # #                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['id_payment_proof'])}",
# # # #                                             className="d-block"))
# # # #             id_card_details.append(html.P([html.Strong("ID Status: "), row['id_status']]))
# # # #
# # # #             if row['id_status'] == 'Verified':
# # # #                 id_card_details.append(
# # # #                     dcc.Link("Download ID Card", href=f"/download-id/{id_app_id}", className="btn btn-primary mt-2",
# # # #                              id={"type": "download-id-link", "index": str(id_app_id)}))
# # # #             else:
# # # #                 id_card_details.append(
# # # #                     dbc.Button("Verify ID Application", id={"type": "verify-id-button", "index": str(id_app_id)},
# # # #                                color="success", className="mt-2"))
# # # #             id_card_details.append(html.Hr())
# # # #         id_card_links = id_card_details
# # # #     else:
# # # #         id_card_links = html.Div([html.P("No ID Application submitted for this company.")])
# # # #
# # # #     details_layout.append(
# # # #         dbc.Row([
# # # #             dbc.Col(
# # # #                 dbc.Card([
# # # #                     dbc.CardHeader("ID Application Documents"),
# # # #                     dbc.CardBody(id_card_links)
# # # #                 ], className="mt-3"),
# # # #                 width=12
# # # #             )
# # # #         ])
# # # #     )
# # # #     return details_layout
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('admin-update-output', 'children'),
# # # #     Input('admin-update-button', 'n_clicks'),
# # # #     [State('admin-table', 'selected_rows'), State('admin-table', 'data'), State('admin-status-dropdown', 'value')],
# # # #     prevent_initial_call=True
# # # # )
# # # # def update_status(n_clicks, selected_rows, table_data, new_status):
# # # #     if not selected_rows or not new_status:
# # # #         raise PreventUpdate
# # # #
# # # #     app_id = table_data[selected_rows[0]]['id']
# # # #     ref_number = f"TAFFA-TRA-{random.randint(10000, 99999)}{'PASS' if new_status == 'Verified' else 'FAIL'}"
# # # #
# # # #     try:
# # # #         conn = sqlite3.connect(DB_PATH)
# # # #         c = conn.cursor()
# # # #         c.execute("UPDATE applications SET status = ?, reference_number = ? WHERE id = ?",
# # # #                   (new_status, ref_number, app_id))
# # # #         conn.commit()
# # # #
# # # #         c.execute("SELECT a.email FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?", (app_id,))
# # # #         agent_email = c.fetchone()[0]
# # # #
# # # #         email_body = (
# # # #             f"Dear Applicant,\n\n"
# # # #             f"The status of your TAFFA membership application has been updated to: {new_status}.\n\n"
# # # #             f"Reference Number: {ref_number}\n\n"
# # # #             f"Thank you,\nTAFFA Administration"
# # # #         )
# # # #
# # # #         email_sent = send_email(agent_email, f"TAFFA Application Update: {new_status}", email_body)
# # # #
# # # #         if email_sent:
# # # #             return [
# # # #                 dbc.Alert(f"Application {app_id} updated to '{new_status}'. A notification has been sent.",
# # # #                           color="success"),
# # # #                 dbc.Toast(
# # # #                     "Email notification sent successfully!",
# # # #                     header="Email Status",
# # # #                     icon="success",
# # # #                     dismissable=True,
# # # #                     is_open=True,
# # # #                     style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# # # #                 )
# # # #             ]
# # # #         else:
# # # #             return dbc.Alert(f"Application {app_id} updated to '{new_status}'. Failed to send email notification.",
# # # #                              color="warning")
# # # #
# # # #     except Exception as e:
# # # #         return dbc.Alert(f"Error updating status: {e}", color="danger")
# # # #     finally:
# # # #         if conn: conn.close()
# # # #
# # # #
# # # # @app.callback(
# # # #     Output({"type": "verify-id-button", "index": MATCH}, "children"),
# # # #     Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
# # # #     State({"type": "verify-id-button", "index": ALL}, "id"),
# # # #     prevent_initial_call=True
# # # # )
# # # # def verify_id_application(n_clicks, button_ids):
# # # #     if not n_clicks or not any(n_clicks):
# # # #         raise PreventUpdate
# # # #
# # # #     triggered_id_json = ctx.triggered[0]['prop_id']
# # # #     triggered_id_dict = json.loads(triggered_id_json)
# # # #     clicked_id = triggered_id_dict['index']
# # # #
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     conn.row_factory = sqlite3.Row
# # # #     c = conn.cursor()
# # # #     id_number = f"TAFFA-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
# # # #     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
# # # #
# # # #     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
# # # #               ('Verified', id_number, expiry_date, clicked_id))
# # # #     conn.commit()
# # # #     conn.close()
# # # #
# # # #     return "Verified!"
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('generate-cert-button', 'disabled'),
# # # #     Input('admin-table', 'selected_rows'),
# # # #     Input('admin-update-output', 'children'),
# # # #     State('admin-table', 'data'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def toggle_generate_button(selected_rows, update_output, table_data):
# # # #     if not selected_rows:
# # # #         return True
# # # #
# # # #     app_id = table_data[selected_rows[0]]['id']
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     c = conn.cursor()
# # # #     c.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
# # # #     status = c.fetchone()[0]
# # # #     conn.close()
# # # #
# # # #     return status != 'Verified'
# # # #
# # # #
# # # # def generate_membership_certificate(app_data):
# # # #     filename = f"Certificate-{app_data['tin_number']}.pdf"
# # # #     filepath = os.path.join(CERTIFICATES_DIR, filename)
# # # #     c = canvas.Canvas(filepath, pagesize=letter)
# # # #     width, height = letter
# # # #
# # # #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # # #
# # # #     if os.path.exists(taffa_logo_path):
# # # #         c.drawImage(taffa_logo_path, 30, height - 150, width=150, height=150, preserveAspectRatio=True, mask='auto')
# # # #
# # # #     c.setFont("Helvetica-Bold", 16)
# # # #     c.setFillColor(colors.black)
# # # #     c.drawRightString(width - 50, height - 110, f"No. {random.randint(1000, 9999)}")
# # # #
# # # #     c.setFont("Helvetica-Bold", 24)
# # # #     c.setFillColor(colors.HexColor('#003366'))
# # # #     c.drawCentredString(width / 2.0, height - 200, "CERTIFICATE OF MEMBERSHIP")
# # # #
# # # #     c.setFont("Helvetica", 14)
# # # #     c.setFillColor(colors.black)
# # # #     c.drawCentredString(width / 2.0, height - 250, "CERTIFICATE IS AWARDED TO")
# # # #
# # # #     c.setFont("Helvetica-Bold", 20)
# # # #     c.drawCentredString(width / 2.0, height - 280, app_data['company_name'].upper())
# # # #
# # # #     c.setFont("Helvetica", 12)
# # # #     c.drawCentredString(width / 2.0, height - 320,
# # # #                         f"as a Tanzania Freight Forwarder Association Member for {date.today().year}")
# # # #
# # # #     c.save()
# # # #     return filename
# # # #
# # # #
# # # # def generate_id_card(id_app_data, agent_data):
# # # #     filename = f"ID-{id_app_data['id_number']}.pdf"
# # # #     filepath = os.path.join(IDS_DIR, filename)
# # # #     c = canvas.Canvas(filepath, pagesize=A4)
# # # #     width, height = A4
# # # #
# # # #     # ID card dimensions
# # # #     card_width = width * 0.75
# # # #     card_height = height * 0.75
# # # #
# # # #     # Calculate margins to center the card on the page
# # # #     x_offset = (width - card_width) / 2
# # # #     y_offset = (height - card_height) / 2
# # # #     content_center_x = x_offset + card_width / 2
# # # #
# # # #     # Draw the border
# # # #     c.setStrokeColor(colors.HexColor('#003366'))
# # # #     c.setFillColor(colors.white)
# # # #     c.setLineWidth(5)
# # # #     c.roundRect(x_offset, y_offset, card_width, card_height, 10, stroke=1, fill=1)
# # # #
# # # #     # Header with TAFFA logo and text
# # # #     header_height = card_height * 0.2
# # # #     c.setFillColor(colors.HexColor('#F0F8FF'))
# # # #     c.rect(x_offset, y_offset + card_height - header_height, card_width, header_height, fill=1, stroke=0)
# # # #
# # # #     # TAFFA Logo
# # # #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # # #     if os.path.exists(taffa_logo_path):
# # # #         logo_size = header_height * 0.8
# # # #         logo_x = x_offset + card_width * 0.05
# # # #         logo_y = y_offset + card_height - header_height + (header_height - logo_size) / 2
# # # #         c.drawImage(taffa_logo_path, logo_x, logo_y, width=logo_size, height=logo_size, preserveAspectRatio=True)
# # # #
# # # #     # Title text
# # # #     c.setFont("Helvetica-Bold", 14)
# # # #     c.setFillColor(colors.HexColor('#003366'))
# # # #     title_y = y_offset + card_height - header_height / 2 + 10
# # # #     c.drawCentredString(x_offset + card_width * 0.5, title_y, "TANZANIA FREIGHT")
# # # #     c.drawCentredString(x_offset + card_width * 0.5, title_y - 20, "FORWARDERS ASSOCIATION")
# # # #
# # # #     # Photo - Centered
# # # #     photo_path = id_app_data['passport_photo']
# # # #     photo_size = card_width * 0.3
# # # #     photo_x = x_offset + (card_width - photo_size) / 2
# # # #     photo_y = y_offset + card_height - header_height - 10 - photo_size
# # # #     if os.path.exists(photo_path):
# # # #         c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True)
# # # #
# # # #     # Personal Details - Centered underneath the photo
# # # #     c.setFont("Helvetica-Bold", 12)
# # # #     c.setFillColor(colors.black)
# # # #     details_y = photo_y - 30
# # # #
# # # #     c.drawCentredString(content_center_x, details_y, f"Name: {id_app_data['full_name']}")
# # # #     c.drawCentredString(content_center_x, details_y - 20, f"Position: {id_app_data['position']}")
# # # #     c.drawCentredString(content_center_x, details_y - 40, f"Company: {agent_data['company_name']}")
# # # #
# # # #     # ID details
# # # #     c.setFont("Helvetica-Bold", 12)
# # # #     c.setFillColor(colors.HexColor('#003366'))
# # # #     id_y_start = details_y - 80
# # # #     c.drawCentredString(content_center_x, id_y_start, f"ID NO: {id_app_data['id_number']}")
# # # #     c.drawCentredString(content_center_x, id_y_start - 20, f"Expiry Date: {id_app_data['expiry_date']}")
# # # #
# # # #     # QR code - Centered at the bottom
# # # #     qr_data = f"ID: {id_app_data['id_number']} | Expiry: {id_app_data['expiry_date']}"
# # # #     qr_img = qrcode.make(qr_data)
# # # #     qr_buffer = io.BytesIO()
# # # #     qr_img.save(qr_buffer, format='PNG')
# # # #     qr_buffer.seek(0)
# # # #
# # # #     qr_size = card_width * 0.25
# # # #     qr_x = content_center_x - qr_size / 2
# # # #     qr_y = y_offset + 20
# # # #     c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)
# # # #
# # # #     c.save()
# # # #     return filename
# # # #
# # # #
# # # # @app.callback(
# # # #     Output('download-cert-link-div', 'children'),
# # # #     Input('generate-cert-button', 'n_clicks'),
# # # #     State('admin-table', 'selected_rows'),
# # # #     State('admin-table', 'data'),
# # # #     prevent_initial_call=True
# # # # )
# # # # def handle_certificate_generation(n_clicks, selected_rows, table_data):
# # # #     if not selected_rows:
# # # #         raise PreventUpdate
# # # #
# # # #     app_id = table_data[selected_rows[0]]['id']
# # # #
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     query = """
# # # #         SELECT a.tin_number, a.company_name, p.reference_number, p.status
# # # #         FROM agents a JOIN applications p ON a.id = p.agent_id
# # # #         WHERE p.id = ?
# # # #     """
# # # #     df = pd.read_sql_query(query, conn, params=(app_id,))
# # # #     conn.close()
# # # #
# # # #     if df.empty:
# # # #         return dbc.Alert("Could not find application data.", color="danger")
# # # #
# # # #     app_data = df.to_dict('records')[0]
# # # #     filename = generate_membership_certificate(app_data)
# # # #
# # # #     return dcc.Link(f"Download Certificate for {app_data['company_name']}",
# # # #                     href=f"/download-cert/{os.path.basename(filename)}")
# # # #
# # # #
# # # # @app.callback(
# # # #     Output({"type": "download-id-link", "index": MATCH}, "children"),
# # # #     Input({"type": "verify-id-button", "index": MATCH}, "n_clicks"),
# # # #     State({"type": "verify-id-button", "index": ALL}, "id"),
# # # #     prevent_initial_call=True
# # # # )
# # # # def handle_id_generation(n_clicks, button_ids):
# # # #     if not n_clicks or not any(n_clicks):
# # # #         raise PreventUpdate
# # # #
# # # #     triggered_id_json = ctx.triggered[0]['prop_id']
# # # #     triggered_id_dict = json.loads(triggered_id_json)
# # # #     clicked_id = triggered_id_dict['index']
# # # #
# # # #     conn = sqlite3.connect(DB_PATH)
# # # #     conn.row_factory = sqlite3.Row
# # # #     c = conn.cursor()
# # # #
# # # #     c.execute("SELECT * FROM id_applications WHERE id = ?", (clicked_id,))
# # # #     id_app_data = c.fetchone()
# # # #
# # # #     if not id_app_data:
# # # #         return dbc.Alert("ID application data not found.", color="danger")
# # # #
# # # #     c.execute("SELECT * FROM applications WHERE id = ?", (id_app_data['application_id'],))
# # # #     main_app_data = c.fetchone()
# # # #
# # # #     c.execute("SELECT * FROM agents WHERE id = ?", (main_app_data['agent_id'],))
# # # #     agent_data = c.fetchone()
# # # #
# # # #     filename = generate_id_card(id_app_data, agent_data)
# # # #
# # # #     return dcc.Link("Download ID Card", href=f"/download-id/{os.path.basename(filename)}")
# # # #
# # # #
# # # # @server.route('/download-cert/<filename>')
# # # # def serve_pdf(filename):
# # # #     return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)
# # # #
# # # #
# # # # @server.route('/download-id/<filename>')
# # # # def serve_id(filename):
# # # #     return send_from_directory(IDS_DIR, filename, as_attachment=True)
# # # #
# # # #
# # # # @server.route('/download-file/<app_id>/<filename>')
# # # # def download_uploaded_file(app_id, filename):
# # # #     app_folder = os.path.join(DOCUMENTS_DIR, app_id)
# # # #     return send_from_directory(app_folder, filename, as_attachment=True)
# # # #
# # # #
# # # # if __name__ == '__main__':
# # # #     if not os.path.exists(DOCUMENTS_DIR):
# # # #         os.makedirs(DOCUMENTS_DIR)
# # # #     if not os.path.exists(CERTIFICATES_DIR):
# # # #         os.makedirs(CERTIFICATES_DIR)
# # # #     if not os.path.exists(IDS_DIR):
# # # #         os.makedirs(IDS_DIR)
# # # #
# # # #     assets_dir = os.path.join(BASE_DIR, 'assets')
# # # #     if not os.path.exists(assets_dir):
# # # #         os.makedirs(assets_dir)
# # # #
# # # #     app.run(debug=True, port=5878)
# # #
# # #
# # # import dash
# # # from dash import dcc, html, Input, Output, State, ctx, dash_table
# # # import dash_bootstrap_components as dbc
# # # from dash.exceptions import PreventUpdate
# # # import sqlite3
# # # import pandas as pd
# # # from datetime import datetime, date, timedelta
# # # import base64
# # # import io
# # # from reportlab.lib.pagesizes import letter, A4
# # # from reportlab.pdfgen import canvas
# # # from reportlab.lib.utils import ImageReader
# # # from reportlab.lib import colors
# # # from reportlab.lib.units import inch
# # # from PIL import Image
# # # import os
# # # import random
# # # import time
# # # import smtplib
# # # from email.message import EmailMessage
# # # import socket
# # # from flask import send_from_directory
# # # import qrcode
# # # import hashlib
# # # from dash.dependencies import MATCH, ALL
# # # import json
# # #
# # # # Initialize the Dash app with Flask server and suppress callback exceptions
# # # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True,
# # #                 title="TAFFA Portal")
# # # server = app.server
# # #
# # # # --- Admin Credentials ---
# # # ADMIN_USER = "admin"
# # # ADMIN_PASS_HASH = hashlib.sha256("password".encode('utf-8')).hexdigest()
# # #
# # # # --- Database Setup with Absolute Path ---
# # # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # # DB_PATH = os.path.join(BASE_DIR, "tra_cfa_data.db")
# # # DOCUMENTS_DIR = os.path.join(BASE_DIR, "uploaded_documents")
# # # CERTIFICATES_DIR = os.path.join(BASE_DIR, "certificates")
# # # IDS_DIR = os.path.join(BASE_DIR, "id_cards")
# # #
# # #
# # # def init_db():
# # #     conn = sqlite3.connect(DB_PATH)
# # #     c = conn.cursor()
# # #
# # #     # Drop tables to ensure a clean slate and prevent schema errors on re-runs
# # #     c.execute('DROP TABLE IF EXISTS id_applications')
# # #     c.execute('DROP TABLE IF EXISTS applications')
# # #     c.execute('DROP TABLE IF EXISTS agents')
# # #     c.execute('DROP TABLE IF EXISTS taffa_id_applications')
# # #
# # #     # agents table updated to match the latest fields
# # #     c.execute('''
# # #         CREATE TABLE IF NOT EXISTS agents (
# # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #             tin_number TEXT NOT NULL UNIQUE,
# # #             company_name TEXT NOT NULL,
# # #             contact_person TEXT NOT NULL,
# # #             email TEXT NOT NULL,
# # #             phone TEXT NOT NULL,
# # #             physical_address TEXT,
# # #             postal_address TEXT,
# # #             website TEXT,
# # #             taffa_membership_no TEXT,
# # #             director_1 TEXT,
# # #             director_2 TEXT,
# # #             director_3 TEXT,
# # #             cert_incorporation_no TEXT,
# # #             business_license_no TEXT,
# # #             membership_type TEXT,
# # #             submission_date TEXT NOT NULL
# # #         )
# # #     ''')
# # #     # applications table updated to store file paths as TEXT
# # #     c.execute('''
# # #         CREATE TABLE IF NOT EXISTS applications (
# # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #             agent_id INTEGER,
# # #             tax_compliance TEXT,
# # #             taffa_status TEXT,
# # #             policy_compliance TEXT,
# # #             payment_confirmation TEXT,
# # #             business_license TEXT,
# # #             tax_clearance_cert TEXT,
# # #             taffa_cert TEXT,
# # #             cert_incorporation TEXT,
# # #             memo_articles TEXT,
# # #             audited_accounts TEXT,
# # #             director_images TEXT,
# # #             brella_search TEXT,
# # #             agreed_to_terms INTEGER,
# # #             status TEXT DEFAULT 'Pending',
# # #             reference_number TEXT,
# # #             FOREIGN KEY (agent_id) REFERENCES agents (id)
# # #         )
# # #     ''')
# # #     # New table for ID applications
# # #     c.execute('''
# # #         CREATE TABLE IF NOT EXISTS id_applications (
# # #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #             application_id INTEGER,
# # #             full_name TEXT,
# # #             nida_number TEXT,
# # #             position TEXT,
# # #             passport_photo TEXT,
# # #             id_payment_proof TEXT,
# # #             id_status TEXT DEFAULT 'Pending',
# # #             id_number TEXT,
# # #             expiry_date TEXT,
# # #             FOREIGN KEY (application_id) REFERENCES applications (id)
# # #         )
# # #     ''')
# # #
# # #     conn.commit()
# # #     conn.close()
# # #
# # #
# # # init_db()
# # #
# # # # --- Logo Paths ---
# # # taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # # taffa_logo_src = "/assets/LOGO.png"
# # #
# # #
# # # # --- Reusable Components ---
# # # def logo_header(logo_src, text):
# # #     return dbc.Row([
# # #         dbc.Col(html.Img(src=logo_src, height="80px"), width="auto"),
# # #         dbc.Col(html.H5(text, className="align-self-center"))
# # #     ], className="mb-4 align-items-center justify-content-center")
# # #
# # #
# # # def send_email(recipient_email: str, subject: str, body: str):
# # #     """Sends an email notification."""
# # #     sender_email = "administrator@capitalpayinternational.com"
# # #     sender_password = "ahxr wusz rqvp jpsx"
# # #     smtp_server = "smtp.gmail.com"
# # #     smtp_port = 587
# # #
# # #     if not sender_password:
# # #         print("Error: Email password is not set.")
# # #         return False
# # #
# # #     msg = EmailMessage()
# # #     msg['Subject'] = f"Update: Milestone Reached - {subject}"
# # #     msg['From'] = sender_email
# # #     msg['To'] = recipient_email
# # #     msg.set_content(body)
# # #
# # #     try:
# # #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# # #             server.starttls()
# # #             server.login(sender_email, sender_password)
# # #             server.send_message(msg)
# # #             print(f"Email notification sent successfully to {recipient_email}!")
# # #             return True
# # #     except socket.gaierror as e:
# # #         print(f"Network error: {e}. Could not find host: '{smtp_server}'.")
# # #         return False
# # #     except Exception as e:
# # #         print(f"An unexpected error occurred: {e}")
# # #         return False
# # #
# # #
# # # # --- App Layout ---
# # # app.layout = dbc.Container([
# # #     dcc.Store(id='payment-store'),
# # #     dcc.Store(id='login-state', data={'is_authenticated': False}),
# # #     dbc.Row([
# # #         dbc.Col(html.Img(src="/assets/LOGO.png", height="100px"), width="auto"),
# # #         dbc.Col(html.H1("Customs Agent Accreditation Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
# # #                 width="auto")
# # #     ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),
# # #
# # #     dbc.Tabs(id='tabs', children=[
# # #         dbc.Tab(label="New Application", children=[
# # #             dbc.Card(dbc.CardBody([
# # #                 html.H4("Membership Application Form", className="card-title text-primary"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text'), width=6),
# # #                     dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text'), width=6),
# # #                 ], className="mb-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text'),
# # #                             width=6),
# # #                     dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text'), width=6),
# # #                 ], className="mb-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='website', placeholder='Website', type='text'), width=6),
# # #                     dbc.Col(dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
# # #                                       type='text'), width=6),
# # #                 ], className="mb-3"),
# # #                 html.Hr(),
# # #                 html.H4("Contact Person", className="card-title text-primary mt-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='contact-person', placeholder='Contact Person Name *', type='text'), width=4),
# # #                     dbc.Col(dbc.Input(id='email', placeholder='Email Address *', type='email'), width=4),
# # #                     dbc.Col(dbc.Input(id='phone', placeholder='Mobile Number *', type='text'), width=4),
# # #                 ], className="mb-3"),
# # #                 html.Hr(),
# # #                 html.H4("Directors", className="card-title text-primary mt-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text'), width=4),
# # #                     dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text'), width=4),
# # #                     dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text'), width=4),
# # #                 ], className="mb-3"),
# # #                 html.Hr(),
# # #                 html.H4("Company Details", className="card-title text-primary mt-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
# # #                                       type='text'), width=6),
# # #                     dbc.Col(dbc.Input(id='business-license-no', placeholder='Business License No. *', type='text'),
# # #                             width=6),
# # #                 ], className="mb-3"),
# # #                 dcc.Dropdown(id='membership-type', options=[
# # #                     {'label': 'Ordinary Member', 'value': 'Ordinary'},
# # #                     {'label': 'Inhouse Member', 'value': 'Inhouse'}
# # #                 ], placeholder="Choose Membership Type *", className="mb-3"),
# # #                 html.Hr(),
# # #                 html.H4("Compliance Details (For Verification)", className="card-title text-primary mt-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
# # #                                                                        {'label': 'Non-Compliant',
# # #                                                                         'value': 'Non-Compliant'}],
# # #                                          placeholder="Tax Compliance Status"), width=6),
# # #                     dbc.Col(dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
# # #                                                                      {'label': 'Inactive/Expired',
# # #                                                                       'value': 'Inactive'}],
# # #                                          placeholder="TAFFA Membership Status"), width=6),
# # #                 ], className="mb-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dcc.Dropdown(id='policy-compliance',
# # #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# # #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# # #                                          placeholder="Policy Compliance Status"), width=6),
# # #                     dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# # #                                                                              {'label': 'Unpaid', 'value': 'Unpaid'}],
# # #                                          placeholder="Accreditation Fee Payment", value="Unpaid"), width=4),
# # #                     dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success"), width=2)
# # #                 ], className="mb-3 align-items-center"),
# # #                 html.Hr(),
# # #                 dcc.Checklist(options=[
# # #                     {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations', 'value': 1}],
# # #                     id='agree-terms', className="mt-4"),
# # #                 html.Div(dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
# # #                                     className="mt-4"), className="text-center"),
# # #                 html.Div(id='submission-output', className="mt-4")
# # #             ]))
# # #         ]),
# # #         dbc.Tab(label="TAFFA ID Application", children=[
# # #             dbc.Card(dbc.CardBody([
# # #                 html.H4("TAFFA ID Application", className="card-title text-primary"),
# # #                 html.P("This form is for TAFFA members to apply for an ID card."),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='id-full-name', placeholder='Full Name *', type='text'), width=6),
# # #                     dbc.Col(dbc.Input(id='id-nida-number', placeholder='NIDA Number *', type='text'), width=6),
# # #                 ], className="mb-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='id-position', placeholder='Position *', type='text'), width=6),
# # #                     dbc.Col([dcc.Upload(id='upload-passport-photo', children=html.Button('Upload Passport Photo *'),
# # #                                         className="w-100 mb-2"), html.Span(id='output-passport-photo')]),
# # #                 ], className="mb-3"),
# # #                 dbc.Row([
# # #                     dbc.Col([dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof *'),
# # #                                         className="w-100 mb-2"), html.Span(id='output-id-payment')]),
# # #                 ], className="mb-3"),
# # #                 dbc.Input(id='id-application-tin', placeholder='Your Company TIN *', type='text', className="mb-3"),
# # #                 dbc.Button('Submit ID Application', id='submit-id-button', n_clicks=0, color="primary", size="lg",
# # #                            className="mt-4"),
# # #                 html.Div(id='id-submission-output', className="mt-4")
# # #             ]))
# # #         ]),
# # #         dbc.Tab(label="Renew Membership", children=[
# # #             dbc.Card(dbc.CardBody([
# # #                 html.H4("Renew Membership", className="card-title text-primary"),
# # #                 html.P("Use this form to renew your annual membership and update company details."),
# # #                 dbc.Row([
# # #                     dbc.Col(dbc.Input(id='renew-tin-number', placeholder='Your Company TIN *', type='text'), width=6),
# # #                     dbc.Col(dbc.Input(id='renew-taffa-no', placeholder='Your TAFFA Membership No. *', type='text'),
# # #                             width=6),
# # #                 ], className="mb-3"),
# # #                 html.Hr(),
# # #                 html.H4("Compliance Details (For Renewal Verification)", className="card-title text-primary mt-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dcc.Dropdown(id='renew-tax-compliance',
# # #                                          options=[{'label': 'Compliant', 'value': 'Compliant'},
# # #                                                   {'label': 'Non-Compliant', 'value': 'Non-Compliant'}],
# # #                                          placeholder="Tax Compliance Status"), width=6),
# # #                     dbc.Col(dcc.Dropdown(id='renew-taffa-status',
# # #                                          options=[{'label': 'Active Member', 'value': 'Active'},
# # #                                                   {'label': 'Inactive/Expired', 'value': 'Inactive'}],
# # #                                          placeholder="TAFFA Membership Status"), width=6),
# # #                 ], className="mb-3"),
# # #                 dbc.Row([
# # #                     dbc.Col(dcc.Dropdown(id='renew-policy-compliance',
# # #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# # #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# # #                                          placeholder="Policy Compliance Status"), width=6),
# # #                     dbc.Col(dcc.Dropdown(id='renew-payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# # #                                                                                    {'label': 'Unpaid',
# # #                                                                                     'value': 'Unpaid'}],
# # #                                          placeholder="Renewal Fee Payment", value="Unpaid"), width=4),
# # #                     dbc.Col(dbc.Button("Pay Renewal Fee", id="renew-pay-button", color="success"), width=2)
# # #                 ], className="mb-3 align-items-center"),
# # #                 html.Hr(),
# # #                 html.H4("Document Upload (Renewal)", className="card-title text-primary mt-4"),
# # #                 dbc.Row([
# # #                     dbc.Col([dcc.Upload(id='renew-upload-cert-incorporation',
# # #                                         children=html.Button('Cert of Incorporation *'), className="w-100 mb-2"),
# # #                              html.Span(id='renew-output-cert-incorporation')]),
# # #                     dbc.Col([dcc.Upload(id='renew-upload-business-license', children=html.Button('Business License *'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-business-license')]),
# # #                     dbc.Col([dcc.Upload(id='renew-upload-brella-search', children=html.Button('Brella Search *'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-brella-search')]),
# # #                     dbc.Col([dcc.Upload(id='renew-upload-directors-images', children=html.Button('Directors Images *'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-directors-images')]),
# # #                 ]),
# # #                 dbc.Row([
# # #                     dbc.Col([dcc.Upload(id='renew-upload-tax-clearance', children=html.Button('Tax Clearance Cert'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-tax-clearance')]),
# # #                     dbc.Col([dcc.Upload(id='renew-upload-taffa-cert', children=html.Button('TAFFA Certificate'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-taffa-cert')]),
# # #                     dbc.Col([dcc.Upload(id='renew-upload-memo-articles', children=html.Button('Memo & Articles'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-memo-articles')]),
# # #                     dbc.Col([dcc.Upload(id='renew-upload-audited-accounts', children=html.Button('Audited Accounts'),
# # #                                         className="w-100 mb-2"), html.Span(id='renew-output-audited-accounts')]),
# # #                 ]),
# # #                 html.Div(
# # #                     dbc.Button('Submit Renewal', id='submit-renewal-button', n_clicks=0, color="primary", size="lg",
# # #                                className="mt-4"), className="text-center"),
# # #                 html.Div(id='renewal-submission-output', className="mt-4")
# # #             ]))
# # #         ]),
# # #         dbc.Tab(label="View Submissions", children=[
# # #             dbc.Card(dbc.CardBody([
# # #                 html.H4("Submitted Applications", className="card-title"),
# # #                 dash_table.DataTable(
# # #                     id='applications-table',
# # #                     columns=[
# # #                         {"name": "TIN", "id": "tin_number"},
# # #                         {"name": "Company Name", "id": "company_name"},
# # #                         {"name": "Submission Date", "id": "submission_date"},
# # #                         {"name": "Status", "id": "status"},
# # #                         {"name": "Reference Number", "id": "reference_number"},
# # #                     ],
# # #                     style_cell={'textAlign': 'left'},
# # #                 ),
# # #                 dbc.Button("Refresh Data", id="refresh-button", className="mt-3")
# # #             ]))
# # #         ]),
# # #         dbc.Tab(label="Admin Verification", id='admin-tab-content')
# # #     ]),
# # #     dbc.Popover(
# # #         [
# # #             dbc.PopoverHeader("Capital Pay Engine"),
# # #             dbc.PopoverBody(
# # #                 html.Div([
# # #                     dbc.Button("Pay with Equity Bank", id="pay-equity-btn", color="primary", className="d-block mb-2"),
# # #                     dbc.Button("Pay with NBC Bank", id="pay-nbc-btn", color="primary", className="d-block mb-2"),
# # #                     dbc.Button("Pay with M-Pesa", id="pay-mpesa-btn", color="primary", className="d-block")
# # #                 ])
# # #             ),
# # #         ],
# # #         id="payment-method-popover",
# # #         target="",
# # #         trigger="manual",
# # #     ),
# # #     dbc.Popover(
# # #         dbc.PopoverBody("Payment of 20,000 TZS successful!", className="text-success"),
# # #         id="payment-success-popover",
# # #         target="",
# # #         trigger="manual",
# # #     ),
# # #     dcc.Interval(
# # #         id='interval-popover',
# # #         interval=5 * 1000,
# # #         n_intervals=0,
# # #         disabled=True,
# # #     ),
# # # ], fluid=True)
# # #
# # #
# # # def save_uploaded_file(contents, filename, app_id, field_name):
# # #     if not contents:
# # #         return None
# # #
# # #     file_data = base64.b64decode(contents.split(',')[1])
# # #     app_folder = os.path.join(DOCUMENTS_DIR, str(app_id))
# # #     os.makedirs(app_folder, exist_ok=True)
# # #     unique_filename = f"{field_name}_{filename}"
# # #     file_path = os.path.join(app_folder, unique_filename)
# # #
# # #     with open(file_path, 'wb') as f:
# # #         f.write(file_data)
# # #
# # #     return file_path
# # #
# # #
# # # @app.callback(
# # #     Output('login-state', 'data'),
# # #     Output('admin-login-alert', 'children'),
# # #     Output('admin-login-alert', 'is_open'),
# # #     Input('admin-login-button', 'n_clicks'),
# # #     State('admin-username', 'value'),
# # #     State('admin-password', 'value'),
# # #     prevent_initial_call=True
# # # )
# # # def check_login(n_clicks, username, password):
# # #     if not n_clicks:
# # #         raise PreventUpdate
# # #
# # #     if username == ADMIN_USER and hashlib.sha256(password.encode('utf-8')).hexdigest() == ADMIN_PASS_HASH:
# # #         return {'is_authenticated': True}, "", False
# # #     else:
# # #         return {'is_authenticated': False}, "Invalid username or password.", True
# # #
# # #
# # # @app.callback(
# # #     Output('admin-tab-content', 'children'),
# # #     Input('login-state', 'data')
# # # )
# # # def render_admin_tab_content(data):
# # #     if data['is_authenticated']:
# # #         return [
# # #             dbc.Card(dbc.CardBody([
# # #                 html.H4("Verify Applications", className="card-title"),
# # #                 dash_table.DataTable(
# # #                     id='admin-table',
# # #                     columns=[
# # #                         {"name": "App ID", "id": "id"},
# # #                         {"name": "TIN", "id": "tin_number"},
# # #                         {"name": "Company Name", "id": "company_name"},
# # #                         {"name": "Status", "id": "status"},
# # #                     ],
# # #                     style_cell={'textAlign': 'left'},
# # #                     row_selectable='single',
# # #                 ),
# # #                 dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3"),
# # #                 html.Hr(),
# # #                 html.Div(id='admin-details-view')
# # #             ]))
# # #         ]
# # #     else:
# # #         return [
# # #             dbc.Card(dbc.CardBody([
# # #                 html.H4("Admin Login", className="card-title"),
# # #                 dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
# # #                 dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
# # #                 dbc.Button("Login", id="admin-login-button", color="primary"),
# # #                 dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
# # #             ]))
# # #         ]
# # #
# # #
# # # @app.callback(
# # #     Output('output-passport-photo', 'children'),
# # #     Output('output-id-payment', 'children'),
# # #     Input('upload-passport-photo', 'filename'),
# # #     Input('upload-id-payment', 'filename'),
# # #     prevent_initial_call=True
# # # )
# # # def update_id_upload_output(photo_name, payment_name):
# # #     return (
# # #         f'✓ {photo_name}' if photo_name else '',
# # #         f'✓ {payment_name}' if payment_name else '',
# # #     )
# # #
# # #
# # # @app.callback(
# # #     Output('renew-output-cert-incorporation', 'children'),
# # #     Output('renew-output-business-license', 'children'),
# # #     Output('renew-output-brella-search', 'children'),
# # #     Output('renew-output-directors-images', 'children'),
# # #     Output('renew-output-tax-clearance', 'children'),
# # #     Output('renew-output-taffa-cert', 'children'),
# # #     Output('renew-output-memo-articles', 'children'),
# # #     Output('renew-output-audited-accounts', 'children'),
# # #     Input('renew-upload-cert-incorporation', 'filename'),
# # #     Input('renew-upload-business-license', 'filename'),
# # #     Input('renew-upload-brella-search', 'filename'),
# # #     Input('renew-upload-directors-images', 'filename'),
# # #     Input('renew-upload-tax-clearance', 'filename'),
# # #     Input('renew-upload-taffa-cert', 'filename'),
# # #     Input('renew-upload-memo-articles', 'filename'),
# # #     Input('renew-upload-audited-accounts', 'filename'),
# # #     prevent_initial_call=True
# # # )
# # # def update_renewal_upload_output(cert_inc, biz_lic, brella, dir_img, tax_cert, taffa_cert, memo, audit):
# # #     return (
# # #         f'✓ {cert_inc}' if cert_inc else '',
# # #         f'✓ {biz_lic}' if biz_lic else '',
# # #         f'✓ {brella}' if brella else '',
# # #         f'✓ {dir_img}' if dir_img else '',
# # #         f'✓ {tax_cert}' if tax_cert else '',
# # #         f'✓ {taffa_cert}' if taffa_cert else '',
# # #         f'✓ {memo}' if memo else '',
# # #         f'✓ {audit}' if audit else '',
# # #     )
# # #
# # #
# # # @app.callback(
# # #     Output("payment-method-popover", "is_open"),
# # #     Output("payment-method-popover", "target"),
# # #     Input("pay-button", "n_clicks"),
# # #     Input("renew-pay-button", "n_clicks"),
# # #     prevent_initial_call=True
# # # )
# # # def toggle_payment_popover(n_clicks_pay, n_clicks_renew):
# # #     if ctx.triggered_id == "pay-button":
# # #         return True, "pay-button"
# # #     elif ctx.triggered_id == "renew-pay-button":
# # #         return True, "renew-pay-button"
# # #     return False, ""
# # #
# # #
# # # @app.callback(
# # #     Output("payment-success-popover", "is_open"),
# # #     Output("payment-success-popover", "target", allow_duplicate=True),
# # #     Output("payment-method-popover", "is_open", allow_duplicate=True),
# # #     Output("payment-store", "data"),
# # #     Output("interval-popover", "disabled"),
# # #     Input("pay-equity-btn", "n_clicks"),
# # #     Input("pay-nbc-btn", "n_clicks"),
# # #     Input("pay-mpesa-btn", "n_clicks"),
# # #     State("payment-method-popover", "target"),
# # #     prevent_initial_call=True
# # # )
# # # def handle_payment_confirmation(equity_clicks, nbc_clicks, mpesa_clicks, target_id):
# # #     if not any([equity_clicks, nbc_clicks, mpesa_clicks]):
# # #         raise PreventUpdate
# # #
# # #     time.sleep(1)
# # #     trx_id = f"CP{random.randint(100000, 999999)}"
# # #
# # #     return True, target_id, False, {'status': 'Paid', 'trx_id': trx_id}, False
# # #
# # #
# # # @app.callback(
# # #     Output("payment-success-popover", "is_open", allow_duplicate=True),
# # #     Output("interval-popover", "disabled", allow_duplicate=True),
# # #     Input("interval-popover", "n_intervals"),
# # #     State("payment-success-popover", "is_open"),
# # #     prevent_initial_call=True
# # # )
# # # def hide_payment_popover(n, is_open):
# # #     if is_open:
# # #         return False, True
# # #     raise PreventUpdate
# # #
# # #
# # # @app.callback(
# # #     Output("payment-confirmation", "value"),
# # #     Output("pay-button", "disabled"),
# # #     Input("payment-store", "data"),
# # #     prevent_initial_call=True
# # # )
# # # def update_payment_status(data):
# # #     if data and data.get("status") == "Paid":
# # #         return "Paid", True
# # #     return "Unpaid", False
# # #
# # #
# # # @app.callback(
# # #     Output('submission-output', 'children'),
# # #     Input('submit-button', 'n_clicks'),
# # #     [State('tin-number', 'value'), State('company-name', 'value'), State('contact-person', 'value'),
# # #      State('email', 'value'), State('phone', 'value'), State('physical-address', 'value'),
# # #      State('postal-address', 'value'), State('website', 'value'), State('taffa-membership-no', 'value'),
# # #      State('director-1', 'value'), State('director-2', 'value'), State('director-3', 'value'),
# # #      State('cert-incorporation-no', 'value'), State('business-license-no', 'value'),
# # #      State('membership-type', 'value'), State('agree-terms', 'value'),
# # #      State('tax-compliance', 'value'), State('taffa-status', 'value'), State('policy-compliance', 'value'),
# # #      State('payment-confirmation', 'value')],
# # #     prevent_initial_call=True
# # # )
# # # def submit_membership_application(n_clicks, tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no,
# # #                                   director_1, director_2, director_3, cert_inc_no, biz_lic_no, mem_type, agreed,
# # #                                   tax, taffa, policy, payment):
# # #     required_fields = [tin, company, contact, email, phone, phys_addr, post_addr, director_1, cert_inc_no, biz_lic_no,
# # #                        mem_type, agreed]
# # #     if not all(required_fields):
# # #         return dbc.Alert("Please fill all fields marked with * and upload the required documents.", color="danger")
# # #     if not agreed:
# # #         return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning")
# # #
# # #     try:
# # #         conn = sqlite3.connect(DB_PATH)
# # #         c = conn.cursor()
# # #         c.execute("""INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
# # #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
# # #                   (tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no, director_1, director_2,
# # #                    director_3, cert_inc_no, biz_lic_no, mem_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
# # #         agent_id = c.lastrowid
# # #
# # #         c.execute("""INSERT INTO applications (agent_id, agreed_to_terms, tax_compliance, taffa_status, policy_compliance, payment_confirmation)
# # #                      VALUES (?, ?, ?, ?, ?, ?)""",
# # #                   (agent_id, 1, tax, taffa, policy, payment))
# # #         conn.commit()
# # #         return dbc.Alert("Membership application submitted successfully!", color="success")
# # #     except sqlite3.IntegrityError:
# # #         return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger")
# # #     except Exception as e:
# # #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# # #     finally:
# # #         if conn: conn.close()
# # #
# # #
# # # @app.callback(
# # #     Output('id-submission-output', 'children'),
# # #     Input('submit-id-button', 'n_clicks'),
# # #     [State('id-full-name', 'value'), State('id-nida-number', 'value'), State('id-position', 'value'),
# # #      State('id-application-tin', 'value'),
# # #      State('upload-passport-photo', 'contents'), State('upload-id-payment', 'contents'),
# # #      State('upload-passport-photo', 'filename'), State('upload-id-payment', 'filename')],
# # #     prevent_initial_call=True
# # # )
# # # def submit_id_application(n_clicks, full_name, nida_number, position, tin, photo_cont, payment_cont, photo_name,
# # #                           payment_name):
# # #     required_fields = [full_name, nida_number, position, tin, photo_cont, payment_cont]
# # #     if not all(required_fields):
# # #         return dbc.Alert("Please fill all fields and upload required documents.", color="danger")
# # #
# # #     try:
# # #         conn = sqlite3.connect(DB_PATH)
# # #         conn.row_factory = sqlite3.Row
# # #         c = conn.cursor()
# # #
# # #         c.execute("SELECT id FROM agents WHERE tin_number = ?", (tin,))
# # #         agent_id_result = c.fetchone()
# # #
# # #         if not agent_id_result:
# # #             return dbc.Alert(f"No existing TAFFA member found with TIN {tin}.", color="danger")
# # #         agent_id = agent_id_result['id']
# # #
# # #         c.execute("SELECT id FROM applications WHERE agent_id = ? ORDER BY id DESC LIMIT 1", (agent_id,))
# # #         application_id_result = c.fetchone()
# # #
# # #         if not application_id_result:
# # #             return dbc.Alert(f"No completed membership application found for TIN {tin}.", color="danger")
# # #         application_id = application_id_result['id']
# # #
# # #         photo_path = save_uploaded_file(photo_cont, photo_name, application_id, 'passport_photo')
# # #         payment_path = save_uploaded_file(payment_cont, payment_name, application_id, 'id_payment_proof')
# # #
# # #         c.execute("""INSERT INTO id_applications (application_id, full_name, nida_number, position, passport_photo, id_payment_proof)
# # #                      VALUES (?, ?, ?, ?, ?, ?)""",
# # #                   (application_id, full_name, nida_number, position, photo_path, payment_path))
# # #         id_app_id = c.lastrowid
# # #         conn.commit()
# # #
# # #         id_app_data = c.execute("SELECT * FROM id_applications WHERE id = ?", (id_app_id,)).fetchone()
# # #         agent_data = c.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
# # #
# # #         filename = generate_id_card(id_app_data, agent_data)
# # #         download_link = dcc.Link("Download ID Card", href=f"/download-id/{os.path.basename(filename)}",
# # #                                  className="btn btn-primary mt-2")
# # #
# # #         return [
# # #             dbc.Alert("ID card application submitted successfully!", color="success"),
# # #             html.Div(download_link, className="mt-2")
# # #         ]
# # #
# # #     except Exception as e:
# # #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# # #     finally:
# # #         if conn: conn.close()
# # #
# # #
# # # @app.callback(
# # #     Output('renewal-submission-output', 'children'),
# # #     Input('submit-renewal-button', 'n_clicks'),
# # #     [State('renew-tin-number', 'value'), State('renew-taffa-no', 'value'),
# # #      State('renew-tax-compliance', 'value'), State('renew-taffa-status', 'value'),
# # #      State('renew-policy-compliance', 'value'), State('renew-payment-confirmation', 'value'),
# # #      State('renew-upload-cert-incorporation', 'contents'), State('renew-upload-business-license', 'contents'),
# # #      State('renew-upload-brella-search', 'contents'), State('renew-upload-directors-images', 'contents'),
# # #      State('renew-upload-tax-clearance', 'contents'), State('renew-upload-taffa-cert', 'contents'),
# # #      State('renew-upload-memo-articles', 'contents'), State('renew-upload-audited-accounts', 'contents'),
# # #      State('renew-upload-cert-incorporation', 'filename'), State('renew-upload-business-license', 'filename'),
# # #      State('renew-upload-brella-search', 'filename'), State('renew-upload-directors-images', 'filename'),
# # #      State('renew-upload-tax-clearance', 'filename'), State('renew-upload-taffa-cert', 'filename'),
# # #      State('renew-upload-memo-articles', 'filename'), State('renew-upload-audited-accounts', 'filename')],
# # #     prevent_initial_call=True
# # # )
# # # def submit_renewal(n_clicks, tin, taffa_no, tax, taffa, policy, payment,
# # #                    cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
# # #                    memo_cont, audit_cont, cert_inc_name, biz_lic_name, brella_name, dir_img_name, tax_cert_name,
# # #                    taffa_cert_name, memo_name, audit_name):
# # #     required_uploads = [cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
# # #                         memo_cont, audit_cont]
# # #     if not all(required_uploads):
# # #         return dbc.Alert("Please upload all required documents for renewal.", color="danger")
# # #
# # #     return [
# # #         dbc.Toast(
# # #             "Member license renewed!",
# # #             header="Renewal Status",
# # #             icon="success",
# # #             dismissable=True,
# # #             is_open=True,
# # #             style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# # #         )
# # #     ]
# # #
# # #
# # # @app.callback(
# # #     Output('applications-table', 'data'),
# # #     [Input('refresh-button', 'n_clicks'), Input('submission-output', 'children')]
# # # )
# # # def update_table(n_clicks, submission_output):
# # #     conn = sqlite3.connect(DB_PATH)
# # #     query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
# # #     df = pd.read_sql_query(query, conn)
# # #     conn.close()
# # #     return df.to_dict('records')
# # #
# # #
# # # @app.callback(
# # #     Output('admin-table', 'data'),
# # #     Input('admin-refresh-button', 'n_clicks'),
# # #     prevent_initial_call=True
# # # )
# # # def update_admin_table(n_clicks):
# # #     conn = sqlite3.connect(DB_PATH)
# # #     query = "SELECT p.id, a.tin_number, a.company_name, p.status FROM agents a JOIN applications p ON a.id = p.agent_id"
# # #     df = pd.read_sql_query(query, conn)
# # #     conn.close()
# # #     return df.to_dict('records')
# # #
# # #
# # # @app.callback(
# # #     Output('admin-details-view', 'children'),
# # #     Input('admin-table', 'selected_rows'),
# # #     State('admin-table', 'data'),
# # #     prevent_initial_call=True
# # # )
# # # def display_admin_details(selected_rows, table_data):
# # #     if not selected_rows:
# # #         return []
# # #
# # #     app_id = table_data[selected_rows[0]]['id']
# # #     conn = sqlite3.connect(DB_PATH)
# # #     conn.row_factory = sqlite3.Row
# # #     c = conn.cursor()
# # #     c.execute("""
# # #         SELECT * FROM agents a
# # #         JOIN applications p ON a.id = p.agent_id
# # #         WHERE p.id = ?
# # #     """, (app_id,))
# # #     data = c.fetchone()
# # #
# # #     id_applications_query = """
# # #         SELECT id, full_name, passport_photo, id_payment_proof, id_status FROM id_applications
# # #         WHERE application_id = ?
# # #     """
# # #     id_applications = pd.read_sql_query(id_applications_query, conn, params=(app_id,))
# # #     conn.close()
# # #
# # #     if not data:
# # #         return dbc.Alert("Could not retrieve application details.", color="danger")
# # #
# # #     status_color = {
# # #         "Verified": "success",
# # #         "Cancelled": "danger",
# # #         "Pending": "warning"
# # #     }.get(data['status'], "secondary")
# # #
# # #     document_links = []
# # #     document_fields = {
# # #         "Certificate of Incorporation": "cert_incorporation",
# # #         "Business License": "business_license",
# # #         "Brella Search": "brella_search",
# # #         "Directors Images": "director_images",
# # #         "Tax Clearance Cert": "tax_clearance_cert",
# # #         "TAFFA Certificate": "taffa_cert",
# # #         "Memo & Articles": "memo_articles",
# # #         "Audited Accounts": "audited_accounts",
# # #     }
# # #
# # #     for doc_name, field in document_fields.items():
# # #         if data[field]:
# # #             filename = os.path.basename(data[field])
# # #             download_link = dcc.Link(
# # #                 f"Download {doc_name}",
# # #                 href=f"/download-file/{data['agent_id']}/{filename}",
# # #                 className="d-block"
# # #             )
# # #             document_links.append(download_link)
# # #
# # #     details_layout = [
# # #         dbc.Row([
# # #             dbc.Col([
# # #                 dbc.Card([
# # #                     dbc.CardHeader("Company & Contact Information"),
# # #                     dbc.CardBody([
# # #                         html.P([html.Strong("Company Name: "), data['company_name']]),
# # #                         html.P([html.Strong("TIN Number: "), data['tin_number']]),
# # #                         html.P([html.Strong("Physical Address: "), data['physical_address']]),
# # #                         html.P([html.Strong("Contact Person: "), data['contact_person']]),
# # #                         html.P([html.Strong("Email: "), data['email']]),
# # #                         html.P([html.Strong("Phone: "), data['phone']]),
# # #                     ])
# # #                 ]),
# # #                 dbc.Card([
# # #                     dbc.CardHeader("Director Information"),
# # #                     dbc.CardBody([
# # #                         html.P([html.Strong("Director 1: "), data['director_1']]),
# # #                         html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"]),
# # #                         html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"]),
# # #                     ])
# # #                 ], className="mt-3"),
# # #             ], width=6),
# # #             dbc.Col([
# # #                 dbc.Card([
# # #                     dbc.CardHeader("Compliance & Verification"),
# # #                     dbc.CardBody([
# # #                         html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"]),
# # #                         html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"]),
# # #                         html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"]),
# # #                         html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']]),
# # #                         html.P([html.Strong("Current Status: "),
# # #                                 html.Strong(data['status'], className=f"text-{status_color}")])
# # #                     ])
# # #                 ]),
# # #                 dbc.Card([
# # #                     dbc.CardHeader("Uploaded Documents (Membership)"),
# # #                     dbc.CardBody(document_links)
# # #                 ], className="mt-3"),
# # #                 dbc.Card([
# # #                     dbc.CardHeader("Actions (Membership)"),
# # #                     dbc.CardBody([
# # #                         html.H5("Update Status for Selected Application"),
# # #                         dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
# # #                                                                           {'label': 'Cancelled', 'value': 'Cancelled'}],
# # #                                      placeholder="Select new status"),
# # #                         dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2"),
# # #                         dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
# # #                                    className="mt-2 ms-2", disabled=data['status'] != 'Verified'),
# # #                         html.Div(id="download-cert-link-div", className="mt-2"),
# # #                         html.Div(id='admin-update-output', className="mt-3")
# # #                     ])
# # #                 ], className="mt-3"),
# # #             ], width=6),
# # #         ], className="mt-4")
# # #     ]
# # #
# # #     id_card_links = []
# # #     if not id_applications.empty:
# # #         id_card_details = [html.Hr(), html.H5("ID Card Applications", className="card-title")]
# # #         for index, row in id_applications.iterrows():
# # #             id_app_id = row['id']
# # #             id_card_details.append(html.P(html.Strong(f"ID for: {row['full_name']}")))
# # #             id_card_details.append(dcc.Link("Download Passport Photo",
# # #                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['passport_photo'])}",
# # #                                             className="d-block"))
# # #             id_card_details.append(dcc.Link("Download ID Payment Proof",
# # #                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['id_payment_proof'])}",
# # #                                             className="d-block"))
# # #             id_card_details.append(html.P([html.Strong("ID Status: "), row['id_status']]))
# # #
# # #             if row['id_status'] == 'Verified':
# # #                 # The corrected link now has a download attribute and is not a button
# # #                 id_card_details.append(
# # #                     dcc.Link("Download ID Card", href=f"/download-id/{id_app_id}", download="", target="_blank",
# # #                              className="btn btn-primary mt-2"))
# # #             else:
# # #                 id_card_details.append(
# # #                     dbc.Button("Verify ID Application", id={"type": "verify-id-button", "index": str(id_app_id)},
# # #                                color="success", className="mt-2"))
# # #             id_card_details.append(html.Hr())
# # #         id_card_links = id_card_details
# # #     else:
# # #         id_card_links = html.Div([html.P("No ID Application submitted for this company.")])
# # #
# # #     details_layout.append(
# # #         dbc.Row([
# # #             dbc.Col(
# # #                 dbc.Card([
# # #                     dbc.CardHeader("ID Application Documents"),
# # #                     dbc.CardBody(id_card_links)
# # #                 ], className="mt-3"),
# # #                 width=12
# # #             )
# # #         ])
# # #     )
# # #     return details_layout
# # #
# # #
# # # @app.callback(
# # #     Output('admin-update-output', 'children'),
# # #     Input('admin-update-button', 'n_clicks'),
# # #     [State('admin-table', 'selected_rows'), State('admin-table', 'data'), State('admin-status-dropdown', 'value')],
# # #     prevent_initial_call=True
# # # )
# # # def update_status(n_clicks, selected_rows, table_data, new_status):
# # #     if not selected_rows or not new_status:
# # #         raise PreventUpdate
# # #
# # #     app_id = table_data[selected_rows[0]]['id']
# # #     ref_number = f"TAFFA-TRA-{random.randint(10000, 99999)}{'PASS' if new_status == 'Verified' else 'FAIL'}"
# # #
# # #     try:
# # #         conn = sqlite3.connect(DB_PATH)
# # #         c = conn.cursor()
# # #         c.execute("UPDATE applications SET status = ?, reference_number = ? WHERE id = ?",
# # #                   (new_status, ref_number, app_id))
# # #         conn.commit()
# # #
# # #         c.execute("SELECT a.email FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?", (app_id,))
# # #         agent_email = c.fetchone()[0]
# # #
# # #         email_body = (
# # #             f"Dear Applicant,\n\n"
# # #             f"The status of your TAFFA membership application has been updated to: {new_status}.\n\n"
# # #             f"Reference Number: {ref_number}\n\n"
# # #             f"Thank you,\nTAFFA Administration"
# # #         )
# # #
# # #         email_sent = send_email(agent_email, f"TAFFA Application Update: {new_status}", email_body)
# # #
# # #         if email_sent:
# # #             return [
# # #                 dbc.Alert(f"Application {app_id} updated to '{new_status}'. A notification has been sent.",
# # #                           color="success"),
# # #                 dbc.Toast(
# # #                     "Email notification sent successfully!",
# # #                     header="Email Status",
# # #                     icon="success",
# # #                     dismissable=True,
# # #                     is_open=True,
# # #                     style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# # #                 )
# # #             ]
# # #         else:
# # #             return dbc.Alert(f"Application {app_id} updated to '{new_status}'. Failed to send email notification.",
# # #                              color="warning")
# # #
# # #     except Exception as e:
# # #         return dbc.Alert(f"Error updating status: {e}", color="danger")
# # #     finally:
# # #         if conn: conn.close()
# # #
# # #
# # # @app.callback(
# # #     Output({"type": "verify-id-button", "index": MATCH}, "children"),
# # #     Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
# # #     State({"type": "verify-id-button", "index": ALL}, "id"),
# # #     prevent_initial_call=True
# # # )
# # # def verify_id_application(n_clicks, button_ids):
# # #     if not n_clicks or not any(n_clicks):
# # #         raise PreventUpdate
# # #
# # #     triggered_id_json = ctx.triggered[0]['prop_id']
# # #     triggered_id_dict = json.loads(triggered_id_json)
# # #     clicked_id = triggered_id_dict['index']
# # #
# # #     conn = sqlite3.connect(DB_PATH)
# # #     conn.row_factory = sqlite3.Row
# # #     c = conn.cursor()
# # #     id_number = f"TAFFA-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
# # #     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
# # #
# # #     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
# # #               ('Verified', id_number, expiry_date, clicked_id))
# # #     conn.commit()
# # #     conn.close()
# # #
# # #     return "Verified!"
# # #
# # #
# # # @app.callback(
# # #     Output('generate-cert-button', 'disabled'),
# # #     Input('admin-table', 'selected_rows'),
# # #     Input('admin-update-output', 'children'),
# # #     State('admin-table', 'data'),
# # #     prevent_initial_call=True
# # # )
# # # def toggle_generate_button(selected_rows, update_output, table_data):
# # #     if not selected_rows:
# # #         return True
# # #
# # #     app_id = table_data[selected_rows[0]]['id']
# # #     conn = sqlite3.connect(DB_PATH)
# # #     c = conn.cursor()
# # #     c.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
# # #     status = c.fetchone()[0]
# # #     conn.close()
# # #
# # #     return status != 'Verified'
# # #
# # #
# # # def generate_membership_certificate(app_data):
# # #     filename = f"Certificate-{app_data['tin_number']}.pdf"
# # #     filepath = os.path.join(CERTIFICATES_DIR, filename)
# # #     c = canvas.Canvas(filepath, pagesize=letter)
# # #     width, height = letter
# # #
# # #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # #
# # #     if os.path.exists(taffa_logo_path):
# # #         c.drawImage(taffa_logo_path, 30, height - 150, width=150, height=150, preserveAspectRatio=True, mask='auto')
# # #
# # #     c.setFont("Helvetica-Bold", 16)
# # #     c.setFillColor(colors.black)
# # #     c.drawRightString(width - 50, height - 110, f"No. {random.randint(1000, 9999)}")
# # #
# # #     c.setFont("Helvetica-Bold", 24)
# # #     c.setFillColor(colors.HexColor('#003366'))
# # #     c.drawCentredString(width / 2.0, height - 200, "CERTIFICATE OF MEMBERSHIP")
# # #
# # #     c.setFont("Helvetica", 14)
# # #     c.setFillColor(colors.black)
# # #     c.drawCentredString(width / 2.0, height - 250, "CERTIFICATE IS AWARDED TO")
# # #
# # #     c.setFont("Helvetica-Bold", 20)
# # #     c.drawCentredString(width / 2.0, height - 280, app_data['company_name'].upper())
# # #
# # #     c.setFont("Helvetica", 12)
# # #     c.drawCentredString(width / 2.0, height - 320,
# # #                         f"as a Tanzania Freight Forwarder Association Member for {date.today().year}")
# # #
# # #     c.save()
# # #     return filename
# # #
# # #
# # # def generate_id_card(id_app_data, agent_data):
# # #     filename = f"ID-{id_app_data['id_number']}.pdf"
# # #     filepath = os.path.join(IDS_DIR, filename)
# # #     c = canvas.Canvas(filepath, pagesize=A4)
# # #     width, height = A4
# # #
# # #     # ID card dimensions
# # #     card_width = width * 0.75
# # #     card_height = height * 0.75
# # #
# # #     # Calculate offsets to center the card on the page
# # #     x_offset = (width - card_width) / 2
# # #     y_offset = (height - card_height) / 2
# # #     content_center_x = x_offset + card_width / 2
# # #
# # #     # Draw the border
# # #     c.setStrokeColor(colors.HexColor('#003366'))
# # #     c.setFillColor(colors.white)
# # #     c.setLineWidth(5)
# # #     c.roundRect(x_offset, y_offset, card_width, card_height, 10, stroke=1, fill=1)
# # #
# # #     # Header with TAFFA logo and text
# # #     header_height = card_height * 0.2
# # #     c.setFillColor(colors.HexColor('#F0F8FF'))
# # #     c.rect(x_offset, y_offset + card_height - header_height, card_width, header_height, fill=1, stroke=0)
# # #
# # #     # TAFFA Logo
# # #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # #     if os.path.exists(taffa_logo_path):
# # #         logo_size = header_height * 0.8
# # #         logo_x = x_offset + card_width * 0.05
# # #         logo_y = y_offset + card_height - header_height + (header_height - logo_size) / 2
# # #         c.drawImage(taffa_logo_path, logo_x, logo_y, width=logo_size, height=logo_size, preserveAspectRatio=True)
# # #
# # #     # Title text
# # #     c.setFont("Helvetica-Bold", 14)
# # #     c.setFillColor(colors.HexColor('#003366'))
# # #     title_y = y_offset + card_height - header_height / 2 + 10
# # #     c.drawCentredString(x_offset + card_width * 0.5, title_y, "TANZANIA FREIGHT")
# # #     c.drawCentredString(x_offset + card_width * 0.5, title_y - 20, "FORWARDERS ASSOCIATION")
# # #
# # #     # Photo - Centered
# # #     photo_path = id_app_data['passport_photo']
# # #     photo_size = card_width * 0.3
# # #     photo_x = content_center_x - photo_size / 2
# # #     photo_y = y_offset + card_height - header_height - 10 - photo_size
# # #     if os.path.exists(photo_path):
# # #         c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True)
# # #     else:
# # #         c.drawString(photo_x, photo_y + photo_size / 2, "Photo not found")
# # #
# # #     # Personal Details - Centered underneath the photo
# # #     c.setFont("Helvetica-Bold", 12)
# # #     c.setFillColor(colors.black)
# # #     details_y = photo_y - 30
# # #
# # #     c.drawCentredString(content_center_x, details_y, f"Name: {id_app_data['full_name']}")
# # #     c.drawCentredString(content_center_x, details_y - 20, f"Position: {id_app_data['position']}")
# # #     c.drawCentredString(content_center_x, details_y - 40, f"Company: {agent_data['company_name']}")
# # #
# # #     # ID details
# # #     c.setFont("Helvetica-Bold", 12)
# # #     c.setFillColor(colors.HexColor('#003366'))
# # #     id_y_start = details_y - 80
# # #     c.drawCentredString(content_center_x, id_y_start, f"ID NO: {id_app_data['id_number']}")
# # #     c.drawCentredString(content_center_x, id_y_start - 20, f"Expiry Date: {id_app_data['expiry_date']}")
# # #
# # #     # QR code - Centered at the bottom
# # #     qr_data = f"ID: {id_app_data['id_number']} | Expiry: {id_app_data['expiry_date']}"
# # #     qr_img = qrcode.make(qr_data)
# # #     qr_buffer = io.BytesIO()
# # #     qr_img.save(qr_buffer, format='PNG')
# # #     qr_buffer.seek(0)
# # #
# # #     qr_size = card_width * 0.25
# # #     qr_x = content_center_x - qr_size / 2
# # #     qr_y = y_offset + 20
# # #     c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)
# # #
# # #     c.save()
# # #     return filename
# # #
# # #
# # # @app.callback(
# # #     Output('download-cert-link-div', 'children'),
# # #     Input('generate-cert-button', 'n_clicks'),
# # #     State('admin-table', 'selected_rows'),
# # #     State('admin-table', 'data'),
# # #     prevent_initial_call=True
# # # )
# # # def handle_certificate_generation(n_clicks, selected_rows, table_data):
# # #     if not selected_rows:
# # #         raise PreventUpdate
# # #
# # #     app_id = table_data[selected_rows[0]]['id']
# # #
# # #     conn = sqlite3.connect(DB_PATH)
# # #     query = """
# # #         SELECT a.tin_number, a.company_name, p.reference_number, p.status
# # #         FROM agents a JOIN applications p ON a.id = p.agent_id
# # #         WHERE p.id = ?
# # #     """
# # #     df = pd.read_sql_query(query, conn, params=(app_id,))
# # #     conn.close()
# # #
# # #     if df.empty:
# # #         return dbc.Alert("Could not find application data.", color="danger")
# # #
# # #     app_data = df.to_dict('records')[0]
# # #     filename = generate_membership_certificate(app_data)
# # #
# # #     return dcc.Link(f"Download Certificate for {app_data['company_name']}",
# # #                     href=f"/download-cert/{os.path.basename(filename)}")
# # #
# # #
# # # @app.callback(
# # #     Output({"type": "download-id-link", "index": MATCH}, "children"),
# # #     Input({"type": "verify-id-button", "index": MATCH}, "n_clicks"),
# # #     State({"type": "verify-id-button", "index": ALL}, "id"),
# # #     prevent_initial_call=True
# # # )
# # # def verify_id_application(n_clicks, button_ids):
# # #     if not n_clicks or not any(n_clicks):
# # #         raise PreventUpdate
# # #
# # #     triggered_id_json = ctx.triggered[0]['prop_id']
# # #     triggered_id_dict = json.loads(triggered_id_json)
# # #     clicked_id = triggered_id_dict['index']
# # #
# # #     conn = sqlite3.connect(DB_PATH)
# # #     conn.row_factory = sqlite3.Row
# # #     c = conn.cursor()
# # #     id_number = f"TAFFA-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
# # #     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
# # #
# # #     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
# # #               ('Verified', id_number, expiry_date, clicked_id))
# # #     conn.commit()
# # #     conn.close()
# # #
# # #     return "Verified!"
# # #
# # #
# # # @server.route('/download-cert/<filename>')
# # # def serve_pdf(filename):
# # #     return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)
# # #
# # #
# # # @server.route('/download-id/<id_app_id>')
# # # def serve_id(id_app_id):
# # #     conn = sqlite3.connect(DB_PATH)
# # #     conn.row_factory = sqlite3.Row
# # #     c = conn.cursor()
# # #     c.execute("SELECT id_number FROM id_applications WHERE id = ?", (id_app_id,))
# # #     id_number = c.fetchone()['id_number']
# # #     conn.close()
# # #
# # #     filename = f"ID-{id_number}.pdf"
# # #
# # #     return send_from_directory(IDS_DIR, filename, as_attachment=True)
# # #
# # #
# # # @server.route('/download-file/<app_id>/<filename>')
# # # def download_uploaded_file(app_id, filename):
# # #     app_folder = os.path.join(DOCUMENTS_DIR, app_id)
# # #     return send_from_directory(app_folder, filename, as_attachment=True)
# # #
# # #
# # # if __name__ == '__main__':
# # #     if not os.path.exists(DOCUMENTS_DIR):
# # #         os.makedirs(DOCUMENTS_DIR)
# # #     if not os.path.exists(CERTIFICATES_DIR):
# # #         os.makedirs(CERTIFICATES_DIR)
# # #     if not os.path.exists(IDS_DIR):
# # #         os.makedirs(IDS_DIR)
# # #
# # #     assets_dir = os.path.join(BASE_DIR, 'assets')
# # #     if not os.path.exists(assets_dir):
# # #         os.makedirs(assets_dir)
# # #
# # #     app.run(debug=True, port=5078)
# #
# #
# # import dash
# # from dash import dcc, html, Input, Output, State, ctx, dash_table
# # import dash_bootstrap_components as dbc
# # from dash.exceptions import PreventUpdate
# # import sqlite3
# # import pandas as pd
# # from datetime import datetime, date, timedelta
# # import base64
# # import io
# # from reportlab.lib.pagesizes import letter, A4
# # from reportlab.pdfgen import canvas
# # from reportlab.lib.utils import ImageReader
# # from reportlab.lib import colors
# # from reportlab.lib.units import inch
# # from PIL import Image
# # import os
# # import random
# # import time
# # import smtplib
# # from email.message import EmailMessage
# # import socket
# # from flask import send_from_directory
# # import qrcode
# # import hashlib
# # from dash.dependencies import MATCH, ALL
# # import json
# #
# # # Initialize the Dash app with Flask server and suppress callback exceptions
# # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True,
# #                 title="TAFFA Portal")
# # server = app.server
# #
# # # --- Admin Credentials ---
# # ADMIN_USER = "admin"
# # ADMIN_PASS_HASH = hashlib.sha256("password".encode('utf-8')).hexdigest()
# #
# # # --- Database Setup with Absolute Path ---
# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # DB_PATH = os.path.join(BASE_DIR, "tra_cfa_data.db")
# # DOCUMENTS_DIR = os.path.join(BASE_DIR, "uploaded_documents")
# # CERTIFICATES_DIR = os.path.join(BASE_DIR, "certificates")
# # IDS_DIR = os.path.join(BASE_DIR, "id_cards")
# #
# #
# # def init_db():
# #     conn = sqlite3.connect(DB_PATH)
# #     c = conn.cursor()
# #
# #     # Drop tables to ensure a clean slate and prevent schema errors on re-runs
# #     c.execute('DROP TABLE IF EXISTS id_applications')
# #     c.execute('DROP TABLE IF EXISTS applications')
# #     c.execute('DROP TABLE IF EXISTS agents')
# #     c.execute('DROP TABLE IF EXISTS taffa_id_applications')
# #
# #     # agents table updated to match the latest fields
# #     c.execute('''
# #         CREATE TABLE IF NOT EXISTS agents (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             tin_number TEXT NOT NULL UNIQUE,
# #             company_name TEXT NOT NULL,
# #             contact_person TEXT NOT NULL,
# #             email TEXT NOT NULL,
# #             phone TEXT NOT NULL,
# #             physical_address TEXT,
# #             postal_address TEXT,
# #             website TEXT,
# #             taffa_membership_no TEXT,
# #             director_1 TEXT,
# #             director_2 TEXT,
# #             director_3 TEXT,
# #             cert_incorporation_no TEXT,
# #             business_license_no TEXT,
# #             membership_type TEXT,
# #             submission_date TEXT NOT NULL
# #         )
# #     ''')
# #     # applications table updated to store file paths as TEXT
# #     c.execute('''
# #         CREATE TABLE IF NOT EXISTS applications (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             agent_id INTEGER,
# #             tax_compliance TEXT,
# #             taffa_status TEXT,
# #             policy_compliance TEXT,
# #             payment_confirmation TEXT,
# #             business_license TEXT,
# #             tax_clearance_cert TEXT,
# #             taffa_cert TEXT,
# #             cert_incorporation TEXT,
# #             memo_articles TEXT,
# #             audited_accounts TEXT,
# #             director_images TEXT,
# #             brella_search TEXT,
# #             agreed_to_terms INTEGER,
# #             status TEXT DEFAULT 'Pending',
# #             reference_number TEXT,
# #             FOREIGN KEY (agent_id) REFERENCES agents (id)
# #         )
# #     ''')
# #     # New table for ID applications
# #     c.execute('''
# #         CREATE TABLE IF NOT EXISTS id_applications (
# #             id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             application_id INTEGER,
# #             full_name TEXT,
# #             nida_number TEXT,
# #             position TEXT,
# #             passport_photo TEXT,
# #             id_payment_proof TEXT,
# #             id_status TEXT DEFAULT 'Pending',
# #             id_number TEXT,
# #             expiry_date TEXT,
# #             FOREIGN KEY (application_id) REFERENCES applications (id)
# #         )
# #     ''')
# #
# #     conn.commit()
# #     conn.close()
# #
# #
# # init_db()
# #
# # # --- Logo Paths ---
# # taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# # taffa_logo_src = "/assets/LOGO.png"
# #
# #
# # # --- Reusable Components ---
# # def logo_header(logo_src, text):
# #     return dbc.Row([
# #         dbc.Col(html.Img(src=logo_src, height="80px"), width="auto"),
# #         dbc.Col(html.H5(text, className="align-self-center"))
# #     ], className="mb-4 align-items-center justify-content-center")
# #
# #
# # def send_email(recipient_email: str, subject: str, body: str):
# #     """Sends an email notification."""
# #     sender_email = "administrator@capitalpayinternational.com"
# #     sender_password = "ahxr wusz rqvp jpsx"
# #     smtp_server = "smtp.gmail.com"
# #     smtp_port = 587
# #
# #     if not sender_password:
# #         print("Error: Email password is not set.")
# #         return False
# #
# #     msg = EmailMessage()
# #     msg['Subject'] = f"Update: Milestone Reached - {subject}"
# #     msg['From'] = sender_email
# #     msg['To'] = recipient_email
# #     msg.set_content(body)
# #
# #     try:
# #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# #             server.starttls()
# #             server.login(sender_email, sender_password)
# #             server.send_message(msg)
# #             print(f"Email notification sent successfully to {recipient_email}!")
# #             return True
# #     except socket.gaierror as e:
# #         print(f"Network error: {e}. Could not find host: '{smtp_server}'.")
# #         return False
# #     except Exception as e:
# #         print(f"An unexpected error occurred: {e}")
# #         return False
# #
# #
# # # --- App Layout ---
# # app.layout = dbc.Container([
# #     dcc.Store(id='payment-store'),
# #     dcc.Store(id='login-state', data={'is_authenticated': False}),
# #     dbc.Row([
# #         dbc.Col(html.Img(src="/assets/LOGO.png", height="100px"), width="auto"),
# #         dbc.Col(html.H1("Customs Agent Accreditation Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
# #                 width="auto")
# #     ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),
# #
# #     dbc.Tabs(id='tabs', children=[
# #         dbc.Tab(label="New Application", children=[
# #             dbc.Card(dbc.CardBody([
# #                 html.H4("Membership Application Form", className="card-title text-primary"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text'), width=6),
# #                     dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text'), width=6),
# #                 ], className="mb-3"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text'),
# #                             width=6),
# #                     dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text'), width=6),
# #                 ], className="mb-3"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='website', placeholder='Website', type='text'), width=6),
# #                     dbc.Col(dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
# #                                       type='text'), width=6),
# #                 ], className="mb-3"),
# #                 html.Hr(),
# #                 html.H4("Contact Person", className="card-title text-primary mt-3"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='contact-person', placeholder='Contact Person Name *', type='text'), width=4),
# #                     dbc.Col(dbc.Input(id='email', placeholder='Email Address *', type='email'), width=4),
# #                     dbc.Col(dbc.Input(id='phone', placeholder='Mobile Number *', type='text'), width=4),
# #                 ], className="mb-3"),
# #                 html.Hr(),
# #                 html.H4("Directors", className="card-title text-primary mt-3"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text'), width=4),
# #                     dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text'), width=4),
# #                     dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text'), width=4),
# #                 ], className="mb-3"),
# #                 html.Hr(),
# #                 html.H4("Company Details", className="card-title text-primary mt-3"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
# #                                       type='text'), width=6),
# #                     dbc.Col(dbc.Input(id='business-license-no', placeholder='Business License No. *', type='text'),
# #                             width=6),
# #                 ], className="mb-3"),
# #                 dcc.Dropdown(id='membership-type', options=[
# #                     {'label': 'Ordinary Member', 'value': 'Ordinary'},
# #                     {'label': 'Inhouse Member', 'value': 'Inhouse'}
# #                 ], placeholder="Choose Membership Type *", className="mb-3"),
# #                 html.Hr(),
# #                 html.H4("Compliance Details (For Verification)", className="card-title text-primary mt-3"),
# #                 dbc.Row([
# #                     dbc.Col(dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
# #                                                                        {'label': 'Non-Compliant',
# #                                                                         'value': 'Non-Compliant'}],
# #                                          placeholder="Tax Compliance Status"), width=6),
# #                     dbc.Col(dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
# #                                                                      {'label': 'Inactive/Expired',
# #                                                                       'value': 'Inactive'}],
# #                                          placeholder="TAFFA Membership Status"), width=6),
# #                 ], className="mb-3"),
# #                 dbc.Row([
# #                     dbc.Col(dcc.Dropdown(id='policy-compliance',
# #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# #                                          placeholder="Policy Compliance Status"), width=6),
# #                     dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# #                                                                              {'label': 'Unpaid', 'value': 'Unpaid'}],
# #                                          placeholder="Accreditation Fee Payment", value="Unpaid"), width=4),
# #                     dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success"), width=2)
# #                 ], className="mb-3 align-items-center"),
# #                 html.Hr(),
# #                 dcc.Checklist(options=[
# #                     {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations', 'value': 1}],
# #                     id='agree-terms', className="mt-4"),
# #                 html.Div(dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
# #                                     className="mt-4"), className="text-center"),
# #                 html.Div(id='submission-output', className="mt-4")
# #             ]))
# #         ]),
# #         dbc.Tab(label="TAFFA ID Application", children=[
# #             dbc.Card(dbc.CardBody([
# #                 html.H4("TAFFA ID Application", className="card-title text-primary"),
# #                 html.P("This form is for TAFFA members to apply for an ID card."),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='id-full-name', placeholder='Full Name *', type='text'), width=6),
# #                     dbc.Col(dbc.Input(id='id-nida-number', placeholder='NIDA Number *', type='text'), width=6),
# #                 ], className="mb-3"),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='id-position', placeholder='Position *', type='text'), width=6),
# #                     dbc.Col([dcc.Upload(id='upload-passport-photo', children=html.Button('Upload Passport Photo *'),
# #                                         className="w-100 mb-2"), html.Span(id='output-passport-photo')]),
# #                 ], className="mb-3"),
# #                 dbc.Row([
# #                     dbc.Col([dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof *'),
# #                                         className="w-100 mb-2"), html.Span(id='output-id-payment')]),
# #                 ], className="mb-3"),
# #                 dbc.Input(id='id-application-tin', placeholder='Your Company TIN *', type='text', className="mb-3"),
# #                 dbc.Button('Submit ID Application', id='submit-id-button', n_clicks=0, color="primary", size="lg",
# #                            className="mt-4"),
# #                 html.Div(id='id-submission-output', className="mt-4")
# #             ]))
# #         ]),
# #         dbc.Tab(label="Renew Membership", children=[
# #             dbc.Card(dbc.CardBody([
# #                 html.H4("Renew Membership", className="card-title text-primary"),
# #                 html.P("Use this form to renew your annual membership and update company details."),
# #                 dbc.Row([
# #                     dbc.Col(dbc.Input(id='renew-tin-number', placeholder='Your Company TIN *', type='text'), width=6),
# #                     dbc.Col(dbc.Input(id='renew-taffa-no', placeholder='Your TAFFA Membership No. *', type='text'),
# #                             width=6),
# #                 ], className="mb-3"),
# #                 html.Hr(),
# #                 html.H4("Compliance Details (For Renewal Verification)", className="card-title text-primary mt-3"),
# #                 dbc.Row([
# #                     dbc.Col(dcc.Dropdown(id='renew-tax-compliance',
# #                                          options=[{'label': 'Compliant', 'value': 'Compliant'},
# #                                                   {'label': 'Non-Compliant', 'value': 'Non-Compliant'}],
# #                                          placeholder="Tax Compliance Status"), width=6),
# #                     dbc.Col(dcc.Dropdown(id='renew-taffa-status',
# #                                          options=[{'label': 'Active Member', 'value': 'Active'},
# #                                                   {'label': 'Inactive/Expired', 'value': 'Inactive'}],
# #                                          placeholder="TAFFA Membership Status"), width=6),
# #                 ], className="mb-3"),
# #                 dbc.Row([
# #                     dbc.Col(dcc.Dropdown(id='renew-policy-compliance',
# #                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
# #                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
# #                                          placeholder="Policy Compliance Status"), width=6),
# #                     dbc.Col(dcc.Dropdown(id='renew-payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
# #                                                                                    {'label': 'Unpaid',
# #                                                                                     'value': 'Unpaid'}],
# #                                          placeholder="Renewal Fee Payment", value="Unpaid"), width=4),
# #                     dbc.Col(dbc.Button("Pay Renewal Fee", id="renew-pay-button", color="success"), width=2)
# #                 ], className="mb-3 align-items-center"),
# #                 html.Hr(),
# #                 html.H4("Document Upload (Renewal)", className="card-title text-primary mt-4"),
# #                 dbc.Row([
# #                     dbc.Col([dcc.Upload(id='renew-upload-cert-incorporation',
# #                                         children=html.Button('Cert of Incorporation *'), className="w-100 mb-2"),
# #                              html.Span(id='renew-output-cert-incorporation')]),
# #                     dbc.Col([dcc.Upload(id='renew-upload-business-license', children=html.Button('Business License *'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-business-license')]),
# #                     dbc.Col([dcc.Upload(id='renew-upload-brella-search', children=html.Button('Brella Search *'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-brella-search')]),
# #                     dbc.Col([dcc.Upload(id='renew-upload-directors-images', children=html.Button('Directors Images *'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-directors-images')]),
# #                 ]),
# #                 dbc.Row([
# #                     dbc.Col([dcc.Upload(id='renew-upload-tax-clearance', children=html.Button('Tax Clearance Cert'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-tax-clearance')]),
# #                     dbc.Col([dcc.Upload(id='renew-upload-taffa-cert', children=html.Button('TAFFA Certificate'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-taffa-cert')]),
# #                     dbc.Col([dcc.Upload(id='renew-upload-memo-articles', children=html.Button('Memo & Articles'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-memo-articles')]),
# #                     dbc.Col([dcc.Upload(id='renew-upload-audited-accounts', children=html.Button('Audited Accounts'),
# #                                         className="w-100 mb-2"), html.Span(id='renew-output-audited-accounts')]),
# #                 ]),
# #                 html.Div(
# #                     dbc.Button('Submit Renewal', id='submit-renewal-button', n_clicks=0, color="primary", size="lg",
# #                                className="mt-4"), className="text-center"),
# #                 html.Div(id='renewal-submission-output', className="mt-4")
# #             ]))
# #         ]),
# #         dbc.Tab(label="View Submissions", children=[
# #             dbc.Card(dbc.CardBody([
# #                 html.H4("Submitted Applications", className="card-title"),
# #                 dash_table.DataTable(
# #                     id='applications-table',
# #                     columns=[
# #                         {"name": "TIN", "id": "tin_number"},
# #                         {"name": "Company Name", "id": "company_name"},
# #                         {"name": "Submission Date", "id": "submission_date"},
# #                         {"name": "Status", "id": "status"},
# #                         {"name": "Reference Number", "id": "reference_number"},
# #                     ],
# #                     style_cell={'textAlign': 'left'},
# #                 ),
# #                 dbc.Button("Refresh Data", id="refresh-button", className="mt-3")
# #             ]))
# #         ]),
# #         dbc.Tab(label="Admin Verification", id='admin-tab-content')
# #     ]),
# #     dbc.Popover(
# #         [
# #             dbc.PopoverHeader("Capital Pay Engine"),
# #             dbc.PopoverBody(
# #                 html.Div([
# #                     dbc.Button("Pay with Equity Bank", id="pay-equity-btn", color="primary", className="d-block mb-2"),
# #                     dbc.Button("Pay with NBC Bank", id="pay-nbc-btn", color="primary", className="d-block mb-2"),
# #                     dbc.Button("Pay with M-Pesa", id="pay-mpesa-btn", color="primary", className="d-block")
# #                 ])
# #             ),
# #         ],
# #         id="payment-method-popover",
# #         target="",
# #         trigger="manual",
# #     ),
# #     dbc.Popover(
# #         dbc.PopoverBody("Payment of 20,000 TZS successful!", className="text-success"),
# #         id="payment-success-popover",
# #         target="",
# #         trigger="manual",
# #     ),
# #     dcc.Interval(
# #         id='interval-popover',
# #         interval=5 * 1000,
# #         n_intervals=0,
# #         disabled=True,
# #     ),
# # ], fluid=True)
# #
# #
# # def save_uploaded_file(contents, filename, app_id, field_name):
# #     if not contents:
# #         return None
# #
# #     file_data = base64.b64decode(contents.split(',')[1])
# #     app_folder = os.path.join(DOCUMENTS_DIR, str(app_id))
# #     os.makedirs(app_folder, exist_ok=True)
# #     unique_filename = f"{field_name}_{filename}"
# #     file_path = os.path.join(app_folder, unique_filename)
# #
# #     with open(file_path, 'wb') as f:
# #         f.write(file_data)
# #
# #     return file_path
# #
# #
# # @app.callback(
# #     Output('login-state', 'data'),
# #     Output('admin-login-alert', 'children'),
# #     Output('admin-login-alert', 'is_open'),
# #     Input('admin-login-button', 'n_clicks'),
# #     State('admin-username', 'value'),
# #     State('admin-password', 'value'),
# #     prevent_initial_call=True
# # )
# # def check_login(n_clicks, username, password):
# #     if not n_clicks:
# #         raise PreventUpdate
# #
# #     if username == ADMIN_USER and hashlib.sha256(password.encode('utf-8')).hexdigest() == ADMIN_PASS_HASH:
# #         return {'is_authenticated': True}, "", False
# #     else:
# #         return {'is_authenticated': False}, "Invalid username or password.", True
# #
# #
# # @app.callback(
# #     Output('admin-tab-content', 'children'),
# #     Input('login-state', 'data')
# # )
# # def render_admin_tab_content(data):
# #     if data['is_authenticated']:
# #         return [
# #             dbc.Card(dbc.CardBody([
# #                 html.H4("Verify Applications", className="card-title"),
# #                 dash_table.DataTable(
# #                     id='admin-table',
# #                     columns=[
# #                         {"name": "App ID", "id": "id"},
# #                         {"name": "TIN", "id": "tin_number"},
# #                         {"name": "Company Name", "id": "company_name"},
# #                         {"name": "Status", "id": "status"},
# #                     ],
# #                     style_cell={'textAlign': 'left'},
# #                     row_selectable='single',
# #                 ),
# #                 dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3"),
# #                 html.Hr(),
# #                 html.Div(id='admin-details-view')
# #             ]))
# #         ]
# #     else:
# #         return [
# #             dbc.Card(dbc.CardBody([
# #                 html.H4("Admin Login", className="card-title"),
# #                 dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
# #                 dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
# #                 dbc.Button("Login", id="admin-login-button", color="primary"),
# #                 dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
# #             ]))
# #         ]
# #
# #
# # @app.callback(
# #     Output('output-passport-photo', 'children'),
# #     Output('output-id-payment', 'children'),
# #     Input('upload-passport-photo', 'filename'),
# #     Input('upload-id-payment', 'filename'),
# #     prevent_initial_call=True
# # )
# # def update_id_upload_output(photo_name, payment_name):
# #     return (
# #         f'✓ {photo_name}' if photo_name else '',
# #         f'✓ {payment_name}' if payment_name else '',
# #     )
# #
# #
# # @app.callback(
# #     Output('renew-output-cert-incorporation', 'children'),
# #     Output('renew-output-business-license', 'children'),
# #     Output('renew-output-brella-search', 'children'),
# #     Output('renew-output-directors-images', 'children'),
# #     Output('renew-output-tax-clearance', 'children'),
# #     Output('renew-output-taffa-cert', 'children'),
# #     Output('renew-output-memo-articles', 'children'),
# #     Output('renew-output-audited-accounts', 'children'),
# #     Input('renew-upload-cert-incorporation', 'filename'),
# #     Input('renew-upload-business-license', 'filename'),
# #     Input('renew-upload-brella-search', 'filename'),
# #     Input('renew-upload-directors-images', 'filename'),
# #     Input('renew-upload-tax-clearance', 'filename'),
# #     Input('renew-upload-taffa-cert', 'filename'),
# #     Input('renew-upload-memo-articles', 'filename'),
# #     Input('renew-upload-audited-accounts', 'filename'),
# #     prevent_initial_call=True
# # )
# # def update_renewal_upload_output(cert_inc, biz_lic, brella, dir_img, tax_cert, taffa_cert, memo, audit):
# #     return (
# #         f'✓ {cert_inc}' if cert_inc else '',
# #         f'✓ {biz_lic}' if biz_lic else '',
# #         f'✓ {brella}' if brella else '',
# #         f'✓ {dir_img}' if dir_img else '',
# #         f'✓ {tax_cert}' if tax_cert else '',
# #         f'✓ {taffa_cert}' if taffa_cert else '',
# #         f'✓ {memo}' if memo else '',
# #         f'✓ {audit}' if audit else '',
# #     )
# #
# #
# # @app.callback(
# #     Output("payment-method-popover", "is_open"),
# #     Output("payment-method-popover", "target"),
# #     Input("pay-button", "n_clicks"),
# #     Input("renew-pay-button", "n_clicks"),
# #     prevent_initial_call=True
# # )
# # def toggle_payment_popover(n_clicks_pay, n_clicks_renew):
# #     if ctx.triggered_id == "pay-button":
# #         return True, "pay-button"
# #     elif ctx.triggered_id == "renew-pay-button":
# #         return True, "renew-pay-button"
# #     return False, ""
# #
# #
# # @app.callback(
# #     Output("payment-success-popover", "is_open"),
# #     Output("payment-success-popover", "target", allow_duplicate=True),
# #     Output("payment-method-popover", "is_open", allow_duplicate=True),
# #     Output("payment-store", "data"),
# #     Output("interval-popover", "disabled"),
# #     Input("pay-equity-btn", "n_clicks"),
# #     Input("pay-nbc-btn", "n_clicks"),
# #     Input("pay-mpesa-btn", "n_clicks"),
# #     State("payment-method-popover", "target"),
# #     prevent_initial_call=True
# # )
# # def handle_payment_confirmation(equity_clicks, nbc_clicks, mpesa_clicks, target_id):
# #     if not any([equity_clicks, nbc_clicks, mpesa_clicks]):
# #         raise PreventUpdate
# #
# #     time.sleep(1)
# #     trx_id = f"CP{random.randint(100000, 999999)}"
# #
# #     return True, target_id, False, {'status': 'Paid', 'trx_id': trx_id}, False
# #
# #
# # @app.callback(
# #     Output("payment-success-popover", "is_open", allow_duplicate=True),
# #     Output("interval-popover", "disabled", allow_duplicate=True),
# #     Input("interval-popover", "n_intervals"),
# #     State("payment-success-popover", "is_open"),
# #     prevent_initial_call=True
# # )
# # def hide_payment_popover(n, is_open):
# #     if is_open:
# #         return False, True
# #     raise PreventUpdate
# #
# #
# # @app.callback(
# #     Output("payment-confirmation", "value"),
# #     Output("pay-button", "disabled"),
# #     Input("payment-store", "data"),
# #     prevent_initial_call=True
# # )
# # def update_payment_status(data):
# #     if data and data.get("status") == "Paid":
# #         return "Paid", True
# #     return "Unpaid", False
# #
# #
# # @app.callback(
# #     Output('submission-output', 'children'),
# #     Input('submit-button', 'n_clicks'),
# #     [State('tin-number', 'value'), State('company-name', 'value'), State('contact-person', 'value'),
# #      State('email', 'value'), State('phone', 'value'), State('physical-address', 'value'),
# #      State('postal-address', 'value'), State('website', 'value'), State('taffa-membership-no', 'value'),
# #      State('director-1', 'value'), State('director-2', 'value'), State('director-3', 'value'),
# #      State('cert-incorporation-no', 'value'), State('business-license-no', 'value'),
# #      State('membership-type', 'value'), State('agree-terms', 'value'),
# #      State('tax-compliance', 'value'), State('taffa-status', 'value'), State('policy-compliance', 'value'),
# #      State('payment-confirmation', 'value')],
# #     prevent_initial_call=True
# # )
# # def submit_membership_application(n_clicks, tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no,
# #                                   director_1, director_2, director_3, cert_inc_no, biz_lic_no, mem_type, agreed,
# #                                   tax, taffa, policy, payment):
# #     required_fields = [tin, company, contact, email, phone, phys_addr, post_addr, director_1, cert_inc_no, biz_lic_no,
# #                        mem_type, agreed]
# #     if not all(required_fields):
# #         return dbc.Alert("Please fill all fields marked with * and upload the required documents.", color="danger")
# #     if not agreed:
# #         return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning")
# #
# #     try:
# #         conn = sqlite3.connect(DB_PATH)
# #         c = conn.cursor()
# #         c.execute("""INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
# #                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
# #                   (tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no, director_1, director_2,
# #                    director_3, cert_inc_no, biz_lic_no, mem_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
# #         agent_id = c.lastrowid
# #
# #         c.execute("""INSERT INTO applications (agent_id, agreed_to_terms, tax_compliance, taffa_status, policy_compliance, payment_confirmation)
# #                      VALUES (?, ?, ?, ?, ?, ?)""",
# #                   (agent_id, 1, tax, taffa, policy, payment))
# #         conn.commit()
# #         return dbc.Alert("Membership application submitted successfully!", color="success")
# #     except sqlite3.IntegrityError:
# #         return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger")
# #     except Exception as e:
# #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# #     finally:
# #         if conn: conn.close()
# #
# #
# # @app.callback(
# #     Output('id-submission-output', 'children'),
# #     Input('submit-id-button', 'n_clicks'),
# #     [State('id-full-name', 'value'), State('id-nida-number', 'value'), State('id-position', 'value'),
# #      State('id-application-tin', 'value'),
# #      State('upload-passport-photo', 'contents'), State('upload-id-payment', 'contents'),
# #      State('upload-passport-photo', 'filename'), State('upload-id-payment', 'filename')],
# #     prevent_initial_call=True
# # )
# # def submit_id_application(n_clicks, full_name, nida_number, position, tin, photo_cont, payment_cont, photo_name,
# #                           payment_name):
# #     required_fields = [full_name, nida_number, position, tin, photo_cont, payment_cont]
# #     if not all(required_fields):
# #         return dbc.Alert("Please fill all fields and upload required documents.", color="danger")
# #
# #     try:
# #         conn = sqlite3.connect(DB_PATH)
# #         conn.row_factory = sqlite3.Row
# #         c = conn.cursor()
# #
# #         c.execute("SELECT id FROM agents WHERE tin_number = ?", (tin,))
# #         agent_id_result = c.fetchone()
# #
# #         if not agent_id_result:
# #             return dbc.Alert(f"No existing TAFFA member found with TIN {tin}.", color="danger")
# #         agent_id = agent_id_result['id']
# #
# #         c.execute("SELECT id FROM applications WHERE agent_id = ? ORDER BY id DESC LIMIT 1", (agent_id,))
# #         application_id_result = c.fetchone()
# #
# #         if not application_id_result:
# #             return dbc.Alert(f"No completed membership application found for TIN {tin}.", color="danger")
# #         application_id = application_id_result['id']
# #
# #         photo_path = save_uploaded_file(photo_cont, photo_name, application_id, 'passport_photo')
# #         payment_path = save_uploaded_file(payment_cont, payment_name, application_id, 'id_payment_proof')
# #
# #         c.execute("""INSERT INTO id_applications (application_id, full_name, nida_number, position, passport_photo, id_payment_proof)
# #                      VALUES (?, ?, ?, ?, ?, ?)""",
# #                   (application_id, full_name, nida_number, position, photo_path, payment_path))
# #         id_app_id = c.lastrowid
# #         conn.commit()
# #
# #         id_app_data = c.execute("SELECT * FROM id_applications WHERE id = ?", (id_app_id,)).fetchone()
# #         agent_data = c.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
# #
# #         filename = generate_id_card(id_app_data, agent_data)
# #         download_link = dcc.Link("Download ID Card", href=f"/download-id/{os.path.basename(filename)}",
# #                                  className="btn btn-primary mt-2")
# #
# #         return [
# #             dbc.Alert("ID card application submitted successfully!", color="success"),
# #             html.Div(download_link, className="mt-2")
# #         ]
# #
# #     except Exception as e:
# #         return dbc.Alert(f"An error occurred: {e}", color="danger")
# #     finally:
# #         if conn: conn.close()
# #
# #
# # @app.callback(
# #     Output('renewal-submission-output', 'children'),
# #     Input('submit-renewal-button', 'n_clicks'),
# #     [State('renew-tin-number', 'value'), State('renew-taffa-no', 'value'),
# #      State('renew-tax-compliance', 'value'), State('renew-taffa-status', 'value'),
# #      State('renew-policy-compliance', 'value'), State('renew-payment-confirmation', 'value'),
# #      State('renew-upload-cert-incorporation', 'contents'), State('renew-upload-business-license', 'contents'),
# #      State('renew-upload-brella-search', 'contents'), State('renew-upload-directors-images', 'contents'),
# #      State('renew-upload-tax-clearance', 'contents'), State('renew-upload-taffa-cert', 'contents'),
# #      State('renew-upload-memo-articles', 'contents'), State('renew-upload-audited-accounts', 'contents'),
# #      State('renew-upload-cert-incorporation', 'filename'), State('renew-upload-business-license', 'filename'),
# #      State('renew-upload-brella-search', 'filename'), State('renew-upload-directors-images', 'filename'),
# #      State('renew-upload-tax-clearance', 'filename'), State('renew-upload-taffa-cert', 'filename'),
# #      State('renew-upload-memo-articles', 'filename'), State('renew-upload-audited-accounts', 'filename')],
# #     prevent_initial_call=True
# # )
# # def submit_renewal(n_clicks, tin, taffa_no, tax, taffa, policy, payment,
# #                    cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
# #                    memo_cont, audit_cont, cert_inc_name, biz_lic_name, brella_name, dir_img_name, tax_cert_name,
# #                    taffa_cert_name, memo_name, audit_name):
# #     required_uploads = [cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
# #                         memo_cont, audit_cont]
# #     if not all(required_uploads):
# #         return dbc.Alert("Please upload all required documents for renewal.", color="danger")
# #
# #     return [
# #         dbc.Toast(
# #             "Member license renewed!",
# #             header="Renewal Status",
# #             icon="success",
# #             dismissable=True,
# #             is_open=True,
# #             style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# #         )
# #     ]
# #
# #
# # @app.callback(
# #     Output('applications-table', 'data'),
# #     [Input('refresh-button', 'n_clicks'), Input('submission-output', 'children')]
# # )
# # def update_table(n_clicks, submission_output):
# #     conn = sqlite3.connect(DB_PATH)
# #     query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
# #     df = pd.read_sql_query(query, conn)
# #     conn.close()
# #     return df.to_dict('records')
# #
# #
# # @app.callback(
# #     Output('admin-table', 'data'),
# #     Input('admin-refresh-button', 'n_clicks'),
# #     prevent_initial_call=True
# # )
# # def update_admin_table(n_clicks):
# #     conn = sqlite3.connect(DB_PATH)
# #     query = "SELECT p.id, a.tin_number, a.company_name, p.status FROM agents a JOIN applications p ON a.id = p.agent_id"
# #     df = pd.read_sql_query(query, conn)
# #     conn.close()
# #     return df.to_dict('records')
# #
# #
# # @app.callback(
# #     Output('admin-details-view', 'children'),
# #     Input('admin-table', 'selected_rows'),
# #     State('admin-table', 'data'),
# #     prevent_initial_call=True
# # )
# # def display_admin_details(selected_rows, table_data):
# #     if not selected_rows:
# #         return []
# #
# #     app_id = table_data[selected_rows[0]]['id']
# #     conn = sqlite3.connect(DB_PATH)
# #     conn.row_factory = sqlite3.Row
# #     c = conn.cursor()
# #     c.execute("""
# #         SELECT * FROM agents a
# #         JOIN applications p ON a.id = p.agent_id
# #         WHERE p.id = ?
# #     """, (app_id,))
# #     data = c.fetchone()
# #
# #     id_applications_query = """
# #         SELECT id, full_name, passport_photo, id_payment_proof, id_status FROM id_applications
# #         WHERE application_id = ?
# #     """
# #     id_applications = pd.read_sql_query(id_applications_query, conn, params=(app_id,))
# #     conn.close()
# #
# #     if not data:
# #         return dbc.Alert("Could not retrieve application details.", color="danger")
# #
# #     status_color = {
# #         "Verified": "success",
# #         "Cancelled": "danger",
# #         "Pending": "warning"
# #     }.get(data['status'], "secondary")
# #
# #     document_links = []
# #     document_fields = {
# #         "Certificate of Incorporation": "cert_incorporation",
# #         "Business License": "business_license",
# #         "Brella Search": "brella_search",
# #         "Directors Images": "director_images",
# #         "Tax Clearance Cert": "tax_clearance_cert",
# #         "TAFFA Certificate": "taffa_cert",
# #         "Memo & Articles": "memo_articles",
# #         "Audited Accounts": "audited_accounts",
# #     }
# #
# #     for doc_name, field in document_fields.items():
# #         if data[field]:
# #             filename = os.path.basename(data[field])
# #             download_link = dcc.Link(
# #                 f"Download {doc_name}",
# #                 href=f"/download-file/{data['agent_id']}/{filename}",
# #                 className="d-block"
# #             )
# #             document_links.append(download_link)
# #
# #     details_layout = [
# #         dbc.Row([
# #             dbc.Col([
# #                 dbc.Card([
# #                     dbc.CardHeader("Company & Contact Information"),
# #                     dbc.CardBody([
# #                         html.P([html.Strong("Company Name: "), data['company_name']]),
# #                         html.P([html.Strong("TIN Number: "), data['tin_number']]),
# #                         html.P([html.Strong("Physical Address: "), data['physical_address']]),
# #                         html.P([html.Strong("Contact Person: "), data['contact_person']]),
# #                         html.P([html.Strong("Email: "), data['email']]),
# #                         html.P([html.Strong("Phone: "), data['phone']]),
# #                     ])
# #                 ]),
# #                 dbc.Card([
# #                     dbc.CardHeader("Director Information"),
# #                     dbc.CardBody([
# #                         html.P([html.Strong("Director 1: "), data['director_1']]),
# #                         html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"]),
# #                         html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"]),
# #                     ])
# #                 ], className="mt-3"),
# #             ], width=6),
# #             dbc.Col([
# #                 dbc.Card([
# #                     dbc.CardHeader("Compliance & Verification"),
# #                     dbc.CardBody([
# #                         html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"]),
# #                         html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"]),
# #                         html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"]),
# #                         html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']]),
# #                         html.P([html.Strong("Current Status: "),
# #                                 html.Strong(data['status'], className=f"text-{status_color}")])
# #                     ])
# #                 ]),
# #                 dbc.Card([
# #                     dbc.CardHeader("Uploaded Documents (Membership)"),
# #                     dbc.CardBody(document_links)
# #                 ], className="mt-3"),
# #                 dbc.Card([
# #                     dbc.CardHeader("Actions (Membership)"),
# #                     dbc.CardBody([
# #                         html.H5("Update Status for Selected Application"),
# #                         dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
# #                                                                           {'label': 'Cancelled', 'value': 'Cancelled'}],
# #                                      placeholder="Select new status"),
# #                         dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2"),
# #                         dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
# #                                    className="mt-2 ms-2", disabled=data['status'] != 'Verified'),
# #                         html.Div(id="download-cert-link-div", className="mt-2"),
# #                         html.Div(id='admin-update-output', className="mt-3")
# #                     ])
# #                 ], className="mt-3"),
# #             ], width=6),
# #         ], className="mt-4")
# #     ]
# #
# #     id_card_links = []
# #     if not id_applications.empty:
# #         id_card_details = [html.Hr(), html.H5("ID Card Applications", className="card-title")]
# #         for index, row in id_applications.iterrows():
# #             id_app_id = row['id']
# #             id_card_details.append(html.P(html.Strong(f"ID for: {row['full_name']}")))
# #             id_card_details.append(dcc.Link("Download Passport Photo",
# #                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['passport_photo'])}",
# #                                             className="d-block"))
# #             id_card_details.append(dcc.Link("Download ID Payment Proof",
# #                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['id_payment_proof'])}",
# #                                             className="d-block"))
# #             id_card_details.append(html.P([html.Strong("ID Status: "), row['id_status']]))
# #
# #             if row['id_status'] == 'Verified':
# #                 id_card_details.append(
# #                     dcc.Link("Download ID Card", href=f"/download-id/{id_app_id}", download="", target="_blank",
# #                              className="btn btn-primary mt-2"))
# #             else:
# #                 id_card_details.append(
# #                     dbc.Button("Verify ID Application", id={"type": "verify-id-button", "index": str(id_app_id)},
# #                                color="success", className="mt-2"))
# #             id_card_details.append(html.Hr())
# #         id_card_links = id_card_details
# #     else:
# #         id_card_links = html.Div([html.P("No ID Application submitted for this company.")])
# #
# #     details_layout.append(
# #         dbc.Row([
# #             dbc.Col(
# #                 dbc.Card([
# #                     dbc.CardHeader("ID Application Documents"),
# #                     dbc.CardBody(id_card_links)
# #                 ], className="mt-3"),
# #                 width=12
# #             )
# #         ])
# #     )
# #     return details_layout
# #
# #
# # @app.callback(
# #     Output('admin-update-output', 'children'),
# #     Input('admin-update-button', 'n_clicks'),
# #     [State('admin-table', 'selected_rows'), State('admin-table', 'data'), State('admin-status-dropdown', 'value')],
# #     prevent_initial_call=True
# # )
# # def update_status(n_clicks, selected_rows, table_data, new_status):
# #     if not selected_rows or not new_status:
# #         raise PreventUpdate
# #
# #     app_id = table_data[selected_rows[0]]['id']
# #     ref_number = f"TAFFA-TRA-{random.randint(10000, 99999)}{'PASS' if new_status == 'Verified' else 'FAIL'}"
# #
# #     try:
# #         conn = sqlite3.connect(DB_PATH)
# #         c = conn.cursor()
# #         c.execute("UPDATE applications SET status = ?, reference_number = ? WHERE id = ?",
# #                   (new_status, ref_number, app_id))
# #         conn.commit()
# #
# #         c.execute("SELECT a.email FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?", (app_id,))
# #         agent_email = c.fetchone()[0]
# #
# #         email_body = (
# #             f"Dear Applicant,\n\n"
# #             f"The status of your TAFFA membership application has been updated to: {new_status}.\n\n"
# #             f"Reference Number: {ref_number}\n\n"
# #             f"Thank you,\nTAFFA Administration"
# #         )
# #
# #         email_sent = send_email(agent_email, f"TAFFA Application Update: {new_status}", email_body)
# #
# #         if email_sent:
# #             return [
# #                 dbc.Alert(f"Application {app_id} updated to '{new_status}'. A notification has been sent.",
# #                           color="success"),
# #                 dbc.Toast(
# #                     "Email notification sent successfully!",
# #                     header="Email Status",
# #                     icon="success",
# #                     dismissable=True,
# #                     is_open=True,
# #                     style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
# #                 )
# #             ]
# #         else:
# #             return dbc.Alert(f"Application {app_id} updated to '{new_status}'. Failed to send email notification.",
# #                              color="warning")
# #
# #     except Exception as e:
# #         return dbc.Alert(f"Error updating status: {e}", color="danger")
# #     finally:
# #         if conn: conn.close()
# #
# #
# # @app.callback(
# #     Output({"type": "verify-id-button", "index": MATCH}, "children"),
# #     Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
# #     State({"type": "verify-id-button", "index": ALL}, "id"),
# #     prevent_initial_call=True
# # )
# # def verify_id_application(n_clicks, button_ids):
# #     if not n_clicks or not any(n_clicks):
# #         raise PreventUpdate
# #
# #     triggered_id_json = ctx.triggered[0]['prop_id']
# #     triggered_id_dict = json.loads(triggered_id_json)
# #     clicked_id = triggered_id_dict['index']
# #
# #     conn = sqlite3.connect(DB_PATH)
# #     conn.row_factory = sqlite3.Row
# #     c = conn.cursor()
# #     id_number = f"TAFFA-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
# #     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
# #
# #     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
# #               ('Verified', id_number, expiry_date, clicked_id))
# #     conn.commit()
# #     conn.close()
# #
# #     return "Verified!"
# #
# #
# # @app.callback(
# #     Output('generate-cert-button', 'disabled'),
# #     Input('admin-table', 'selected_rows'),
# #     Input('admin-update-output', 'children'),
# #     State('admin-table', 'data'),
# #     prevent_initial_call=True
# # )
# # def toggle_generate_button(selected_rows, update_output, table_data):
# #     if not selected_rows:
# #         return True
# #
# #     app_id = table_data[selected_rows[0]]['id']
# #     conn = sqlite3.connect(DB_PATH)
# #     c = conn.cursor()
# #     c.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
# #     status = c.fetchone()[0]
# #     conn.close()
# #
# #     return status != 'Verified'
# #
# #
# # def generate_membership_certificate(app_data):
# #     filename = f"Certificate-{app_data['tin_number']}.pdf"
# #     filepath = os.path.join(CERTIFICATES_DIR, filename)
# #     c = canvas.Canvas(filepath, pagesize=letter)
# #     width, height = letter
# #
# #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# #
# #     if os.path.exists(taffa_logo_path):
# #         c.drawImage(taffa_logo_path, 30, height - 150, width=150, height=150, preserveAspectRatio=True, mask='auto')
# #
# #     c.setFont("Helvetica-Bold", 16)
# #     c.setFillColor(colors.black)
# #     c.drawRightString(width - 50, height - 110, f"No. {random.randint(1000, 9999)}")
# #
# #     c.setFont("Helvetica-Bold", 24)
# #     c.setFillColor(colors.HexColor('#003366'))
# #     c.drawCentredString(width / 2.0, height - 200, "CERTIFICATE OF MEMBERSHIP")
# #
# #     c.setFont("Helvetica", 14)
# #     c.setFillColor(colors.black)
# #     c.drawCentredString(width / 2.0, height - 250, "CERTIFICATE IS AWARDED TO")
# #
# #     c.setFont("Helvetica-Bold", 20)
# #     c.drawCentredString(width / 2.0, height - 280, app_data['company_name'].upper())
# #
# #     c.setFont("Helvetica", 12)
# #     c.drawCentredString(width / 2.0, height - 320,
# #                         f"as a Tanzania Freight Forwarder Association Member for {date.today().year}")
# #
# #     c.save()
# #     return filename
# #
# #
# # def generate_id_card(id_app_data, agent_data):
# #     filename = f"ID-{id_app_data['id_number']}.pdf"
# #     filepath = os.path.join(IDS_DIR, filename)
# #     c = canvas.Canvas(filepath, pagesize=A4)
# #     width, height = A4
# #
# #     # ID card dimensions
# #     card_width = width * 0.75
# #     card_height = height * 0.75
# #
# #     # Calculate margins to center the card on the page
# #     x_offset = (width - card_width) / 2
# #     y_offset = (height - card_height) / 2
# #
# #     # Draw the border
# #     c.setStrokeColor(colors.HexColor('#003366'))
# #     c.setLineWidth(5)
# #     c.roundRect(x_offset, y_offset, card_width, card_height, 10, stroke=1, fill=0)
# #
# #     # Header with TAFFA logo and text
# #     header_height = card_height * 0.2
# #     c.setFillColor(colors.HexColor('#F0F8FF'))
# #     c.rect(x_offset, y_offset + card_height - header_height, card_width, header_height, fill=1, stroke=0)
# #
# #     # TAFFA Logo
# #     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# #     if os.path.exists(taffa_logo_path):
# #         logo_size = header_height * 0.8
# #         logo_x = x_offset + card_width * 0.05
# #         logo_y = y_offset + card_height - header_height + (header_height - logo_size) / 2
# #         c.drawImage(taffa_logo_path, logo_x, logo_y, width=logo_size, height=logo_size, preserveAspectRatio=True)
# #
# #     # Title text
# #     c.setFont("Helvetica-Bold", 14)
# #     c.setFillColor(colors.HexColor('#003366'))
# #     title_x = x_offset + card_width * 0.5
# #     title_y = y_offset + card_height - header_height / 2 + 10
# #     c.drawCentredString(title_x, title_y, "TANZANIA FREIGHT")
# #     c.drawCentredString(title_x, title_y - 20, "FORWARDERS ASSOCIATION")
# #
# #     # Photo - Centered
# #     photo_path = id_app_data['passport_photo']
# #     photo_size = card_width * 0.3
# #     photo_x = x_offset + (card_width - photo_size) / 2
# #     photo_y = y_offset + card_height - header_height - 10 - photo_size
# #     if os.path.exists(photo_path):
# #         c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True)
# #
# #     # Personal Details - Centered underneath the photo
# #     c.setFont("Helvetica-Bold", 12)
# #     c.setFillColor(colors.black)
# #     details_y = photo_y - 30
# #     content_center_x = x_offset + card_width / 2
# #
# #     c.drawCentredString(content_center_x, details_y, f"Name: {id_app_data['full_name']}")
# #     c.drawCentredString(content_center_x, details_y - 20, f"Position: {id_app_data['position']}")
# #     c.drawCentredString(content_center_x, details_y - 40, f"Company: {agent_data['company_name']}")
# #
# #     # ID details
# #     c.setFont("Helvetica-Bold", 12)
# #     c.setFillColor(colors.HexColor('#003366'))
# #     id_y_start = details_y - 80
# #     c.drawCentredString(content_center_x, id_y_start, f"ID NO: {id_app_data['id_number']}")
# #     c.drawCentredString(content_center_x, id_y_start - 20, f"Expiry Date: {id_app_data['expiry_date']}")
# #
# #     # QR code - Centered at the bottom
# #     qr_data = f"ID: {id_app_data['id_number']} | Expiry: {id_app_data['expiry_date']}"
# #     qr_img = qrcode.make(qr_data)
# #     qr_buffer = io.BytesIO()
# #     qr_img.save(qr_buffer, format='PNG')
# #     qr_buffer.seek(0)
# #
# #     qr_size = card_width * 0.25
# #     qr_x = content_center_x - qr_size / 2
# #     qr_y = y_offset + 20
# #     c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)
# #
# #     c.save()
# #     return filename
# #
# #
# # @app.callback(
# #     Output('download-cert-link-div', 'children'),
# #     Input('generate-cert-button', 'n_clicks'),
# #     State('admin-table', 'selected_rows'),
# #     State('admin-table', 'data'),
# #     prevent_initial_call=True
# # )
# # def handle_certificate_generation(n_clicks, selected_rows, table_data):
# #     if not selected_rows:
# #         raise PreventUpdate
# #
# #     app_id = table_data[selected_rows[0]]['id']
# #
# #     conn = sqlite3.connect(DB_PATH)
# #     query = """
# #         SELECT a.tin_number, a.company_name, p.reference_number, p.status
# #         FROM agents a JOIN applications p ON a.id = p.agent_id
# #         WHERE p.id = ?
# #     """
# #     df = pd.read_sql_query(query, conn, params=(app_id,))
# #     conn.close()
# #
# #     if df.empty:
# #         return dbc.Alert("Could not find application data.", color="danger")
# #
# #     app_data = df.to_dict('records')[0]
# #     filename = generate_membership_certificate(app_data)
# #
# #     return dcc.Link(f"Download Certificate for {app_data['company_name']}",
# #                     href=f"/download-cert/{os.path.basename(filename)}")
# #
# #
# # @app.callback(
# #     Output({"type": "download-id-link", "index": MATCH}, "children"),
# #     Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
# #     State({"type": "verify-id-button", "index": ALL}, "id"),
# #     prevent_initial_call=True
# # )
# # def verify_id_application(n_clicks, button_ids):
# #     if not n_clicks or not any(n_clicks):
# #         raise PreventUpdate
# #
# #     triggered_id_json = ctx.triggered[0]['prop_id']
# #     triggered_id_dict = json.loads(triggered_id_json)
# #     clicked_id = triggered_id_dict['index']
# #
# #     conn = sqlite3.connect(DB_PATH)
# #     conn.row_factory = sqlite3.Row
# #     c = conn.cursor()
# #     id_number = f"TAFFA-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
# #     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
# #
# #     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
# #               ('Verified', id_number, expiry_date, clicked_id))
# #     conn.commit()
# #     conn.close()
# #
# #     return "Verified!"
# #
# #
# # @server.route('/download-cert/<filename>')
# # def serve_pdf(filename):
# #     return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)
# #
# #
# # @server.route('/download-id/<filename>')
# # def serve_id(filename):
# #     return send_from_directory(IDS_DIR, filename, as_attachment=True)
# #
# #
# # @server.route('/download-file/<app_id>/<filename>')
# # def download_uploaded_file(app_id, filename):
# #     app_folder = os.path.join(DOCUMENTS_DIR, app_id)
# #     return send_from_directory(app_folder, filename, as_attachment=True)
# #
# #
# # if __name__ == '__main__':
# #     if not os.path.exists(DOCUMENTS_DIR):
# #         os.makedirs(DOCUMENTS_DIR)
# #     if not os.path.exists(CERTIFICATES_DIR):
# #         os.makedirs(CERTIFICATES_DIR)
# #     if not os.path.exists(IDS_DIR):
# #         os.makedirs(IDS_DIR)
# #
# #     assets_dir = os.path.join(BASE_DIR, 'assets')
# #     if not os.path.exists(assets_dir):
# #         os.makedirs(assets_dir)
# #
# #     app.run(debug=True, port=5678)
#
#
# import dash
# from dash import dcc, html, Input, Output, State, ctx, dash_table
# import dash_bootstrap_components as dbc
# from dash.exceptions import PreventUpdate
# import sqlite3
# import pandas as pd
# from datetime import datetime, date, timedelta
# import base64
# import io
# from reportlab.lib.pagesizes import letter, A4
# from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader
# from reportlab.lib import colors
# import os
# import random
# import time
# import smtplib
# from email.message import EmailMessage
# import socket
# from flask import send_from_directory, abort
# import qrcode
# import hashlib
# from dash.dependencies import MATCH, ALL
# import json
#
# # Initialize the Dash app with Flask server and suppress callback exceptions
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], suppress_callback_exceptions=True,
#                 title="TAFFA Portal")
# server = app.server
#
# # --- Admin Credentials ---
# ADMIN_USER = "admin"
# ADMIN_PASS_HASH = hashlib.sha256("password".encode('utf-8')).hexdigest()
#
# # --- Database Setup with Absolute Path ---
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "tra_cfa_data.db")
# DOCUMENTS_DIR = os.path.join(BASE_DIR, "uploaded_documents")
# CERTIFICATES_DIR = os.path.join(BASE_DIR, "certificates")
# IDS_DIR = os.path.join(BASE_DIR, "id_cards")
#
#
# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#
#     # Drop tables to ensure a clean slate and prevent schema errors on re-runs
#     c.execute('DROP TABLE IF EXISTS id_applications')
#     c.execute('DROP TABLE IF EXISTS applications')
#     c.execute('DROP TABLE IF EXISTS agents')
#     c.execute('DROP TABLE IF EXISTS taffa_id_applications')
#     c.execute('DROP TABLE IF EXISTS shipments')
#     c.execute('DROP TABLE IF EXISTS cargo')
#     c.execute('DROP TABLE IF EXISTS invoices')
#     c.execute('DROP TABLE IF EXISTS payments')
#     c.execute('DROP TABLE IF EXISTS analytics_reports')
#
#     # agents table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS agents (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             tin_number TEXT NOT NULL UNIQUE,
#             company_name TEXT NOT NULL,
#             contact_person TEXT NOT NULL,
#             email TEXT NOT NULL,
#             phone TEXT NOT NULL,
#             physical_address TEXT,
#             postal_address TEXT,
#             website TEXT,
#             taffa_membership_no TEXT,
#             director_1 TEXT,
#             director_2 TEXT,
#             director_3 TEXT,
#             cert_incorporation_no TEXT,
#             business_license_no TEXT,
#             membership_type TEXT,
#             submission_date TEXT NOT NULL
#         )
#     ''')
#     # applications table
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS applications (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             agent_id INTEGER,
#             tax_compliance TEXT,
#             taffa_status TEXT,
#             policy_compliance TEXT,
#             payment_confirmation TEXT,
#             business_license TEXT,
#             tax_clearance_cert TEXT,
#             taffa_cert TEXT,
#             cert_incorporation TEXT,
#             memo_articles TEXT,
#             audited_accounts TEXT,
#             director_images TEXT,
#             brella_search TEXT,
#             agreed_to_terms INTEGER,
#             status TEXT DEFAULT 'Pending',
#             reference_number TEXT,
#             FOREIGN KEY (agent_id) REFERENCES agents (id)
#         )
#     ''')
#     # New table for ID applications
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS id_applications (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             application_id INTEGER,
#             full_name TEXT,
#             nida_number TEXT,
#             position TEXT,
#             passport_photo TEXT,
#             id_payment_proof TEXT,
#             id_status TEXT DEFAULT 'Pending',
#             id_number TEXT,
#             expiry_date TEXT,
#             FOREIGN KEY (application_id) REFERENCES applications (id)
#         )
#     ''')
#
#     # New tables for the Admin Dashboard features
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS shipments (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             agent_id INTEGER,
#             tracking_number TEXT,
#             status TEXT,
#             FOREIGN KEY (agent_id) REFERENCES agents (id)
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS cargo (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             shipment_id INTEGER,
#             description TEXT,
#             quantity INTEGER,
#             FOREIGN KEY (shipment_id) REFERENCES shipments (id)
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS invoices (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             agent_id INTEGER,
#             invoice_number TEXT,
#             amount REAL,
#             status TEXT,
#             FOREIGN KEY (agent_id) REFERENCES agents (id)
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS payments (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             agent_id INTEGER,
#             payment_type TEXT,
#             amount REAL,
#             status TEXT,
#             FOREIGN KEY (agent_id) REFERENCES agents (id)
#         )
#     ''')
#
#     conn.commit()
#     conn.close()
#
#
# init_db()
#
# # --- Logo Paths ---
# taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
# taffa_logo_src = "/assets/LOGO.png"
#
#
# # --- Reusable Components ---
# def logo_header(logo_src, text):
#     return dbc.Row([
#         dbc.Col(html.Img(src=logo_src, height="80px"), width="auto"),
#         dbc.Col(html.H5(text, className="align-self-center"))
#     ], className="mb-4 align-items-center justify-content-center")
#
#
# def send_email(recipient_email: str, subject: str, body: str):
#     """Sends an email notification."""
#     sender_email = "administrator@capitalpayinternational.com"
#     sender_password = "ahxr wusz rqvp jpsx"
#     smtp_server = "smtp.gmail.com"
#     smtp_port = 587
#
#     if not sender_password:
#         print("Error: Email password is not set.")
#         return False
#
#     msg = EmailMessage()
#     msg['Subject'] = f"Update: Milestone Reached - {subject}"
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg.set_content(body)
#
#     try:
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.send_message(msg)
#             print(f"Email notification sent successfully to {recipient_email}!")
#             return True
#     except socket.gaierror as e:
#         print(f"Network error: {e}. Could not find host: '{smtp_server}'.")
#         return False
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return False
#
#
# # --- App Layout ---
# app.layout = dbc.Container([
#     dcc.Store(id='payment-store'),
#     dcc.Store(id='login-state', data={'is_authenticated': False}),
#     dbc.Row([
#         dbc.Col(html.Img(src="/assets/LOGO.png", height="100px"), width="auto"),
#         dbc.Col(html.H1("Customs Agent Accreditation Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
#                 width="auto")
#     ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),
#
#     dbc.Tabs(id='tabs', children=[
#         dbc.Tab(label="New Application", children=[
#             dbc.Card(dbc.CardBody([
#                 html.H4("Membership Application Form", className="card-title text-primary"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text'), width=6),
#                     dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text'), width=6),
#                 ], className="mb-3"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text'),
#                             width=6),
#                     dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text'), width=6),
#                 ], className="mb-3"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='website', placeholder='Website', type='text'), width=6),
#                     dbc.Col(dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
#                                       type='text'), width=6),
#                 ], className="mb-3"),
#                 html.Hr(),
#                 html.H4("Contact Person", className="card-title text-primary mt-3"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='contact-person', placeholder='Contact Person Name *', type='text'), width=4),
#                     dbc.Col(dbc.Input(id='email', placeholder='Email Address *', type='email'), width=4),
#                     dbc.Col(dbc.Input(id='phone', placeholder='Mobile Number *', type='text'), width=4),
#                 ], className="mb-3"),
#                 html.Hr(),
#                 html.H4("Directors", className="card-title text-primary mt-3"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text'), width=4),
#                     dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text'), width=4),
#                     dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text'), width=4),
#                 ], className="mb-3"),
#                 html.Hr(),
#                 html.H4("Company Details", className="card-title text-primary mt-3"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
#                                       type='text'), width=6),
#                     dbc.Col(dbc.Input(id='business-license-no', placeholder='Business License No. *', type='text'),
#                             width=6),
#                 ], className="mb-3"),
#                 dcc.Dropdown(id='membership-type', options=[
#                     {'label': 'Ordinary Member', 'value': 'Ordinary'},
#                     {'label': 'Inhouse Member', 'value': 'Inhouse'}
#                 ], placeholder="Choose Membership Type *", className="mb-3"),
#                 html.Hr(),
#                 html.H4("Compliance Details (For Verification)", className="card-title text-primary mt-3"),
#                 dbc.Row([
#                     dbc.Col(dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
#                                                                        {'label': 'Non-Compliant',
#                                                                         'value': 'Non-Compliant'}],
#                                          placeholder="Tax Compliance Status"), width=6),
#                     dbc.Col(dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
#                                                                      {'label': 'Inactive/Expired',
#                                                                       'value': 'Inactive'}],
#                                          placeholder="TAFFA Membership Status"), width=6),
#                 ], className="mb-3"),
#                 dbc.Row([
#                     dbc.Col(dcc.Dropdown(id='policy-compliance',
#                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
#                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
#                                          placeholder="Policy Compliance Status"), width=6),
#                     dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
#                                                                              {'label': 'Unpaid', 'value': 'Unpaid'}],
#                                          placeholder="Accreditation Fee Payment", value="Unpaid"), width=4),
#                     dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success"), width=2)
#                 ], className="mb-3 align-items-center"),
#                 html.Hr(),
#                 dcc.Checklist(options=[
#                     {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations', 'value': 1}],
#                     id='agree-terms', className="mt-4"),
#                 html.Div(dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
#                                     className="mt-4"), className="text-center"),
#                 html.Div(id='submission-output', className="mt-4")
#             ]))
#         ]),
#         dbc.Tab(label="TAFFA ID Application", children=[
#             dbc.Card(dbc.CardBody([
#                 html.H4("TAFFA ID Application", className="card-title text-primary"),
#                 html.P("This form is for TAFFA members to apply for an ID card."),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='id-full-name', placeholder='Full Name *', type='text'), width=6),
#                     dbc.Col(dbc.Input(id='id-nida-number', placeholder='NIDA Number *', type='text'), width=6),
#                 ], className="mb-3"),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='id-position', placeholder='Position *', type='text'), width=6),
#                     dbc.Col([dcc.Upload(id='upload-passport-photo', children=html.Button('Upload Passport Photo *'),
#                                         className="w-100 mb-2"), html.Span(id='output-passport-photo')]),
#                 ], className="mb-3"),
#                 dbc.Row([
#                     dbc.Col([dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof *'),
#                                         className="w-100 mb-2"), html.Span(id='output-id-payment')]),
#                 ], className="mb-3"),
#                 dbc.Input(id='id-application-tin', placeholder='Your Company TIN *', type='text', className="mb-3"),
#                 dbc.Button('Submit ID Application', id='submit-id-button', n_clicks=0, color="primary", size="lg",
#                            className="mt-4"),
#                 html.Div(id='id-submission-output', className="mt-4")
#             ]))
#         ]),
#         dbc.Tab(label="Renew Membership", children=[
#             dbc.Card(dbc.CardBody([
#                 html.H4("Renew Membership", className="card-title text-primary"),
#                 html.P("Use this form to renew your annual membership and update company details."),
#                 dbc.Row([
#                     dbc.Col(dbc.Input(id='renew-tin-number', placeholder='Your Company TIN *', type='text'), width=6),
#                     dbc.Col(dbc.Input(id='renew-taffa-no', placeholder='Your TAFFA Membership No. *', type='text'),
#                             width=6),
#                 ], className="mb-3"),
#                 html.Hr(),
#                 html.H4("Compliance Details (For Renewal Verification)", className="card-title text-primary mt-3"),
#                 dbc.Row([
#                     dbc.Col(dcc.Dropdown(id='renew-tax-compliance',
#                                          options=[{'label': 'Compliant', 'value': 'Compliant'},
#                                                   {'label': 'Non-Compliant', 'value': 'Non-Compliant'}],
#                                          placeholder="Tax Compliance Status"), width=6),
#                     dbc.Col(dcc.Dropdown(id='renew-taffa-status',
#                                          options=[{'label': 'Active Member', 'value': 'Active'},
#                                                   {'label': 'Inactive/Expired', 'value': 'Inactive'}],
#                                          placeholder="TAFFA Membership Status"), width=6),
#                 ], className="mb-3"),
#                 dbc.Row([
#                     dbc.Col(dcc.Dropdown(id='renew-policy-compliance',
#                                          options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
#                                                   {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
#                                          placeholder="Policy Compliance Status"), width=6),
#                     dbc.Col(dcc.Dropdown(id='renew-payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
#                                                                                    {'label': 'Unpaid',
#                                                                                     'value': 'Unpaid'}],
#                                          placeholder="Renewal Fee Payment", value="Unpaid"), width=4),
#                     dbc.Col(dbc.Button("Pay Renewal Fee", id="renew-pay-button", color="success"), width=2)
#                 ], className="mb-3 align-items-center"),
#                 html.Hr(),
#                 html.H4("Document Upload (Renewal)", className="card-title text-primary mt-4"),
#                 dbc.Row([
#                     dbc.Col([dcc.Upload(id='renew-upload-cert-incorporation',
#                                         children=html.Button('Cert of Incorporation *'), className="w-100 mb-2"),
#                              html.Span(id='renew-output-cert-incorporation')]),
#                     dbc.Col([dcc.Upload(id='renew-upload-business-license', children=html.Button('Business License *'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-business-license')]),
#                     dbc.Col([dcc.Upload(id='renew-upload-brella-search', children=html.Button('Brella Search *'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-brella-search')]),
#                     dbc.Col([dcc.Upload(id='renew-upload-directors-images', children=html.Button('Directors Images *'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-directors-images')]),
#                 ]),
#                 dbc.Row([
#                     dbc.Col([dcc.Upload(id='renew-upload-tax-clearance', children=html.Button('Tax Clearance Cert'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-tax-clearance')]),
#                     dbc.Col([dcc.Upload(id='renew-upload-taffa-cert', children=html.Button('TAFFA Certificate'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-taffa-cert')]),
#                     dbc.Col([dcc.Upload(id='renew-upload-memo-articles', children=html.Button('Memo & Articles'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-memo-articles')]),
#                     dbc.Col([dcc.Upload(id='renew-upload-audited-accounts', children=html.Button('Audited Accounts'),
#                                         className="w-100 mb-2"), html.Span(id='renew-output-audited-accounts')]),
#                 ]),
#                 html.Div(
#                     dbc.Button('Submit Renewal', id='submit-renewal-button', n_clicks=0, color="primary", size="lg",
#                                className="mt-4"), className="text-center"),
#                 html.Div(id='renewal-submission-output', className="mt-4")
#             ]))
#         ]),
#         dbc.Tab(label="View Submissions", children=[
#             dbc.Card(dbc.CardBody([
#                 html.H4("Submitted Applications", className="card-title"),
#                 dash_table.DataTable(
#                     id='applications-table',
#                     columns=[
#                         {"name": "TIN", "id": "tin_number"},
#                         {"name": "Company Name", "id": "company_name"},
#                         {"name": "Submission Date", "id": "submission_date"},
#                         {"name": "Status", "id": "status"},
#                         {"name": "Reference Number", "id": "reference_number"},
#                     ],
#                     style_cell={'textAlign': 'left'},
#                 ),
#                 dbc.Button("Refresh Data", id="refresh-button", className="mt-3")
#             ]))
#         ]),
#         dbc.Tab(label="Admin Verification", id='admin-tab-content')
#     ]),
#     dbc.Popover(
#         [
#             dbc.PopoverHeader("Capital Pay Engine"),
#             dbc.PopoverBody(
#                 html.Div([
#                     dbc.Button("Pay with Equity Bank", id="pay-equity-btn", color="primary", className="d-block mb-2"),
#                     dbc.Button("Pay with NBC Bank", id="pay-nbc-btn", color="primary", className="d-block mb-2"),
#                     dbc.Button("Pay with M-Pesa", id="pay-mpesa-btn", color="primary", className="d-block")
#                 ])
#             ),
#         ],
#         id="payment-method-popover",
#         target="",
#         trigger="manual",
#     ),
#     dbc.Popover(
#         dbc.PopoverBody("Payment of 20,000 TZS successful!", className="text-success"),
#         id="payment-success-popover",
#         target="",
#         trigger="manual",
#     ),
#     dcc.Interval(
#         id='interval-popover',
#         interval=5 * 1000,
#         n_intervals=0,
#         disabled=True,
#     ),
# ], fluid=True)
#
#
# def save_uploaded_file(contents, filename, app_id, field_name):
#     if not contents:
#         return None
#
#     file_data = base64.b64decode(contents.split(',')[1])
#     app_folder = os.path.join(DOCUMENTS_DIR, str(app_id))
#     os.makedirs(app_folder, exist_ok=True)
#     unique_filename = f"{field_name}_{filename}"
#     file_path = os.path.join(app_folder, unique_filename)
#
#     with open(file_path, 'wb') as f:
#         f.write(file_data)
#
#     return file_path
#
#
# @app.callback(
#     Output('login-state', 'data'),
#     Output('admin-login-alert', 'children'),
#     Output('admin-login-alert', 'is_open'),
#     Input('admin-login-button', 'n_clicks'),
#     State('admin-username', 'value'),
#     State('admin-password', 'value'),
#     prevent_initial_call=True
# )
# def check_login(n_clicks, username, password):
#     if not n_clicks:
#         raise PreventUpdate
#
#     if username == ADMIN_USER and hashlib.sha256(password.encode('utf-8')).hexdigest() == ADMIN_PASS_HASH:
#         return {'is_authenticated': True}, "", False
#     else:
#         return {'is_authenticated': False}, "Invalid username or password.", True
#
#
# @app.callback(
#     Output('admin-tab-content', 'children'),
#     Input('login-state', 'data')
# )
# def render_admin_tab_content(data):
#     if data['is_authenticated']:
#         return [
#             dbc.Card(dbc.CardBody([
#                 html.H4("Admin Dashboard", className="card-title text-primary"),
#                 dbc.Tabs([
#                     dbc.Tab(label="Overview", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Key Performance Indicators (KPIs)", className="card-title"),
#                             html.P("High-level summary of agents' metrics."),
#                             # Add more KPIs and visualizations here
#                         ])),
#                     ]),
#                     dbc.Tab(label="Operations", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Shipments & Cargo Management", className="card-title"),
#                             html.P("Manage and track shipments and cargo items."),
#                             # Add shipment and cargo tables and forms here
#                         ])),
#                     ]),
#                     dbc.Tab(label="Financials", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Invoicing & Payments", className="card-title"),
#                             html.P("Generate and track invoices and payments."),
#                             # Add invoicing and payment modules here
#                         ])),
#                     ]),
#                     dbc.Tab(label="Reporting", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Reports & Analytics", className="card-title"),
#                             html.P("Generate and export detailed reports."),
#                             # Add report generation forms and charts here
#                         ])),
#                     ]),
#                     dbc.Tab(label="Verification", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H4("Verify Applications", className="card-title"),
#                             dash_table.DataTable(
#                                 id='admin-table',
#                                 columns=[
#                                     {"name": "App ID", "id": "id"},
#                                     {"name": "TIN", "id": "tin_number"},
#                                     {"name": "Company Name", "id": "company_name"},
#                                     {"name": "Status", "id": "status"},
#                                 ],
#                                 style_cell={'textAlign': 'left'},
#                                 row_selectable='single',
#                             ),
#                             dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3"),
#                             html.Hr(),
#                             html.Div(id='admin-details-view')
#                         ]))
#                     ])
#                 ])
#             ]))
#         ]
#     else:
#         return [
#             dbc.Card(dbc.CardBody([
#                 html.H4("Admin Login", className="card-title"),
#                 dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
#                 dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
#                 dbc.Button("Login", id="admin-login-button", color="primary"),
#                 dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
#             ]))
#         ]
#
#
# @app.callback(
#     Output('output-passport-photo', 'children'),
#     Output('output-id-payment', 'children'),
#     Input('upload-passport-photo', 'filename'),
#     Input('upload-id-payment', 'filename'),
#     prevent_initial_call=True
# )
# def update_id_upload_output(photo_name, payment_name):
#     return (
#         f'✓ {photo_name}' if photo_name else '',
#         f'✓ {payment_name}' if payment_name else '',
#     )
#
#
# @app.callback(
#     Output('renew-output-cert-incorporation', 'children'),
#     Output('renew-output-business-license', 'children'),
#     Output('renew-output-brella-search', 'children'),
#     Output('renew-output-directors-images', 'children'),
#     Output('renew-output-tax-clearance', 'children'),
#     Output('renew-output-taffa-cert', 'children'),
#     Output('renew-output-memo-articles', 'children'),
#     Output('renew-output-audited-accounts', 'children'),
#     Input('renew-upload-cert-incorporation', 'filename'),
#     Input('renew-upload-business-license', 'filename'),
#     Input('renew-upload-brella-search', 'filename'),
#     Input('renew-upload-directors-images', 'filename'),
#     Input('renew-upload-tax-clearance', 'filename'),
#     Input('renew-upload-taffa-cert', 'filename'),
#     Input('renew-upload-memo-articles', 'filename'),
#     Input('renew-upload-audited-accounts', 'filename'),
#     prevent_initial_call=True
# )
# def update_renewal_upload_output(cert_inc, biz_lic, brella, dir_img, tax_cert, taffa_cert, memo, audit):
#     return (
#         f'✓ {cert_inc}' if cert_inc else '',
#         f'✓ {biz_lic}' if biz_lic else '',
#         f'✓ {brella}' if brella else '',
#         f'✓ {dir_img}' if dir_img else '',
#         f'✓ {tax_cert}' if tax_cert else '',
#         f'✓ {taffa_cert}' if taffa_cert else '',
#         f'✓ {memo}' if memo else '',
#         f'✓ {audit}' if audit else '',
#     )
#
#
# @app.callback(
#     Output("payment-method-popover", "is_open"),
#     Output("payment-method-popover", "target"),
#     Input("pay-button", "n_clicks"),
#     Input("renew-pay-button", "n_clicks"),
#     prevent_initial_call=True
# )
# def toggle_payment_popover(n_clicks_pay, n_clicks_renew):
#     if ctx.triggered_id == "pay-button":
#         return True, "pay-button"
#     elif ctx.triggered_id == "renew-pay-button":
#         return True, "renew-pay-button"
#     return False, ""
#
#
# @app.callback(
#     Output("payment-success-popover", "is_open"),
#     Output("payment-success-popover", "target", allow_duplicate=True),
#     Output("payment-method-popover", "is_open", allow_duplicate=True),
#     Output("payment-store", "data"),
#     Output("interval-popover", "disabled"),
#     Input("pay-equity-btn", "n_clicks"),
#     Input("pay-nbc-btn", "n_clicks"),
#     Input("pay-mpesa-btn", "n_clicks"),
#     State("payment-method-popover", "target"),
#     prevent_initial_call=True
# )
# def handle_payment_confirmation(equity_clicks, nbc_clicks, mpesa_clicks, target_id):
#     if not any([equity_clicks, nbc_clicks, mpesa_clicks]):
#         raise PreventUpdate
#
#     time.sleep(1)
#     trx_id = f"CP{random.randint(100000, 999999)}"
#
#     return True, target_id, False, {'status': 'Paid', 'trx_id': trx_id}, False
#
#
# @app.callback(
#     Output("payment-success-popover", "is_open", allow_duplicate=True),
#     Output("interval-popover", "disabled", allow_duplicate=True),
#     Input("interval-popover", "n_intervals"),
#     State("payment-success-popover", "is_open"),
#     prevent_initial_call=True
# )
# def hide_payment_popover(n, is_open):
#     if is_open:
#         return False, True
#     raise PreventUpdate
#
#
# @app.callback(
#     Output("payment-confirmation", "value"),
#     Output("pay-button", "disabled"),
#     Input("payment-store", "data"),
#     prevent_initial_call=True
# )
# def update_payment_status(data):
#     if data and data.get("status") == "Paid":
#         return "Paid", True
#     return "Unpaid", False
#
#
# @app.callback(
#     Output('submission-output', 'children'),
#     Input('submit-button', 'n_clicks'),
#     [State('tin-number', 'value'), State('company-name', 'value'), State('contact-person', 'value'),
#      State('email', 'value'), State('phone', 'value'), State('physical-address', 'value'),
#      State('postal-address', 'value'), State('website', 'value'), State('taffa-membership-no', 'value'),
#      State('director-1', 'value'), State('director-2', 'value'), State('director-3', 'value'),
#      State('cert-incorporation-no', 'value'), State('business-license-no', 'value'),
#      State('membership-type', 'value'), State('agree-terms', 'value'),
#      State('tax-compliance', 'value'), State('taffa-status', 'value'), State('policy-compliance', 'value'),
#      State('payment-confirmation', 'value')],
#     prevent_initial_call=True
# )
# def submit_membership_application(n_clicks, tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no,
#                                   director_1, director_2, director_3, cert_inc_no, biz_lic_no, mem_type, agreed,
#                                   tax, taffa, policy, payment):
#     required_fields = [tin, company, contact, email, phone, phys_addr, post_addr, director_1, cert_inc_no, biz_lic_no,
#                        mem_type, agreed]
#     if not all(required_fields):
#         return dbc.Alert("Please fill all fields marked with * and upload the required documents.", color="danger")
#     if not agreed:
#         return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning")
#
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         c = conn.cursor()
#         c.execute("""INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, director_2, director_3, cert_incorporation_no, business_license_no, membership_type, submission_date)
#                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
#                   (tin, company, contact, email, phone, phys_addr, post_addr, web, taffa_no, director_1, director_2,
#                    director_3, cert_inc_no, biz_lic_no, mem_type, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#         agent_id = c.lastrowid
#
#         c.execute("""INSERT INTO applications (agent_id, agreed_to_terms, tax_compliance, taffa_status, policy_compliance, payment_confirmation)
#                      VALUES (?, ?, ?, ?, ?, ?)""",
#                   (agent_id, 1, tax, taffa, policy, payment))
#         conn.commit()
#         return dbc.Alert("Membership application submitted successfully!", color="success")
#     except sqlite3.IntegrityError:
#         return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger")
#     except Exception as e:
#         return dbc.Alert(f"An error occurred: {e}", color="danger")
#     finally:
#         if conn: conn.close()
#
#
# @app.callback(
#     Output('id-submission-output', 'children'),
#     Input('submit-id-button', 'n_clicks'),
#     [State('id-full-name', 'value'), State('id-nida-number', 'value'), State('id-position', 'value'),
#      State('id-application-tin', 'value'),
#      State('upload-passport-photo', 'contents'), State('upload-id-payment', 'contents'),
#      State('upload-passport-photo', 'filename'), State('upload-id-payment', 'filename')],
#     prevent_initial_call=True
# )
# def submit_id_application(n_clicks, full_name, nida_number, position, tin, photo_cont, payment_cont, photo_name,
#                           payment_name):
#     required_fields = [full_name, nida_number, position, tin, photo_cont, payment_cont]
#     if not all(required_fields):
#         return dbc.Alert("Please fill all fields and upload required documents.", color="danger")
#
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         conn.row_factory = sqlite3.Row
#         c = conn.cursor()
#
#         c.execute("SELECT id FROM agents WHERE tin_number = ?", (tin,))
#         agent_id_result = c.fetchone()
#
#         if not agent_id_result:
#             return dbc.Alert(f"No existing TAFFA member found with TIN {tin}.", color="danger")
#         agent_id = agent_id_result['id']
#
#         c.execute("SELECT id FROM applications WHERE agent_id = ? ORDER BY id DESC LIMIT 1", (agent_id,))
#         application_id_result = c.fetchone()
#
#         if not application_id_result:
#             return dbc.Alert(f"No completed membership application found for TIN {tin}.", color="danger")
#         application_id = application_id_result['id']
#
#         photo_path = save_uploaded_file(photo_cont, photo_name, application_id, 'passport_photo')
#         payment_path = save_uploaded_file(payment_cont, payment_name, application_id, 'id_payment_proof')
#
#         c.execute("""INSERT INTO id_applications (application_id, full_name, nida_number, position, passport_photo, id_payment_proof)
#                      VALUES (?, ?, ?, ?, ?, ?)""",
#                   (application_id, full_name, nida_number, position, photo_path, payment_path))
#         id_app_id = c.lastrowid
#         conn.commit()
#
#         id_app_data = c.execute("SELECT * FROM id_applications WHERE id = ?", (id_app_id,)).fetchone()
#         agent_data = c.execute("SELECT * FROM agents WHERE id = ?", (agent_id,)).fetchone()
#
#         filename = generate_id_card(id_app_data, agent_data)
#         download_link = dcc.Link("Download ID Card", href=f"/download-id/{os.path.basename(filename)}",
#                                  className="btn btn-primary mt-2")
#
#         return [
#             dbc.Alert("ID card application submitted successfully!", color="success"),
#             html.Div(download_link, className="mt-2")
#         ]
#
#     except Exception as e:
#         return dbc.Alert(f"An error occurred: {e}", color="danger")
#     finally:
#         if conn: conn.close()
#
#
# @app.callback(
#     Output('renewal-submission-output', 'children'),
#     Input('submit-renewal-button', 'n_clicks'),
#     [State('renew-tin-number', 'value'), State('renew-taffa-no', 'value'),
#      State('renew-tax-compliance', 'value'), State('renew-taffa-status', 'value'),
#      State('renew-policy-compliance', 'value'), State('renew-payment-confirmation', 'value'),
#      State('renew-upload-cert-incorporation', 'contents'), State('renew-upload-business-license', 'contents'),
#      State('renew-upload-brella-search', 'contents'), State('renew-upload-directors-images', 'contents'),
#      State('renew-upload-tax-clearance', 'contents'), State('renew-upload-taffa-cert', 'contents'),
#      State('renew-upload-memo-articles', 'contents'), State('renew-upload-audited-accounts', 'contents'),
#      State('renew-upload-cert-incorporation', 'filename'), State('renew-upload-business-license', 'filename'),
#      State('renew-upload-brella-search', 'filename'), State('renew-upload-directors-images', 'filename'),
#      State('renew-upload-tax-clearance', 'filename'), State('renew-upload-taffa-cert', 'filename'),
#      State('renew-upload-memo-articles', 'filename'), State('renew-upload-audited-accounts', 'filename')],
#     prevent_initial_call=True
# )
# def submit_renewal(n_clicks, tin, taffa_no, tax, taffa, policy, payment,
#                    cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
#                    memo_cont, audit_cont, cert_inc_name, biz_lic_name, brella_name, dir_img_name, tax_cert_name,
#                    taffa_cert_name, memo_name, audit_name):
#     required_uploads = [cert_inc_cont, biz_lic_cont, brella_cont, dir_img_cont, tax_cert_cont, taffa_cert_cont,
#                         memo_cont, audit_cont]
#     if not all(required_uploads):
#         return dbc.Alert("Please upload all required documents for renewal.", color="danger")
#
#     return [
#         dbc.Toast(
#             "Member license renewed!",
#             header="Renewal Status",
#             icon="success",
#             dismissable=True,
#             is_open=True,
#             style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
#         )
#     ]
#
#
# @app.callback(
#     Output('applications-table', 'data'),
#     [Input('refresh-button', 'n_clicks'), Input('submission-output', 'children')]
# )
# def update_table(n_clicks, submission_output):
#     conn = sqlite3.connect(DB_PATH)
#     query = "SELECT a.tin_number, a.company_name, a.submission_date, p.status, p.reference_number FROM agents a JOIN applications p ON a.id = p.agent_id"
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df.to_dict('records')
#
#
# @app.callback(
#     Output('admin-table', 'data'),
#     Input('admin-refresh-button', 'n_clicks'),
#     prevent_initial_call=True
# )
# def update_admin_table(n_clicks):
#     conn = sqlite3.connect(DB_PATH)
#     query = "SELECT p.id, a.tin_number, a.company_name, p.status FROM agents a JOIN applications p ON a.id = p.agent_id"
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df.to_dict('records')
#
#
# @app.callback(
#     Output('admin-details-view', 'children'),
#     Input('admin-table', 'selected_rows'),
#     State('admin-table', 'data'),
#     prevent_initial_call=True
# )
# def display_admin_details(selected_rows, table_data):
#     if not selected_rows:
#         return []
#
#     app_id = table_data[selected_rows[0]]['id']
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#     c.execute("""
#         SELECT * FROM agents a
#         JOIN applications p ON a.id = p.agent_id
#         WHERE p.id = ?
#     """, (app_id,))
#     data = c.fetchone()
#
#     id_applications_query = """
#         SELECT id, full_name, passport_photo, id_payment_proof, id_status FROM id_applications
#         WHERE application_id = ?
#     """
#     id_applications = pd.read_sql_query(id_applications_query, conn, params=(app_id,))
#     conn.close()
#
#     if not data:
#         return dbc.Alert("Could not retrieve application details.", color="danger")
#
#     status_color = {
#         "Verified": "success",
#         "Cancelled": "danger",
#         "Pending": "warning"
#     }.get(data['status'], "secondary")
#
#     document_links = []
#     document_fields = {
#         "Certificate of Incorporation": "cert_incorporation",
#         "Business License": "business_license",
#         "Brella Search": "brella_search",
#         "Directors Images": "director_images",
#         "Tax Clearance Cert": "tax_clearance_cert",
#         "TAFFA Certificate": "taffa_cert",
#         "Memo & Articles": "memo_articles",
#         "Audited Accounts": "audited_accounts",
#     }
#
#     for doc_name, field in document_fields.items():
#         if data[field]:
#             filename = os.path.basename(data[field])
#             download_link = dcc.Link(
#                 f"Download {doc_name}",
#                 href=f"/download-file/{data['agent_id']}/{filename}",
#                 className="d-block"
#             )
#             document_links.append(download_link)
#
#     details_layout = [
#         dbc.Row([
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Company & Contact Information"),
#                     dbc.CardBody([
#                         html.P([html.Strong("Company Name: "), data['company_name']]),
#                         html.P([html.Strong("TIN Number: "), data['tin_number']]),
#                         html.P([html.Strong("Physical Address: "), data['physical_address']]),
#                         html.P([html.Strong("Contact Person: "), data['contact_person']]),
#                         html.P([html.Strong("Email: "), data['email']]),
#                         html.P([html.Strong("Phone: "), data['phone']]),
#                     ])
#                 ]),
#                 dbc.Card([
#                     dbc.CardHeader("Director Information"),
#                     dbc.CardBody([
#                         html.P([html.Strong("Director 1: "), data['director_1']]),
#                         html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"]),
#                         html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"]),
#                     ])
#                 ], className="mt-3"),
#             ], width=6),
#             dbc.Col([
#                 dbc.Card([
#                     dbc.CardHeader("Compliance & Verification"),
#                     dbc.CardBody([
#                         html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"]),
#                         html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"]),
#                         html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"]),
#                         html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']]),
#                         html.P([html.Strong("Current Status: "),
#                                 html.Strong(data['status'], className=f"text-{status_color}")])
#                     ])
#                 ]),
#                 dbc.Card([
#                     dbc.CardHeader("Uploaded Documents (Membership)"),
#                     dbc.CardBody(document_links)
#                 ], className="mt-3"),
#                 dbc.Card([
#                     dbc.CardHeader("Actions (Membership)"),
#                     dbc.CardBody([
#                         html.H5("Update Status for Selected Application"),
#                         dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
#                                                                           {'label': 'Cancelled', 'value': 'Cancelled'}],
#                                      placeholder="Select new status"),
#                         dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2"),
#                         dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
#                                    className="mt-2 ms-2", disabled=data['status'] != 'Verified'),
#                         html.Div(id="download-cert-link-div", className="mt-2"),
#                         html.Div(id='admin-update-output', className="mt-3")
#                     ])
#                 ], className="mt-3"),
#             ], width=6),
#         ], className="mt-4")
#     ]
#
#     id_card_links = []
#     if not id_applications.empty:
#         id_card_details = [html.Hr(), html.H5("ID Card Applications", className="card-title")]
#         for index, row in id_applications.iterrows():
#             id_app_id = row['id']
#             id_card_details.append(html.P(html.Strong(f"ID for: {row['full_name']}")))
#             id_card_details.append(dcc.Link("Download Passport Photo",
#                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['passport_photo'])}",
#                                             className="d-block"))
#             id_card_details.append(dcc.Link("Download ID Payment Proof",
#                                             href=f"/download-file/{data['agent_id']}/{os.path.basename(row['id_payment_proof'])}",
#                                             className="d-block"))
#             id_card_details.append(html.P([html.Strong("ID Status: "), row['id_status']]))
#
#             if row['id_status'] == 'Verified':
#                 id_card_details.append(
#                     dcc.Link("Download ID Card", href=f"/download-id/{id_app_id}", download="TAFFA_ID.pdf",
#                              target="_blank", className="btn btn-primary mt-2"))
#             else:
#                 id_card_details.append(
#                     dbc.Button("Verify ID Application", id={"type": "verify-id-button", "index": str(id_app_id)},
#                                color="success", className="mt-2"))
#             id_card_details.append(html.Hr())
#         id_card_links = id_card_details
#     else:
#         id_card_links = html.Div([html.P("No ID Application submitted for this company.")])
#
#     details_layout.append(
#         dbc.Row([
#             dbc.Col(
#                 dbc.Card([
#                     dbc.CardHeader("ID Application Documents"),
#                     dbc.CardBody(id_card_links)
#                 ], className="mt-3"),
#                 width=12
#             )
#         ])
#     )
#     return details_layout
#
#
# @app.callback(
#     Output('admin-update-output', 'children'),
#     Input('admin-update-button', 'n_clicks'),
#     [State('admin-table', 'selected_rows'), State('admin-table', 'data'), State('admin-status-dropdown', 'value')],
#     prevent_initial_call=True
# )
# def update_status(n_clicks, selected_rows, table_data, new_status):
#     if not selected_rows or not new_status:
#         raise PreventUpdate
#
#     app_id = table_data[selected_rows[0]]['id']
#     ref_number = f"TAFFA-TRA-{random.randint(10000, 99999)}{'PASS' if new_status == 'Verified' else 'FAIL'}"
#
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         c = conn.cursor()
#         c.execute("UPDATE applications SET status = ?, reference_number = ? WHERE id = ?",
#                   (new_status, ref_number, app_id))
#         conn.commit()
#
#         c.execute("SELECT a.email FROM agents a JOIN applications p ON a.id = p.agent_id WHERE p.id = ?", (app_id,))
#         agent_email = c.fetchone()[0]
#
#         email_body = (
#             f"Dear Applicant,\n\n"
#             f"The status of your TAFFA membership application has been updated to: {new_status}.\n\n"
#             f"Reference Number: {ref_number}\n\n"
#             f"Thank you,\nTAFFA Administration"
#         )
#
#         email_sent = send_email(agent_email, f"TAFFA Application Update: {new_status}", email_body)
#
#         if email_sent:
#             return [
#                 dbc.Alert(f"Application {app_id} updated to '{new_status}'. A notification has been sent.",
#                           color="success"),
#                 dbc.Toast(
#                     "Email notification sent successfully!",
#                     header="Email Status",
#                     icon="success",
#                     dismissable=True,
#                     is_open=True,
#                     style={"position": "fixed", "top": "1rem", "right": "1rem", "width": "350px"}
#                 )
#             ]
#         else:
#             return dbc.Alert(f"Application {app_id} updated to '{new_status}'. Failed to send email notification.",
#                              color="warning")
#
#     except Exception as e:
#         return dbc.Alert(f"Error updating status: {e}", color="danger")
#     finally:
#         if conn: conn.close()
#
#
# @app.callback(
#     Output({"type": "verify-id-button", "index": MATCH}, "children"),
#     Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
#     State({"type": "verify-id-button", "index": ALL}, "id"),
#     prevent_initial_call=True
# )
# def verify_id_application(n_clicks, button_ids):
#     if not n_clicks or not any(n_clicks):
#         raise PreventUpdate
#
#     triggered_id_json = ctx.triggered[0]['prop_id']
#     triggered_id_dict = json.loads(triggered_id_json)
#     clicked_id = triggered_id_dict['index']
#
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#
#     c.execute("""SELECT p.reference_number FROM id_applications i
#                  JOIN applications p ON i.application_id = p.id
#                  WHERE i.id = ?""", (clicked_id,))
#     ref_number_result = c.fetchone()
#
#     if not ref_number_result:
#         return dbc.Alert("Could not find membership reference number.", color="danger")
#
#     id_number = ref_number_result['reference_number']
#     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
#
#     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
#               ('Verified', id_number, expiry_date, clicked_id))
#     conn.commit()
#     conn.close()
#
#     return "Verified!"
#
#
# @app.callback(
#     Output('generate-cert-button', 'disabled'),
#     Input('admin-table', 'selected_rows'),
#     Input('admin-update-output', 'children'),
#     State('admin-table', 'data'),
#     prevent_initial_call=True
# )
# def toggle_generate_button(selected_rows, update_output, table_data):
#     if not selected_rows:
#         return True
#
#     app_id = table_data[selected_rows[0]]['id']
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT status FROM applications WHERE id = ?", (app_id,))
#     status = c.fetchone()[0]
#     conn.close()
#
#     return status != 'Verified'
#
#
# def generate_membership_certificate(app_data):
#     filename = f"Certificate-{app_data['tin_number']}.pdf"
#     filepath = os.path.join(CERTIFICATES_DIR, filename)
#     c = canvas.Canvas(filepath, pagesize=letter)
#     width, height = letter
#
#     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
#
#     if os.path.exists(taffa_logo_path):
#         c.drawImage(taffa_logo_path, 30, height - 150, width=150, height=150, preserveAspectRatio=True, mask='auto')
#
#     c.setFont("Helvetica-Bold", 16)
#     c.setFillColor(colors.black)
#     c.drawRightString(width - 50, height - 110, f"No. {random.randint(1000, 9999)}")
#
#     c.setFont("Helvetica-Bold", 24)
#     c.setFillColor(colors.HexColor('#003366'))
#     c.drawCentredString(width / 2.0, height - 200, "CERTIFICATE OF MEMBERSHIP")
#
#     c.setFont("Helvetica", 14)
#     c.setFillColor(colors.black)
#     c.drawCentredString(width / 2.0, height - 250, "CERTIFICATE IS AWARDED TO")
#
#     c.setFont("Helvetica-Bold", 20)
#     c.drawCentredString(width / 2.0, height - 280, app_data['company_name'].upper())
#
#     c.setFont("Helvetica", 12)
#     c.drawCentredString(width / 2.0, height - 320,
#                         f"as a Tanzania Freight Forwarder Association Member for {date.today().year}")
#
#     c.save()
#     return filename
#
#
# def generate_id_card(id_app_data, agent_data):
#     filename = f"ID-{id_app_data['id_number']}.pdf"
#     filepath = os.path.join(IDS_DIR, filename)
#     c = canvas.Canvas(filepath, pagesize=A4)
#     width, height = A4
#
#     # ID card dimensions
#     card_width = width * 0.75
#     card_height = height * 0.75
#
#     # Calculate offsets to center the card on the page
#     x_offset = (width - card_width) / 2
#     y_offset = (height - card_height) / 2
#
#     # Draw the border
#     c.setStrokeColor(colors.HexColor('#003366'))
#     c.setLineWidth(5)
#     c.roundRect(x_offset, y_offset, card_width, card_height, 10, stroke=1, fill=0)
#
#     # Header with TAFFA logo and text
#     header_height = card_height * 0.2
#     c.setFillColor(colors.HexColor('#F0F8FF'))  # light blue background
#     c.rect(x_offset, y_offset + card_height - header_height, card_width, header_height, fill=1, stroke=0)
#
#     # TAFFA Logo
#     taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
#     if os.path.exists(taffa_logo_path):
#         logo_size = header_height * 0.8
#         logo_x = x_offset + card_width * 0.05
#         logo_y = y_offset + card_height - header_height + (header_height - logo_size) / 2
#         c.drawImage(taffa_logo_path, logo_x, logo_y, width=logo_size, height=logo_size, preserveAspectRatio=True)
#
#     # Title text
#     c.setFont("Helvetica-Bold", 14)
#     c.setFillColor(colors.HexColor('#003366'))
#     title_x = x_offset + card_width * 0.5
#     title_y = y_offset + card_height - header_height / 2 + 10
#     c.drawCentredString(title_x, title_y, "TANZANIA FREIGHT")
#     c.drawCentredString(x_offset + card_width * 0.5, title_y - 20, "FORWARDERS ASSOCIATION")
#
#     # Photo
#     photo_path = id_app_data['passport_photo']
#     photo_size = card_width * 0.3
#     photo_x = x_offset + (card_width - photo_size) / 2
#     photo_y = y_offset + card_height - header_height - 10 - photo_size
#     if os.path.exists(photo_path):
#         c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True)
#
#     # Personal Details - Centered underneath the photo
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(colors.black)
#     details_y = photo_y - 30
#     content_center_x = x_offset + card_width / 2
#
#     c.drawCentredString(content_center_x, details_y, f"Name: {id_app_data['full_name']}")
#     c.drawCentredString(content_center_x, details_y - 20, f"Position: {id_app_data['position']}")
#     c.drawCentredString(content_center_x, details_y - 40, f"Company: {agent_data['company_name']}")
#
#     # ID details
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(colors.HexColor('#003366'))
#     id_y_start = details_y - 80
#     c.drawCentredString(content_center_x, id_y_start, f"ID NO: {id_app_data['id_number']}")
#     c.drawCentredString(content_center_x, id_y_start - 20, f"Expiry Date: {id_app_data['expiry_date']}")
#
#     # QR code - Centered at the bottom
#     qr_data = f"ID: {id_app_data['id_number']} | Expiry: {id_app_data['expiry_date']}"
#     qr_img = qrcode.make(qr_data)
#     qr_buffer = io.BytesIO()
#     qr_img.save(qr_buffer, format='PNG')
#     qr_buffer.seek(0)
#
#     qr_size = card_width * 0.25
#     qr_x = content_center_x - qr_size / 2
#     qr_y = y_offset + 20
#     c.drawImage(ImageReader(qr_buffer), qr_x, qr_y, width=qr_size, height=qr_size)
#
#     c.save()
#     return filename
#
#
# @app.callback(
#     Output('download-cert-link-div', 'children'),
#     Input('generate-cert-button', 'n_clicks'),
#     State('admin-table', 'selected_rows'),
#     State('admin-table', 'data'),
#     prevent_initial_call=True
# )
# def handle_certificate_generation(n_clicks, selected_rows, table_data):
#     if not selected_rows:
#         raise PreventUpdate
#
#     app_id = table_data[selected_rows[0]]['id']
#
#     conn = sqlite3.connect(DB_PATH)
#     query = """
#         SELECT a.tin_number, a.company_name, p.reference_number, p.status
#         FROM agents a JOIN applications p ON a.id = p.agent_id
#         WHERE p.id = ?
#     """
#     df = pd.read_sql_query(query, conn, params=(app_id,))
#     conn.close()
#
#     if df.empty:
#         return dbc.Alert("Could not find application data.", color="danger")
#
#     app_data = df.to_dict('records')[0]
#     filename = generate_membership_certificate(app_data)
#
#     return dcc.Link(f"Download Certificate for {app_data['company_name']}",
#                     href=f"/download-cert/{os.path.basename(filename)}")
#
#
# @app.callback(
#     Output({"type": "download-id-link", "index": MATCH}, "children"),
#     Input({"type": "verify-id-button", "index": ALL}, "n_clicks"),
#     State({"type": "verify-id-button", "index": ALL}, "id"),
#     prevent_initial_call=True
# )
# def verify_id_application(n_clicks, button_ids):
#     if not n_clicks or not any(n_clicks):
#         raise PreventUpdate
#
#     triggered_id_json = ctx.triggered[0]['prop_id']
#     triggered_id_dict = json.loads(triggered_id_json)
#     clicked_id = triggered_id_dict['index']
#
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     c = conn.cursor()
#
#     c.execute("""SELECT p.reference_number FROM id_applications i
#                  JOIN applications p ON i.application_id = p.id
#                  WHERE i.id = ?""", (clicked_id,))
#     ref_number_result = c.fetchone()
#
#     if not ref_number_result:
#         return dbc.Alert("Could not find membership reference number.", color="danger")
#
#     id_number = ref_number_result['reference_number']
#     expiry_date = (date.today() + timedelta(days=365)).strftime('%d-%b-%Y')
#
#     c.execute("UPDATE id_applications SET id_status = ?, id_number = ?, expiry_date = ? WHERE id = ?",
#               ('Verified', id_number, expiry_date, clicked_id))
#     conn.commit()
#     conn.close()
#
#     return "Verified!"
#
#
# @server.route('/download-cert/<filename>')
# def serve_pdf(filename):
#     return send_from_directory(CERTIFICATES_DIR, filename, as_attachment=True)
#
#
# @server.route('/download-id/<filename>')
# def serve_id(filename):
#     return send_from_directory(IDS_DIR, filename, as_attachment=True)
#
#
# @server.route('/download-file/<app_id>/<filename>')
# def download_uploaded_file(app_id, filename):
#     app_folder = os.path.join(DOCUMENTS_DIR, app_id)
#     return send_from_directory(app_folder, filename, as_attachment=True)
#
#
# if __name__ == '__main__':
#     if not os.path.exists(DOCUMENTS_DIR):
#         os.makedirs(DOCUMENTS_DIR)
#     if not os.path.exists(CERTIFICATES_DIR):
#         os.makedirs(CERTIFICATES_DIR)
#     if not os.path.exists(IDS_DIR):
#         os.makedirs(IDS_DIR)
#
#     assets_dir = os.path.join(BASE_DIR, 'assets')
#     if not os.path.exists(assets_dir):
#         os.makedirs(assets_dir)
#
#     app.run(debug=True, port=5088)
#
