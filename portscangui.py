import tkinter as tk
from tkinter import messagebox, scrolledtext
import socket
import threading
import sys
import time
from PIL import Image, ImageTk
from db_helper import insert_scan_result


class PortScanGUI:
		def __init__(self, master):
			self.master = master
			self.ip_s = 1
			self.ip_f = 1024
			self.log = []
			self.ports = []
			self.target = 'localhost'
			self.setup_gui()

		def setup_gui(self):
			# self.master.title('Narayan Port Scanner')
			# self.master.geometry("1100x620")
			self.master.configure(background='#00069b')

			# Colors and Theme
			m1c = '#00ee00'
			bgc = '#000'
			fgc = 'white'
			self.master.tk_setPalette(background=bgc, foreground=m1c, activeBackground=fgc, activeForeground=bgc)

			# GUI Components
			tk.Label(self.master, text="Narayan Port Scanner", font=("Helvetica", 16, 'underline'), bg=bgc, fg=m1c).place(x=16, y=10)
			tk.Label(self.master, text="Target: ", bg=bgc, fg=m1c).place(x=16, y=90)
			self.L22 = tk.Entry(self.master)
			self.L22.place(x=180, y=90, width=200)  # Adjusted width
			self.L22.insert(0, "localhost")

			tk.Label(self.master, text="Ports: ", bg=bgc, fg=m1c).place(x=16, y=158)
			self.L24 = tk.Entry(self.master)
			self.L24.place(x=180, y=158, width=95)
			self.L24.insert(0, "1")

			self.L25 = tk.Entry(self.master)
			self.L25.place(x=290, y=158, width=95)
			self.L25.insert(0, "1024")

			self.L27 = tk.Label(self.master, text="[ ... ]", bg=bgc, fg=m1c)
			self.L27.place(x=180, y=220)

			# Results listbox with scrollbar
			frame = tk.Frame(self.master, bg=bgc)
			frame.place(x=16, y=275, width=1068, height=215)  # Adjusted width
			self.listbox = tk.Listbox(frame, width=106, height=6, bg=bgc, fg=m1c)  # Adjusted width
			self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
			scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
			scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
			self.listbox.config(yscrollcommand=scrollbar.set)

			# Control buttons
			# Control buttons
			tk.Button(self.master, text="Start Scan", command=self.start_scan, bg="#FF0000", fg=m1c).place(x=16, y=500, width=534)   # Red background
			tk.Button(self.master, text="Save Result", command=self.save_scan, bg="#FF0000", fg=m1c).place(x=566, y=500, width=518)  # Red background
 # Adjusted width


		def scan_port(self, target, port):
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(4)
				connection = s.connect_ex((target, port))
				if connection == 0:
					message = f'Port {port} \t[open]'
					self.log.append(message)
					self.ports.append(port)
					self.listbox.insert(tk.END, message)
					self.update_result()
					insert_scan_result(target, port, "open")  
				
				s.close()
			except Exception as e:
				print(f'> Error scanning port {port}: {e}')

		def update_result(self):
			result_text = f"[ {len(self.ports)} / {self.ip_f - self.ip_s + 1} ] ~ {self.target}"
			self.L27.configure(text=result_text)

		def start_scan(self):
			self.log.clear()
			self.ports.clear()
			self.listbox.delete(0, tk.END)
			self.target = self.L22.get()
			self.ip_s = int(self.L24.get())
			self.ip_f = int(self.L25.get())

			self.log.append('> Port Scanner\n' + '=' * 14 + '\n')
			self.log.append(f'Target:\t{self.target}')

			try:
				self.target = socket.gethostbyname(self.target)
				self.log.append(f'IP Addr.:\t{self.target}')
				self.log.append(f'Ports:\t[ {self.ip_s} / {self.ip_f} ]\n')

				for port in range(self.ip_s, self.ip_f + 1):
					threading.Thread(target=self.scan_port, args=(self.target, port), daemon=True).start()
			except Exception as e:
				messagebox.showerror("Error", f"Could not resolve {self.target}: {e}")

		def save_scan(self):
			filename = f'portscan-{self.target}.txt'
			with open(filename, 'w') as file:
				for entry in self.log:
					file.write(entry + '\n')
			messagebox.showinfo("Save Successful", f"Results saved to {filename}")

		def clear_scan(self):
			self.listbox.delete(0, tk.END)

# Example of standalone operation for testing
if __name__ == "__main__":
    root = tk.Tk()
    app = PortScanGUI(root)
    root.mainloop()
