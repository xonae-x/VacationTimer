import tkinter as tk
from tkinter import messagebox
import datetime
import winsound


class VacationTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vacation Timer")
        self.root.geometry("500x400")
        self.root.config(bg="#f7f7f7")
        self.root.resizable(False, False)

        # Initialize variables
        self.target_time = None
        self.vacation_name = None
        self.countdown_window = None
        self.show_timer_window = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Vacation Timer", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#2c3e50")
        self.title_label.pack(pady=20)

        # Date picker
        self.label_date = tk.Label(self.root, text="Select Date (MM/DD/YYYY):", font=("Arial", 12), bg="#f7f7f7", fg="#2c3e50")
        self.label_date.pack(pady=5)
        self.date_entry = tk.Entry(self.root, font=("Arial", 12), width=25, bd=2, relief="solid")
        self.date_entry.insert(0, "MM/DD/YYYY")
        self.date_entry.pack(pady=5)

        # Time picker (Hour, Minute, AM/PM)
        self.label_time = tk.Label(self.root, text="Select Time:", font=("Arial", 12), bg="#f7f7f7", fg="#2c3e50")
        self.label_time.pack(pady=5)

        self.hour_var = tk.StringVar(value="01")
        self.minute_var = tk.StringVar(value="00")
        self.ampm_var = tk.StringVar(value="AM")

        time_frame = tk.Frame(self.root, bg="#f7f7f7")
        time_frame.pack(pady=5)

        self.hour_dropdown = tk.OptionMenu(time_frame, self.hour_var, *[f"{i:02}" for i in range(1, 13)])
        self.hour_dropdown.config(width=4, font=("Arial", 12))
        self.hour_dropdown.pack(side=tk.LEFT, padx=5)

        self.minute_dropdown = tk.OptionMenu(time_frame, self.minute_var, *[f"{i:02}" for i in range(0, 60, 5)])
        self.minute_dropdown.config(width=4, font=("Arial", 12))
        self.minute_dropdown.pack(side=tk.LEFT, padx=5)

        self.ampm_dropdown = tk.OptionMenu(time_frame, self.ampm_var, "AM", "PM")
        self.ampm_dropdown.config(width=6, font=("Arial", 12))
        self.ampm_dropdown.pack(side=tk.LEFT, padx=5)

        # Vacation Name
        self.label_name = tk.Label(self.root, text="Vacation Name:", font=("Arial", 12), bg="#f7f7f7", fg="#2c3e50")
        self.label_name.pack(pady=5)
        self.name_entry = tk.Entry(self.root, font=("Arial", 12), width=25, bd=2, relief="solid")
        self.name_entry.pack(pady=5)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Timer", font=("Arial", 14, "bold"), bg="#2ecc71", fg="white", relief="solid", command=self.start_timer)
        self.start_button.pack(pady=20, ipady=10, ipadx=20)

    def start_timer(self):
        # Get user inputs
        self.vacation_name = self.name_entry.get()
        date_str = self.date_entry.get()
        hour = int(self.hour_var.get())
        minute = int(self.minute_var.get())
        ampm = self.ampm_var.get()

        if not self.vacation_name or date_str == "MM/DD/YYYY":
            messagebox.showerror("Error", "Please enter a valid vacation name and date.")
            return

        try:
            # Parse the date
            target_date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")
            return

        # Adjust for AM/PM time format
        if ampm == "PM" and hour != 12:
            hour += 12
        elif ampm == "AM" and hour == 12:
            hour = 0

        # Set the target time
        self.target_time = target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)

        # Start countdown
        self.start_countdown()

    def start_countdown(self):
        # Create a new window for the countdown
        self.countdown_window = tk.Toplevel(self.root)
        self.countdown_window.title(f"Time until {self.vacation_name}!")
        self.countdown_window.geometry("500x300")
        self.countdown_window.config(bg="#34495e")

        self.label_countdown = tk.Label(self.countdown_window, font=("Arial", 30, "bold"), text="", bg="#34495e", fg="#ecf0f1")
        self.label_countdown.pack(expand=True)

        # Add the Hide button
        self.hide_button = tk.Button(self.countdown_window, text="Hide", font=("Arial", 12), bg="#e74c3c", fg="white", relief="solid", command=self.hide_countdown)
        self.hide_button.pack(pady=20)

        # Start countdown updates every second
        self.update_countdown()

    def update_countdown(self):
        # Calculate the remaining time
        time_remaining = self.target_time - datetime.datetime.now()
        days = time_remaining.days
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Update the countdown label
        self.label_countdown.config(text=f"Time until: {self.vacation_name}\n"
                                        f"{days}d {hours}h {minutes}m {seconds}s")

        if time_remaining.total_seconds() > 0:
            # Update the countdown every 1000 ms (1 second)
            self.countdown_window.after(1000, self.update_countdown)
        else:
            # Timer is up, show the message and play the beep sound
            self.label_countdown.config(text=f"Vacation: {self.vacation_name}!")
            self.play_beep()
            self.show_popup()

    def play_beep(self):
        # Play a beep sound for 5 seconds
        for _ in range(5):
            winsound.Beep(1000, 500)  # Beep at 1000 Hz for 500 ms

    def show_popup(self):
        # Show popup message after countdown ends
        messagebox.showinfo("Vacation Timer", f"The timer for {self.vacation_name} is up!")

    def hide_countdown(self):
        # Hide the countdown window
        self.countdown_window.withdraw()

        # Create a small window with a "Show Timer" button
        self.show_timer_window = tk.Toplevel(self.root)
        self.show_timer_window.title("Show Timer")
        self.show_timer_window.geometry("200x100")
        self.show_timer_window.config(bg="#f7f7f7")

        show_button = tk.Button(self.show_timer_window, text="Show Timer", font=("Arial", 12), bg="#2ecc71", fg="white", relief="solid", command=self.show_countdown)
        show_button.pack(expand=True)

    def show_countdown(self):
        # Destroy the show timer window
        if self.show_timer_window:
            self.show_timer_window.destroy()

        # Reopen the countdown window
        self.countdown_window.deiconify()


# Set up the Tkinter root window
root = tk.Tk()

# Create the VacationTimerApp instance
app = VacationTimerApp(root)

# Run the application
root.mainloop()
