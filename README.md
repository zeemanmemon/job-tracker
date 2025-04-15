 Job Tracker App body { font-family: Arial, sans-serif; margin: 2rem; line-height: 1.6; background-color: #f9f9f9; color: #333; } h1, h2 { color: #2c3e50; } pre { background: #eee; padding: 1rem; overflow-x: auto; border-radius: 5px; } code { background: #eee; padding: 2px 4px; border-radius: 3px; } .author { margin-top: 3rem; font-style: italic; } 

🧾 Job Tracker App (Python + Tkinter)
=====================================

A simple desktop app to help you **track job applications**, manage statuses, and export filtered results to Excel.

✅ Features
----------

* Add job entries with title, company, status, date applied, job link, and notes
* Edit or delete existing entries
* Filter jobs by **status** (Applied, Interview, Offer, Rejected)
* Export filtered jobs to Excel with automatic timestamped filenames
* Built-in calendar widget for selecting application dates

🛠 Requirements
---------------

* Python 3.7+
* `tkcalendar`
* `openpyxl`

    pip install -r requirements.txt

📦 Project Structure
--------------------

    job-tracker/
    ├── tracker_gui.py          # Main GUI code
    ├── storage.py              # Handles CSV load/save logic
    ├── job_data.csv            # Stores your job entries
    ├── requirements.txt        # Python package requirements
    └── README.md               # Project documentation
    

🚀 How to Run
-------------

    python tracker_gui.py

📤 Exporting to Excel
---------------------

Click **“Export to Excel”** to save all filtered job entries into an `.xlsx` file.

Files are named like:

    Filtered_Jobs_2025-04-15_23-50.xlsx

💡 Future Ideas
---------------

* Filter by company name or date range
* Export selected jobs only
* Add PDF export support
* Tagging or favorites
* Dark mode toggle

**Made by Zeeman Memon** 
