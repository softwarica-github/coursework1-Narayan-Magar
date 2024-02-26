import tkinter as tk
import tkinter.messagebox as MB
import datetime
import platform
import os
import socket
import threading
import subprocess
from tkinter import PhotoImage 

from PIL import Image, ImageTk
from port_pinger import PPPPP_GUI
# from packet_sniffer import PacketSniffer
from tkinter.scrolledtext import ScrolledText
from gui_sniffer import *
from portscangui import *
from db_helper import setup_database

# Globals
window = tk.Tk()
window.title("NetworkAnalysisTookKit")
window_Width = 1100
window_Height = 620
ScreenWidth = window.winfo_screenwidth()
ScreenHeight = window.winfo_screenheight()
Appear_in_the_Middle = '%dx%d+%d+%d' % (window_Width, window_Height, (ScreenWidth - window_Width) / 2, (ScreenHeight - window_Height) / 2)
window.geometry(Appear_in_the_Middle)
window.resizable(width=False, height=False)
window.configure(bg='#00069b')

# ---Class--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class NetworkToolkitGUI:
    setup_database()
    def __init__(self, master):
        self.master = master
        self.init_menu_bar()
        self.dashboard_frame = None
        self.port_pinger_frame = None
        self.packet_sniffer_frame = None
        self.network_mapper_frame = None
        self.show_dashboard()

    def init_menu_bar(self):
        self.main_menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.main_menu_bar)

        # Create the menu items
        self.main_menu_bar.add_command(label="Dashboard", command=self.show_dashboard)
        self.main_menu_bar.add_command(label="Port Scanner", command=self.show_port_scanner)
        self.main_menu_bar.add_command(label="Packet Sniffer", command=self.show_packet_sniffer)
        self.main_menu_bar.add_command(label="Network Pinger", command=self.show_port_pinger)

        # Create buttons below the menu bar
        self.button_frame = tk.Frame(self.master, bg='#00069b')
        self.button_frame.pack(fill=tk.X)

        dashboard_button = tk.Button(self.button_frame, text="Dashboard", command=self.show_dashboard)
        dashboard_button.pack(side=tk.LEFT, padx=5, pady=5)

        port_scanner_button = tk.Button(self.button_frame, text="Port Scanner", command=self.show_port_scanner)
        port_scanner_button.pack(side=tk.LEFT, padx=5, pady=5)

        packet_sniffer_button = tk.Button(self.button_frame, text="Packet Sniffer", command=self.show_packet_sniffer)
        packet_sniffer_button.pack(side=tk.LEFT, padx=5, pady=5)

        port_pinger_button = tk.Button(self.button_frame, text="Network Pinger", command=self.show_port_pinger)
        port_pinger_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Keep the rest of the class methods unchanged...


    def clear_frames(self):
        # Utility function to clear the window before loading new content
        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Menu):
                continue  # Skip the menu bar
            widget.destroy()

    def show_dashboard(self):
        self.clear_frames()
        self.dashboard_frame = tk.Frame(self.master, bg='#00069b')
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)

        # Dynamic path construction
        script_dir = os.path.dirname(__file__)  # <-- Absolute dir the script is in
        rel_path = "network_analyser.jpg"
        image_path = os.path.join(script_dir, rel_path)

        original_image = Image.open(image_path)
        resized_image = original_image.resize((window_Width, window_Height), Image.LANCZOS)
        self.dashboard_image = ImageTk.PhotoImage(resized_image)

        image_label = tk.Label(self.dashboard_frame, image=self.dashboard_image)
        image_label.pack(fill='both', expand=True)

        label = tk.Label(image_label, text="Welcome to the Network Toolkit Dashboard", bg='white', fg='black', font=('Arial', 14))
        label.pack(side='bottom', pady=10)

    def show_port_pinger(self):
        self.clear_frames()
        # Placeholder for the port pinger interface
        self.port_pinger_frame = PPPPP_GUI(self.master)  # Reuse your existing GUI class here

    def show_packet_sniffer(self):
        self.clear_frames()
        self.packet_sniffer_frame = tk.Frame(self.master, bg='#123456')
        self.packet_sniffer_frame.pack(fill=tk.BOTH, expand=True)

        # Make sure you're passing self.packet_sniffer_frame as the parent to GUIPacketSniffer
        self.packet_sniffer = GUIPacketSniffer(self.packet_sniffer_frame)
    def show_port_scanner(self):
        self.clear_frames()  # Clear the current GUI frames
        # Instead of creating a new top-level window, use the existing main window
        self.port_scanner_frame = tk.Frame(self.master, bg='#00069b')  # Adjust the background color as needed
        self.port_scanner_frame.pack(fill=tk.BOTH, expand=True)
        # Initialize the PortScanGUI within this frame
        PortScanGUI(self.port_scanner_frame)

# -----Invocations-----
GUI = NetworkToolkitGUI(window)  # Instantiate the main GUI class

# ---Launch Main Window---
window.mainloop()
