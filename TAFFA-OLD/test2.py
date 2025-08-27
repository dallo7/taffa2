# # import dash
# # from dash import dcc, html, Input, Output, State
# # import dash_bootstrap_components as dbc
# # import random
# # from datetime import date
# #
# # # Initialize the Dash app with a Bootstrap theme for better styling
# # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# #
# # # Define the layout of the app
# # app.layout = dbc.Container([
# #     dbc.Row(dbc.Col(html.H1("Tanzania CFA Portal", className="text-center my-4"))),
# #     dbc.Row(dbc.Col(html.P("Client & Document Submission", className="text-center text-muted"))),
# #
# #     html.Hr(),  # Separator
# #
# #     # Section 1: Client Information
# #     dbc.Card(
# #         dbc.CardBody([
# #             html.H4("1. Client Information", className="card-title"),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Client Company Name"),
# #                     dbc.Input(id="client-name", type="text", placeholder="e.g., ABC Logistics")
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Client TIN"),
# #                     dbc.Input(id="client-tin", type="text", placeholder="e.g., 123-456-789")
# #                 ], className="mb-3")),
# #             ]),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Business License No."),
# #                     dbc.Input(id="biz-license", type="text", placeholder="e.g., BLN/XYZ/001")
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Primary Contact"),
# #                     dbc.Input(id="contact-person", type="text", placeholder="e.g., Jane Doe")
# #                 ], className="mb-3")),
# #             ]),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Contact Phone"),
# #                     dbc.Input(id="contact-phone", type="tel", placeholder="e.g., +255-7XX-XXX-XXX")
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Email Address"),
# #                     dbc.Input(id="email", type="email", placeholder="e.g., jane@example.com")
# #                 ], className="mb-3")),
# #             ]),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("TAFFA Agent ID"),
# #                     dcc.Dropdown(
# #                         id="taffa-agent-id",
# #                         options=[{"label": "DFO001", "value": "DFO001"}, {"label": "DFO002", "value": "DFO002"}],
# #                         placeholder="Select your TAFFA Agent ID"
# #                     )
# #                 ], className="mb-3")),
# #                 dbc.Col(dcc.Upload(
# #                     id='upload-authorization',
# #                     children=html.Div([
# #                         'Drag and Drop or ',
# #                         html.A('Select Authorization Letter')
# #                     ]),
# #                     style={
# #                         'width': '100%',
# #                         'height': '60px',
# #                         'lineHeight': '60px',
# #                         'borderWidth': '1px',
# #                         'borderStyle': 'dashed',
# #                         'borderRadius': '5px',
# #                         'textAlign': 'center',
# #                         'margin': '10px 0'
# #                     },
# #                     multiple=False
# #                 )),
# #             ])
# #         ])
# #     ),
# #
# #     # Section 2: Shipment Details
# #     dbc.Card(
# #         dbc.CardBody([
# #             html.H4("2. Shipment Details", className="card-title"),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Type of Shipment"),
# #                     dcc.Dropdown(
# #                         id="shipment-type",
# #                         options=[{"label": "Import", "value": "Import"}, {"label": "Export", "value": "Export"}],
# #                         placeholder="Select type"
# #                     )
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Bill of Lading / AWB No."),
# #                     dbc.Input(id="bl-awb-no", type="text", placeholder="e.g., BLAWB12345")
# #                 ], className="mb-3")),
# #             ]),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Commercial Invoice No."),
# #                     dbc.Input(id="invoice-no", type="text", placeholder="e.g., INV-00123")
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Shipper/Consignor Name"),
# #                     dbc.Input(id="shipper-name", type="text", placeholder="e.g., Global Exporters Inc.")
# #                 ], className="mb-3")),
# #             ]),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Origin Port/Country"),
# #                     dbc.Input(id="origin-port", type="text", placeholder="e.g., Shanghai, China")
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Destination Port/Country"),
# #                     dbc.Input(id="destination-port", type="text", placeholder="e.g., Dar es Salaam, Tanzania")
# #                 ], className="mb-3")),
# #             ]),
# #             dbc.Row([
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Date of Arrival"),
# #                     dcc.DatePickerSingle(
# #                         id='arrival-date',
# #                         placeholder='Select a date'
# #                     )
# #                 ], className="mb-3")),
# #                 dbc.Col(dbc.InputGroup([
# #                     dbc.InputGroupText("Cargo Description"),
# #                     dbc.Input(id="cargo-desc", type="text", placeholder="e.g., 200 boxes of electronics")
# #                 ], className="mb-3")),
# #             ])
# #         ])
# #         , className="mt-4"),
# #
# #     # URN Generation & Display
# #     dbc.Row(dbc.Col(
# #         dbc.Button("Generate URN & Proceed", id="generate-urn-btn", color="primary", className="mt-4 w-100"),
# #         width=6, className="mx-auto"
# #     )),
# #
# #     dbc.Modal([
# #         dbc.ModalHeader(dbc.ModalTitle("URN Generated Successfully!")),
# #         dbc.ModalBody(
# #             html.Div([
# #                 html.P("Your Unique Reference Number is:", className="text-center"),
# #                 html.H2(id="urn-output", className="text-center text-primary fw-bold"),
# #                 dbc.Button("Copy URN", id="copy-btn", color="secondary", className="mt-3"),
# #                 dcc.Clipboard(target_id="urn-output", title="Copy to clipboard",
# #                               style={"position": "absolute", "right": "20px", "top": "20px"}),
# #             ], className="text-center")
# #         ),
# #         dbc.ModalFooter(
# #             dbc.Button("Proceed to Document Upload", id="proceed-btn", href="/document-upload", color="success")
# #         ),
# #     ], id="urn-modal", is_open=False),
# #
# #     html.Div(id="dummy-output", style={"display": "none"})  # Used for the callback to trigger the modal
# # ], className="mt-5 mb-5", fluid=True)
# #
# #
# # # Callback to generate URN and open the modal
# # @app.callback(
# #     Output("urn-modal", "is_open"),
# #     Output("urn-output", "children"),
# #     Input("generate-urn-btn", "n_clicks"),
# #     State("taffa-agent-id", "value"),
# #     State("client-tin", "value"),
# #     State("bl-awb-no", "value"),
# #     prevent_initial_call=True
# # )
# # def generate_urn(n_clicks, taffa_agent_id, client_tin, bl_awb_no):
# #     if n_clicks is None:
# #         return False, ""
# #
# #     # Basic validation for mandatory fields
# #     if not all([taffa_agent_id, client_tin, bl_awb_no]):
# #         # In a real app, you would show an error message
# #         return False, "Please fill in all mandatory fields."
# #
# #     # Get the last two digits of the current year
# #     current_year = date.today().strftime("%y")
# #
# #     # Generate a random 4-digit number
# #     random_part = str(random.randint(1000, 9999))
# #
# #     # Construct the URN
# #     urn = f"SUC-{current_year}-{taffa_agent_id}{random_part}"
# #
# #     return True, urn
# #
# #
# # # Run the app
# # if __name__ == '__main__':
# #     app.run(debug=True)
# #
# # import dash
# # from dash import dcc, html, Input, Output, State, callback_context, dash_table
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from datetime import datetime, timedelta
# # import pandas as pd
# # import numpy as np
# # from dash.exceptions import PreventUpdate
# # import uuid
# #
# # # Initialize Dash app
# # app = dash.Dash(__name__)
# #
# #
# # # Sample data for analytics
# # def generate_sample_data():
# #     np.random.seed(42)
# #     dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
# #
# #     consignments_data = []
# #     for i, date in enumerate(dates):
# #         daily_consignments = np.random.poisson(5)
# #         for j in range(daily_consignments):
# #             consignments_data.append({
# #                 'date': date,
# #                 'consignment_id': f'CONS-{i:03d}-{j:02d}',
# #                 'importer': np.random.choice(
# #                     ['ABC Ltd', 'XYZ Corp', 'Global Trading', 'Import Masters', 'Trade Solutions']),
# #                 'cfa': np.random.choice(
# #                     ['Maersk Tanzania Ltd', 'DSV Air & Sea Ltd', 'Bollore Transport', 'DHL Supply Chain']),
# #                 'value': np.random.uniform(10000, 500000),
# #                 'status': np.random.choice(['Completed', 'Processing', 'Pending Payment', 'TANCIS Integration'],
# #                                            p=[0.6, 0.2, 0.1, 0.1]),
# #                 'goods_type': np.random.choice(['Electronics', 'Machinery', 'Textiles', 'Food Products', 'Chemicals']),
# #                 'port': np.random.choice(['Dar es Salaam', 'Mtwara', 'Tanga', 'Mwanza'])
# #             })
# #
# #     return pd.DataFrame(consignments_data)
# #
# #
# # # Generate sample data
# # df_consignments = generate_sample_data()
# #
# # # CSS Styling
# # external_stylesheets = [
# #     'https://codepen.io/chriddyp/pen/bWLwgP.css',
# #     'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
# # ]
# #
# # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# #
# # # Custom CSS
# # app.index_string = '''
# # <!DOCTYPE html>
# # <html>
# #     <head>
# #         {%metas%}
# #         <title>{%title%}</title>
# #         {%favicon%}
# #         {%css%}
# #         <style>
# #             body {
# #                 font-family: 'Arial', sans-serif;
# #                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# #                 margin: 0;
# #             }
# #             .main-container {
# #                 background: white;
# #                 margin: 20px;
# #                 border-radius: 15px;
# #                 box-shadow: 0 10px 30px rgba(0,0,0,0.1);
# #                 overflow: hidden;
# #             }
# #             .header {
# #                 background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
# #                 color: white;
# #                 padding: 20px;
# #                 text-align: center;
# #             }
# #             .step-indicator {
# #                 display: flex;
# #                 justify-content: space-between;
# #                 padding: 20px;
# #                 background: #f8f9fa;
# #                 border-bottom: 1px solid #dee2e6;
# #             }
# #             .step {
# #                 display: flex;
# #                 align-items: center;
# #                 flex: 1;
# #                 position: relative;
# #             }
# #             .step-circle {
# #                 width: 40px;
# #                 height: 40px;
# #                 border-radius: 50%;
# #                 display: flex;
# #                 align-items: center;
# #                 justify-content: center;
# #                 font-weight: bold;
# #                 margin-right: 10px;
# #             }
# #             .step-active .step-circle {
# #                 background: #007bff;
# #                 color: white;
# #             }
# #             .step-completed .step-circle {
# #                 background: #28a745;
# #                 color: white;
# #             }
# #             .step-pending .step-circle {
# #                 background: #e9ecef;
# #                 color: #6c757d;
# #                 border: 2px solid #dee2e6;
# #             }
# #             .content-area {
# #                 padding: 30px;
# #             }
# #             .card {
# #                 background: white;
# #                 border-radius: 10px;
# #                 padding: 20px;
# #                 margin: 20px 0;
# #                 box-shadow: 0 4px 15px rgba(0,0,0,0.1);
# #                 border-left: 5px solid #007bff;
# #             }
# #             .form-group {
# #                 margin-bottom: 20px;
# #             }
# #             .form-label {
# #                 font-weight: bold;
# #                 margin-bottom: 5px;
# #                 display: block;
# #                 color: #333;
# #             }
# #             .btn {
# #                 padding: 12px 25px;
# #                 border: none;
# #                 border-radius: 5px;
# #                 cursor: pointer;
# #                 font-size: 16px;
# #                 transition: all 0.3s;
# #                 text-decoration: none;
# #                 display: inline-block;
# #             }
# #             .btn-primary {
# #                 background: linear-gradient(135deg, #007bff, #0056b3);
# #                 color: white;
# #             }
# #             .btn-primary:hover {
# #                 transform: translateY(-2px);
# #                 box-shadow: 0 5px 15px rgba(0,123,255,0.3);
# #             }
# #             .btn-success {
# #                 background: linear-gradient(135deg, #28a745, #1e7e34);
# #                 color: white;
# #             }
# #             .alert {
# #                 padding: 15px;
# #                 border-radius: 5px;
# #                 margin: 15px 0;
# #             }
# #             .alert-success {
# #                 background: #d4edda;
# #                 color: #155724;
# #                 border-left: 5px solid #28a745;
# #             }
# #             .alert-info {
# #                 background: #cce7ff;
# #                 color: #004085;
# #                 border-left: 5px solid #007bff;
# #             }
# #             .reference-number {
# #                 font-family: 'Courier New', monospace;
# #                 font-size: 24px;
# #                 font-weight: bold;
# #                 background: #f8f9fa;
# #                 padding: 15px;
# #                 border-radius: 5px;
# #                 text-align: center;
# #                 border: 2px dashed #007bff;
# #             }
# #             .nav-tabs {
# #                 display: flex;
# #                 border-bottom: 2px solid #dee2e6;
# #                 margin-bottom: 20px;
# #             }
# #             .nav-tab {
# #                 padding: 15px 25px;
# #                 cursor: pointer;
# #                 border-bottom: 3px solid transparent;
# #                 transition: all 0.3s;
# #                 color: #6c757d;
# #             }
# #             .nav-tab.active {
# #                 color: #007bff;
# #                 border-bottom-color: #007bff;
# #                 background: #f8f9fa;
# #             }
# #             .nav-tab:hover {
# #                 background: #f8f9fa;
# #                 color: #007bff;
# #             }
# #             .dashboard-metrics {
# #                 display: grid;
# #                 grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
# #                 gap: 20px;
# #                 margin-bottom: 30px;
# #             }
# #             .metric-card {
# #                 background: white;
# #                 padding: 25px;
# #                 border-radius: 10px;
# #                 box-shadow: 0 4px 15px rgba(0,0,0,0.1);
# #                 text-align: center;
# #                 border-top: 5px solid #007bff;
# #             }
# #             .metric-value {
# #                 font-size: 32px;
# #                 font-weight: bold;
# #                 color: #007bff;
# #                 margin-bottom: 5px;
# #             }
# #             .metric-label {
# #                 color: #6c757d;
# #                 font-size: 14px;
# #             }
# #         </style>
# #     </head>
# #     <body>
# #         {%app_entry%}
# #         <footer>
# #             {%config%}
# #             {%scripts%}
# #             {%renderer%}
# #         </footer>
# #     </body>
# # </html>
# # '''
# #
# # # App layout
# # app.layout = html.Div([
# #     dcc.Store(id='current-step-store', data=1),
# #     dcc.Store(id='consignment-data-store', data={}),
# #     dcc.Store(id='reference-number-store', data=''),
# #     dcc.Store(id='active-tab-store', data='clearing'),
# #
# #     html.Div([
# #         # Header
# #         html.Div([
# #             html.H1([
# #                 html.I(className="fas fa-shield-alt", style={'marginRight': '15px'}),
# #                 "TAFFA Clearing & Analytics System"
# #             ], style={'margin': 0, 'fontSize': '28px'}),
# #             html.P("Tanzania Freight Forwarders Association - Integrated Dashboard",
# #                    style={'margin': '5px 0 0 0', 'opacity': 0.9})
# #         ], className='header'),
# #
# #         # Navigation Tabs
# #         html.Div([
# #             html.Div("Clearing Process", id='tab-clearing', className='nav-tab active'),
# #             html.Div("Analytics Dashboard", id='tab-analytics', className='nav-tab'),
# #             html.Div("Consignment Tracker", id='tab-tracker', className='nav-tab'),
# #             html.Div("Reports", id='tab-reports', className='nav-tab'),
# #         ], className='nav-tabs'),
# #
# #         # Content Area
# #         html.Div(id='main-content', className='content-area')
# #
# #     ], className='main-container')
# # ], style={'minHeight': '100vh'})
# #
# #
# # # --- Content Creation Functions ---
# #
# # # Clearing Process Content
# # def create_clearing_content(current_step, consignment_data, reference_number):
# #     # Step Indicator
# #     steps = [
# #         {"num": 1, "title": "Consignment Details", "icon": "fas fa-file-alt"},
# #         {"num": 2, "title": "Invoice Generation", "icon": "fas fa-dollar-sign"},
# #         {"num": 3, "title": "Payment Processing", "icon": "fas fa-credit-card"},
# #         {"num": 4, "title": "Accreditation", "icon": "fas fa-certificate"},
# #         {"num": 5, "title": "TANCIS Integration", "icon": "fas fa-link"}
# #     ]
# #
# #     step_indicators = []
# #     for step in steps:
# #         status_class = "step-completed" if current_step > step["num"] else \
# #             "step-active" if current_step == step["num"] else "step-pending"
# #
# #         step_indicators.append(
# #             html.Div([
# #                 html.Div([
# #                     html.I(className=step["icon"]) if current_step > step["num"] else \
# #                         html.I(className="fas fa-check") if current_step == step["num"] else str(step["num"])
# #                 ], className='step-circle'),
# #                 html.Div([
# #                     html.Div(f"Step {step['num']}", style={'fontSize': '12px', 'color': '#6c757d'}),
# #                     html.Div(step["title"], style={'fontSize': '14px', 'fontWeight': 'bold'})
# #                 ])
# #             ], className=f'step {status_class}')
# #         )
# #
# #     content = [
# #         html.Div(step_indicators, className='step-indicator')
# #     ]
# #
# #     # Step 1: Consignment Details
# #     if current_step == 1:
# #         content.append(html.Div([
# #             html.H2("Consignment Registration", style={'marginBottom': '20px'}),
# #             html.P("Enter details about the consignment and parties involved",
# #                    style={'color': '#6c757d', 'marginBottom': '30px'}),
# #
# #             html.Div([
# #                 html.Div([
# #                     html.Label("Importer Details", className='form-label'),
# #                     dcc.Input(
# #                         id='importer-input',
# #                         type='text',
# #                         placeholder='Enter importer name/company',
# #                         value=consignment_data.get('importer', ''),
# #                         style={'width': '100%', 'padding': '12px', 'borderRadius': '5px',
# #                                'border': '1px solid #ccc', 'fontSize': '16px'}
# #                     )
# #                 ], className='form-group'),
# #
# #                 html.Div([
# #                     html.Label("Clearing & Forwarding Agent (CFA)", className='form-label'),
# #                     dcc.Dropdown(
# #                         id='cfa-dropdown',
# #                         options=[
# #                             {'label': 'Maersk Tanzania Ltd', 'value': 'Maersk Tanzania Ltd'},
# #                             {'label': 'DSV Air & Sea Ltd', 'value': 'DSV Air & Sea Ltd'},
# #                             {'label': 'Bollore Transport & Logistics', 'value': 'Bollore Transport & Logistics'},
# #                             {'label': 'DHL Supply Chain', 'value': 'DHL Supply Chain'}
# #                         ],
# #                         value=consignment_data.get('cfa', None),
# #                         placeholder='Select CFA',
# #                         style={'fontSize': '16px'}
# #                     )
# #                 ], className='form-group'),
# #
# #                 html.Div([
# #                     html.Label("Consignment Value (USD)", className='form-label'),
# #                     dcc.Input(
# #                         id='value-input',
# #                         type='number',
# #                         placeholder='Enter total value',
# #                         value=consignment_data.get('value', ''),
# #                         style={'width': '100%', 'padding': '12px', 'borderRadius': '5px',
# #                                'border': '1px solid #ccc', 'fontSize': '16px'}
# #                     )
# #                 ], className='form-group'),
# #
# #                 html.Div([
# #                     html.Label("Goods Description", className='form-label'),
# #                     dcc.Input(
# #                         id='goods-input',
# #                         type='text',
# #                         placeholder='Brief description of goods',
# #                         value=consignment_data.get('goods', ''),
# #                         style={'width': '100%', 'padding': '12px', 'borderRadius': '5px',
# #                                'border': '1px solid #ccc', 'fontSize': '16px'}
# #                     )
# #                 ], className='form-group'),
# #             ], style={'display': 'grid', 'gridTemplateColumns': '1fr 1fr', 'gap': '20px'}),
# #
# #             html.Div(id='step1-error-message', style={'color': 'red', 'marginTop': '10px'}),
# #
# #             html.Div([
# #                 html.Button("Generate Invoice", id='step1-next-btn', className='btn btn-primary')
# #             ], style={'textAlign': 'right', 'marginTop': '30px'})
# #         ], className='card'))
# #
# #     # Step 2: Invoice Generation
# #     elif current_step == 2:
# #         value = float(consignment_data.get('value', 0))
# #         taffa_fee = value * 0.002 if value else 0
# #         content.append(html.Div([
# #             html.H2("Invoice Generated", style={'marginBottom': '20px'}),
# #             html.P("Review invoice details and proceed to payment",
# #                    style={'color': '#6c757d', 'marginBottom': '30px'}),
# #
# #             html.Div([
# #                 html.Div([
# #                     html.Strong("Importer: "), consignment_data.get('importer', 'N/A')
# #                 ], style={'marginBottom': '10px'}),
# #                 html.Div([
# #                     html.Strong("CFA: "), consignment_data.get('cfa', 'N/A')
# #                 ], style={'marginBottom': '10px'}),
# #                 html.Div([
# #                     html.Strong("Consignment Value: "), f"${value:,.2f}"
# #                 ], style={'marginBottom': '10px'}),
# #                 html.Div([
# #                     html.Strong("TAFFA Fee (0.2%): "), f"${taffa_fee:,.2f}"
# #                 ], style={'marginBottom': '10px', 'fontSize': '18px', 'color': '#007bff'})
# #             ], className='card'),
# #
# #             html.Div([
# #                 html.I(className="fas fa-info-circle", style={'marginRight': '10px'}),
# #                 html.Strong("Payment Instructions: "),
# #                 "Please pay the TAFFA fee through CapitalPay integration."
# #             ], className='alert alert-info'),
# #
# #             html.Div([
# #                 html.Button("Back to Edit", id='step2-back-btn', className='btn',
# #                             style={'marginRight': '15px', 'background': '#6c757d', 'color': 'white'}),
# #                 html.Button("Proceed to Payment", id='step2-next-btn', className='btn btn-success')
# #             ], style={'textAlign': 'right', 'marginTop': '30px'})
# #         ]))
# #
# #     # Step 3: Payment Processing
# #     elif current_step == 3:
# #         value = float(consignment_data.get('value', 0))
# #         taffa_fee = value * 0.002 if value else 0
# #         content.append(html.Div([
# #             html.H2("CapitalPay Integration", style={'marginBottom': '20px'}),
# #             html.P("Secure payment processing through CapitalPay",
# #                    style={'color': '#6c757d', 'marginBottom': '30px'}),
# #
# #             html.Div([
# #                 html.Div([
# #                     html.I(className="fas fa-credit-card",
# #                            style={'fontSize': '48px', 'color': '#007bff', 'marginBottom': '20px'}),
# #                     html.H3("Payment Amount", style={'marginBottom': '10px'}),
# #                     html.Div(f"${taffa_fee:,.2f}",
# #                              style={'fontSize': '36px', 'fontWeight': 'bold', 'color': '#28a745',
# #                                     'marginBottom': '10px'}),
# #                     html.P("TAFFA Processing Fee")
# #                 ], style={'textAlign': 'center', 'padding': '40px'})
# #             ], className='card'),
# #
# #             html.Div([
# #                 html.Button([
# #                     html.I(className="fas fa-lock", style={'marginRight': '10px'}),
# #                     "Pay via CapitalPay"
# #                 ], id='payment-btn', className='btn btn-primary',
# #                     style={'fontSize': '18px', 'padding': '15px 30px'})
# #             ], style={'textAlign': 'center', 'marginTop': '30px'}),
# #
# #             html.Div(id='payment-status')
# #         ]))
# #
# #     # Step 4: Accreditation
# #     elif current_step == 4:
# #         content.append(html.Div([
# #             html.Div([
# #                 html.I(className="fas fa-check-circle",
# #                        style={'fontSize': '64px', 'color': '#28a745', 'marginBottom': '20px'}),
# #                 html.H2("Accreditation Generated", style={'marginBottom': '10px'}),
# #                 html.P("Your unique reference number has been created")
# #             ], style={'textAlign': 'center', 'marginBottom': '30px'}),
# #
# #             html.Div([
# #                 html.H3("TAFFA Reference Number", style={'textAlign': 'center', 'marginBottom': '20px'}),
# #                 html.Div(reference_number, className='reference-number'),
# #                 html.P("Use this reference number for TANCIS integration",
# #                        style={'textAlign': 'center', 'marginTop': '15px', 'color': '#6c757d'})
# #             ], className='card'),
# #
# #             html.Div([
# #                 html.Button([
# #                     html.I(className="fas fa-download", style={'marginRight': '10px'}),
# #                     "Download Certificate"
# #                 ], className='btn btn-primary', style={'marginRight': '15px'}),
# #                 html.Button([
# #                     html.I(className="fas fa-link", style={'marginRight': '10px'}),
# #                     "Integrate with TANCIS"
# #                 ], id='step4-next-btn', className='btn btn-success')
# #             ], style={'textAlign': 'center', 'marginTop': '30px'})
# #         ]))
# #
# #     # Step 5: TANCIS Integration
# #     elif current_step == 5:
# #         content.append(html.Div([
# #             html.H2("TANCIS Integration", style={'marginBottom': '20px'}),
# #             html.P("Connect with Tanzania Customs Integrated System",
# #                    style={'color': '#6c757d', 'marginBottom': '30px'}),
# #
# #             html.Div([
# #                 html.I(className="fas fa-exclamation-triangle", style={'marginRight': '10px'}),
# #                 html.Strong("Important: "),
# #                 "Enter your TAFFA reference number in the TANCIS Declaration form or CFA module."
# #             ], className='alert alert-info'),
# #
# #             html.Div([
# #                 html.Div([
# #                     html.H3("Your TAFFA Reference"),
# #                     html.Div(reference_number, className='reference-number'),
# #                     html.Button("Copy Reference", className='btn btn-primary',
# #                                 style={'width': '100%', 'marginTop': '15px'})
# #                 ], className='card', style={'flex': '1', 'marginRight': '20px'}),
# #
# #                 html.Div([
# #                     html.H3("TANCIS Integration Status"),
# #                     html.Div([
# #                         html.Label("TANCIS Reference Number", className='form-label'),
# #                         dcc.Input(
# #                             id='tancis-reference-input',
# #                             type='text',
# #                             placeholder='Enter TANCIS reference',
# #                             style={'width': '100%', 'padding': '12px', 'borderRadius': '5px',
# #                                    'border': '1px solid #ccc', 'fontSize': '16px', 'marginBottom': '15px'}
# #                         ),
# #                         html.Button("Link with TANCIS", className='btn btn-success',
# #                                     style={'width': '100%'})
# #                     ])
# #                 ], className='card', style={'flex': '1'})
# #             ], style={'display': 'flex'}),
# #             html.Div([
# #                 html.Button("Start New Clearing", id='start-new-btn', className='btn btn-primary')
# #             ], style={'textAlign': 'center', 'marginTop': '30px'})
# #         ]))
# #
# #     return content
# #
# #
# # # Analytics Dashboard Content
# # def create_analytics_content():
# #     # Calculate metrics
# #     total_consignments = len(df_consignments)
# #     total_value = df_consignments['value'].sum()
# #     avg_processing_time = "2.3 days"  # Mock data
# #     success_rate = (len(df_consignments[df_consignments['status'] == 'Completed']) / total_consignments * 100)
# #
# #     # Monthly trends
# #     monthly_data = df_consignments.groupby(df_consignments['date'].dt.to_period('M')).agg({
# #         'consignment_id': 'count',
# #         'value': 'sum'
# #     }).reset_index()
# #     monthly_data['date'] = monthly_data['date'].astype(str)
# #
# #     # Status distribution
# #     status_counts = df_consignments['status'].value_counts()
# #
# #     # CFA performance
# #     cfa_performance = df_consignments.groupby('cfa').agg({
# #         'consignment_id': 'count',
# #         'value': 'mean'
# #     }).reset_index().sort_values('consignment_id', ascending=False)
# #
# #     # Port distribution
# #     port_data = df_consignments['port'].value_counts()
# #
# #     return html.Div([
# #         # Metrics Cards
# #         html.Div([
# #             html.Div([
# #                 html.Div(f"{total_consignments:,}", className='metric-value'),
# #                 html.Div("Total Consignments", className='metric-label')
# #             ], className='metric-card'),
# #             html.Div([
# #                 html.Div(f"${total_value / 1000000:.1f}M", className='metric-value'),
# #                 html.Div("Total Value", className='metric-label')
# #             ], className='metric-card'),
# #             html.Div([
# #                 html.Div(avg_processing_time, className='metric-value'),
# #                 html.Div("Avg Processing Time", className='metric-label')
# #             ], className='metric-card'),
# #             html.Div([
# #                 html.Div(f"{success_rate:.1f}%", className='metric-value'),
# #                 html.Div("Success Rate", className='metric-label')
# #             ], className='metric-card')
# #         ], className='dashboard-metrics'),
# #
# #         # Charts Row 1
# #         html.Div([
# #             html.Div([
# #                 dcc.Graph(
# #                     figure=px.line(monthly_data, x='date', y='consignment_id',
# #                                    title='Monthly Consignment Trends',
# #                                    labels={'consignment_id': 'Number of Consignments', 'date': 'Month'},
# #                                    markers=True)
# #                     .update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20), plot_bgcolor='white')
# #                 )
# #             ], className='card', style={'flex': '1', 'marginRight': '20px'}),
# #
# #             html.Div([
# #                 dcc.Graph(
# #                     figure=px.pie(values=status_counts.values, names=status_counts.index,
# #                                   title='Consignment Status Distribution', hole=0.3)
# #                     .update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20))
# #                 )
# #             ], className='card', style={'flex': '1'})
# #         ], style={'display': 'flex', 'marginBottom': '20px'}),
# #
# #         # Charts Row 2
# #         html.Div([
# #             html.Div([
# #                 dcc.Graph(
# #                     figure=px.bar(cfa_performance, x='cfa', y='consignment_id',
# #                                   title='CFA Performance - Total Consignments',
# #                                   labels={'consignment_id': 'Number of Consignments', 'cfa': 'CFA'})
# #                     .update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20), plot_bgcolor='white')
# #                 )
# #             ], className='card', style={'flex': '1', 'marginRight': '20px'}),
# #
# #             html.Div([
# #                 dcc.Graph(
# #                     figure=px.bar(x=port_data.index, y=port_data.values,
# #                                   title='Consignments by Port',
# #                                   labels={'x': 'Port', 'y': 'Number of Consignments'})
# #                     .update_layout(height=350, margin=dict(t=50, b=20, l=20, r=20), plot_bgcolor='white')
# #                 )
# #             ], className='card', style={'flex': '1'})
# #         ], style={'display': 'flex'})
# #     ])
# #
# #
# # # Consignment Tracker Content
# # def create_tracker_content():
# #     return html.Div([
# #         html.H2("Consignment Tracker", style={'marginBottom': '30px'}),
# #
# #         html.Div([
# #             html.Div([
# #                 html.Label("Search by Keyword (ID, Importer, CFA, etc.)", className='form-label'),
# #                 dcc.Input(
# #                     id='search-input',
# #                     type='text',
# #                     placeholder='Enter keyword...',
# #                     style={'width': '100%', 'padding': '12px', 'borderRadius': '5px',
# #                            'border': '1px solid #ccc', 'fontSize': '16px'}
# #                 )
# #             ], style={'flex': '2'}),
# #         ], style={'display': 'flex', 'alignItems': 'end', 'marginBottom': '30px'}),
# #
# #         html.Div([
# #             dash_table.DataTable(
# #                 id='consignments-table',
# #                 columns=[
# #                     {'name': 'Date', 'id': 'date', 'type': 'datetime'},
# #                     {'name': 'Consignment ID', 'id': 'consignment_id'},
# #                     {'name': 'Importer', 'id': 'importer'},
# #                     {'name': 'CFA', 'id': 'cfa'},
# #                     {'name': 'Value (USD)', 'id': 'value', 'type': 'numeric', 'format': {'specifier': ',.0f'}},
# #                     {'name': 'Status', 'id': 'status'},
# #                     {'name': 'Port', 'id': 'port'}
# #                 ],
# #                 data=df_consignments.sort_values('date', ascending=False).to_dict('records'),
# #                 style_cell={'textAlign': 'left', 'padding': '10px', 'fontFamily': 'Arial'},
# #                 style_header={'backgroundColor': '#1e3c72', 'color': 'white', 'fontWeight': 'bold'},
# #                 style_data_conditional=[
# #                     {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'},
# #                     {'if': {'column_id': 'status', 'filter_query': '{status} = "Completed"'},
# #                      'backgroundColor': '#d4edda', 'color': '#155724'},
# #                     {'if': {'column_id': 'status', 'filter_query': '{status} = "Processing"'},
# #                      'backgroundColor': '#fff3cd', 'color': '#856404'},
# #                     {'if': {'column_id': 'status', 'filter_query': '{status} = "Pending Payment"'},
# #                      'backgroundColor': '#f8d7da', 'color': '#721c24'},
# #                     {'if': {'column_id': 'status', 'filter_query': '{status} = "TANCIS Integration"'},
# #                      'backgroundColor': '#cce7ff', 'color': '#004085'},
# #                 ],
# #                 page_size=15,
# #                 sort_action='native'
# #             )
# #         ], className='card')
# #     ])
# #
# #
# # # Reports Content
# # def create_reports_content():
# #     return html.Div([
# #         html.H2("Reports & Data Export", style={'marginBottom': '30px'}),
# #
# #         html.Div([
# #             # Custom Report Generator
# #             html.Div([
# #                 html.H3("Custom Report Generator"),
# #                 html.Div([
# #                     html.Label("Select Date Range", className='form-label'),
# #                     dcc.DatePickerRange(
# #                         id='report-date-picker',
# #                         min_date_allowed=df_consignments['date'].min(),
# #                         max_date_allowed=df_consignments['date'].max(),
# #                         initial_visible_month=df_consignments['date'].max(),
# #                         start_date=df_consignments['date'].max() - timedelta(days=30),
# #                         end_date=df_consignments['date'].max(),
# #                         style={'width': '100%'}
# #                     ),
# #                 ], className='form-group'),
# #                 html.Div([
# #                     html.Label("Filter by Status", className='form-label'),
# #                     dcc.Dropdown(
# #                         id='report-status-filter',
# #                         options=[{'label': s, 'value': s} for s in df_consignments['status'].unique()],
# #                         multi=True,
# #                         placeholder="All Statuses"
# #                     )
# #                 ], className='form-group'),
# #                 html.Button([
# #                     html.I(className="fas fa-download", style={'marginRight': '10px'}),
# #                     "Download Custom Report (Excel)"
# #                 ], className='btn btn-success', style={'width': '100%'})
# #             ], className='card', style={'flex': '2', 'marginRight': '20px'}),
# #
# #             # Quick Reports
# #             html.Div([
# #                 html.H3("Quick Reports"),
# #                 html.Div([
# #                     html.Button([
# #                         html.I(className="fas fa-file-pdf", style={'marginRight': '10px'}),
# #                         "Monthly Summary"
# #                     ], className='btn btn-primary', style={'marginBottom': '10px', 'width': '100%'}),
# #                     html.Button([
# #                         html.I(className="fas fa-file-excel", style={'marginRight': '10px'}),
# #                         "CFA Performance"
# #                     ], className='btn btn-primary',
# #                         style={'background': '#1e7e34', 'marginBottom': '10px', 'width': '100%'}),
# #                     html.Button([
# #                         html.I(className="fas fa-chart-bar", style={'marginRight': '10px'}),
# #                         "Port Analytics"
# #                     ], className='btn btn-primary',
# #                         style={'background': '#6c757d', 'marginBottom': '10px', 'width': '100%'})
# #                 ])
# #             ], className='card', style={'flex': '1'})
# #         ], style={'display': 'flex'})
# #     ])
# #
# #
# # # --- Callbacks ---
# #
# # # Callback to manage tab switching and content rendering
# # @app.callback(
# #     Output('main-content', 'children'),
# #     Output('active-tab-store', 'data'),
# #     Output('tab-clearing', 'className'),
# #     Output('tab-analytics', 'className'),
# #     Output('tab-tracker', 'className'),
# #     Output('tab-reports', 'className'),
# #     Input('tab-clearing', 'n_clicks'),
# #     Input('tab-analytics', 'n_clicks'),
# #     Input('tab-tracker', 'n_clicks'),
# #     Input('tab-reports', 'n_clicks'),
# #     State('active-tab-store', 'data'),
# #     State('current-step-store', 'data'),
# #     State('consignment-data-store', 'data'),
# #     State('reference-number-store', 'data')
# # )
# # def render_tab_content(clearing_clicks, analytics_clicks, tracker_clicks, reports_clicks,
# #                        active_tab, current_step, consignment_data, reference_number):
# #     ctx = callback_context
# #     button_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else 'tab-clearing'
# #
# #     tabs = {
# #         'tab-clearing': 'clearing',
# #         'tab-analytics': 'analytics',
# #         'tab-tracker': 'tracker',
# #         'tab-reports': 'reports'
# #     }
# #
# #     active_tab = tabs.get(button_id, 'clearing')
# #
# #     class_names = {tab: 'nav-tab' for tab in tabs}
# #     class_names[f'tab-{active_tab}'] = 'nav-tab active'
# #
# #     if active_tab == 'clearing':
# #         content = create_clearing_content(current_step, consignment_data, reference_number)
# #     elif active_tab == 'analytics':
# #         content = create_analytics_content()
# #     elif active_tab == 'tracker':
# #         content = create_tracker_content()
# #     else:
# #         content = create_reports_content()
# #
# #     return content, active_tab, class_names['tab-clearing'], class_names['tab-analytics'], class_names['tab-tracker'], \
# #     class_names['tab-reports']
# #
# #
# # # Callback to manage the clearing process flow
# # @app.callback(
# #     Output('current-step-store', 'data'),
# #     Output('consignment-data-store', 'data'),
# #     Output('reference-number-store', 'data'),
# #     Output('step1-error-message', 'children', allow_duplicate=True),
# #     Input('step1-next-btn', 'n_clicks'),
# #     Input('step2-back-btn', 'n_clicks'),
# #     Input('step2-next-btn', 'n_clicks'),
# #     Input('payment-btn', 'n_clicks'),
# #     Input('step4-next-btn', 'n_clicks'),
# #     Input('start-new-btn', 'n_clicks'),
# #     State('current-step-store', 'data'),
# #     State('consignment-data-store', 'data'),
# #     State('reference-number-store', 'data'),
# #     State('importer-input', 'value'),
# #     State('cfa-dropdown', 'value'),
# #     State('value-input', 'value'),
# #     State('goods-input', 'value'),
# #     prevent_initial_call=True
# # )
# # def manage_clearing_steps(
# #         step1_next, step2_back, step2_next, pay, step4_next, start_new,
# #         current_step, consignment_data, reference_number,
# #         importer, cfa, value, goods
# # ):
# #     ctx = callback_context
# #     if not ctx.triggered:
# #         raise PreventUpdate
# #
# #     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
# #     error_msg = ""
# #
# #     if button_id == 'step1-next-btn':
# #         if not all([importer, cfa, value, goods]):
# #             error_msg = "Please fill out all fields before proceeding."
# #             return dash.no_update, dash.no_update, dash.no_update, error_msg
# #         consignment_data = {'importer': importer, 'cfa': cfa, 'value': value, 'goods': goods}
# #         current_step = 2
# #     elif button_id == 'step2-back-btn':
# #         current_step = 1
# #     elif button_id == 'step2-next-btn':
# #         current_step = 3
# #     elif button_id == 'payment-btn':
# #         reference_number = f"TAFFA-{uuid.uuid4().hex[:8].upper()}"
# #         current_step = 4
# #     elif button_id == 'step4-next-btn':
# #         current_step = 5
# #     elif button_id == 'start-new-btn':
# #         current_step = 1
# #         consignment_data = {}
# #         reference_number = ""
# #
# #     return current_step, consignment_data, reference_number, error_msg
# #
# #
# # # Callback to update the consignment tracker table based on search
# # @app.callback(
# #     Output('consignments-table', 'data'),
# #     Input('search-input', 'value')
# # )
# # def update_table(search_value):
# #     if not search_value:
# #         return df_consignments.sort_values('date', ascending=False).to_dict('records')
# #
# #     search_lower = search_value.lower()
# #
# #     # Search across multiple columns
# #     filtered_df = df_consignments[
# #         df_consignments['consignment_id'].str.lower().contains(search_lower) |
# #         df_consignments['importer'].str.lower().contains(search_lower) |
# #         df_consignments['cfa'].str.lower().contains(search_lower) |
# #         df_consignments['status'].str.lower().contains(search_lower) |
# #         df_consignments['port'].str.lower().contains(search_lower)
# #         ]
# #
# #     return filtered_df.sort_values('date', ascending=False).to_dict('records')
# #
# #
# # # Main entry point
# # if __name__ == '__main__':
# #     app.run(debug=True)
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
# from reportlab.lib.units import inch
# from PIL import Image
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
# import plotly.graph_objects as go
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
#                             dbc.Row([
#                                 dbc.Col(dbc.Card(dbc.CardBody([html.H6("Total Agents"), html.H2("1,250")]))),
#                                 dbc.Col(dbc.Card(dbc.CardBody([html.H6("Active Certifications"), html.H2("980")]))),
#                                 dbc.Col(dbc.Card(dbc.CardBody([html.H6("Compliance Score"), html.H2("85%")]))),
#                             ], className="mb-3"),
#                             html.H5("Quick Actions", className="card-title mt-4"),
#                             dbc.Row([
#                                 dbc.Col(dbc.Button("Update Profile", color="info", className="w-100")),
#                                 dbc.Col(dbc.Button("Upload Documents", color="info", className="w-100")),
#                                 dbc.Col(dbc.Button("View Notifications", color="info", className="w-100")),
#                             ]),
#                         ])),
#                     ]),
#                     dbc.Tab(label="Operations", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Shipments & Cargo Management", className="card-title"),
#                             dbc.Table.from_dataframe(pd.DataFrame({
#                                 "Shipment ID": ["SHP001", "SHP002", "SHP003"],
#                                 "Status": ["Delivered", "Active", "Pending Documents"],
#                                 "Cargo": ["Electronics", "Medical Supplies", "Vehicle Parts"]
#                             }), striped=True, bordered=True, hover=True),
#                         ])),
#                     ]),
#                     dbc.Tab(label="Financials", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Invoicing & Payments", className="card-title"),
#                             dbc.Table.from_dataframe(pd.DataFrame({
#                                 "Invoice No.": ["INV001", "INV002", "INV003"],
#                                 "Amount": ["$5,000", "$2,500", "$1,000"],
#                                 "Status": ["Paid", "Overdue", "Pending"]
#                             }), striped=True, bordered=True, hover=True),
#                         ])),
#                     ]),
#                     dbc.Tab(label="Reporting", children=[
#                         dbc.Card(dbc.CardBody([
#                             html.H5("Analytics & Reports", className="card-title"),
#                             dcc.Graph(figure=go.Figure(
#                                 data=[go.Bar(y=[20, 14, 23, 20], x=['Q1', 'Q2', 'Q3', 'Q4'])],
#                                 layout=go.Layout(title="Revenue by Quarter")
#                             )),
#                             dbc.Button("Export Reports", color="info", className="mt-3")
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
#     app.run(debug=True, port=5543)


# dash_app.py

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
from reportlab.lib.units import inch
from PIL import Image
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
            INSERT INTO agents (tin_number, company_name, contact_person, email, phone, physical_address, postal_address, website, taffa_membership_no, director_1, business_license_no, membership_type, submission_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
        agent_tin, agent_name, contact_person, email, phone, "Dar es Salaam", "P.O. Box 1234", f"www.{agent_name}.com",
        f"TAFFA{i}", f"Ahmed Salum {i}", f"BLN/TZA/{i}", "Ordinary", submission_date))
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
    dcc.Store(id='login-state', data={'is_authenticated': False}),

    dbc.Row([
        dbc.Col(html.Img(src="../assets/LOGO.png", height="100px"), width="auto"),
        dbc.Col(html.H1("Unified TAFFA & CFA Portal", style={'color': '#0d6efd', 'alignSelf': 'center'}),
                width="auto")
    ], style={'marginBottom': '1.5rem', 'marginTop': '1.5rem', 'alignItems': 'center', 'justifyContent': 'center'}),

    dbc.Tabs(id='main-tabs', children=[
        dbc.Tab(label="TAFFA PORTAL", children=[
            dbc.Tabs(id='taffa-tabs', children=[
                dbc.Tab(label="New Application", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Membership Application Form", className="card-title text-primary"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='company-name', placeholder='Company Name *', type='text'), width=6),
                            dbc.Col(dbc.Input(id='tin-number', placeholder='TIN Number *', type='text'), width=6),
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='physical-address', placeholder='Physical/Office Address *', type='text'),
                                width=6),
                            dbc.Col(dbc.Input(id='postal-address', placeholder='Postal Address *', type='text'),
                                    width=6),
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='website', placeholder='Website', type='text'), width=6),
                            dbc.Col(
                                dbc.Input(id='taffa-membership-no', placeholder='TAFFA Membership No. (For Renewals)',
                                          type='text'), width=6),
                        ], className="mb-3"),
                        html.Hr(),
                        html.H4("Contact Person", className="card-title text-primary mt-3"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='contact-person-taffa', placeholder='Contact Person Name *', type='text'),
                                width=4),
                            dbc.Col(dbc.Input(id='email-taffa', placeholder='Email Address *', type='email'), width=4),
                            dbc.Col(dbc.Input(id='phone-taffa', placeholder='Mobile Number *', type='text'), width=4),
                        ], className="mb-3"),
                        html.Hr(),
                        html.H4("Directors", className="card-title text-primary mt-3"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='director-1', placeholder='Director 1 Name *', type='text'), width=4),
                            dbc.Col(dbc.Input(id='director-2', placeholder='Director 2 Name (Optional)', type='text'),
                                    width=4),
                            dbc.Col(dbc.Input(id='director-3', placeholder='Director 3 Name (Optional)', type='text'),
                                    width=4),
                        ], className="mb-3"),
                        html.Hr(),
                        html.H4("Company Details", className="card-title text-primary mt-3"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='cert-incorporation-no', placeholder='Certificate of Incorporation No. *',
                                          type='text'), width=6),
                            dbc.Col(dbc.Input(id='business-license-no-taffa', placeholder='Business License No. *',
                                              type='text'),
                                    width=6),
                        ], className="mb-3"),
                        dcc.Dropdown(id='membership-type', options=[
                            {'label': 'Ordinary Member', 'value': 'Ordinary'},
                            {'label': 'Inhouse Member', 'value': 'Inhouse'}
                        ], placeholder="Choose Membership Type *", className="mb-3"),
                        html.Hr(),
                        html.H4("Compliance Details (For Verification)", className="card-title text-primary mt-3"),
                        dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(id='tax-compliance', options=[{'label': 'Compliant', 'value': 'Compliant'},
                                                                           {'label': 'Non-Compliant',
                                                                            'value': 'Non-Compliant'}],
                                             placeholder="Tax Compliance Status"), width=6),
                            dbc.Col(
                                dcc.Dropdown(id='taffa-status', options=[{'label': 'Active Member', 'value': 'Active'},
                                                                         {'label': 'Inactive/Expired',
                                                                          'value': 'Inactive'}],
                                             placeholder="TAFFA Membership Status"), width=6),
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='policy-compliance',
                                                 options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
                                                          {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
                                                 placeholder="Policy Compliance Status"), width=6),
                            dbc.Col(dcc.Dropdown(id='payment-confirmation', options=[{'label': 'Paid', 'value': 'Paid'},
                                                                                     {'label': 'Unpaid',
                                                                                      'value': 'Unpaid'}],
                                                 placeholder="Accreditation Fee Payment", value="Unpaid"), width=4),
                            dbc.Col(dbc.Button("Pay Accreditation Fee", id="pay-button", color="success"), width=2)
                        ], className="mb-3 align-items-center"),
                        html.Hr(),
                        dcc.Checklist(options=[
                            {'label': ' I have read and agree to the Taffa Constitution and Taffa Regulations',
                             'value': 1}],
                            id='agree-terms', className="mt-4"),
                        html.Div(
                            dbc.Button('Submit Application', id='submit-button', n_clicks=0, color="primary", size="lg",
                                       className="mt-4"), className="text-center"),
                        html.Div(id='submission-output', className="mt-4")
                    ]))
                ]),
                dbc.Tab(label="TAFFA ID Application", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("TAFFA ID Application", className="card-title text-primary"),
                        html.P("This form is for TAFFA members to apply for an ID card."),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='id-full-name', placeholder='Full Name *', type='text'), width=6),
                            dbc.Col(dbc.Input(id='id-nida-number', placeholder='NIDA Number *', type='text'), width=6),
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='id-position', placeholder='Position *', type='text'), width=6),
                            dbc.Col(
                                [dcc.Upload(id='upload-passport-photo', children=html.Button('Upload Passport Photo *'),
                                            className="w-100 mb-2"), html.Span(id='output-passport-photo')]),
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(
                                [dcc.Upload(id='upload-id-payment', children=html.Button('Upload ID Payment Proof *'),
                                            className="w-100 mb-2"), html.Span(id='output-id-payment')]),
                        ], className="mb-3"),
                        dbc.Input(id='id-application-tin', placeholder='Your Company TIN *', type='text',
                                  className="mb-3"),
                        dbc.Button('Submit ID Application', id='submit-id-button', n_clicks=0, color="primary",
                                   size="lg",
                                   className="mt-4"),
                        html.Div(id='id-submission-output', className="mt-4")
                    ]))
                ]),
                dbc.Tab(label="Renew Membership", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Renew Membership", className="card-title text-primary"),
                        html.P("Use this form to renew your annual membership and update company details."),
                        dbc.Row([
                            dbc.Col(dbc.Input(id='renew-tin-number', placeholder='Your Company TIN *', type='text'),
                                    width=6),
                            dbc.Col(
                                dbc.Input(id='renew-taffa-no', placeholder='Your TAFFA Membership No. *', type='text'),
                                width=6),
                        ], className="mb-3"),
                        html.Hr(),
                        html.H4("Compliance Details (For Renewal Verification)",
                                className="card-title text-primary mt-3"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='renew-tax-compliance',
                                                 options=[{'label': 'Compliant', 'value': 'Compliant'},
                                                          {'label': 'Non-Compliant', 'value': 'Non-Compliant'}],
                                                 placeholder="Tax Compliance Status"), width=6),
                            dbc.Col(dcc.Dropdown(id='renew-taffa-status',
                                                 options=[{'label': 'Active Member', 'value': 'Active'},
                                                          {'label': 'Inactive/Expired', 'value': 'Inactive'}],
                                                 placeholder="TAFFA Membership Status"), width=6),
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col(dcc.Dropdown(id='renew-policy-compliance',
                                                 options=[{'label': 'Fully Compliant', 'value': 'Compliant'},
                                                          {'label': 'Minor Infractions', 'value': 'Minor Infractions'}],
                                                 placeholder="Policy Compliance Status"), width=6),
                            dbc.Col(dcc.Dropdown(id='renew-payment-confirmation',
                                                 options=[{'label': 'Paid', 'value': 'Paid'},
                                                          {'label': 'Unpaid',
                                                           'value': 'Unpaid'}],
                                                 placeholder="Renewal Fee Payment", value="Unpaid"), width=4),
                            dbc.Col(dbc.Button("Pay Renewal Fee", id="renew-pay-button", color="success"), width=2)
                        ], className="mb-3 align-items-center"),
                        html.Hr(),
                        html.H4("Document Upload (Renewal)", className="card-title text-primary mt-4"),
                        dbc.Row([
                            dbc.Col([dcc.Upload(id='renew-upload-cert-incorporation',
                                                children=html.Button('Cert of Incorporation *'),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-cert-incorporation')]),
                            dbc.Col([dcc.Upload(id='renew-upload-business-license',
                                                children=html.Button('Business License *'),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-business-license')]),
                            dbc.Col(
                                [dcc.Upload(id='renew-upload-brella-search', children=html.Button('Brella Search *'),
                                            className="w-100 mb-2"), html.Span(id='renew-output-brella-search')]),
                            dbc.Col([dcc.Upload(id='renew-upload-directors-images',
                                                children=html.Button('Directors Images *'),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-directors-images')]),
                        ]),
                        dbc.Row([
                            dbc.Col(
                                [dcc.Upload(id='renew-upload-tax-clearance', children=html.Button('Tax Clearance Cert'),
                                            className="w-100 mb-2"), html.Span(id='renew-output-tax-clearance')]),
                            dbc.Col([dcc.Upload(id='renew-upload-taffa-cert', children=html.Button('TAFFA Certificate'),
                                                className="w-100 mb-2"), html.Span(id='renew-output-taffa-cert')]),
                            dbc.Col(
                                [dcc.Upload(id='renew-upload-memo-articles', children=html.Button('Memo & Articles'),
                                            className="w-100 mb-2"), html.Span(id='renew-output-memo-articles')]),
                            dbc.Col([dcc.Upload(id='renew-upload-audited-accounts',
                                                children=html.Button('Audited Accounts'),
                                                className="w-100 mb-2"),
                                     html.Span(id='renew-output-audited-accounts')]),
                        ]),
                        html.Div(
                            dbc.Button('Submit Renewal', id='submit-renewal-button', n_clicks=0, color="primary",
                                       size="lg",
                                       className="mt-4"), className="text-center"),
                        html.Div(id='renewal-submission-output', className="mt-4")
                    ]))
                ]),
                dbc.Tab(label="View Submissions", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Submitted Applications", className="card-title"),
                        dash_table.DataTable(
                            id='applications-table',
                            columns=[
                                {"name": "TIN", "id": "tin_number"},
                                {"name": "Company Name", "id": "company_name"},
                                {"name": "Submission Date", "id": "submission_date"},
                                {"name": "Status", "id": "status"},
                                {"name": "Reference Number", "id": "reference_number"},
                            ],
                            style_cell={'textAlign': 'left'},
                        ),
                        dbc.Button("Refresh Data", id="refresh-button", className="mt-3")
                    ]))
                ]),
                dbc.Tab(label="Client & Document Submission", children=[
                    dbc.Card(
                        dbc.CardBody([
                            html.H1("Tanzania CFA Portal", className="text-center my-4"),
                            html.P("Client & Document Submission", className="text-center text-muted"),
                            html.Hr(),
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("1. Client Information", className="card-title"),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Client Company Name"),
                                            dbc.Input(id="client-name", type="text", placeholder="e.g., ABC Logistics")
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Client TIN"),
                                            dbc.Input(id="client-tin", type="text", placeholder="e.g., 123-456-789")
                                        ], className="mb-3")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Business License No."),
                                            dbc.Input(id="biz-license", type="text", placeholder="e.g., BLN/XYZ/001")
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Primary Contact"),
                                            dbc.Input(id="contact-person", type="text", placeholder="e.g., Jane Doe")
                                        ], className="mb-3")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Contact Phone"),
                                            dbc.Input(id="contact-phone", type="tel",
                                                      placeholder="e.g., +255-7XX-XXX-XXX")
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Email Address"),
                                            dbc.Input(id="email", type="email", placeholder="e.g., jane@example.com")
                                        ], className="mb-3")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("TAFFA Agent ID"),
                                            dcc.Dropdown(
                                                id="taffa-agent-id",
                                                options=[{"label": "DFO001", "value": "DFO001"},
                                                         {"label": "DFO002", "value": "DFO002"},
                                                         {"label": "DFO003", "value": "DFO003"}],
                                                placeholder="Select your TAFFA Agent ID"
                                            )
                                        ], className="mb-3")),
                                        dbc.Col(dcc.Upload(
                                            id='upload-authorization',
                                            children=html.Div([
                                                'Drag and Drop or ',
                                                html.A('Select Authorization Letter')
                                            ]),
                                            style={
                                                'width': '100%',
                                                'height': '60px',
                                                'lineHeight': '60px',
                                                'borderWidth': '1px',
                                                'borderStyle': 'dashed',
                                                'borderRadius': '5px',
                                                'textAlign': 'center',
                                                'margin': '10px 0'
                                            },
                                            multiple=False
                                        )),
                                    ])
                                ])
                            ),
                            dbc.Card(
                                dbc.CardBody([
                                    html.H4("2. Shipment Details", className="card-title"),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Type of Shipment"),
                                            dcc.Dropdown(
                                                id="shipment-type",
                                                options=[{"label": "Import", "value": "Import"},
                                                         {"label": "Export", "value": "Export"}],
                                                placeholder="Select type"
                                            )
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Bill of Lading / AWB No."),
                                            dbc.Input(id="bl-awb-no", type="text", placeholder="e.g., BLAWB12345")
                                        ], className="mb-3")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Commercial Invoice No."),
                                            dbc.Input(id="invoice-no", type="text", placeholder="e.g., INV-00123")
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Shipper/Consignor Name"),
                                            dbc.Input(id="shipper-name", type="text",
                                                      placeholder="e.g., Global Exporters Inc.")
                                        ], className="mb-3")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Origin Port/Country"),
                                            dbc.Input(id="origin-port", type="text",
                                                      placeholder="e.g., Shanghai, China")
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Destination Port/Country"),
                                            dbc.Input(id="destination-port", type="text",
                                                      placeholder="e.g., Dar es Salaam, Tanzania")
                                        ], className="mb-3")),
                                    ]),
                                    dbc.Row([
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Date of Arrival"),
                                            dcc.DatePickerSingle(
                                                id='arrival-date',
                                                placeholder='Select a date'
                                            )
                                        ], className="mb-3")),
                                        dbc.Col(dbc.InputGroup([
                                            dbc.InputGroupText("Cargo Description"),
                                            dbc.Input(id="cargo-desc", type="text",
                                                      placeholder="e.g., 200 boxes of electronics")
                                        ], className="mb-3")),
                                    ])
                                ]), className="mt-4"),
                            dbc.Row(dbc.Col(
                                dbc.Button("Generate URN & Submit Consignment", id="generate-urn-btn", color="primary",
                                           className="mt-4 w-100"),
                                width=6, className="mx-auto"
                            )),
                            dbc.Modal([
                                dbc.ModalHeader(dbc.ModalTitle("URN Generated Successfully!")),
                                dbc.ModalBody(
                                    html.Div([
                                        html.P("Your Unique Reference Number is:", className="text-center"),
                                        html.H2(id="urn-output", className="text-center text-primary fw-bold"),
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
                        ])
                    )
                ]),
            ])
        ]),
        dbc.Tab(label="ADMIN LOGIN", children=[
            dcc.Store(id='admin-login-state', data={'is_authenticated': False}),
            html.Div(id="admin-content-container", children=[
                dbc.Card(dbc.CardBody([
                    html.H4("Admin Login", className="card-title"),
                    dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
                    dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
                    dbc.Button("Login", id="admin-login-button", color="primary"),
                    dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
                ]))
            ])
        ], id="admin-main-tab")
    ]),
    dbc.Popover(
        [
            dbc.PopoverHeader("Capital Pay Engine"),
            dbc.PopoverBody(
                html.Div([
                    dbc.Button("Pay with Equity Bank", id="pay-equity-btn", color="primary", className="d-block mb-2"),
                    dbc.Button("Pay with NBC Bank", id="pay-nbc-btn", color="primary", className="d-block mb-2"),
                    dbc.Button("Pay with M-Pesa", id="pay-mpesa-btn", color="primary", className="d-block")
                ])
            ),
        ],
        id="payment-method-popover",
        target="",
        trigger="manual",
    ),
    dbc.Popover(
        dbc.PopoverBody("Payment of 20,000 TZS successful!", className="text-success"),
        id="payment-success-popover",
        target="",
        trigger="manual",
    ),
    dcc.Interval(
        id='interval-popover',
        interval=5 * 1000,
        n_intervals=0,
        disabled=True,
    ),
], fluid=True)


# --- Callbacks for Client & Document Submission ---

@app.callback(
    Output("urn-modal", "is_open"),
    Output("urn-output", "children"),
    Input("generate-urn-btn", "n_clicks"),
    State("taffa-agent-id", "value"),
    State("client-tin", "value"),
    State("bl-awb-no", "value"),
    State("client-name", "value"),
    State("shipper-name", "value"),
    State("origin-port", "value"),
    State("destination-port", "value"),
    State("cargo-desc", "value"),
    State("arrival-date", "date"),
    prevent_initial_call=True
)
def generate_urn(n_clicks, taffa_agent_id, client_tin, bl_awb_no, client_name, shipper_name, origin_port,
                 destination_port, cargo_desc, arrival_date):
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
            html.H3("Admin Dashboard", className="text-center my-4"),
            dbc.Button("Logout", id="admin-logout-btn", color="danger", className="float-end"),
            dbc.Tabs([
                dbc.Tab(label="Overview", children=[
                    dbc.Card(dbc.CardBody([
                        html.H5("Key Performance Indicators (KPIs)", className="card-title"),
                        dbc.Row([
                            dbc.Col(dbc.Card(dbc.CardBody(
                                [html.H6("Total Agents"), html.H2(id="kpi-total-agents", className="text-center")]))),
                            dbc.Col(dbc.Card(dbc.CardBody([html.H6("Active Certifications"),
                                                           html.H2(id="kpi-active-certs", className="text-center")]))),
                            dbc.Col(dbc.Card(dbc.CardBody([html.H6("New Applications (30 Days)"),
                                                           html.H2(id="kpi-new-apps", className="text-center")]))),
                        ], className="mb-3"),
                        dcc.Graph(id="membership-status-pie-chart")
                    ]))
                ]),
                dbc.Tab(label="Verification", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Verify Applications", className="card-title"),
                        dash_table.DataTable(
                            id='admin-table',
                            columns=[
                                {"name": "App ID", "id": "id"},
                                {"name": "TIN", "id": "tin_number"},
                                {"name": "Company Name", "id": "company_name"},
                                {"name": "Status", "id": "status"},
                            ],
                            style_cell={'textAlign': 'left'},
                            row_selectable='single',
                        ),
                        dbc.Button("Refresh Admin Data", id="admin-refresh-button", className="mt-3"),
                        html.Hr(),
                        html.Div(id='admin-details-view')
                    ]))
                ]),
                dbc.Tab(label="Consignment Tracker", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Master Consignment Tracker", className="card-title text-primary"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Input(id='tracker-search-bar', placeholder='Search by URN, BL/AWB, or Client...',
                                          type='text'), width=6),
                            dbc.Col(dcc.DatePickerRange(id='tracker-date-range',
                                                        start_date=date.today() - timedelta(days=30),
                                                        end_date=date.today()), width=4),
                            dbc.Col(dbc.Button("Search", id="tracker-search-btn", color="primary"), width=2)
                        ], className="mb-3"),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("Total Consignments", className="card-title"),
                                        html.H2(id="total-consignments-kpi", className="text-center text-primary"),
                                    ])
                                ), width=4
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("In Transit", className="card-title"),
                                        html.H2(id="in-transit-kpi", className="text-center text-warning"),
                                    ])
                                ), width=4
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody([
                                        html.H6("Cleared", className="card-title"),
                                        html.H2(id="cleared-kpi", className="text-center text-success"),
                                    ])
                                ), width=4
                            )
                        ], className="mb-4"),
                        dbc.Row([
                            dbc.Col(dcc.Graph(id='consignment-status-pie'), width=6),
                            dbc.Col(dcc.Graph(id='cargo-type-bar'), width=6)
                        ], className="mb-4"),
                        html.Div([
                            html.H5("Consignment List", className="mt-4"),
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
                                sort_action="native",
                                page_action="native",
                                page_size=10,
                                row_selectable='single'
                            ),
                            html.Div(id='consignment-details-view', className="mt-3")
                        ])
                    ]))
                ]),
                dbc.Tab(label="View Submissions", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Submitted Applications", className="card-title"),
                        dash_table.DataTable(
                            id='admin-applications-table',
                            columns=[
                                {"name": "TIN", "id": "tin_number"},
                                {"name": "Company Name", "id": "company_name"},
                                {"name": "Submission Date", "id": "submission_date"},
                                {"name": "Status", "id": "status"},
                                {"name": "Reference Number", "id": "reference_number"},
                            ],
                            style_cell={'textAlign': 'left'},
                        ),
                        dbc.Button("Refresh Submissions", id="admin-refresh-submissions-btn", className="mt-3")
                    ]))
                ]),
                dbc.Tab(label="Financials", children=[
                    dbc.Card(dbc.CardBody([
                        html.H4("Financials", className="card-title"),
                        dbc.Row([
                            dbc.Col(
                                dbc.Card(dbc.CardBody([html.H6("Total Revenue"),
                                                       html.H2(id="kpi-total-revenue", className="text-center")])),
                                width=6
                            ),
                            dbc.Col(
                                dbc.Card(dbc.CardBody([html.H6("Pending Invoices"),
                                                       html.H2(id="kpi-pending-invoices", className="text-center")])),
                                width=6
                            )
                        ], className="mb-4"),
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
                        html.H5("Invoice List", className="mt-4"),
                        dash_table.DataTable(
                            id='invoices-table',
                            columns=[
                                {"name": "Invoice Number", "id": "invoice_number"},
                                {"name": "Amount", "id": "amount"},
                                {"name": "Status", "id": "status"},
                                {"name": "Company Name", "id": "company_name"}
                            ],
                            style_table={'overflowX': 'auto'},
                        )
                    ]))
                ])
            ])
        ]
    else:
        return [
            dbc.Card(dbc.CardBody([
                html.H4("Admin Login", className="card-title"),
                dbc.Input(id='admin-username', placeholder='Username', type='text', className="mb-3"),
                dbc.Input(id='admin-password', placeholder='Password', type='password', className="mb-3"),
                dbc.Button("Login", id="admin-login-button", color="primary"),
                dbc.Alert(id='admin-login-alert', color="danger", is_open=False, className="mt-3")
            ]))
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
        return dbc.Alert("Please fill all fields marked with * and agree to the terms.", color="danger")
    if not agreed:
        return dbc.Alert("You must agree to the Taffa Constitution and Regulations.", color="warning")
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
        return dbc.Alert("Membership application submitted successfully!", color="success")
    except sqlite3.IntegrityError:
        return dbc.Alert(f"An application for TIN {tin} already exists.", color="danger")
    except Exception as e:
        return dbc.Alert(f"An error occurred: {e}", color="danger")
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
        return dbc.Alert("Please fill all fields and upload required documents.", color="danger")
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id FROM agents WHERE tin_number = ?", (tin,))
        agent_id_result = c.fetchone()
        if not agent_id_result:
            return dbc.Alert(f"No existing TAFFA member found with TIN {tin}.", color="danger")
        agent_id = agent_id_result['id']
        c.execute("SELECT id FROM applications WHERE agent_id = ? ORDER BY id DESC LIMIT 1", (agent_id,))
        application_id_result = c.fetchone()
        if not application_id_result:
            return dbc.Alert(f"No completed membership application found for TIN {tin}.", color="danger")
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
            dbc.Alert("ID card application submitted successfully!", color="success"),
            html.Div(download_link, className="mt-2")
        ]
    except Exception as e:
        return dbc.Alert(f"An error occurred: {e}", color="danger")
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
                    dbc.CardHeader("Company & Contact Information"),
                    dbc.CardBody([
                        html.P([html.Strong("Company Name: "), data['company_name']]),
                        html.P([html.Strong("TIN Number: "), data['tin_number']]),
                        html.P([html.Strong("Physical Address: "), data['physical_address']]),
                        html.P([html.Strong("Contact Person: "), data['contact_person']]),
                        html.P([html.Strong("Email: "), data['email']]),
                        html.P([html.Strong("Phone: "), data['phone']]),
                    ])
                ]),
                dbc.Card([
                    dbc.CardHeader("Director Information"),
                    dbc.CardBody([
                        html.P([html.Strong("Director 1: "), data['director_1']]),
                        html.P([html.Strong("Director 2: "), data['director_2'] or "N/A"]),
                        html.P([html.Strong("Director 3: "), data['director_3'] or "N/A"]),
                    ])
                ], className="mt-3"),
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Compliance & Verification"),
                    dbc.CardBody([
                        html.P([html.Strong("Tax Compliance: "), data['tax_compliance'] or "Not Provided"]),
                        html.P([html.Strong("TAFFA Status: "), data['taffa_status'] or "Not Provided"]),
                        html.P([html.Strong("Policy Compliance: "), data['policy_compliance'] or "Not Provided"]),
                        html.P([html.Strong("Payment Confirmation: "), data['payment_confirmation']]),
                        html.P([html.Strong("Current Status: "),
                                html.Strong(data['status'], className=f"text-{status_color}")])
                    ])
                ]),
                dbc.Card([
                    dbc.CardHeader("Uploaded Documents (Membership)"),
                    dbc.CardBody(document_links)
                ], className="mt-3"),
                dbc.Card([
                    dbc.CardHeader("Actions (Membership)"),
                    dbc.CardBody([
                        html.H5("Update Status for Selected Application"),
                        dcc.Dropdown(id='admin-status-dropdown', options=[{'label': 'Verified', 'value': 'Verified'},
                                                                          {'label': 'Cancelled', 'value': 'Cancelled'}],
                                     placeholder="Select new status"),
                        dbc.Button("Update Status", id="admin-update-button", color="success", className="mt-2"),
                        dbc.Button("Generate Certificate", id="generate-cert-button", color="info",
                                   className="mt-2 ms-2", disabled=data['status'] != 'Verified'),
                        html.Div(id="download-cert-link-div", className="mt-2"),
                        html.Div(id='admin-update-output', className="mt-3")
                    ])
                ], className="mt-3"),
            ], width=6),
        ], className="mt-4")
    ]
    id_card_links = []
    if not id_applications.empty:
        id_card_details = [html.Hr(), html.H5("ID Card Applications", className="card-title")]
        for index, row in id_applications.iterrows():
            id_app_id = row['id']
            id_card_details.append(html.P(html.Strong(f"ID for: {row['full_name']}")))
            id_card_details.append(dcc.Link("Download Passport Photo",
                                            href=f"/download-file/{data['agent_id']}/{os.path.basename(row['passport_photo'])}",
                                            className="d-block"))
            id_card_details.append(dcc.Link("Download ID Payment Proof",
                                            href=f"/download-file/{data['agent_id']}/{os.path.basename(row['id_payment_proof'])}",
                                            className="d-block"))
            id_card_details.append(html.P([html.Strong("ID Status: "), row['id_status']]))
            if row['id_status'] == 'Verified':
                id_card_details.append(
                    dcc.Link("Download ID Card", href=f"/download-id/{id_app_id}", download="TAFFA_ID.pdf",
                             target="_blank", className="btn btn-primary mt-2"))
            else:
                id_card_details.append(
                    dbc.Button("Verify ID Application", id={"type": "verify-id-button", "index": str(id_app_id)},
                               color="success", className="mt-2"))
            id_card_details.append(html.Hr())
        id_card_links = id_card_details
    else:
        id_card_links = html.Div([html.P("No ID Application submitted for this company.")])
    details_layout.append(
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader("ID Application Documents"),
                    dbc.CardBody(id_card_links)
                ], className="mt-3"),
                width=12
            )
        ])
    )
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
                          color="success"),
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
                             color="warning")
    except Exception as e:
        return dbc.Alert(f"Error updating status: {e}", color="danger")
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
    if os.path.exists(taffa_logo_path):
        c.drawImage(taffa_logo_path, 30, height - 150, width=150, height=150, preserveAspectRatio=True, mask='auto')
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.black)
    c.drawRightString(width - 50, height - 110, f"No. {random.randint(1000, 9999)}")
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#003366'))
    c.drawCentredString(width / 2.0, height - 200, "CERTIFICATE OF MEMBERSHIP")
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2.0, height - 250, "CERTIFICATE IS AWARDED TO")
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2.0, height - 280, app_data['company_name'].upper())
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2.0, height - 320,
                        f"as a Tanzania Freight Forwarder Association Member for {date.today().year}")
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
    c.setStrokeColor(colors.HexColor('#003366'))
    c.setLineWidth(5)
    c.roundRect(x_offset, y_offset, card_width, card_height, 10, stroke=1, fill=0)
    header_height = card_height * 0.2
    c.setFillColor(colors.HexColor('#F0F8FF'))
    c.rect(x_offset, y_offset + card_height - header_height, card_width, header_height, fill=1, stroke=0)
    taffa_logo_path = os.path.join(BASE_DIR, "assets", "LOGO.png")
    if os.path.exists(taffa_logo_path):
        c.drawImage(taffa_logo_path, x_offset + 20, y_offset + card_height - header_height + 10, width=80, height=80,
                    preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor('#003366'))
    c.drawCentredString(x_offset + card_width / 2, y_offset + card_height - 50,
                        "TANZANIA FREIGHT FORWARDERS ASSOCIATION")
    photo_path = id_app_data['passport_photo']
    photo_size = card_width * 0.3
    photo_x = x_offset + (card_width - photo_size) / 2
    photo_y = y_offset + card_height - header_height - 10 - photo_size
    if os.path.exists(photo_path):
        c.drawImage(photo_path, photo_x, photo_y, width=photo_size, height=photo_size, preserveAspectRatio=True)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    details_y = photo_y - 30
    content_center_x = x_offset + card_width / 2
    c.drawCentredString(content_center_x, details_y, f"Name: {id_app_data['full_name']}")
    c.drawCentredString(content_center_x, details_y - 20, f"Position: {id_app_data['position']}")
    c.drawCentredString(content_center_x, details_y - 40, f"Company: {agent_data['company_name']}")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#003366'))
    id_y_start = details_y - 80
    c.drawCentredString(content_center_x, id_y_start, f"ID NO: {id_app_data['id_number']}")
    c.drawCentredString(content_center_x, id_y_start - 20, f"Expiry Date: {id_app_data['expiry_date']}")
    qr_data = f"ID: {id_app_data['id_number']} | Expiry: {id_app_data['expiry_date']}"
    qr_img = qrcode.make(qr_data)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_size = card_width * 0.25
    qr_x = content_center_x - qr_size / 2
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
        return dbc.Alert("Could not find application data.", color="danger")
    app_data = df.to_dict('records')[0]
    filename = generate_membership_certificate(app_data)
    return dcc.Link(f"Download Certificate for {app_data['company_name']}",
                    href=f"/download-cert/{os.path.basename(filename)}")


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
    conn.close()

    invoices_df = pd.merge(invoices_df, agents_df, left_on='agent_id', right_on='id', how='left')

    total_revenue = invoices_df[invoices_df['status'] == 'Paid']['amount'].sum()
    pending_invoices = invoices_df[invoices_df['status'] == 'Pending']['amount'].sum()

    invoice_status_counts = invoices_df['status'].value_counts().reset_index()
    invoice_status_counts.columns = ['Status', 'Count']
    revenue_pie = px.pie(invoice_status_counts, values='Count', names='Status', title='Invoices by Status')

    payments_by_type = payments_df['payment_type'].value_counts().reset_index()
    payments_by_type.columns = ['Payment Type', 'Count']
    payments_bar = px.bar(payments_by_type, x='Payment Type', y='Count', title='Payments by Type')

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
        Input('generate-urn-btn', 'n_clicks')
    ]
)
def update_consignment_dashboard(n_clicks, search_term, start_date, end_date, urn_clicks):
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
            html.H5(f"Consignment Details: {row['urn']}", className="card-title"),
            html.P([html.Strong("Client Company: "), row['client_company']]),
            html.P([html.Strong("TAFFA Agent ID: "), row['taffa_agent_id']]),
            html.P([html.Strong("Bill of Lading / AWB No.: "), row['bl_awb_no']]),
            html.P([html.Strong("Shipper/Consignor: "), row['shipper_name']]),
            html.P([html.Strong("Origin: "), row['origin_port']]),
            html.P([html.Strong("Destination: "), row['destination_port']]),
            html.P([html.Strong("Cargo Description: "), row['cargo_desc']]),
            html.P([html.Strong("Status: "), html.Span(row['status'], className=f"badge rounded-pill bg-{'warning' if row['status'] == 'In Transit' else 'success' if row['status'] == 'Cleared' else 'info'}")])
        ]),
        className="mt-3"
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
    app.run(debug=True, port=5543)