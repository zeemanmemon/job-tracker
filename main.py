import tkinter as tk
from tracker_gui import JobTrackerApp

def start_app():
    root = tk.Tk()
    root.title("Job Tracker")
    root.geometry("800x600")
    app = JobTrackerApp(root)
    root.mainloop()

if __name__ == "__main__":
    start_app()
