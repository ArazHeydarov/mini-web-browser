from tkinter import Label, Entry
import requests
from tkhtmlview import HTMLScrolledText
from threading import Lock, Thread
from time import sleep
from random import choice

class HtmlView:
    def __init__(self, root):
        """
        This class is used to create a HTML view widget
        :param root:
        """
        self.lock = Lock()
        self.age = Age()
        self.label = Label(root)
        self.html_view = HTMLScrolledText(root, width=50)
        self.url: str = ""
        self.timerThread = Thread(target=self.age_counter)

    def set_html(self, entry: Entry):
        """
        This function is used to set the HTML content of the view
        :param entry:
        :return:
        """
        self.url = entry.get()
        self.refresh_page()

    def refresh_page(self):
        """
        This function is used to refresh the page
        :return:
        """
        self.lock.acquire()
        self.label.config(text='Loading...')
        response = self.fetch_url()
        self.html_view.set_html(response.text)
        self.lock.release()
        self.age.set_age(0)

    def fetch_url(self):
        """
        This function is used to fetch the URL
        :return:
        """
        resp = None
        try:
            resp = requests.get(self.url)
        except requests.exceptions.MissingSchema as ms:
            resp = requests.get('https://' + self.url)
        finally:
            return resp

    def age_counter(self):
        """
        This function is used to count the age of the view and setting the label accordingly
        :return:
        """
        while True:
            sleep(1)
            age = self.age.increase_age()
            if age >= 60:
                self.refresh_page()
                continue
            self.label.config(text=f"Age is {self.age.get_age()} seconds")

    def start_timer_thread(self):
        """
        This function is used to start the timer thread
        :return:
        """
        if not self.timerThread.is_alive():
            self.timerThread.start()


class Age:
    def __init__(self):
        """
        This class is used to create an age object
        :return:
        """
        self.age = 60
        self.lock = Lock()

    def increase_age(self):
        """
        This function is user to increase age value by one in thread safe mode
        :return:
        """
        self.lock.acquire()
        self.age += 1
        self.lock.release()
        return self.get_age()

    def get_age(self):
        """
        This function is used to get the age value in thread safe mode
        :return:
        """
        self.lock.acquire()
        age = self.age
        self.lock.release()
        return age

    def set_age(self, age):
        """
        This function is used to set the age value in thread safe mode
        :param age:
        :return:
        """
        self.lock.acquire()
        self.age = age
        self.lock.release()

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
