import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, parent, colors, on_login_success, on_register_success=None):
        self.window = tk.Toplevel(parent)
        self.window.title("Login")
        self.window.geometry("400x500")
        self.window.configure(bg=colors['bg_dark'])
        self.colors = colors
        self.on_login_success = on_login_success
        self.on_register_success = on_register_success or on_login_success

        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_login_form()

    def create_login_form(self):
        # Main container with padding
        container = tk.Frame(self.window, bg=self.colors['bg_dark'])
        container.pack(fill='both', expand=True, padx=40, pady=40)

        # Title
        tk.Label(container, text="Welcome Back",
                font=('Arial', 24, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=(0, 30))

        # Username
        tk.Label(container, text="Username",
                font=('Arial', 12),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        self.username_entry = tk.Entry(container, 
                                     font=('Arial', 12),
                                     width=30)
        self.username_entry.pack(pady=(5, 20))

        # Password
        tk.Label(container, text="Password",
                font=('Arial', 12),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        self.password_entry = tk.Entry(container, 
                                     font=('Arial', 12),
                                     width=30,
                                     show="•")
        self.password_entry.pack(pady=(5, 30))

        # Login button
        login_btn = tk.Button(container, text="LOGIN",
                            bg=self.colors['red'],
                            fg=self.colors['text'],
                            font=('Arial', 14, 'bold'),
                            bd=0, padx=30, pady=12,
                            cursor='hand2',
                            command=self.login)
        login_btn.pack(pady=(0, 20))

        # Add hover effect
        login_btn.bind('<Enter>', lambda e: login_btn.configure(bg=self.colors['hover_red']))
        login_btn.bind('<Leave>', lambda e: login_btn.configure(bg=self.colors['red']))

        # Register link
        register_frame = tk.Frame(container, bg=self.colors['bg_dark'])
        register_frame.pack(pady=10)
        
        tk.Label(register_frame, text="Don't have an account? ",
                font=('Arial', 11),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(side='left')
        
        register_link = tk.Label(register_frame, text="Register",
                               font=('Arial', 11, 'bold'),
                               fg=self.colors['red'],
                               bg=self.colors['bg_dark'],
                               cursor='hand2')
        register_link.pack(side='left')
        
        register_link.bind('<Button-1>', lambda e: self.show_register())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.window.destroy()
        self.on_login_success(username, password)

    def show_register(self):
        self.window.destroy()
        RegisterWindow(self.window.master, self.colors, self.on_register_success)

class RegisterWindow:
    def __init__(self, parent, colors, on_register_success):
        self.window = tk.Toplevel(parent)
        self.window.title("Register")
        self.window.geometry("400x600")
        self.window.configure(bg=colors['bg_dark'])
        self.colors = colors
        self.on_register_success = on_register_success

        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_register_form()

    def create_register_form(self):
        # Main container with padding
        container = tk.Frame(self.window, bg=self.colors['bg_dark'])
        container.pack(fill='both', expand=True, padx=40, pady=40)

        # Title
        tk.Label(container, text="Create Account",
                font=('Arial', 24, 'bold'),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(pady=(0, 30))

        # Full Name
        tk.Label(container, text="Full Name",
                font=('Arial', 12),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        self.fullname_entry = tk.Entry(container, 
                                     font=('Arial', 12),
                                     width=30)
        self.fullname_entry.pack(pady=(5, 20))

        # Email
        tk.Label(container, text="Email",
                font=('Arial', 12),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        self.email_entry = tk.Entry(container, 
                                  font=('Arial', 12),
                                  width=30)
        self.email_entry.pack(pady=(5, 20))

        # Username
        tk.Label(container, text="Username",
                font=('Arial', 12),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        self.username_entry = tk.Entry(container, 
                                     font=('Arial', 12),
                                     width=30)
        self.username_entry.pack(pady=(5, 20))

        # Password
        tk.Label(container, text="Password",
                font=('Arial', 12),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(anchor='w')
        
        self.password_entry = tk.Entry(container, 
                                     font=('Arial', 12),
                                     width=30,
                                     show="•")
        self.password_entry.pack(pady=(5, 30))

        # Register button
        register_btn = tk.Button(container, text="REGISTER",
                               bg=self.colors['red'],
                               fg=self.colors['text'],
                               font=('Arial', 14, 'bold'),
                               bd=0, padx=30, pady=12,
                               cursor='hand2',
                               command=self.register)
        register_btn.pack(pady=(0, 20))

        # Add hover effect
        register_btn.bind('<Enter>', lambda e: register_btn.configure(bg=self.colors['hover_red']))
        register_btn.bind('<Leave>', lambda e: register_btn.configure(bg=self.colors['red']))

        # Login link
        login_frame = tk.Frame(container, bg=self.colors['bg_dark'])
        login_frame.pack(pady=10)
        
        tk.Label(login_frame, text="Already have an account? ",
                font=('Arial', 11),
                fg=self.colors['text'],
                bg=self.colors['bg_dark']).pack(side='left')
        
        login_link = tk.Label(login_frame, text="Login",
                            font=('Arial', 11, 'bold'),
                            fg=self.colors['red'],
                            bg=self.colors['bg_dark'],
                            cursor='hand2')
        login_link.pack(side='left')
        
        login_link.bind('<Button-1>', lambda e: self.show_login())

    def register(self):
        fullname = self.fullname_entry.get().strip()
        email = self.email_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not all([fullname, email, username, password]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        self.window.destroy()
        self.on_register_success(username, password, fullname, email)

    def show_login(self):
        self.window.destroy()
        LoginWindow(self.window.master, self.colors, self.on_register_success)