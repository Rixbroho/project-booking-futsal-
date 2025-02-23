import tkinter as tk
from tkinter import ttk, messagebox

class ViewBookingsDialog:
    def __init__(self, parent, colors, bookings, on_cancel):
        self.window = tk.Toplevel(parent)
        self.window.title("All Bookings")
        self.window.geometry("1000x700")
        self.window.configure(bg=colors['bg_dark'])
        self.colors = colors
        self.bookings = bookings
        self.on_cancel = on_cancel

        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_dialog_content()

        # Remove the global mousewheel binding when window is destroyed
        self.window.bind("<Destroy>", lambda e: self.cleanup_bindings(e))

    def cleanup_bindings(self, event):
        # Only cleanup if this window is being destroyed
        if str(event.widget) == str(self.window):
            try:
                self.window.unbind_all("<MouseWheel>")
            except:
                pass

    def create_dialog_content(self):
        # Main container
        container = tk.Frame(self.window, bg=self.colors['bg_dark'])
        container.pack(fill='both', expand=True)

        # Title
        tk.Label(container, text="Current Bookings",
                font=('Arial', 24, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=20)

        # Create a frame for the bookings list
        list_frame = tk.Frame(container, bg=self.colors['bg_dark'])
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
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')

        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)

        # Add scrollbar to treeview
        tree_scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        tree_scroll.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

        self.refresh_bookings()

        # Fixed button frame at the bottom
        button_frame = tk.Frame(self.window, bg=self.colors['bg_dark'], pady=20)
        button_frame.pack(side='bottom', fill='x')

        # Add separator above buttons
        separator = ttk.Separator(self.window, orient='horizontal')
        separator.pack(side='bottom', fill='x')

        # Button container for centering
        btn_container = tk.Frame(button_frame, bg=self.colors['bg_dark'])
        btn_container.pack(expand=True)

        # Cancel Booking button
        cancel_booking_btn = tk.Button(btn_container, text="CANCEL BOOKING",
                                     bg=self.colors['red'],
                                     fg=self.colors['text'],
                                     font=('Arial', 16, 'bold'),
                                     bd=0, padx=30, pady=15,
                                     cursor='hand2',
                                     command=self.cancel_selected_booking)
        cancel_booking_btn.pack(side='left', padx=10)
        
        # Add hover effect
        cancel_booking_btn.bind('<Enter>', lambda e: cancel_booking_btn.configure(bg=self.colors['hover_red']))
        cancel_booking_btn.bind('<Leave>', lambda e: cancel_booking_btn.configure(bg=self.colors['red']))

        # Close button
        close_btn = tk.Button(btn_container, text="CLOSE",
                            bg=self.colors['secondary'],
                            fg=self.colors['text'],
                            font=('Arial', 16, 'bold'),
                            bd=0, padx=30, pady=15,
                            cursor='hand2',
                            command=self.window.destroy)
        close_btn.pack(side='left', padx=10)

    def refresh_bookings(self):
        self.tree.delete(*self.tree.get_children())
        if not self.bookings:
            self.tree.insert('', 'end', values=('No bookings', 'found', '', '', ''))
        else:
            for date in sorted(self.bookings.keys()):
                for time, details in sorted(self.bookings[date].items()):
                    self.tree.insert('', 'end', values=(
                        date,
                        time,
                        details['customer_name'],
                        details['location'],
                        details['game']
                    ))

    def cancel_selected_booking(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a booking to cancel")
            return
        
        item = self.tree.item(selected_item[0])
        date, time = item['values'][0], item['values'][1]
        
        if messagebox.askyesno("Confirm Cancellation", 
                             f"Are you sure you want to cancel the booking for:\n\n"
                             f"Date: {date}\nTime: {time}"):
            if self.on_cancel(date, time):
                self.refresh_bookings()