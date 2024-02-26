from tkinter import *
from tkinter import scrolledtext
from PIL import Image, ImageTk

from scapy.all import sniff, AsyncSniffer
from db_helper import insert_packet_sniff_result


class GUIPacketSniffer:
    def __init__(self, root):
        self.root = root
        self.sniffer = None
        self.packet_list = []
        self.setup_gui()

    def setup_gui(self):
        # self.root.title("GUI Packet Sniffer")
        # self.root.geometry("900x700")  # Adjusted for better layout
        self.root.configure(bg='#00069b')  # A deep blue theme for outer part

        # Create a main frame to hold packet display and details
        self.main_frame = Frame(self.root, bg='#00069b')
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Packet Display Box
        self.packet_display = scrolledtext.ScrolledText(self.main_frame, height=25, state='disabled', bg='black', fg='white', bd=0, font=('Courier', 10))
        self.packet_display.pack(expand=True, fill='both', side=TOP, padx=5, pady=(5,0))
        self.packet_display.bind("<Double-1>", self.display_packet_details)

        # Packet Details Display Box, made smaller as requested
        self.packet_details_display = scrolledtext.ScrolledText(self.main_frame, height=8, state='disabled', bg='black', fg='white', bd=0, font=('Courier', 10))
        self.packet_details_display.pack(expand=False, fill='both', side=TOP, padx=5, pady=(5,5))

        # Frame for buttons, ensuring 100% width
        self.button_frame = Frame(self.root, bg='#123456')
        self.button_frame.pack(fill='x', side=BOTTOM, padx=10, pady=(0,10))

        # Start Button
        self.start_button = Button(self.button_frame, text="Start Sniffing", command=self.start_sniffing, bg='#4CAF50', fg='white', relief='flat', font=('Helvetica', 12), anchor="w")
        self.start_button.pack(fill='x', side=LEFT, expand=True, padx=(0,2))

        # Stop Button
        self.stop_button = Button(self.button_frame, text="Stop Sniffing", command=self.stop_sniffing, bg='#F44336', fg='white', relief='flat', font=('Helvetica', 12), anchor="w")
        self.stop_button.pack(fill='x', side=LEFT, expand=True, padx=(2,0))

    def update_packet_display(self, packet):
        self.packet_display.configure(state='normal')
        packet_summary = packet.summary()
        self.packet_display.insert('end', packet_summary + '\n')
        self.packet_display.configure(state='disabled')
        self.packet_display.see('end')

    def packet_processing(self, packet):
        packet_summary = packet.summary()
        packet_details = packet.show(dump=True)
        
        # Store the packet summary and details in the list for UI update
        self.packet_list.append((packet_summary, packet_details))
        
        # Insert packet summary and details into the database
        insert_packet_sniff_result(packet_summary, packet_details)
        
        # Update the UI with the new packet
        self.root.after(0, self.update_packet_display, packet)  


    def start_sniffing(self):
        if self.sniffer is None:
            self.sniffer = AsyncSniffer(prn=self.packet_processing, store=False)
            self.sniffer.start()
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')

    def stop_sniffing(self):
        if self.sniffer is not None:
            self.sniffer.stop()
            self.sniffer = None
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')

    def display_packet_details(self, event=None):
     try:
        index = self.packet_display.index("@%s,%s linestart" % (event.x, event.y))
        line = int(index.split(".")[0]) - 1
        _, packet_details = self.packet_list[line]  # Unpack the tuple
        self.packet_details_display.configure(state='normal')
        self.packet_details_display.delete(1.0, 'end')
        self.packet_details_display.insert('end', packet_details)  # Insert the details directly
        self.packet_details_display.configure(state='disabled')
     except IndexError:
        pass  # Click was not on a packet


if __name__ == "__main__":
    root = Tk()
    app = GUIPacketSniffer(root)
    root.mainloop()
