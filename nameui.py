import sys
import pandas as pd
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading, traceback, time, logging, logging.config
# Makes sure we are running a threaed tkinter build
Tcl().eval('set tcl_platform(threaded)')




class Root_Win:
    """
    Class representing the window the GUI, contains all frames, parent
    object of all the frames. Provides methods for manipulating the frames
    as a whole frame. Object that is created by main file for creating the GUI
    """

    # Integer codes for logging levels
    info = 20
    warn = 30
    error = 40

    # Format for logs
    formatter = logging.Formatter('%(asctime)s | %(levelname)s\n%(message)s',
                                  datefmt='%Y-%m-%d, %H:%M:%S')

    def __init__(self, main_model, test=False):
        """
        Constructor for the Root_Win object. Sets up each frame and event
        binding.
        @params - main_model - the Model object from main. Calls it's
                  process_input method on the input
        @return - A Root_Win object
        """
        self._main_model = main_model
        self._test = test
        self._thread = None

        self._win = Tk()
        self._win.title("Name Pronuncation Program")
        self._win.wm_title("Name Pronuncation Program")

        # Binds protocol for when the window is 'x'ed out.
        self._win.protocol("WM_DELETE_WINDOW", self.exit_program)
        # Overrides the thread exception handling
        threading.excepthook = self.catch_thread_exception
        # Overrides gui thread exception handling
        sys.excepthook = self.catch_exception

        # log files
        message_handler = logging.FileHandler('message.log')
        error_handler = logging.FileHandler('error.log')
        message_handler.setFormatter(Root_Win.formatter)
        error_handler.setFormatter(Root_Win.formatter)

        self._message_log = logging.getLogger("Message Log")
        self._error_log =  logging.getLogger("Error Log")

        self._message_log.setLevel(Root_Win.info)
        self._error_log.setLevel(Root_Win.error)

        self._message_log.addHandler(message_handler)
        self._error_log.addHandler(error_handler)



        # Virtual Event bindings.
        # IF YOU WANT A VIRTUAL EVENT TO RUN A METHOD WHEN FIRED,
        # IT MUST BE BOUND TO THAT METHOD HERE
        self._win.bind("<<ThreadEnded>>", self.thread_finished)
        self._win.bind("<<AddProgress>>", self.add_progress)
        self._win.bind("<<SendMessage>>", self.to_gui_message_log)


        self._intro_frame = Intro_Frame(self)
        self._manual_frame = Manual_Entry_Frame(self, self._main_model, test)
        self._file_frame = File_Entry_Frame(self, self._main_model, test)
        self._progress_frame = Progress_Frame(self)

        self._doing_manual = False
        self._doing_file = False

        self._intro_frame._frame.grid(row = 0, column = 0, padx = 10, pady = 10,
                                      sticky="NSEW")
        self._manual_frame._frame.grid(row = 0, column = 1,
                                       padx = 10, pady = 10, sticky="NSEW")
        self._file_frame._frame.grid(row = 1, column = 0,
                                       padx = 10, pady = 10, sticky="NSEW")
        self._progress_frame._frame.grid(row = 1, column = 1,
                                         padx = 10, pady = 10, sticky = "NSEW")

        self._win.columnconfigure(0, weight=2)
        self._win.columnconfigure(1, weight=2)
        self._win.rowconfigure(0, weight=2)
        self._win.rowconfigure(1, weight=2)


    def exit_program(self):
        """
        Method that is called when the 'WM_DELETE_WINDOW', or 'xing out',
        window event is fired. Default is to destroy the window, kills the
        GUI.
        @params - self
        @returns - None
        """
        box_msg = "Are you sure you want to quit?"
        if threading.active_count() > 1:
            box_msg += " Warning! The main program is currently running. " \
                       "If you exit, it will stop running."
        out = messagebox.showinfo(type="yesno",
                                   message=box_msg)
        # cancel exit
        if out == "no":
            return
        self._win.destroy()
        self._win.quit()

    def get_win(self):
        """
        Accessor the the _win attribute.
        @params - self
        @return - self._win (a tk Window)
        """
        return self._win

    def mainloop(self):
        """
        Wrapper for tkinter's mainloop method
        @params - self
        @returns - None
        """
        self._win.mainloop()

    def disable_entry(self):
        """
        Method disables the manual entry and file entry frames with a call
        to their disable method.
        @params - self
        @returns - None
        """
        self._manual_frame.disable()
        self._file_frame.disable()

    def enable_entry(self):
        """
        Method enables the manual entry and file entry frames with a call
        to their enable method.
        @params - self
        @returns - None
        """
        self._manual_frame.enable()
        self._file_frame.enable()

    def generate_event(self, event):
        """
        Method is a wrapper for Tkinter's event_generate method.
        I call it generate_event because I like that better than
        event_generate
        @params - self
                - event: a string denoting the event to be fired.
                         virtual (abitartily defined) events are denoted
                         with << and >> Ex: <<Event_Here>>.
                         To actually have something happen when a virtual event
                         fires, the event must be bound to a method in
                         the object's constructor.
        @returns - None
        """
        self._win.event_generate(event)

    def thread_finished(self, _):
        """
        Method that is ran when the virtual event for the non-gui
        thread finishing normally is fired. Tests to see which type of entry
        occured calls that type of output, then resets the GUI to a single
        threaded state (enable frames, set status attributes to False)
        @params - self
                - _ - This parameter is a string that denotes the virtual
                      event which called this function. Currently unused.
        @returns - None
        """
        if self._doing_manual:
            self._manual_frame.thread_finished()
            self._doing_manual = False
        elif self._doing_file:
            self._file_frame.thread_finished()
            self._doing_file = False

        self.enable_entry()
        self.reset_progress()

    def hide_prog_lbl(self):
        """
        Wrapper for progress frame's hide_label
        @params - self
        @returns - None
        """
        self._progress_frame.hide_label()

    def set_thread(self, value):
        """
        Method for setting the object's thread attribute
        @params - self
                - value: the python thread object to be assigned to self._thread
        @returns - None
        """
        self._thread = value

    def get_thread(self):
        """
        Method for accessing the object's thread attribute.
        @params - self
        @returns - self._thread - a python thread object
        """
        return self._thread

    def set_doing_file(self, value):
        """
        Method for setting the object's doing_file status attribute
        @params - self
                - value: a boolean value
        @returns - None
        """
        self._doing_file = value

    def set_doing_manual(self, value):
        """
        Method for setting the object's doing_manual status attribute
        @params - self
                - value: a boolean value
        @returns - None
        """
        self._doing_manual = value

    def add_progress(self, _):
        """
        Method for adding progress to the progress frame's progressbar.
        Ran when the <<AddProgress>> virtual event is fired.
        @params - self
                - _: This unused parameter denotes the name of the event
                     this method was fired by.
        @returns - None
        """
        self._main_model.lock.acquire()
        self._progress_frame.add_progress(self._main_model.prog_val)
        self._main_model.lock.release()

    def reset_progress(self):
        """
        Method for resetting the progress frame's progressbar
        @params - self
        @returns - None
        """
        self._progress_frame.reset_progress()

    def to_gui_message_log(self, _):
        """
        Method for sending a message (info or warning) to the message log
        Runs when the <<SendMessage>> virtual event is fired.
        @params - self
                - _: This unused parameter denotes the name of the event
                     this method was fired by.
        @returns - None
        """
        self._main_model.lock.acquire()
        # The message itself
        message = self._main_model.to_gui_message
        # Whether we want to output a warning or a message
        if self._main_model.is_warning:
            level = Root_Win.warn
            self._progress_frame.show_label()
        else:
            level = Root_Win.info
        self._main_model.lock.release()

        self.to_message_log(message, level)

    def to_message_log(self, output, level):
        """
        Wrapper Method for _message_log's .log method for logging a message.
        @params - self
                - output: the message to be output
                - level: An integer denoting the level of the message
                  (info is 20, warning 30, error 40)
        @returns - None
        """
        self._message_log.log(level, output)

    def to_error_log(self, output):
        """
        Wrapper Method for _error_log's .error method for logging an error.
        @params - self
                - output: the message to be output

        @returns - None
        """
        self._error_log.error(output)


    def catch_exception(self, exc_type, exc_value, exc_traceback):
        """
        Method that is called when an exception occurs in the gui thread.
        Overrides the provided sys.excepthook so that we can write the error a
        log, then exit the program with a return value of 1, indicating error.
        @params - self
                - exc_type: an exception type
                - exc_value: The value passed with the exception
                - exc_traceback: A traceback object for the exception
        @returns - None
        """
        self.to_error_log("".join(traceback.format_exception(exc_type,
                                  exc_value, exc_traceback)))
        exc_name = str(exc_type)
        exc_name = exc_name[exc_name.find('\'') + 1:].strip("'>")
        if exc_name.find("Error") == -1:
            exc_name += " error"
        messagebox.showinfo(message=f"An uncaught {exc_name} " \
                                     "occurred in the GUI. Check error.log " \
                                     "for more details.")

        sys.exit(1)



    def catch_thread_exception(self, args):
        """
        Method that is called when an exception occurs in the non-gui thread.
        Overrides the provided threading.excepthook so that we can reset the
        GUI to a single-thread state.
        @params - self
                - args: a tuple containing:
                        exc_type: an exception type
                        exc_value: The value passed with the exception
                        exc_traceback: A traceback object for the exception
                        thread: Which thread the exception occured in
        @returns - None
        """
        exc_type, exc_value, exc_traceback, thread = args
        self.to_error_log("".join(traceback.format_exception(exc_type,
                                  exc_value, exc_traceback)))

        exc_name = str(exc_type)
        exc_name = exc_name[exc_name.find('\'') + 1:].strip("'>")
        if exc_name.find("Error") == -1:
            exc_name += " error"

        messagebox.showinfo(message=f"An uncaught error of type: {exc_type}, " \
                                     "occurred in the non-gui thread. Check " \
                                     "error.log for more details.")

        self._doing_file = False
        self._doing_manual = False
        out_file = self._file_frame.get_outfile()
        if out_file:
            out_file.close()
            self._file_frame.set_outfile(None)

        self.reset_progress()
        self.enable_entry()

class GUI_Frame:
    """
    Parent Class for all GUI Frames. Provides disable and
    enable.
    """

    def __init__(self, parent, text = ""):
        """
        Constructor for GUI Frames. Sets the parent attribute and
        Creates the ttk (Label)Frame
        @params - parent: The parent object of the frame. (Root_Win)
                - text: The text to display on the border of the frame
        @returns A GUI_Frame Object
        """
        self._parent = parent
        self._frame = ttk.Labelframe(self._parent.get_win(),
                                     padding = "5 5 10 10", text=text)

    def disable(self):
        """
        Method disables(greys out) each child widget in the frame
        @params - self
        @returns - None
        """
        for child in self._frame.winfo_children():
            child.configure(state='disable')

    def enable(self):
        """
        Method enables each child widget in the frame
        @params - self
        @returns - None
        """
        for child in self._frame.winfo_children():
            child.configure(state='enable')

class Intro_Frame(GUI_Frame):
    """
    Class representing the top-left frame, which currently
    contains some text welcoming the user to the program. Will likely
    eventually include options for the program.
    """

    def __init__(self, parent):
        """
        Constructor for Intro_Frames. Takes parent, passes to super's
        constructor, creates the label, and places it in the frame.
        @params - parent
        @returns - An Intro_Frame Object
        """
        super().__init__(parent, "Welcome & Options")
        self._label = ttk.Label(self._frame, text="Hello! Welcome to " \
                                "the name pronuncation program!")
        # for debugging
        self._thrd_button = ttk.Button(self._frame, text="threads",
                                       command=self.count_threads)
        self._label.grid(row = 0, column = 0)
        #self._thrd_button.grid(row = 1, column = 0)
        # To add options........

    def count_threads(self):
        """
        Debugging method
        """
        print("Number of threads", threading.active_count())


class Manual_Entry_Frame(GUI_Frame):
    """
    Class reperesenting the frame for manual entry of names to the program.
    Contains a constructor and a method that fires when the user presses the
    run button.
    """
    def __init__(self, parent, main_model, test):
        """
        Constructor for the Manual_Entry_Frame. Calls the parent constructor,
        creates the GUI elements and places them. User_in is a variable
        representing the value of the input field.
        @params - parent - parent object of the frame
                - main_model - the Model object from main. Calls it's
                  process_input method on the input and retrives output from it
        @returns - A Manual_Entry_Frame object.
        """
        super().__init__(parent, text="Manual Entry")
        self._main_model = main_model
        self._test = test

        self._lbl = ttk.Label(self._frame, text="Please enter a name: ")
        self._enter_button = ttk.Button(self._frame, text="Run",
                                        command=self.input_to_main)

        # Variable for storing the value in the entry field. StringVar is a
        # Tkinter specific class that it uses for this.
        self._user_in = StringVar()
        self._entry_field = ttk.Entry(self._frame, textvariable=self._user_in)


        # Formatting
        self._lbl.grid(row = 0, column = 0, pady=10)
        self._entry_field.grid(row = 0, column = 1, pady=10)
        self._enter_button.grid(row = 1, column = 1)

    def input_to_main(self):
        """
        Method that is called when the user presses the 'run' button. Makes
        sure the user has entered something, and if so, converts the input
        to a dataframe, runs link_cmd on it, and outputs the result to
        a message box.
        @params - self
        @returns - None
        """
        user_input = str(self._user_in.get())
        if user_input != "":
            self._parent.set_doing_manual(True)
            self._user_in.set("")
            in_data = pd.DataFrame([user_input])
            self._parent.disable_entry()
            self._parent.hide_prog_lbl()

            # Set up the thread

            # For testing the gui
            if self._test:
                self._parent.set_thread(threading.Thread(
                                        target=self._main_model.test_gui,
                                        args=(in_data,), daemon=True))
            # For actually running
            else:
                self._parent.set_thread(threading.Thread(
                                        target=self._main_model.process_input,
                                        args=(in_data,), daemon=True))
            # run the thread
            self._parent.get_thread().start()
        else:
            messagebox.showinfo(message="Please enter something")



    def thread_finished(self):
        """
        Method that is called by the parent's thread_finished method if
        doing_manual is true. Method outputs the main model's result attribute
        in a messagebox.
        @params - self
        @returns - None
        """
        self._main_model.lock.acquire()
        df = self._main_model.result
        output = f"{df.iloc[0][0]}: ({df.iloc[0][1]}, {df.iloc[0][2]}, " \
                 f"{df.iloc[0][3]}, {df.iloc[0][4]}, {df.iloc[0][5]}, " \
                 f"{df.iloc[0][6]}, {df.iloc[0][7]})\n"
        output += "Scores are: (Combined Score, Bigrams Letters Score, " \
                   "Bigrams Phoneme Score, Trigrams Letter Score, " \
                   "Trigrams Phoneme Score, isEnglishNN Score, LanguageFamily)"
        messagebox.showinfo(message=output)

        self._main_model.lock.release()


class File_Entry_Frame(GUI_Frame):
    """
    Class representing the frame for File Entry. Provides methods for
    the user to enter input/output filenames, and to pass the data to
    the main program.
    """

    def __init__(self, parent, main_model, test):
        """
        Constructor. Calls the parent constructor, then creates and places
        the GUI widgets. Sets up several variables to store the filenames
        the user inputs.
        @params - parent: the parent object of the frame
                - main_model - the Model object from main. Calls it's
                  process_input method on the input
        @returns - A File_Entry_Frame object
        """
        super().__init__(parent, "File Entry")
        self._main_model = main_model
        self._test = test
        # Needed for multithreading since we write the data to the file
        # only after the thread finished, but we want to open before we run the
        # thread, to see if we have any issues opening it
        self._out_file = None

        self._inputf_lbl = ttk.Label(self._frame, text="Please Enter an Input" \
                                     " File Name: ")
        self._outputf_lbl = ttk.Label(self._frame, text="Please Enter an " \
                                      "Output File Name: ")

        self._inputf_text = StringVar(self._frame)
        self._inputf_field = ttk.Entry(self._frame,
                                       textvariable=self._inputf_text)

        self._outputf_text = StringVar(self._frame)
        self._outputf_field = ttk.Entry(self._frame,
                                        textvariable=self._outputf_text)

        self._inputf_button = ttk.Button(self._frame, text="Browse",
                                         command=self.set_infile_name)
        self._outputf_button = ttk.Button(self._frame, text="Browse",
                                          command=self.set_outfile_name)

        self._run_button = ttk.Button(self._frame, text="Run",
                                      command=self.input_to_main)

        # Formatting
        self._inputf_lbl.grid(row = 0, column = 0, sticky="NSW", padx = (0, 5))
        self._inputf_field.grid(row = 0, column = 1)
        self._inputf_button.grid(row = 0, column = 2, padx = 10, pady = 10)
        self._outputf_lbl.grid(row = 1, column = 0, sticky="NSW", padx = (0, 5))
        self._outputf_field.grid(row = 1, column = 1)
        self._outputf_button.grid(row = 1, column = 2, padx = 10, pady = 10)
        self._run_button.grid(row = 2, column = 2, padx = 10, pady = 10)


    def get_outfile(self):
        """
        Method is accessor for the _out_file attribute
        @params - self
        @returns - self._out_file: a file object
        """
        return self._out_file

    def set_outfile(self, value):
        """
        Method is a setter for the _out_file attribute
        @params - self
                - value: the new value for _out_file (should be a file or None)
        @returns - None
        """
        self._out_file = value

    def set_infile_name(self):
        """
        Method that runs a file dialog for the user to select an input file.
        Sets the inputf_text attribute to the user's input.
        @params - self
        @returns - None
        """
        done = False
        while not done:
            input_name = filedialog.askopenfilename(title="Select an input file",
                                                    filetypes=[("CSV",".csv")])
            if input_name == "":
                out = messagebox.showinfo(type="okcancel",
                                          message="Please select a file")

                # exit file entry
                if out == "cancel":
                    return

            else:
                done = True

        self._inputf_text.set(input_name)

    def set_outfile_name(self):
        """
        Method that runs a file dialog for the user to select an output file.
        Sets the outputf_text attribute to the user's input.
        @params - self
        @returns - None
        """
        done = False
        while not done:
            output_name = filedialog.asksaveasfilename(title="Select an " \
                          "output file", initialfile="Untitled.csv",
                          filetypes = [("CSV", ".csv")],
                          defaultextension='.csv')

            if output_name == "":
                out = messagebox.showinfo(type="okcancel",
                                          message="Please select a file")
                # exit file entry
                if out == "cancel":
                    return
            else:
                done = True

        self._outputf_text.set(output_name)


    def input_to_main(self):
        """
        Method that connects to the main program. Retrivies the inputf and
        outputf texts to check if they are empty. If so, it exits, prompting
        the user to enter both a input and output file name. It additionally
        checks if the input file exists. If the file exists, the method
        reads the data and sends it to the main program by creating a new
        thread and running that thread.

        While the main programming is running, we disable both this frame and
        the manual_entry frame with a call to the parent, so that we do not
        create more than one thread.
        @params - self
        @returns - None
        """
        input_name = self._inputf_text.get()
        output_name = self._outputf_text.get()

        if input_name == "" or output_name == "":
            messagebox.showinfo(message="Please select an input and an " \
                                        "output file.")
            return


        if not path.exists(input_name):
            messagebox.showinfo(message="The given input file does not exist.")
            return

        try:
            in_file = open(input_name, encoding="UTF-8")
        except PermissionError:
            messagebox.showinfo(message="Error: Input File Permisson Denied. " \
                                        "Do you have the file open?")
            return

        try:
            self._out_file = open(output_name, mode="w", encoding="UTF-8")
        except PermissionError:
            messagebox.showinfo(message="Error: Output File Permisson Denied." \
                                        " Do you have the file open?")
            return

        self._inputf_text.set("")
        self._outputf_text.set("")
        in_data = pd.read_csv(in_file, sep=",", header=None)
        in_file.close()

        # Setting GUI to a two thread state
        self._parent.set_doing_file(True)
        self._parent.disable_entry()
        self._parent.hide_prog_lbl()

        # Setting up the thread

        # For testing the gui
        if self._test:
            self._parent.set_thread(threading.Thread(
                                    target=self._main_model.test_gui,
                                    args=(in_data,), daemon=True))
        # For actually running
        else:
            self._parent.set_thread(threading.Thread(
                                    target=self._main_model.process_input,
                                    args=(in_data,), daemon=True))

        # Run the thread
        self._parent.get_thread().start()

    def thread_finished(self):
        """
        Method that is called by parent's thread_finished method if
        doing_file is true. Writes the MainModel's result attribute
        (a pd dataframe) to self._out_file, then closes out_file
        @params - self
        @return - None
        """
        self._main_model.lock.acquire()
        columns = ["Name", "Combined Score", "Bigrams Letters Score",
                   "Bigrams Phoneme Score", "Trigrams Letter Score",
                   "Trigrams Phoneme Score", "isEnglishNN Score",
                   "LanguageFamily"]
        self._main_model.result.to_csv(self._out_file, index=False,
                                       header=columns,
                                       line_terminator = '\n')
        self._out_file.close()
        self._out_file = None
        self._main_model.lock.release()
        self._parent.reset_progress()
        messagebox.showinfo(message="Done!")


class Progress_Frame(GUI_Frame):
    """
    Class representing the bottom-right frame, or the frame containing
    the progress bar and in-gui message log (at some point).
    """
    # To Do: Add text widget for displaying messages/warnings
    def __init__(self, parent):
        """
        Constructor for the Progress_Frame class. Creates the progress bar and
        its varaible that stores the progress value, as well as a label
        that appears when a warning is sent to the message log (latter will
        be replaced at some point)
        """
        super().__init__(parent, "Progress & Messages")

        self._progress_value = IntVar()
        self._progress_bar = ttk.Progressbar(self._frame, length=250, mode=
                                             "determinate", variable=self._progress_value)
        self._log_msg_lbl = ttk.Label(self._frame,
                                  text = "A warning has been sent to the message log")
        self._progress_bar.grid(row = 0, column = 0, sticky="NSEW", padx=5, pady=5)

        self._log_msg_lbl.grid(row = 0, column = 1, padx=5, pady=5)
        self._log_msg_lbl.grid_forget()


    def add_progress(self, value):
        """
        Method that adds an amount of progress equal to value param to the
        object's _progress_value attribute, which _progress_bar uses to update.
        @params - self
                - value: The value to add to the progress bar
        @returns - None
        """
        self._progress_value.set(self._progress_value.get() + value)

    def reset_progress(self):
        """
        Method that resets the object's _progress_value attribute to zero,
        which _progress_bar uses to update to an empty state.
        @params - self
        @returns - None
        """
        self._progress_value.set(0)

    def show_label(self):
        """
        Method for showing the log message label
        @params - self
        @returns - None
        """
        self._log_msg_lbl.grid()

    def hide_label(self):
        """
        Method for hiding the log message label
        @params - self
        @returns - None
        """
        self._log_msg_lbl.grid_forget()


def main():
    """
    Main just sets up the root window and calls it's mainloop.
    """

    root = Root_Win(print_ret)
    root.mainloop()


if __name__ == "__main__":
    main()
