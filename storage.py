# storage.py

import csv
import os

FILENAME = "job_data.csv"
FIELDNAMES = ["title", "company", "status", "date", "link", "notes"]

def load_jobs():
    if not os.path.exists(FILENAME):
        return []

    with open(FILENAME, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_job(job):
    file_exists = os.path.exists(FILENAME)
    with open(FILENAME, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(job)

def delete_job(title, company):
    jobs = load_jobs()
    filtered = [job for job in jobs if not (job["title"] == title and job["company"] == company)]
    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(filtered)

def update_job(old_title, old_company, new_job_data):
    jobs = load_jobs()
    for job in jobs:
        if job["title"] == old_title and job["company"] == old_company:
            job.update(new_job_data)
    with open(FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(jobs)
