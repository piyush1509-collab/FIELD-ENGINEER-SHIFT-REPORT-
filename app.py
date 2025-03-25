from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# ✅ Correctly locate 'credentials.json' within the GitHub repository
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')

# Check if the credentials file exists
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_PATH}")

# Define Google Sheets API scopes
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Authenticate using the service account credentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPES)
client = gspread.authorize(credentials)

# Open the Google Sheet by its key
SHEET_ID = '1LegE5pSPl06OTynxjIxqzGVEtdiiDh8uBQc-k35Upys'  # Replace with actual Google Sheet ID
sheet = client.open_by_key(SHEET_ID)

# Ensure correct mapping of area names to Google Sheets tab names
# Ensure correct mapping of area names to Google Sheets tab names
AREA_MAPPING = {
    "Furnace": "Furnace",
    "Pump-House": "Pump House",
    "Gas-Zone": "Gas Zone",
    "Dispatch": "Dispatch",
    "Material-Handling": "Material Handling"
}

def store_data(area, date, engineer, technician, description, shift, seal_pot_data):
   def store_data(area, date, engineer, technician, description, shift, seal_pot_data):
    area = area.replace(".html", "").replace("-", " ").title()  # ✅ Fix capitalization & spacing

    if area in AREA_MAPPING:
        area = AREA_MAPPING[area]  # Convert to correct Google Sheet tab name

    try:
        worksheet = sheet.worksheet(area)  # ✅ Get the correct sheet
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{area}' not found in Google Sheets. Make sure the sheet name is correct.")

    # ✅ Prepare row with seal pot data
    row_data = [date, engineer, technician, description, shift] + seal_pot_data
    worksheet.append_row(row_data)  # ✅ Append data to Google Sheets

    area = area.replace(".html", "").replace("-", " ").title()  # ✅ Fix capitalization & spacing

    if area in AREA_MAPPING:
        area = AREA_MAPPING[area]  # Convert to correct Google Sheet tab name

    try:
        worksheet = sheet.worksheet(area)  # ✅ Get the correct sheet
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{area}' not found in Google Sheets. Make sure the sheet name is correct.")

    worksheet.append_row([date, engineer, technician, description, shift])  # ✅ Append data
    
from flask import send_from_directory

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Routes for each area
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/<area>", methods=["GET", "POST"])
def report(area):
    if request.method == "POST":
        date = request.form.get("date")
        engineer = request.form.get("engineer")
        technician = request.form.get("technician")
        description = request.form.get("description")
        shift = request.form.get("shift")

        # ✅ Capture seal pot data from the form
        seal_pot_data = [
            request.form.get("corex_gas"),
            request.form.get("cog_top"),
            request.form.get("fabric_filter"),
            request.form.get("psa_header"),
            request.form.get("rgc_suction"),
            request.form.get("rgc_discharge"),
            request.form.get("rgc_condensate"),
        ]

        # ✅ Pass new data to store_data function
        store_data(area, date, engineer, technician, description, shift, seal_pot_data)

        return f"<h2>Report submitted successfully for {area}.</h2>"

    # ✅ Fix: Ensure `.html` is not added twice
    if not area.endswith(".html"):
        template_name = f"{area}.html"
    else:
        template_name = area  # Already has `.html`

    return render_template(template_name)

    if request.method == "POST":
        date = request.form.get("date")
        engineer = request.form.get("engineer")
        technician = request.form.get("technician")
        description = request.form.get("description")
        shift = request.form.get("shift")

        store_data(area, date, engineer, technician, description, shift)

        return f"<h2>Report submitted successfully for {area}.</h2>"

    # ✅ Fix: Ensure `.html` is not added twice
    if not area.endswith(".html"):
        template_name = f"{area}.html"
    else:
        template_name = area  # Already has `.html`

    return render_template(template_name)


if __name__ == "__main__":
    app.run(debug=True)
