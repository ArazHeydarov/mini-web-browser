from tkinter import Tk, Label, Button, Entry
from browser.src import HtmlView, button_func


# Initialize the main window
root = Tk()
root.title("My App")

# Create the entry widget and the label for it
url_label = Label(root, text="Enter URL")
url_entry = Entry(root, width=100)

# Create HTML views
left_hv = HtmlView(root)
right_hv = HtmlView(root)

# Create the fetching button
fetch_button = Button(root, text="Fetch", width=10, command=lambda: button_func(url_entry, left_hv, right_hv))

# Place the widgets in grid
url_label.grid(row=0, column=0)
url_entry.grid(row=0, column=1, columnspan=2, pady=10)
fetch_button.grid(row=0, column=3)
left_hv.label.grid(row=1, column=0, columnspan=2)
right_hv.label.grid(row=1, column=2, columnspan=2)
left_hv.html_view.grid(row=2, column=0, columnspan=2)
right_hv.html_view.grid(row=2, column=2, columnspan=2)

# Start the main loop
root.mainloop()
