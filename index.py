import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, date

class FutsalBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Futsal Range Booking")
        self.root.state('zoomed')
        
        # Define colors
        self.colors = {
            'bg_dark': '#000000',
            'red': '#dc3545',
            'text': '#ffffff',
            'secondary': '#333333',
            'hover_red': '#bb2d3b'  # Darker red for hover effects
        }

        # Configure root window
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Updated locations for Nepal
        self.locations = [
            "Kathmandu - Baneshwor",
            "Kathmandu - Balaju",
            "Kathmandu - Budhanilkantha",
            "Bhaktapur - Suryabinayak",
            "Bhaktapur - Thimi"
        ]
        
        self.games = ["Futsal", "Cricket", "Basketball"]
        
        # Store bookings
        self.bookings = {}
        
        # Create main scrollable canvas
        self.create_scrollable_canvas()
        self.create_widgets()
        
        # Configure style for larger buttons
        self.style = ttk.Style()
        self.style.configure('Large.TButton', padding=15, font=('Arial', 12, 'bold'))

    def create_scrollable_canvas(self):
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.root, bg=self.colors['bg_dark'], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        
        # Create main frame inside canvas
        self.main_frame = tk.Frame(self.canvas, bg=self.colors['bg_dark'])
        
        # Configure canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create window inside canvas
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Configure canvas scrolling
        self.main_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Update the width of the window to match the canvas
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def create_widgets(self):
        # Header with fixed position
        header_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        header_frame.pack(fill='x', padx=20, pady=10)

        # Logo with larger size
        logo_label = tk.Label(header_frame, text="FR", font=('Arial', 32, 'bold'), 
                            fg=self.colors['red'], bg=self.colors['bg_dark'])
        logo_label.pack(side='left')

        # Navigation buttons
        nav_frame = tk.Frame(header_frame, bg=self.colors['bg_dark'])
        nav_frame.pack(side='right')

        # Larger View Bookings button
        view_bookings_btn = tk.Button(nav_frame, text="View All Bookings", 
                                    bg=self.colors['red'],
                                    fg=self.colors['text'],
                                    font=('Arial', 12, 'bold'),
                                    bd=0, padx=30, pady=10,
                                    command=self.view_all_bookings)
        view_bookings_btn.pack(side='right', padx=10)

        nav_items = ['Home', 'Indoor Courts', 'Services', 'Contact Us', 'My Account']
        for item in nav_items:
            btn = tk.Button(nav_frame, text=item, 
                          bg=self.colors['bg_dark'],
                          fg=self.colors['text'], 
                          font=('Arial', 11),
                          bd=0, padx=15, pady=8,
                          activebackground=self.colors['secondary'],
                          activeforeground=self.colors['text'])
            btn.pack(side='left', padx=5)

        self.create_hero_section()
        self.create_booking_form()
        self.create_featured_courts()

    def create_hero_section(self):
        hero_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        hero_frame.pack(fill='x', padx=40, pady=30)

        # Larger hero text
        tk.Label(hero_frame, text="Explore the Sportrange",
                font=('Arial', 48, 'bold'), fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        tk.Label(hero_frame, text="Nepal's Premier Indoor Sports Facility",
                font=('Arial', 20), fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w', pady=10)

        # Larger Quick Booking button
        quick_book_btn = tk.Button(hero_frame, text="Quick Booking →", 
                                 bg=self.colors['red'],
                                 fg=self.colors['text'],
                                 font=('Arial', 14, 'bold'),
                                 bd=0, padx=40, pady=15,
                                 command=self.show_booking_dialog)
        quick_book_btn.pack(anchor='w', pady=30)
        
        # Add hover effect
        quick_book_btn.bind('<Enter>', lambda e: quick_book_btn.configure(bg=self.colors['hover_red']))
        quick_book_btn.bind('<Leave>', lambda e: quick_book_btn.configure(bg=self.colors['red']))

    def create_booking_form(self):
        form_frame = tk.Frame(self.main_frame, bg=self.colors['secondary'])
        form_frame.pack(fill='x', padx=40, pady=20)

        # Inner padding frame
        inner_frame = tk.Frame(form_frame, bg=self.colors['secondary'], padx=30, pady=30)
        inner_frame.pack(fill='x')

        # Form title with larger text
        tk.Label(inner_frame, text="Book Your Court",
                font=('Arial', 24, 'bold'), fg=self.colors['text'],
                bg=self.colors['secondary']).pack(pady=(0, 20))

        # Create a frame for the form elements
        input_frame = tk.Frame(inner_frame, bg=self.colors['secondary'])
        input_frame.pack()

        # Location label and dropdown
        tk.Label(input_frame, text="Select Location:", 
                font=('Arial', 12), fg=self.colors['text'],
                bg=self.colors['secondary']).pack(anchor='w')
        
        self.location_var = tk.StringVar()
        location_dropdown = ttk.Combobox(input_frame, textvariable=self.location_var,
                                       values=self.locations, width=40,
                                       font=('Arial', 11))
        location_dropdown.pack(pady=(5, 15))
        location_dropdown.set("Select your preferred location")

        # Game type label and dropdown
        tk.Label(input_frame, text="Select Game:", 
                font=('Arial', 12), fg=self.colors['text'],
                bg=self.colors['secondary']).pack(anchor='w')
        
        self.game_var = tk.StringVar()
        game_dropdown = ttk.Combobox(input_frame, textvariable=self.game_var,
                                   values=self.games, width=40,
                                   font=('Arial', 11))
        game_dropdown.pack(pady=(5, 20))
        game_dropdown.set("Select your game")

        # Larger Book Now button
        book_btn = tk.Button(input_frame, text="Book Now", 
                           bg=self.colors['red'],
                           fg=self.colors['text'],
                           font=('Arial', 14, 'bold'),
                           bd=0, padx=40, pady=15,
                           command=self.show_booking_dialog)
        book_btn.pack(pady=10)
        
        # Add hover effect
        book_btn.bind('<Enter>', lambda e: book_btn.configure(bg=self.colors['hover_red']))
        book_btn.bind('<Leave>', lambda e: book_btn.configure(bg=self.colors['red']))

    def create_featured_courts(self):
        courts_frame = tk.Frame(self.main_frame, bg=self.colors['bg_dark'])
        courts_frame.pack(fill='x', padx=40, pady=30)

        # Section title
        tk.Label(courts_frame, text="Featured Indoor Courts",
                font=('Arial', 32, 'bold'), fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=30)

        # Courts grid
        grid_frame = tk.Frame(courts_frame, bg=self.colors['bg_dark'])
        grid_frame.pack()

        courts = [
            {"name": "Baneshwor Arena", "location": "Kathmandu, Baneshwor"},
            {"name": "Thimi Sports Complex", "location": "Bhaktapur, Thimi"},
            {"name": "Balaju Futsal Hub", "location": "Kathmandu, Balaju"},
            {"name": "Suryabinayak Stadium", "location": "Bhaktapur, Suryabinayak"}
        ]

        row = 0
        col = 0
        for court in courts:
            self.create_court_card(grid_frame, court, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

    def create_court_card(self, parent, court, row, col):
        # Larger card with more padding
        card = tk.Frame(parent, bg=self.colors['secondary'], padx=20, pady=20)
        card.grid(row=row, column=col, padx=15, pady=15)

        # Court name with larger font
        tk.Label(card, text=court["name"], 
                font=('Arial', 18, 'bold'),
                fg=self.colors['text'], 
                bg=self.colors['secondary']).pack(pady=(0, 10))
        
        # Location with larger font
        tk.Label(card, text=court["location"], 
                font=('Arial', 12),
                fg=self.colors['text'], 
                bg=self.colors['secondary']).pack(pady=(0, 15))

        # Larger Book Now button
        book_btn = tk.Button(card, text="Book Now", 
                           bg=self.colors['red'],
                           fg=self.colors['text'],
                           font=('Arial', 12, 'bold'),
                           bd=0, padx=30, pady=12,
                           command=self.show_booking_dialog)
        book_btn.pack(pady=5)
        
        # Add hover effect
        book_btn.bind('<Enter>', lambda e: book_btn.configure(bg=self.colors['hover_red']))
        book_btn.bind('<Leave>', lambda e: book_btn.configure(bg=self.colors['red']))

    def show_booking_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Book a Court")
        dialog.geometry("700x600")  # Larger dialog
        dialog.configure(bg=self.colors['bg_dark'])

        dialog.transient(self.root)
        dialog.grab_set()

        # Selected location and game
        if hasattr(self, 'location_var') and self.location_var.get() != "Select your preferred location":
            location = self.location_var.get()
        else:
            location = self.locations[0]

        if hasattr(self, 'game_var') and self.game_var.get() != "Select your game":
            game = self.game_var.get()
        else:
            game = self.games[0]

        # Title
        tk.Label(dialog, text="Book Your Session",
                font=('Arial', 24, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=20)

        # Show selected options
        tk.Label(dialog, text=f"Location: {location}", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'], 
                font=('Arial', 14)).pack(pady=5)
        
        tk.Label(dialog, text=f"Game: {game}", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'], 
                font=('Arial', 14)).pack(pady=5)

        # Calendar
        cal_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        cal_frame.pack(pady=20)

        min_date = date.today()
        cal = Calendar(cal_frame, selectmode='day', 
                      date_pattern='y-mm-dd',
                      mindate=min_date, 
                      background=self.colors['red'],
                      foreground=self.colors['text'],
                      font=('Arial', 10))
        cal.pack()

        # Time slots
        time_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        time_frame.pack(pady=20)

        tk.Label(time_frame, text="Select Time Slot:", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'],
                font=('Arial', 12)).pack()

        times = ["08:00-09:00", "09:00-10:00", "10:00-11:00", "11:00-12:00",
                "13:00-14:00", "14:00-15:00", "15:00-16:00", "16:00-17:00",
                "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00"]
        
        time_var = tk.StringVar()
        time_dropdown = ttk.Combobox(time_frame, 
                                   textvariable=time_var,
                                   values=times, 
                                   width=30,
                                   font=('Arial', 11))
        time_dropdown.pack(pady=10)

        # Customer name entry
        name_frame = tk.Frame(dialog, bg=self.colors['bg_dark'])
        name_frame.pack(pady=10)
        
        tk.Label(name_frame, text="Customer Name:", 
                fg=self.colors['text'],
                bg=self.colors['bg_dark'],
                font=('Arial', 12)).pack()
        
        name_entry = tk.Entry(name_frame, 
                            width=30,
                            font=('Arial', 11))
        name_entry.pack(pady=10)

        # Larger Confirm button
        confirm_btn = tk.Button(dialog, text="Confirm Booking",
                              bg=self.colors['red'],
                              fg=self.colors['text'],
                              font=('Arial', 14, 'bold'),
                              bd=0, padx=40, pady=15,
                              command=lambda: self.confirm_booking(
                                  dialog, cal.get_date(),
                                  time_var.get(),
                                  name_entry.get(),
                                  location, game))
        confirm_btn.pack(pady=20)
        
        # Add hover effect
        confirm_btn.bind('<Enter>', lambda e: confirm_btn.configure(bg=self.colors['hover_red']))
        confirm_btn.bind('<Leave>', lambda e: confirm_btn.configure(bg=self.colors['red']))

    def view_all_bookings(self):
        booking_window = tk.Toplevel(self.root)
        booking_window.title("All Bookings")
        booking_window.geometry("1000x700")  # Larger window
        booking_window.configure(bg=self.colors['bg_dark'])

        booking_window.transient(self.root)
        booking_window.grab_set()

        # Title
        tk.Label(booking_window, text="Current Bookings",
                font=('Arial', 24, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=20)

        # Create a frame for the bookings list
        list_frame = tk.Frame(booking_window, bg=self.colors['bg_dark'])
        list_frame.pack(fill='both', expand=True, padx=30, pady=20)

        # Configure style for treeview
        style = ttk.Style()
        style.configure("Treeview", 
                      font=('Arial', 11),
                      rowheight=30)
        style.configure("Treeview.Heading", 
                      font=('Arial', 12, 'bold'))

        # Create treeview with larger columns
        columns = ('Date', 'Time', 'Customer', 'Location', 'Game')
        tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        # Define column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=180)

        # Add scrollbar to treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)

        tree_scroll.pack(side='right', fill='y')
        tree.pack(fill='both', expand=True)

        # Populate treeview with bookings
        if not self.bookings:
            tree.insert('', 'end', values=('No bookings', 'found', '', '', ''))
        else:
            for date in sorted(self.bookings.keys()):
                for time, details in sorted(self.bookings[date].items()):
                    tree.insert('', 'end', values=(
                        date,
                        time,
                        details['customer_name'],
                        details['location'],
                        details['game']
                    ))

        # Larger Close button
        close_btn = tk.Button(booking_window, text="Close",
                            bg=self.colors['red'],
                            fg=self.colors['text'],
                            font=('Arial', 14, 'bold'),
                            bd=0, padx=40, pady=15,
                            command=booking_window.destroy)
        close_btn.pack(pady=20)
        
        # Add hover effect
        close_btn.bind('<Enter>', lambda e: close_btn.configure(bg=self.colors['hover_red']))
        close_btn.bind('<Leave>', lambda e: close_btn.configure(bg=self.colors['red']))

    def confirm_booking(self, dialog, selected_date, time, customer_name, location, game):
        if not time:
            messagebox.showerror("Error", "Please select a time slot")
            return
            
        if not customer_name:
            messagebox.showerror("Error", "Please enter customer name")
            return

        if selected_date not in self.bookings:
            self.bookings[selected_date] = {}

        if time in self.bookings[selected_date]:
            messagebox.showerror("Error", "This time slot is already booked")
            return

        self.bookings[selected_date][time] = {
            'customer_name': customer_name,
            'location': location,
            'game': game
        }

        messagebox.showinfo("Success", 
                          f"Booking confirmed!\n\nDate: {selected_date}\n"
                          f"Time: {time}\nLocation: {location}\n"
                          f"Game: {game}\nCustomer: {customer_name}")
        dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FutsalBookingApp(root)
    root.mainloop()