from flask import Flask, render_template, request, redirect, url_for
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# ✅ Correct path inside your GitHub repository
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "credentials.json")

# Check if the file exists before using it
if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_PATH}")

SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPES)
client = gspread.authorize(credentials)
sheet = client.open_by_key("1LegE5pSPl06OTynxjIxqzGVEtdiiDh8uBQc-k35Upys")

import os

CREDENTIALS_PATH = "FIELD-ENGINEER-SHIFT-REPORT-/credentials.json"  # Use Render Secret File path

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, SCOPES)
client = gspread.authorize(credentials)

client = gspread.authorize(credentials)
sheet = client.open_by_key(SHEET_ID)

# Function to store data in the correct sheet
def store_data(area, date, engineer, technician, description, shift):
    worksheet = sheet.worksheet(area)  # Get the correct sheet (Furnace, Pump House, etc.)
    worksheet.append_row([date, engineer, technician, description, shift])  # Append data

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

    return render_template(f"{area}.html")

if __name__ == "__main__":
    app.run(debug=True)
