import tkinter as tk
from tkinter import filedialog

class EventInvitationManager:

    def __init__(self, master):
        self.master = master
        master.title("Event Invitation Manager")

        # Create labels
        self.label1 = tk.Label(master, text="Event Name:")
        self.label2 = tk.Label(master, text="Event Date:")
        self.label3 = tk.Label(master, text="Event Time:")
        self.label4 = tk.Label(master, text="Guest List:")

        # Create entry fields
        self.entry1 = tk.Entry(master)
        self.entry2 = tk.Entry(master)
        self.entry3 = tk.Entry(master)
        self.entry4 = tk.Entry(master)

        # Create buttons
        self.button1 = tk.Button(master, text="Select Guest List", command=self.select_file)
        self.button2 = tk.Button(master, text="Send Invitations", command=self.send_invitations)

        # Add widgets to the window
        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0)
        self.label3.grid(row=2, column=0)
        self.label4.grid(row=3, column=0)

        self.entry1.grid(row=0, column=1)
        self.entry2.grid(row=1, column=1)
        self.entry3.grid(row=2, column=1)
        self.entry4.grid(row=3, column=1)

        self.button1.grid(row=4, column=0)
        self.button2.grid(row=4, column=1)

    def select_file(self):
        # Open a file dialog to select a guest list file
        file_path = filedialog.askopenfilename()
        self.entry4.insert(0, file_path)

    def send_invitations(self):
        # TODO: implement function to send event invitations
        print("Invitations sent!")

root = tk.Tk()
my_gui = EventInvitationManager(root)
root.mainloop()
