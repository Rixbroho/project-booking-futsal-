import tkinter as tk

class FeaturedCourts:
    def __init__(self, parent, colors, on_book):
        self.parent = parent
        self.colors = colors
        self.on_book = on_book
        
        self.courts = [
            {"name": "Baneshwor Arena", "location": "Kathmandu, Baneshwor"},
            {"name": "Thimi Sports Complex", "location": "Bhaktapur, Thimi"},
            {"name": "Balaju Futsal Hub", "location": "Kathmandu, Balaju"},
            {"name": "Suryabinayak Stadium", "location": "Bhaktapur, Suryabinayak"}
        ]
        
        self.create_courts_section()

    def create_courts_section(self):
        courts_frame = tk.Frame(self.parent, bg=self.colors['bg_dark'])
        courts_frame.pack(fill='x', padx=40, pady=30)

        # Section title
        tk.Label(courts_frame, text="Featured Indoor Courts",
                font=('Arial', 32, 'bold'), fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=30)

        # Courts grid
        grid_frame = tk.Frame(courts_frame, bg=self.colors['bg_dark'])
        grid_frame.pack()

        row = 0
        col = 0
        for court in self.courts:
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
                           command=self.on_book)
        book_btn.pack(pady=5)
        
        # Add hover effect
        book_btn.bind('<Enter>', lambda e: book_btn.configure(bg=self.colors['hover_red']))
        book_btn.bind('<Leave>', lambda e: book_btn.configure(bg=self.colors['red']))
