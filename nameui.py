import sys
import pandas as pd
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading, traceback, time, logging, logging.config, datetime
from logging.handlers import TimedRotatingFileHandler
# Makes sure we are running a threaed tkinter build
Tcl().eval('set tcl_platform(threaded)')




class RootWin:
    """
    Class representing the window the GUI, contains all frames, parent
    object of all the frames. Provides methods for manipulating the frames
    as a whole frame. Object that is created by main file for creating the GUI
    """

    # Format for logs
    formatter = logging.Formatter('%(asctime)s | %(levelname)s\n%(message)s',
                                  datefmt='%Y-%m-%d, %H:%M:%S')

    def __init__(self, main_model, test=False):
        """
        Constructor for the RootWin object. Sets up each frame and event
        binding.
        @params - main_model - the Model object from main. Calls it's
                  processInput method on the input
        @return - A RootWin object
        """
        self._main_model = main_model
        self._test = test
        self._thread = None

        self._win = Tk()
        self._win.title("Name Pronuncation Program")
        self._win.wm_title("Name Pronuncation Program")

        # Binds protocol for when the window is 'x'ed out.
        self._win.protocol("WM_DELETE_WINDOW", self.exitProgram)
        # Overrides the thread exception handling
        threading.excepthook = self.catchThreadException
        # Overrides gui thread exception handling
        #sys.excepthook = self.catchException
        Tk.report_callback_exception = self.catchException

        # log files - Rollover every monday at midnight
        # We must keep one backup (doesn't work otherwise)
        message_handler = TimedRotatingFileHandler('message.log', when='W0',
                                                    atTime=datetime.time(),
                                                    backupCount=1)
        error_handler = TimedRotatingFileHandler('error.log', when='W0',
                                                 atTime=datetime.time(),
                                                 backupCount=1)
        message_handler.setFormatter(RootWin.formatter)
        error_handler.setFormatter(RootWin.formatter)

        self._message_log = logging.getLogger("Message Log")
        self._error_log =  logging.getLogger("Error Log")

        self._message_log.setLevel(logging.INFO)
        self._error_log.setLevel(logging.INFO)

        self._message_log.addHandler(message_handler)
        self._error_log.addHandler(error_handler)

        # Virtual Event bindings.
        # IF YOU WANT A VIRTUAL EVENT TO RUN A METHOD WHEN FIRED,
        # IT MUST BE BOUND TO THAT METHOD HERE
        self._win.bind("<<ThreadEnded>>", self.threadFinished)
        self._win.bind("<<AddProgress>>", self.addProgress)
        self._win.bind("<<SendMessage>>", self.toGuiMessageLog)


        self._intro_frame = IntroFrame(self)

        self._manual_frame = ManualEntryFrame(self, self._main_model, test)
        self._file_frame = FileEntryFrame(self, self._main_model, test)
        self._progress_frame = ProgressFrame(self)

        self._doing_manual = False
        self._doing_file = False

        self._intro_frame._frame.grid(row = 0, column = 0, padx = 10, pady = 10,
                                      sticky="NSEW")
        self._manual_frame._frame.grid(row = 0, column = 1,
                                       padx = 10, pady = 10, sticky="NSW")
        self._file_frame._frame.grid(row = 1, column = 0,
                                       padx = 10, pady = 10, sticky="NSEW")
        self._progress_frame._frame.grid(row = 1, column = 1,
                                         padx = 10, pady = 10, sticky = "NSEW")




    def exitProgram(self):
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
                                   message=box_msg, title="Exit")
        # cancel exit
        if out == "no":
            return
        self._win.destroy()
        self._win.quit()

    def getWin(self):
        """
        Accessor the the _win attribute.
        @params - self
        @return - self._win (a tk Window)
        """
        return self._win

    def mainLoop(self):
        """
        Wrapper for tkinter's mainLoop method
        @params - self
        @returns - None
        """
        self._win.mainloop()

    def disableEntry(self):
        """
        Method disables the manual entry and file entry frames with a call
        to their disable method.
        @params - self
        @returns - None
        """
        self._manual_frame.disable()
        self._file_frame.disable()
        self._intro_frame.disableApply()

    def enableEntry(self):
        """
        Method enables the manual entry and file entry frames with a call
        to their enable method.
        @params - self
        @returns - None
        """
        self._manual_frame.enable()
        self._file_frame.enable()
        self._intro_frame.enableApply()

    def generateEvent(self, event):
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

    def threadFinished(self, _):
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
            self._manual_frame.threadFinished()
            self._doing_manual = False
        elif self._doing_file:
            self._file_frame.threadFinished()
            self._doing_file = False

        self.enableEntry()
        self.resetProgress()
        self.toMessageLog("Sucesfully finished main program execution.",
                            logging.INFO)
        self.toErrorLog("Sucesfully finished main program execution.",
                          logging.INFO)


    def setThread(self, value):
        """
        Method for setting the object's thread attribute
        @params - self
                - value: the python thread object to be assigned to self._thread
        @returns - None
        """
        self._thread = value

    def getThread(self):
        """
        Method for accessing the object's thread attribute.
        @params - self
        @returns - self._thread - a python thread object
        """
        return self._thread

    def setDoingFile(self, value):
        """
        Method for setting the object's doing_file status attribute
        @params - self
                - value: a boolean value
        @returns - None
        """
        self._doing_file = value

    def setDoingManual(self, value):
        """
        Method for setting the object's doing_manual status attribute
        @params - self
                - value: a boolean value
        @returns - None
        """
        self._doing_manual = value


    def applyOptions(self):
        """
        Method ran when the IntroFrame's apply button is pressed, which
        is enabled only in a single-threaded state. This method examines
        the ngrams options selected by the user and calls the main model's
        setNGrams method to apply those changes.
        @params - self
        @returns - None
        """
        dict = self._intro_frame.getOptionValues()
        waitWin = Toplevel(self._win)
        waitWin.title("Applying Options...")
        waitLabel = ttk.Label(waitWin, text = "This may take a moment. Please wait.",
                              font=(None, 18))
        waitLabel.grid(row = 0, column = 0, padx = 5, pady = 5)

        waitLabel.update()
        waitWin.grab_set()        # ensure all input goes to the wait window

        result = []
        for key, value in dict.items():
            if value == 1:
                result.append(key)

        self._main_model.setNGrams(result)
        waitWin.grab_release()
        waitWin.destroy()



    def addProgress(self, _):
        """
        Method for adding progress to the progress frame's progressbar.
        Ran when the <<AddProgress>> virtual event is fired.
        @params - self
                - _: This unused parameter denotes the name of the event
                     this method was fired by.
        @returns - None
        """
        self._main_model.lock.acquire()
        self._progress_frame.addProgress(self._main_model.prog_val)
        self._main_model.lock.release()

    def resetProgress(self):
        """
        Method for resetting the progress frame's progressbar
        @params - self
        @returns - None
        """
        self._progress_frame.resetProgress()

    def toGuiMessageLog(self, _):
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
            level = logging.WARN
        else:
            level = logging.INFO
        self._main_model.lock.release()

        self.toMessageLog(message, level)

    def toMessageLog(self, output, level=logging.WARN):
        """
        Wrapper Method for _message_log's .log method for logging a message.
        @params - self
                - output: the message to be output
                - level: An integer denoting the level of the message
                  (info is 20, warning 30, error 40)
        @returns - None
        """
        self._message_log.log(level, output)
        if(level == logging.WARN):
            self._progress_frame.addText(f"Warning: {output}")
        else:
            self._progress_frame.addText(output)

    def toErrorLog(self, output, level=logging.ERROR):
        """
        Wrapper Method for _error_log's .error method for logging an error.
        @params - self
                - output: the message to be output
                - level: An integer denoting the level of the message
                  (info is 20, warning 30, error 40)

        @returns - None
        """
        self._error_log.log(level, output)


    def catchException(self, exc_type, exc_value, exc_traceback):
        """
        Method that is called when an exception occurs in the gui thread.
        We write the error to the error log then exit the program with a
        return value of 1, indicating error.
        @params - self
                - exc_type: an exception type
                - exc_value: The value passed with the exception
                - exc_traceback: A traceback object for the exception
        @returns - None
        """
        self.toErrorLog("".join(traceback.format_exception(exc_type,
                                  exc_value, exc_traceback)))
        exc_name = str(exc_type)
        exc_name = exc_name[exc_name.find('\'') + 1:].strip("'>")
        if exc_name.find("Error") == -1:
            exc_name += " error"
        messagebox.showinfo(message=f"An uncaught {exc_name} " \
                                     "occurred in the GUI. Check error.log " \
                                     "for more details.")

        sys.exit(1)



    def catchThreadException(self, args):
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
        self.toErrorLog("".join(traceback.format_exception(exc_type,
                                  exc_value, exc_traceback)))

        exc_name = str(exc_type)
        exc_name = exc_name[exc_name.find('\'') + 1:].strip("'>")
        if exc_name.find("Error") == -1:
            exc_name += " error"

        messagebox.showinfo(message=f"An uncaught error of type: {exc_type}, " \
                                     "occurred in the non-gui thread. Check " \
                                     "error.log for more details.")
        self._progress_frame.addText("An error has occured in the main program"\
                                     ". Check the error log for more details.")

        self._doing_file = False
        self._doing_manual = False
        out_file = self._file_frame.getOutFile()
        if out_file:
            out_file.close()
            self._file_frame.setOutFile(None)

        self.resetProgress()
        self.enableEntry()

class GUIFrame:
    """
    Parent Class for all GUI Frames. Provides disable and
    enable.
    """

    def __init__(self, parent, text = ""):
        """
        Constructor for GUI Frames. Sets the parent attribute and
        Creates the ttk (Label)Frame
        @params - parent: The parent object of the frame. (RootWin)
                - text: The text to display on the border of the frame
        @returns A GUIFrame Object
        """
        self._parent = parent
        self._frame = ttk.Labelframe(self._parent.getWin(),
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

class IntroFrame(GUIFrame):
    """
    Class representing the top-left frame, which currently
    contains some text welcoming the user to the program. Will likely
    eventually include options for the program.
    """

    def __init__(self, parent):
        """
        Constructor for IntroFrames. Takes parent, passes to super's
        constructor, creates the label, and places it in the frame.
        @params - parent
        @returns - An IntroFrame Object
        """
        super().__init__(parent, "Welcome & Options")
        self._label = ttk.Label(self._frame, text="Hello! Welcome to " \
                                "the name pronuncation program!\n")

        self._optionFrame = ttk.Labelframe(self._frame, text="Options for n-Grams:")

        self._bigramCheck = IntVar()
        self._trigramCheck = IntVar()
        self._othergramCheck = IntVar()
        self._othergramValue = IntVar()
        self._bigramCheck.set(1)
        self._trigramCheck.set(1)
        self._othergramValue.set(4)


        self._bigramBox = ttk.Checkbutton(self._optionFrame, text = "Bigrams",
                                          variable = self._bigramCheck)
        self._trigramBox = ttk.Checkbutton(self._optionFrame, text = "Trigrams",
                                           variable = self._trigramCheck)
        self._othergramBox = ttk.Checkbutton(self._optionFrame, text = "Other grams:",
                                             variable = self._othergramCheck,
                                             command = self.toggleEntry)

        self._otherEntry = ttk.Combobox(self._optionFrame, textvariable = self._othergramValue)
        self._otherEntry['values'] = ('4', '5', '6')
        self._otherEntry['state'] = 'disable'
        self._otherLabel = ttk.Label(self._optionFrame, text="Values over 4 may provide inaccurate results")

        self._applyButton = ttk.Button(self._optionFrame, text="Apply", command=self._parent.applyOptions)


        self._label.grid(row = 0, column = 0)
        self._optionFrame.grid(row = 1, column = 0, sticky = "EW")
        self._bigramBox.grid(row = 0, column = 0, sticky = "W", pady = 3, padx = 2)
        self._trigramBox.grid(row = 0, column = 1, sticky = "W", pady = 3, padx = 2)
        self._othergramBox.grid(row = 1, column = 0, sticky="NSW", pady = 3, padx = (2, 0))
        self._otherEntry.grid(row = 1, column = 1, pady = 3, padx = (0, 2))
        self._otherLabel.grid(row = 2, column = 0)
        self._applyButton.grid(row = 2, column = 1)

    def getOptionValues(self):
        """
        Method returns a representation of the options selected by the user.
        The representation is a dictionary of the 'n' of the n-gram
        being the key, and the value being 0 or 1, depending on if it has been
        selected by the user or not.
        @params - self
        @returns - a dictionary of string keys and int values
        """
        result = {2:int(self._bigramCheck.get()),
                  3:int(self._trigramCheck.get()),
                  self._othergramValue.get():int(self._othergramCheck.get())}
        return result

    def disableApply(self):
        """
        Method to disable the Apply button (occurs when in a multi-thread state)
        @params - self
        @returns - None
        """
        self._applyButton.configure(state='disable')

    def enableApply(self):
        """
        Method to enable the Apply button (occurs when in a single-thread state)
        @params - self
        @returns - None
        """
        self._applyButton.configure(state='enable')

    def toggleEntry(self):
        """
        Method disables the entry field when the checkbox is turned off
        and enables it when it is turned on
        @params - self
        @returns - None
        """
        if self._othergramCheck.get() == 0:
            self._otherEntry['state'] = 'disable'
        else:
            self._otherEntry['state'] = 'readonly'




class ManualEntryFrame(GUIFrame):
    """
    Class reperesenting the frame for manual entry of names to the program.
    Contains a constructor and a method that fires when the user presses the
    run button.
    """
    def __init__(self, parent, main_model, test):
        """
        Constructor for the ManualEntryFrame. Calls the parent constructor,
        creates the GUI elements and places them. User_in is a variable
        representing the value of the input field.
        @params - parent - parent object of the frame
                - main_model - the Model object from main. Calls it's
                  processInput method on the input and retrives output from it
        @returns - A ManualEntryFrame object.
        """
        super().__init__(parent, text="Manual Entry")
        self._main_model = main_model
        self._test = test

        self._lbl = ttk.Label(self._frame, text="Please enter a name: ")
        self._enter_button = ttk.Button(self._frame, text="Run",
                                        command=self.inputToMain)

        # Variable for storing the value in the entry field. StringVar is a
        # Tkinter specific class that it uses for this.
        self._user_in = StringVar()
        self._entry_field = ttk.Entry(self._frame, textvariable=self._user_in)


        # Formatting
        self._lbl.grid(row = 0, column = 0, pady=10)
        self._entry_field.grid(row = 0, column = 1, pady=10)
        self._enter_button.grid(row = 1, column = 1)

    def inputToMain(self):
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
            self._parent.setDoingManual(True)
            self._user_in.set("")
            in_data = pd.DataFrame([user_input])
            self._parent.disableEntry()

            # Set up the thread

            # For testing the gui
            if self._test:
                self._parent.setThread(threading.Thread(
                                        target=self._main_model.test_gui,
                                        args=(in_data,), daemon=True))
            # For actually running
            else:
                self._parent.setThread(threading.Thread(
                                        target=self._main_model.processInput,
                                        args=(in_data,), daemon=True))
            # run the thread

            self._parent.toMessageLog("Starting main program execution.",
                                        logging.INFO)
            self._parent.toErrorLog("Starting main program execution.",
                                      logging.INFO)
            self._parent.getThread().start()
        else:
            messagebox.showinfo(message="Please enter something")



    def threadFinished(self):
        """
        Method that is called by the parent's threadFinished method if
        doing_manual is true. Method outputs the main model's result attribute
        in a messagebox.
        @params - self
        @returns - None
        """
        self._main_model.lock.acquire()
        df = self._main_model.result
        self._main_model.lock.release()

        outwin = Toplevel(self._parent.getWin())
        outwin.title("Output")
        def close():
                outwin.grab_release()
                outwin.destroy()

        outwin.protocol("WM_DELETE_WINDOW", close) # intercept close button
        outwin.wait_visibility() # can't grab until window appears, so we wait
        outwin.grab_set()        # ensure all input goes to our window

        col_names = ('Name', 'Combined Score', 'nGrams Letters',
                     'nGrams Phonemes', 'isEnglishNN', 'LanguageFamilyNN')


        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 10))
        tree = ttk.Treeview(outwin, columns=col_names, show='headings',
                            height = 1, selectmode="none")

        for name in col_names:
            tree.column(name, width=175)
            tree.heading(name, text=name)


        output = [df.iloc[0][0], df.iloc[0][1], df.iloc[0][2],
                  df.iloc[0][3], df.iloc[0][4], df.iloc[0][5]]

        # END is from tk: tk.END
        tree.insert('', END, values=output)

        exit_button = ttk.Button(outwin, text="Back", command=close)
        tree.grid(row = 0, column = 0, pady=10, padx = 5)
        exit_button.grid(row = 1, column = 0, pady = (0, 5))
        outwin.wait_window()     # block until window is destroyed



class FileEntryFrame(GUIFrame):
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
                  processInput method on the input
        @returns - A FileEntryFrame object
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
                                         command=self.setInFileName)
        self._outputf_button = ttk.Button(self._frame, text="Browse",
                                          command=self.setOutFileName)

        self._run_button = ttk.Button(self._frame, text="Run",
                                      command=self.inputToMain)

        # Formatting
        self._inputf_lbl.grid(row = 0, column = 0, sticky="NSW", padx = (0, 5))
        self._inputf_field.grid(row = 0, column = 1)
        self._inputf_button.grid(row = 0, column = 2, padx = 10, pady = 10)
        self._outputf_lbl.grid(row = 1, column = 0, sticky="NSW", padx = (0, 5))
        self._outputf_field.grid(row = 1, column = 1)
        self._outputf_button.grid(row = 1, column = 2, padx = 10, pady = 10)
        self._run_button.grid(row = 2, column = 2, padx = 10, pady = 10)


    def getOutFile(self):
        """
        Method is accessor for the _out_file attribute
        @params - self
        @returns - self._out_file: a file object
        """
        return self._out_file

    def setOutFile(self, value):
        """
        Method is a setter for the _out_file attribute
        @params - self
                - value: the new value for _out_file (should be a file or None)
        @returns - None
        """
        self._out_file = value

    def setInFileName(self):
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

    def setOutFileName(self):
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


    def inputToMain(self):
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
        self._parent.setDoingFile(True)
        self._parent.disableEntry()

        # Setting up the thread

        # For testing the gui
        if self._test:
            self._parent.setThread(threading.Thread(
                                    target=self._main_model.test_gui,
                                    args=(in_data,), daemon=True))
        # For actually running
        else:
            self._parent.setThread(threading.Thread(
                                    target=self._main_model.processInput,
                                    args=(in_data,), daemon=True))

        # Run the thread
        self._parent.toMessageLog("Starting main program execution.",
                                    logging.INFO)
        self._parent.toErrorLog("Starting main program execution.",
                                  logging.INFO)
        self._parent.getThread().start()

    def threadFinished(self):
        """
        Method that is called by parent's threadFinished method if
        doing_file is true. Writes the MainModel's result attribute
        (a pd dataframe) to self._out_file, then closes out_file
        @params - self
        @return - None
        """
        self._main_model.lock.acquire()
        columns = ('Name', 'Combined Score', 'nGrams Letters',
                   'nGrams Phonemes', 'isEnglishNN', 'LanguageFamilyNN')

        self._main_model.result.to_csv(self._out_file, index=False,
                                       header=columns,
                                       line_terminator = '\n')
        self._out_file.close()
        self._out_file = None
        self._main_model.lock.release()
        self._parent.resetProgress()
        messagebox.showinfo(message="Done!")


class ProgressFrame(GUIFrame):
    """
    Class representing the bottom-right frame, or the frame containing
    the progress bar and in-gui message log (at some point).
    """
    # To Do: Add text widget for displaying messages/warnings
    def __init__(self, parent):
        """
        Constructor for the ProgressFrame class. Creates the progress bar and
        its varaible that stores the progress value, as well as a label
        that appears when a warning is sent to the message log (latter will
        be replaced at some point)
        """
        super().__init__(parent, "Progress & Messages")

        self._progress_value = IntVar()
        self._progress_bar = ttk.Progressbar(self._frame, length=250, mode=
                                             "determinate", variable=self._progress_value)

        self._textCapacity = 10
        self._text_field = Text(self._frame, height = self._textCapacity, width = 100)
        self._text_field['state'] = 'disabled'
        self._textLines = 1

        self._progress_bar.grid(row = 0, column = 0, sticky="NSEW", padx=5, pady=5)
        self._text_field.grid(row = 1, column = 0, padx = 5, pady = 5)


    def addProgress(self, value):
        """
        Method that adds an amount of progress equal to value param to the
        object's _progress_value attribute, which _progress_bar uses to update.
        @params - self
                - value: The value to add to the progress bar
        @returns - None
        """
        self._progress_value.set(self._progress_value.get() + value)

    def resetProgress(self):
        """
        Method that resets the object's _progress_value attribute to zero,
        which _progress_bar uses to update to an empty state.
        @params - self
        @returns - None
        """
        self._progress_value.set(0)


    def addText(self, message):
        """
        Adds message to the text field. Removes oldest entry to make space
        for the newest if necessary.
        @params - self
                - message: the text to add to the textfield
        @returns - None
        """
        self._text_field['state'] = 'normal'
        # If we have extra space in the text field
        if(self._textLines < self._textCapacity):
            self._text_field.insert(f"{self._textLines}.0", f"{message}\n")
            self._textLines += 1
        elif(self._textLines == self._textCapacity):
            self._text_field.insert(f"{self._textLines}.0", f"{message}")
            self._textLines += 1
        else: # size > capacity
            last = message
            for index in reversed(range(1, self._textCapacity + 1)):
                temp = self._text_field.get(f"{index}.0", f"{index}.end")
                self._text_field.replace(f"{index}.0", f"{index}.end",
                                         f"{last}")
                last = temp

        self._text_field['state'] = 'disabled'
