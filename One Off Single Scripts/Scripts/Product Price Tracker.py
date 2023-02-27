import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class ProductPriceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Price Tracker")
        self.root.geometry("500x300")

        # Product URL label and entry box
        self.label1 = tk.Label(self.root, text="Enter the URL of the product you want to track:")
        self.label1.pack(pady=10)
        self.entry1 = tk.Entry(self.root, width=50)
        self.entry1.pack(pady=10)

        # Track Price button
        self.btn1 = tk.Button(self.root, text="Track Price", command=self.track_price)
        self.btn1.pack(pady=10)

        # Price history treeview
        self.tree = ttk.Treeview(self.root, columns=("Date", "Price"), show="headings")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Price", text="Price")
        self.tree.pack(pady=10)

    def track_price(self):
        url = self.entry1.get()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        price = self.extract_price(response.content.decode())

        # Add price and date to the price history treeview
        date = tk.StringVar(value=self.get_current_date())
        self.tree.insert("", "end", values=(date.get(), price))

        messagebox.showinfo("Product Price Tracker", f"The price of the product is: {price}")

    def extract_price(self, html):
        start_index = html.find("$")
        end_index = html.find("<", start_index)
        return html[start_index:end_index]

    def get_current_date(self):
        import datetime
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductPriceTracker(root)
    root.mainloop()
