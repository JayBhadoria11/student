# MITS Student Portal (Demo)

A beginner-friendly multi-page Flask website demonstrating a student dashboard.

## Features
- Student profile (editable demo fields)
- Academic results and simple CGPA calculation
- Attendance by subject and overall attendance
- Achievement badges
- Teacher feedback
- Printable marksheet

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5001

## Important
- The data in `app.py` is sample/demo data. Replace it with verified student and institute data.
- The supplied MITS logo image is used in the sidebar and printable marksheet.
- This starter project stores data in Python variables, not a database. Profile changes last only while the server process is running.
- The CGPA conversion is a simple illustrative 10-point mapping from marks. Use the institute's official grading regulations before treating it as an official result.

## Deploy on Render
Create a new Web Service connected to this repository:
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
