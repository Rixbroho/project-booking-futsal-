import tkinter as tk
from tkinter import ttk, messagebox
from utils.styles import Styles
from components.booking import BookingDialog
from components.view_booking import ViewBookingsDialog
from components.featured_courts import FeaturedCourts

class FutsalBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Futsal Range Booking")
        self.root.state('zoomed')
        
        # Get colors from styles
        self.colors = Styles.COLORS
        
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
        self.bind_mousewheel()

    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind to all possible widgets
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.mousewheel_handler = _on_mousewheel

    def unbind_mousewheel(self):
        # Unbind from all widgets
        self.canvas.unbind_all("<MouseWheel>")

    def on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def create_widgets(self):
        self.create_header()
        self.create_hero_section()
        self.create_booking_form()
        FeaturedCourts(self.main_frame, self.colors, self.show_booking_dialog)

    def create_header(self):
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

        # Inner padding frame with center alignment
        inner_frame = tk.Frame(form_frame, bg=self.colors['secondary'])
        inner_frame.pack(expand=True, padx=30, pady=30)

        # Center the content
        center_frame = tk.Frame(inner_frame, bg=self.colors['secondary'])
        center_frame.pack(expand=True)

        # Form title with larger text
        tk.Label(center_frame, text="Book Your Court",
                font=('Arial', 28, 'bold'), fg=self.colors['text'],
                bg=self.colors['secondary']).pack(pady=(0, 30))

        # Create a frame for the form elements
        input_frame = tk.Frame(center_frame, bg=self.colors['secondary'])
        input_frame.pack(expand=True)

        # Location label and dropdown
        tk.Label(input_frame, text="Select Location:", 
                font=('Arial', 14), fg=self.colors['text'],
                bg=self.colors['secondary']).pack(anchor='w')
        
        self.location_var = tk.StringVar()
        location_dropdown = ttk.Combobox(input_frame, textvariable=self.location_var,
                                       values=self.locations, width=40,
                                       font=('Arial', 12))
        location_dropdown.pack(pady=(5, 20))
        location_dropdown.set("Select your preferred location")

        # Game type label and dropdown
        tk.Label(input_frame, text="Select Game:", 
                font=('Arial', 14), fg=self.colors['text'],
                bg=self.colors['secondary']).pack(anchor='w')
        
        self.game_var = tk.StringVar()
        game_dropdown = ttk.Combobox(input_frame, textvariable=self.game_var,
                                   values=self.games, width=40,
                                   font=('Arial', 12))
        game_dropdown.pack(pady=(5, 30))
        game_dropdown.set("Select your game")

        # Create a separate frame for the button to ensure proper centering
        button_frame = tk.Frame(center_frame, bg=self.colors['secondary'])
        button_frame.pack(expand=True, pady=20)

        # Extra large Book Court button
        book_btn = tk.Button(button_frame, text="BOOK COURT NOW", 
                           bg=self.colors['red'],
                           fg=self.colors['text'],
                           font=('Arial', 20, 'bold'),
                           bd=0, padx=60, pady=25,
                           cursor='hand2',
                           command=self.show_booking_dialog)
        book_btn.pack(expand=True)
        
        # Add hover effect
        book_btn.bind('<Enter>', lambda e: book_btn.configure(bg=self.colors['hover_red']))
        book_btn.bind('<Leave>', lambda e: book_btn.configure(bg=self.colors['red']))

    def show_booking_dialog(self):
        # Temporarily unbind mousewheel from main window
        self.unbind_mousewheel()
        
        # Create and show dialog
        dialog = BookingDialog(self.root, self.colors, self.location_var, self.game_var, self.confirm_booking)
        
        # Rebind mousewheel when dialog closes
        def on_dialog_close(event=None):
            self.bind_mousewheel()
        
        dialog.dialog.bind("<Destroy>", on_dialog_close)

    def view_all_bookings(self):
        # Temporarily unbind mousewheel from main window
        self.unbind_mousewheel()
        
        # Create and show dialog
        dialog = ViewBookingsDialog(self.root, self.colors, self.bookings, self.cancel_booking)
        
        # Rebind mousewheel when dialog closes
        def on_dialog_close(event=None):
            self.bind_mousewheel()
        
        dialog.window.bind("<Destroy>", on_dialog_close)

    def confirm_booking(self, selected_date, time, customer_name, location, game):
        if selected_date not in self.bookings:
            self.bookings[selected_date] = {}

        if time in self.bookings[selected_date]:
            messagebox.showerror("Error", "This time slot is already booked")
            return False

        self.bookings[selected_date][time] = {
            'customer_name': customer_name,
            'location': location,
            'game': game
        }

        messagebox.showinfo("Success", 
                          f"Booking confirmed!\n\nDate: {selected_date}\n"
                          f"Time: {time}\nLocation: {location}\n"
                          f"Game: {game}\nCustomer: {customer_name}")
        
        # Make sure scrolling is re-enabled
        self.bind_mousewheel()
        return True

    def cancel_booking(self, date, time):
        if date in self.bookings and time in self.bookings[date]:
            del self.bookings[date][time]
            if not self.bookings[date]:  # If no more bookings for this date
                del self.bookings[date]
            messagebox.showinfo("Success", "Booking cancelled successfully")
            return True
        return False