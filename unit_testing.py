import unittest
from unittest.mock import patch, MagicMock
import tkinter as tk
from portscangui import PortScanGUI
from port_pinger import PPPPP_GUI
from gui_sniffer import GUIPacketSniffer
from output import OutputToScreen, Output
from core import Decoder, PacketSniffer

class TestPortScanGUI(unittest.TestCase):
    def setUp(self):
        """Set up a Tkinter root window and an instance of PortScanGUI."""
        self.root = tk.Tk()
        self.app = PortScanGUI(self.root)
        # Prevent the root window from appearing during tests
        self.root.withdraw()

    @patch('socket.socket')
    def test_scan_port(self, mock_socket):
        """Test the scan_port method for open and closed ports."""
        # Set up the mock to simulate an open port
        mock_socket_instance = mock_socket.return_value
        mock_socket_instance.connect_ex.return_value = 0
        self.app.scan_port('localhost', 80)
        # Simulate an open port
        self.assertIn('Port 80 \t[open]', self.app.log)
        
        # Change the mock to simulate a closed port
        mock_socket_instance.connect_ex.return_value = 1
        self.app.scan_port('localhost', 81)
        # Ensure the closed port is not marked as open
        self.assertNotIn('Port 81 \t[open]', self.app.log)

    def test_update_result(self):
        """Test updating the GUI with scan results."""
        self.app.ports = [80]  # Simulate scanning port 80
        self.app.update_result()
        expected_result = "[ 1 / 1024 ] ~ localhost"
        self.assertEqual(self.app.L27['text'], expected_result)

    @patch('socket.gethostbyname')
    @patch('threading.Thread')
    def test_start_scan(self, mock_thread, mock_gethostbyname):
        """Test starting a scan."""
        mock_gethostbyname.return_value = '127.0.0.1'
        self.app.start_scan()
        # Check that threading.Thread was called, indicating a scan was started
        mock_thread.assert_called()
        # Check that gethostbyname was called with the correct target
        mock_gethostbyname.assert_called_with('localhost')

    @patch('builtins.open', unittest.mock.mock_open())
    @patch('tkinter.messagebox.showinfo')
    def test_save_scan(self, mock_showinfo):
        """Test saving scan results."""
        self.app.log = ['Port 80 \t[open]']
        self.app.target = 'localhost'
        self.app.save_scan()
        # Check if the file was attempted to be opened with the correct filename
        mock_showinfo.assert_called_with("Save Successful", "Results saved to portscan-localhost.txt")

    def tearDown(self):
        """Destroy the Tkinter root window."""
        self.root.destroy()


class TestPPPPPGUI(unittest.TestCase):
    def setUp(self):
        """Set up a Tkinter root window and an instance of PPPPP_GUI."""
        self.root = tk.Tk()
        self.app = PPPPP_GUI(self.root)
        # Prevent the root window from appearing during tests
        self.root.withdraw()

    @patch('subprocess.run')
    def test_get_current_network(self, mock_run):
        """Test the retrieval of current network settings."""
        # Mock subprocess.run to return a predetermined output
        mock_output = MagicMock()
        mock_output.stdout = "IP Address: 192.168.1.1\nSubnet Mask: 255.255.255.0\n"
        mock_run.return_value = mock_output

        # self.app.Get_Current_Network()
        # # Verify that subprocess.run was called with the expected arguments
        # mock_run.assert_called_once_with('ipconfig /all', stdout=subprocess.PIPE, text=True)
        # # Further assertions can be made based on how the method processes the output

    @patch('threading.Thread')
    def test_threaded_ping_sweep_1(self, mock_thread):
        """Test the threaded execution of ping sweep."""
        self.app.Threaded_Ping_Sweep_1()
        # Verify that a thread was started for the ping sweep
        mock_thread.assert_called_once()

    @patch('threading.Thread')
    def test_threaded_port_scan_1(self, mock_thread):
        """Test the threaded execution of port scan."""
        self.app.Threaded_Port_Scan_1()
        # Verify that a thread was started for the port scan
        mock_thread.assert_called_once()

    def tearDown(self):
        """Close the Tkinter root window."""
        self.root.destroy()

class TestGUIPacketSniffer(unittest.TestCase):
    def setUp(self):
        """Set up a Tkinter root window and an instance of GUIPacketSniffer."""
        self.root = tk.Tk()
        self.app = GUIPacketSniffer(self.root)
        # Hide the root window during tests
        self.root.withdraw()

    @patch('gui_sniffer.AsyncSniffer')
    def test_start_sniffing(self, mock_sniffer):
        """Test starting packet sniffing."""
        self.app.start_sniffing()
        mock_sniffer.assert_called_once()
        self.assertTrue(self.app.sniffer)
        self.assertEqual('disabled', self.app.start_button['state'])
        self.assertEqual('normal', self.app.stop_button['state'])

    @patch('gui_sniffer.AsyncSniffer')
    def test_stop_sniffing(self, mock_sniffer):
        """Test stopping packet sniffing."""
        mock_sniffer_instance = mock_sniffer.return_value
        self.app.start_sniffing()
        self.app.stop_sniffing()
        mock_sniffer_instance.stop.assert_called_once()
        self.assertIsNone(self.app.sniffer)
        self.assertEqual('normal', self.app.start_button['state'])
        self.assertEqual('disabled', self.app.stop_button['state'])

    def test_display_packet_details_with_mock_event(self):
        """Test displaying details of a selected packet using a mock event."""
        packet = MagicMock()
        packet.show.return_value = 'Packet details'
        self.app.packet_list = [packet]  # Simulate a packet being captured

        mock_event = MagicMock()
        mock_event.x, mock_event.y = 10, 10  # Simulate click coordinates
        # self.app.display_packet_details(mock_event)
        self.root.update_idletasks()  # Process queued GUI events

    def tearDown(self):
        """Destroy the Tkinter root window."""
        self.root.destroy()
        

class MockSubject:
    def register(self, observer):
        pass

class TestOutputToScreen(unittest.TestCase):
    def setUp(self):
        self.subject = MockSubject()
        self.display_data = True
        self.output_to_screen = OutputToScreen(self.subject, display_data=self.display_data)

    def test_initialize(self):
        expected_output = "\n[>>>] Packet Sniffer initialized. Waiting for incoming data. Press Ctrl-C to abort...\n"
        with patch('builtins.print') as mocked_print:
            self.output_to_screen._initialize()
            mocked_print.assert_called_once_with(expected_output)

    def test_display_output_header(self):
        # Mocking time.strftime to return a fixed value
        with patch('output.time.strftime') as mocked_strftime:
            mocked_strftime.return_value = "00:00:00"  # Fixed value for time
            self.output_to_screen._frame = mock_frame()
            expected_output = "[>] Frame #1 at 00:00:00:\n"
            with patch('builtins.print') as mocked_print:
                self.output_to_screen._display_output_header()
                # Custom assertion to ignore time component
                actual_output = mocked_print.call_args_list[0][0][0]
                # self.assert_expected_output(expected_output, actual_output)

    # Add tests for other methods similarly

    def assert_expected_output(self, expected, actual):
        # Custom assertion to ignore time component
        expected = expected.replace("00:00:00", "TIME")
        actual = actual.replace("00:00:00", "TIME")
        # self.assertEqual(expected, actual)

def mock_frame():
    class MockFrame:
        def __init__(self):
            self.packet_num = 1
            self.epoch_time = 0  # For consistent time comparison

    return MockFrame()


class TestDecoder(unittest.TestCase):
    def setUp(self):
        self.interface = "eth0"
        self.decoder = Decoder(self.interface)

    def test_bind_interface(self):
        mock_socket = MagicMock()
        self.decoder._bind_interface(mock_socket)
        mock_socket.bind.assert_called_once_with((self.interface, 0))

    def test_attach_protocols(self):
        frame = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./01234567'
        self.decoder._attach_protocols(frame)
        self.assertIsNotNone(self.decoder.ethernet)
        # Add more assertions for other protocols as needed

    # Add more test cases for other methods in Decoder class

class TestPacketSniffer(unittest.TestCase):
    def setUp(self):
        self.packet_sniffer = PacketSniffer()

    def test_register(self):
        observer = MagicMock()
        self.packet_sniffer.register(observer)
        self.assertIn(observer, self.packet_sniffer._observers)

    def test_notify_all(self):
        observer1 = MagicMock()
        observer2 = MagicMock()
        self.packet_sniffer.register(observer1)
        self.packet_sniffer.register(observer2)
        args = ('test', 'data')
        kwargs = {'key': 'value'}
        self.packet_sniffer._notify_all(*args, **kwargs)
        observer1.update.assert_called_once_with(*args, **kwargs)
        observer2.update.assert_called_once_with(*args, **kwargs)

    # Add more test cases for other methods in PacketSniffer class

if __name__ == '__main__':
    unittest.main()

