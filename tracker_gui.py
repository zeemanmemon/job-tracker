import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import date, datetime
from storage import load_jobs, save_job, delete_job, update_job
import openpyxl
from openpyxl.styles import Font

class JobTrackerApp:
    def __init__(self, root):
        self.root = root
        self.jobs = load_jobs()
        self.selected_job = None
        self.setup_ui()

    def setup_ui(self):
        # Form Frame
        form_frame = tk.Frame(self.root, pady=10)
        form_frame.pack(fill='x')

        tk.Label(form_frame, text="Job Title").grid(row=0, column=0)
        self.title_entry = tk.Entry(form_frame)
        self.title_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Company").grid(row=0, column=2)
        self.company_entry = tk.Entry(form_frame)
        self.company_entry.grid(row=0, column=3)

        tk.Label(form_frame, text="Status").grid(row=1, column=0)
        self.status_entry = ttk.Combobox(form_frame, values=["Applied", "Interview", "Offer", "Rejected"])
        self.status_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Date Applied").grid(row=1, column=2)
        self.date_entry = DateEntry(form_frame, width=18, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_entry.grid(row=1, column=3)

        tk.Label(form_frame, text="Job Link").grid(row=2, column=0)
        self.link_entry = tk.Entry(form_frame, width=60)
        self.link_entry.grid(row=2, column=1, columnspan=3)

        tk.Label(form_frame, text="Notes").grid(row=3, column=0)
        self.notes_entry = tk.Entry(form_frame, width=60)
        self.notes_entry.grid(row=3, column=1, columnspan=3)

        # Filter Frame
        filter_frame = tk.Frame(self.root, pady=5)
        filter_frame.pack(fill='x')

        tk.Label(filter_frame, text="Filter by Status").pack(side='left')
        self.filter_status = ttk.Combobox(filter_frame, values=["All", "Applied", "Interview", "Offer", "Rejected"], width=20)
        self.filter_status.set("All")
        self.filter_status.pack(side='left', padx=5)

        tk.Button(filter_frame, text="Search", command=self.filter_jobs).pack(side='left', padx=5)
        tk.Button(filter_frame, text="Clear Filter", command=self.refresh_jobs).pack(side='left', padx=5)
        tk.Button(filter_frame, text="Export to Excel", command=self.export_filtered_jobs).pack(side='left', padx=5)

        # Button Frame
        button_frame = tk.Frame(self.root, pady=10)
        button_frame.pack(fill='x')

        tk.Button(button_frame, text="Add Job", command=self.add_job).pack(side='left', padx=5)
        tk.Button(button_frame, text="Edit Job", command=self.edit_or_update_job).pack(side='left', padx=5)
        tk.Button(button_frame, text="Delete Selected", command=self.delete_selected_job).pack(side='left', padx=5)
        tk.Button(button_frame, text="Refresh", command=self.refresh_jobs).pack(side='right', padx=5)

        # Table
        self.tree = ttk.Treeview(self.root, columns=("Title", "Company", "Status", "Date", "Link", "Notes"), show='headings')
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor='center')
        self.tree.pack(expand=True, fill='both')

        self.refresh_jobs()

    def add_job(self):
        job = {
            "title": self.title_entry.get(),
            "company": self.company_entry.get(),
            "status": self.status_entry.get(),
            "date": self.date_entry.get(),
            "link": self.link_entry.get(),
            "notes": self.notes_entry.get()
        }

        if not job["title"] or not job["company"]:
            messagebox.showerror("Error", "Title and Company are required.")
            return

        save_job(job)
        self.clear_form()
        self.refresh_jobs()

    def edit_or_update_job(self):
        selected = self.tree.selection()

        if not self.selected_job and selected:
            item = self.tree.item(selected[0])
            values = item["values"]

            self.selected_job = {"title": values[0], "company": values[1]}

            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, values[0])

            self.company_entry.delete(0, tk.END)
            self.company_entry.insert(0, values[1])

            self.status_entry.set(values[2])
            self.date_entry.set_date(values[3])

            self.link_entry.delete(0, tk.END)
            self.link_entry.insert(0, values[4])

            self.notes_entry.delete(0, tk.END)
            self.notes_entry.insert(0, values[5])

            messagebox.showinfo("Edit Mode", "Job loaded. Make changes and click 'Edit Job' again to save.")
        elif self.selected_job:
            updated_data = {
                "title": self.title_entry.get(),
                "company": self.company_entry.get(),
                "status": self.status_entry.get(),
                "date": self.date_entry.get(),
                "link": self.link_entry.get(),
                "notes": self.notes_entry.get()
            }

            update_job(self.selected_job["title"], self.selected_job["company"], updated_data)
            messagebox.showinfo("Success", "Job updated successfully.")
            self.clear_form()
            self.refresh_jobs()
            self.selected_job = None
        else:
            messagebox.showwarning("No Selection", "Please select a job first.")

    def delete_selected_job(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            title = item['values'][0]
            company = item['values'][1]
            delete_job(title, company)
            self.refresh_jobs()

    def refresh_jobs(self):
        self.tree.delete(*self.tree.get_children())
        self.jobs = load_jobs()
        for job in self.jobs:
            self.tree.insert("", "end", values=(job["title"], job["company"], job["status"], job["date"], job["link"], job["notes"]))

    def filter_jobs(self):
        selected_status = self.filter_status.get()
        self.tree.delete(*self.tree.get_children())
        self.jobs = load_jobs()

        for job in self.jobs:
            if selected_status == "All" or job["status"] == selected_status:
                self.tree.insert("", "end", values=(job["title"], job["company"], job["status"], job["date"], job["link"], job["notes"]))

    def export_filtered_jobs(self):
        selected_status = self.filter_status.get()
        jobs = load_jobs()

        filtered = [job for job in jobs if selected_status == "All" or job["status"] == selected_status]

        if not filtered:
            messagebox.showinfo("No Data", "No jobs to export.")
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        default_name = f"Filtered_Jobs_{timestamp}.xlsx"

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 initialfile=default_name,
                                                 filetypes=[("Excel files", "*.xlsx")],
                                                 title="Save Filtered Jobs As")
        if not file_path:
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Filtered Jobs"

        headers = ["Title", "Company", "Status", "Date", "Link", "Notes"]
        ws.append(headers)
        for cell in ws[1]:
            cell.font = Font(bold=True)

        for job in filtered:
            ws.append([job["title"], job["company"], job["status"], job["date"], job["link"], job["notes"]])

        wb.save(file_path)
        messagebox.showinfo("Export Successful", f"Jobs exported to:\n{file_path}")

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.status_entry.set('')
        self.date_entry.set_date(date.today())
        self.link_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.selected_job = None
