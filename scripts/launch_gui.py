import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'scripts'))

import tkinter as tk
from tkinter import ttk
import threading
from run_mouse import run_mouse_control

class MouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2-Hand Gesture Control")
        self.root.geometry("380x400")
        
        self.config = {'sensitivity': 1.0}
        self.stop_event = threading.Event()
        self.is_running = False
        self.thread = None
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text="2-Hand Gesture Control", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.btn = tk.Button(self.root, text="Start", command=self.toggle, 
                             font=("Arial", 12), bg="green", fg="white", width=15)
        self.btn.pack(pady=10)
        
        sens_frame = tk.Frame(self.root)
        sens_frame.pack(pady=10, padx=20, fill='x')
        self.sens_lbl = tk.Label(sens_frame, text=f"Sensitivity: {self.config['sensitivity']:.1f}")
        self.sens_lbl.pack(anchor='w')
        ttk.Scale(sens_frame, from_=0.1, to=3.0, command=self.on_sens, 
                  value=self.config['sensitivity']).pack(fill='x')
        
        guide = tk.LabelFrame(self.root, text="Gesture Guide", font=("Arial", 11, "bold"))
        guide.pack(pady=10, padx=20, fill='both', expand=True)
        
        txt = (
            "MOUSE (Right Hand Only)\n"
            "  Index       → Move Cursor\n"
            "  Thumb Pinch → Right Click\n"
            "  Scissor     → Left Click/Drag\n\n"
            "2-HAND (Left Fist + Right Hand)\n"
            "  + Thumbs Up → Play\n"
            "  + Open Palm → Pause\n"
            "  + L-Shape   → Volume (Rotate)\n"
            "  + 2 Fingers → Scroll (Up/Down)\n\n"
            "SWIPE (Right Hand Only)\n"
            "  3 Fingers   → Next/Prev Track"
        )
        tk.Label(guide, text=txt, justify="left", font=("Consolas", 9)).pack(padx=10, pady=5, anchor='w')

    def on_sens(self, val):
        self.config['sensitivity'] = float(val)
        self.sens_lbl.config(text=f"Sensitivity: {float(val):.1f}")

    def toggle(self):
        if not self.is_running:
            self.stop_event.clear()
            self.thread = threading.Thread(target=run_mouse_control, args=(self.config, self.stop_event), daemon=True)
            self.thread.start()
            self.is_running = True
            self.btn.config(text="Stop", bg="red")
        else:
            self.stop_event.set()
            self.is_running = False
            self.btn.config(text="Start", bg="green")

if __name__ == "__main__":
    tk.Tk().withdraw()
    root = tk.Tk()
    MouseApp(root)
    root.mainloop()
