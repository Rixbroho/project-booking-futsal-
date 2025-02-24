import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from app import FutsalBookingApp

if __name__ == "__main__":
    root = tk.Tk()
    app = FutsalBookingApp(root)
    root.mainloop()