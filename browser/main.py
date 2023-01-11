from tkinter import Tk, Label, Button, Entry
from threading import Thread
from random import choice
from browser.src import HtmlView, Age


def button_func(entry: Entry, left_html_view: HtmlView, right_html_view: HtmlView):
    """
    This function is called when the fetch button is clicked.
    :param entry:
    :param left_html_view:
    :param right_html_view:
    :return:
    """
    age_right_value = right_html_view.age.get_age()
    age_left_value = left_html_view.age.get_age()

    # Comparing the ages of views to decide which one to present the new page
    if age_right_value > age_left_value:
        html_view = right_html_view
    elif age_left_value > age_right_value:
        html_view = left_html_view
    else:
        # If the ages are equal, then randomly choose one of the views
        if choice([0, 1]):
            html_view = right_html_view
        else:
            html_view = left_html_view

    # Start the timer thread if it is not already running
    html_view.start_timer_thread()

    # Staring the html viewer thread for selected view
    thread_html_viewer = Thread(target=html_view.set_html, args=(entry,))
    thread_html_viewer.start()


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
