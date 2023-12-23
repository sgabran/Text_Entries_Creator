# 2023-12-23

import os
import os.path
from idlelib.tooltip import *
from tkinter import filedialog
from tkinter import messagebox
import csv

import sys
import shutil

import filename_methods as fm
import misc_methods as mm
from constants import *
from session_log import SessionLog
from user_entry import UserEntry


# Class to create GUI
class MainWindow:
    # Dependencies: MainWindow communicate with classes that are related to GUI contents and buttons
    def __init__(self):  # instantiation function. Use root for GUI and refers to main window

        root = Tk()
        root.title("Text Entries Creator")
        self.root_frame = root
        self.user_entry = UserEntry()
        self.session_log = SessionLog(self.user_entry)

        self.file_contents_raw = ""

        # GUI Frames
        self.frame_root_session = Frame(root)
        self.frame_file = LabelFrame(self.frame_root_session, padx=5, text="File")
        self.frame_review = LabelFrame(self.frame_root_session, width=100, height=5, padx=5, text="Review")

        # Disable resizing the window
        root.resizable(False, False)

        entry_validation_positive_numbers = root.register(mm.only_positive_numbers)
        entry_validation_positive_numbers_nonzero = root.register(mm.only_positive_numbers_nonzero)
        entry_validation_numbers = root.register(mm.only_digits)
        entry_validation_numbers_space = root.register(mm.digits_or_space)
        entry_validation_positive_numbers_comma = root.register(mm.positive_numbers_or_comma)

        # Grids
        self.frame_root_session.grid    (row=0, column=0)
        self.frame_file.grid            (row=0, column=0, padx=5, pady=(5, 5), ipadx=5, ipady=2)
        self.frame_review.grid          (row=1, column=0, padx=5, pady=(5, 5), ipadx=5, ipady=2)

        ######################################################################
        # Frame Session

        # Labels
        label_file_name = Label(self.frame_file, text="File Name")
        label_entry_format = Label(self.frame_file, text="Data")
        label_n_entries = Label(self.frame_file, text="Entries")

        # Entries
        self.entry_file_name_entry = StringVar()
        self.entry_file_name_entry.trace("w", lambda name, index, mode, entry_file_name_entry=self.entry_file_name_entry: self.entry_update_file_name())
        self.entry_file_name = Entry(self.frame_file, width=20, textvariable=self.entry_file_name_entry)
        self.entry_file_name.insert(END, os.path.normcase(""))

        self.entry_n_entries_entry = StringVar()
        self.entry_n_entries_entry.trace("w", lambda name, index, mode, entry_n_entries_entry=self.entry_n_entries_entry: self.entry_update_n_entries())
        self.entry_n_entries = Entry(self.frame_file, width=10, textvariable=self.entry_n_entries_entry, validate="key", validatecommand=(entry_validation_positive_numbers, '%S'))
        self.entry_n_entries.insert(END, str(N_ENTRIES))

        self.entry_data_format_entry = StringVar()
        self.entry_data_format_entry.trace("w", lambda name, index, mode, entry_data_format_entry=self.entry_data_format_entry: self.entry_update_data_format())
        self.entry_data_format = Entry(self.frame_file, width=40, textvariable=self.entry_data_format_entry)

        # Buttons
        self.button_create_file = Button(self.frame_file, text="Create File", command=lambda: self.create_file(), pady=0, width=10, fg='blue')
        self.button_create_sample = Button(self.frame_file, text="Show Sample", fg='green', command=self.show_sample, pady=0, width=12)
        self.button_open_folder = Button(self.frame_file, text="Folder", fg='black', command=self.open_folder, pady=0, width=10)
        self.button_exit = Button(self.frame_file, text="Exit", fg='red', command=self.quit_program, pady=0, width=10)

        # Textbox
        self.textbox_sample = Text(self.frame_review, height=5, width=50)
        self.textbox_sample_vscroll_bar = Scrollbar(self.frame_review, orient="vertical")
        self.textbox_sample_vscroll_bar.config(command=self.textbox_sample.yview)
        self.textbox_sample.config(yscrollcommand=self.textbox_sample_vscroll_bar.set)
        self.textbox_row_clear()

        # Grids
        self.textbox_sample.grid        (row=0, column=0)
        label_file_name.grid            (row=0, column=0, sticky=E)
        self.entry_file_name.grid       (row=0, column=1, sticky=W)
        label_n_entries.grid            (row=1, column=0, sticky=E)
        self.entry_n_entries.grid       (row=1, column=1, sticky=W)
        label_entry_format.grid         (row=2, column=0, sticky=E)
        self.entry_data_format.grid     (row=2, column=1, sticky=W)
        self.button_create_sample.grid  (row=3, column=0, sticky=W)
        self.button_create_file.grid    (row=3, column=1, sticky=W)
        self.button_open_folder.grid    (row=3, column=1, sticky=W, padx=80)
        self.button_exit.grid           (row=3, column=1, sticky=W, padx=160)

        # END OF FRAME #######################################################

        self.root_frame.mainloop()

    ######################################################################

    @staticmethod
    def quit_program():
        # quit()  # quit() does not work with pyinstaller, use sys.exit()
        sys.exit()

    def create_file(self):
        self.show_sample()
        self.save()

    def save(self):
        self.user_entry.file_extension = FILE_EXTENSION
        self.user_entry.file_folder = FILE_FOLDER
        self.user_entry.file_address = fm.FileNameMethods.build_file_name_full(self.user_entry.file_folder, self.user_entry.file_name, self.user_entry.file_extension)
        print("::user_entry.file_name: ", self.user_entry.file_name)
        print("::user_entry.file_extension: ", self.user_entry.file_extension)
        print("::user_entry.file_folder: ", self.user_entry.file_folder)
        print("::user_entry.file_address: ", self.user_entry.file_address)

        self.entry_file_name_entry.set(self.user_entry.file_name)

        if not os.path.exists(self.user_entry.file_folder):
            os.makedirs(self.user_entry.file_folder)
            print(f"Directory '{self.user_entry.file_folder}' created.")
            message = "Created Folder: " + str(self.user_entry.file_folder) + '\n'
            colour = "black"
            self.session_log.write_textbox(message, colour)
        else:
            print(f"Directory '{self.user_entry.file_folder}' already exists.")
            message = "Folder Exists" + '\n'
            colour = "black"
            self.session_log.write_textbox(message, colour)

        with open(self.user_entry.file_address, 'w') as file:
            for item in self.user_entry.entries:
                file.write(str(item) + '\n')

    def show_sample(self):
        self.textbox_row_clear()
        self.create_entries()
        self.textbox_update_list(self.user_entry.entries)

    def open_folder(self):
        if fm.FileNameMethods.check_folder_location_valid(self.user_entry.file_folder):
            os.startfile(self.user_entry.file_folder)
        else:
            messagebox.showinfo(title="Error", message="Folder Does Not Exist")
        return

    def entry_update_file_name(self):
        try:
            file_name = self.entry_file_name.get()
            self.user_entry.file_name = file_name
            print("::user_entry.file_name: ", self.user_entry.file_name)
        except:
            self.user_entry.file_name = FILE_NAME
            print("::user_entry.file_name: ", self.user_entry.file_name)

    def entry_update_n_entries(self):
        try:
            n_entries = int(self.entry_n_entries_entry.get())
            self.user_entry.n_entries = n_entries
            print("::user_entry.n_entries: ", self.user_entry.n_entries)
        except:
            self.user_entry.n_entries = N_ENTRIES
            print("::user_entry.n_entries: ", self.user_entry.n_entries)

    def entry_update_data_format(self):
        try:
            data_format = self.entry_data_format_entry.get()
            self.user_entry.data_format = data_format
            print("::user_entry.data_format: ", self.user_entry.data_format)
        except:
            self.user_entry.data_format = DATA_FORMAT
            print("::user_entry.data_format: ", self.user_entry.data_format)

    def textbox_row_clear(self):
        message = ""
        self.textbox_sample.configure(state='normal')
        self.textbox_sample.delete('1.0', 'end')
        self.textbox_sample.insert('end', message)
        self.textbox_sample.configure(state='disabled')

    def textbox_update(self, data):
        self.textbox_sample.configure(state='normal')
        self.textbox_sample.delete('1.0', 'end')
        self.textbox_sample.insert('end', data)
        self.textbox_sample.configure(state='disabled')

    def textbox_update_list(self, data):
        self.textbox_sample.configure(state='normal')
        self.textbox_sample.delete('1.0', 'end')

        for item in data:
            self.textbox_sample.insert('end', item)
            self.textbox_sample.insert('end', '\n')

        self.textbox_sample.configure(state='disabled')

    @staticmethod
    def save_list_to_file(file_folder, file_name, input_list):
        try:
            # Open file in write mode
            file_path = file_folder + '\\' + file_name + '.txt'
            with open(file_path, 'w') as file:
                # Write each list element to file
                for item in input_list:
                    file.write(str(item) + '\n')
            return 1
        except Exception as e:
            print(f'Error: {str(e)}')
            return 0

    @staticmethod
    def save_list_to_csv(file_folder, file_name, input_list):
        try:
            file_path = file_folder + '\\' + file_name + '.csv'
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in input_list:
                    writer.writerow(row)
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 0

    def create_entries(self):
        result_array = []
        for _ in range(self.user_entry.n_entries):
            result_array.append(self.user_entry.data_format)
        self.user_entry.entries = result_array
