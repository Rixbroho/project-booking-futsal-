import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import date

class BookingDialog:
    def __init__(self, parent, colors, location_var, game_var, on_confirm):
        # using self to allow the class to store and access its own variables and methods and to keep a track of its own data and functions.
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Book a Court")
        self.dialog.geometry("700x700")
        self.dialog.configure(bg=colors['bg_dark'])
        self.colors = colors 
        self.location_var = location_var
        self.game_var = game_var
        self.on_confirm = on_confirm

        self.dialog.transient(parent) #it makes sure that it belongs to parent window
        self.dialog.grab_set() #This makes sure the user can't click anywhere else until they close the pop-up and The user must interact with the pop-up before they can go back to the main window.
        
        self.create_dialog_content()

        # Remove the global mousewheel binding when dialog is destroyed
        self.dialog.bind("<Destroy>", lambda e: self.cleanup_bindings(e))

    def cleanup_bindings(self, event):
        # Only cleanup if this dialog is being destroyed
        if str(event.widget) == str(self.dialog):
            try:
                self.dialog.unbind_all("<MouseWheel>")
            except:
                pass

    def create_dialog_content(self):
        # Create a main container frame
        container = tk.Frame(self.dialog, bg=self.colors['bg_dark'])
        container.pack(fill='both', expand=True)

        # Create a canvas for scrollable content
        canvas = tk.Canvas(container, bg=self.colors['bg_dark'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Create a frame for the scrollable content
        scrollable_frame = tk.Frame(canvas, bg=self.colors['bg_dark'])
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create window in canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=680)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True, padx=(0, 2))
        scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Main content frame with padding
        main_frame = tk.Frame(scrollable_frame, bg=self.colors['bg_dark'], padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)

        # Title
        tk.Label(main_frame, text="Book Your Session",
                font=('Arial', 28, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=(0, 20))

        # Selected options
        tk.Label(main_frame, text=f"Location: {self.location_var.get()}", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'], 
                font=('Arial', 14, 'bold')).pack(pady=5)
        
        tk.Label(main_frame, text=f"Game: {self.game_var.get()}", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'], 
                font=('Arial', 14, 'bold')).pack(pady=5)

        # Calendar
        cal_frame = tk.Frame(main_frame, bg=self.colors['red'], padx=2, pady=2)
        cal_frame.pack(pady=20)

        min_date = date.today()
        self.cal = Calendar(cal_frame, selectmode='day', 
                          date_pattern='y-mm-dd',
                          mindate=min_date, 
                          background=self.colors['bg_dark'],
                          foreground=self.colors['text'],
                          font=('Arial', 12))
        self.cal.pack()

        # Time slots
        time_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        time_frame.pack(pady=20)

        tk.Label(time_frame, text="Select Time Slot:", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'],
                font=('Arial', 14, 'bold')).pack()

        times = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
                "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00",
                "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00"]

        self.time_var = tk.StringVar()
        time_dropdown = ttk.Combobox(time_frame, 
                                   textvariable=self.time_var,
                                   values=times, 
                                   width=30,
                                   font=('Arial', 12))
        time_dropdown.pack(pady=10)

        # Customer name
        name_frame = tk.Frame(main_frame, bg=self.colors['bg_dark'])
        name_frame.pack(pady=20)
        
        tk.Label(name_frame, text="Customer Name:", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'],
                font=('Arial', 14, 'bold')).pack()
        
        self.name_entry = tk.Entry(name_frame, 
                                 width=30,
                                 font=('Arial', 12))
        self.name_entry.pack(pady=10)

        # Add extra space at the bottom for scrolling
        tk.Frame(main_frame, height=100, bg=self.colors['bg_dark']).pack()

        # Fixed button frame at the bottom
        button_frame = tk.Frame(self.dialog, bg=self.colors['bg_dark'], pady=20)
        button_frame.pack(side='bottom', fill='x')

        # Add separator above buttons
        separator = ttk.Separator(self.dialog, orient='horizontal')
        separator.pack(side='bottom', fill='x')

        # Button container for centering
        btn_container = tk.Frame(button_frame, bg=self.colors['bg_dark'])
        btn_container.pack(expand=True)

        # Extra large Confirm button
        confirm_btn = tk.Button(btn_container, text="CONFIRM BOOKING???",
                              bg=self.colors['red'],
                              fg=self.colors['text'],
                              font=('Arial', 20, 'bold'),
                              bd=0, padx=60, pady=25,
                              cursor='hand2',
                              command=self.confirm)
        confirm_btn.pack(side='left', padx=10)
        
        # Add hover effect
        confirm_btn.bind('<Enter>', lambda e: confirm_btn.configure(bg=self.colors['hover_red']))
        confirm_btn.bind('<Leave>', lambda e: confirm_btn.configure(bg=self.colors['red']))

        # Cancel button
        cancel_btn = tk.Button(btn_container, text="CANCEL",
                             bg=self.colors['secondary'],
                             fg=self.colors['text'],
                             font=('Arial', 20, 'bold'),
                             bd=0, padx=40, pady=25,
                             cursor='hand2',
                             command=self.dialog.destroy)
        cancel_btn.pack(side='left', padx=10)

        # Unbind mousewheel when dialog is destroyed
        self.dialog.bind("<Destroy>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def confirm(self):
        selected_date = self.cal.get_date()
        time = self.time_var.get()
        customer_name = self.name_entry.get()
        location = self.location_var.get()
        game = self.game_var.get()

        if not time:
            messagebox.showerror("Error", "Please select a time slot")
            return
            
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return

        self.on_confirm(selected_date, time, customer_name, location, game)
        self.dialog.destroy()