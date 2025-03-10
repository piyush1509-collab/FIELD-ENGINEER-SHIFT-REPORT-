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

# Function to store data in the correct sheet
def store_data(area, date, engineer, technician, description, shift):
    area = area.replace(".html", "")  # ✅ Remove `.html` from the sheet name
    try:
        worksheet = sheet.worksheet(area)  # Get the correct sheet (Furnace, Pump House, etc.)
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{area}' not found in Google Sheets")

    worksheet.append_row([date, engineer, technician, description, shift])  # Append data

    
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

        store_data(area, date, engineer, technician, description, shift)
        return redirect(url_for("home"))

    # ✅ Fix: Prevent `.html.html` duplication
    if not area.endswith(".html"):
        template_name = f"{area}.html"
    else:
        template_name = area  # Already has `.html`

    return render_template(template_name)

if __name__ == "__main__":
    app.run(debug=True)
