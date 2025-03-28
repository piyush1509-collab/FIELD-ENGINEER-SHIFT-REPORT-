from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# Correct path for credentials
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')

# Check if credentials.json exists
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_PATH}")

# Google Sheets API setup
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPES)
client = gspread.authorize(credentials)

# Google Sheet ID
SHEET_ID = '1LegE5pSPl06OTynxjIxqzGVEtdiiDh8uBQc-k35Upys'  # Correct Sheet ID
sheet = client.open_by_key(SHEET_ID)

# Map area names to Google Sheets tab names
AREA_MAPPING = {
    "Furnace": "Furnace",
    "Pump-House": "Pump House",
    "Gas-Zone": "Gas Zone",
    "Dispatch": "Dispatch",
    "Material-Handling": "Material Handling"
}

# Function to store data into the respective Google Sheet tab
def store_data(area, date, engineer, technician, description, shift, seal_pot_data):
    area = area.replace(".html", "").replace("-", " ").title()
    if area in AREA_MAPPING:
        area = AREA_MAPPING[area]
    try:
        worksheet = sheet.worksheet(area)
    except gspread.exceptions.WorksheetNotFound:
        raise ValueError(f"Worksheet '{area}' not found. Check the sheet name.")
    
    # Append the data in the correct worksheet
    worksheet.append_row([date, engineer, technician, description, shift] + seal_pot_data)


# Handle favicon requests
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle reports for different sections
@app.route("/<area>", methods=["GET", "POST"])
def report(area):
    if request.method == "POST":
        date = request.form.get("date")
        engineer = request.form.get("engineer")
        technician = request.form.get("technician")
        description = request.form.get("description")
        shift = request.form.get("shift")

                # Capture seal pot data and additional data from form
        seal_pot_data = [
            request.form.get("corex_gas"),
            request.form.get("cog_top"),
            request.form.get("fabric_filter"),
            request.form.get("psa_header"),
            request.form.get("rgc_suction"),
            request.form.get("rgc_discharge"),
            request.form.get("rgc_condensate"),

            # Equipment Running Status Data
            request.form.get("egc_01"), request.form.get("egc_02"), request.form.get("egc_03"),
            request.form.get("rgc_01"), request.form.get("rgc_02"), request.form.get("tgb"),
            request.form.get("cogc"), request.form.get("psa_01"), request.form.get("psa_02"), request.form.get("psa_03"),

            # Heat Tracing Healthyness Data
            request.form.get("ht_egc_01"), request.form.get("ht_egc_02"), request.form.get("ht_egc_03"),
            request.form.get("ht_psa_header"), request.form.get("ht_psa_01"), request.form.get("ht_psa_02"), request.form.get("ht_psa_03")
        ]


        # Store the form data
        store_data(area, date, engineer, technician, description, shift, seal_pot_data)

        return f"<h2>Report submitted successfully for {area}.</h2>"

    # Ensure correct template is rendered
    if not area.endswith(".html"):
        template_name = f"{area}.html"
    else:
        template_name = area

    return render_template(template_name)

# Error handling for 404
@app.errorhandler(404)
def page_not_found(e):
    return "<h2>Page not found. Check the URL.</h2>", 404

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)

