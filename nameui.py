import sys
import pandas as pd
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class Gui_Win:
    """
    Parent Class for all GUI windows. Provides destory, get_root, show, hide,
    mainloop, and on_closing
    """
    def __init__(self, link_cmd, parent=None):
        """
        Window constructor. Sets up parent variable, link_cmd, the window
        itself, it's frame, and a protocol for 'xing' out of a window,
        which runs the Window's on_closing method.

        @params: link_cmd: The command to fire on the user's input. Intended to
                           link UI to other parts of the program.
                 parent: The parent window of this window.
        @returns: Nothing
        """
        self._parent = parent
        self._link_cmd = link_cmd

        if self._parent:
            # Creating a child window
            self._win = Toplevel(self._parent.get_win())
        else:
            # Root window
            self._win = Tk()
        self._win.title("Name Pronuncation Program")
        self._frame = ttk.Frame(self._win, padding = "5 5 10 10")

        # Binds the event that fires when a window is 'x'ed out to the
        # on closing method
        self._win.protocol("WM_DELETE_WINDOW", self.on_closing)

    def destroy(self):
        """
        Method destroys the object's Tkinter window. Ends any mainloop
        associated with the window.
        @params - self
        @returns - None
        """
        self._win.destroy()

    def get_win(self):
        """
        Method returns the self._win attribute of self.
        @params - self
        @returns - self._win: the Tkinter window of the object.
        """
        return self._win

    def show(self):
        """
        Method is a wrapper for Tkinter's deiconify, which shows the
        window.
        @params - self
        @returns - None
        """
        self._win.deiconify()

    def hide(self):
        """
        Method is a wrapper for Tkinter's withdraw, which hides the
        window.
        @params - self
        @returns - None
        """
        self._win.withdraw()

    def mainloop(self):
        """
        Method is a wrapper for Tkinter's mainloop, which runs the event loop
        associated with the window.
        @params - self
        @returns - None
        """
        self._win.mainloop()

    def on_closing(self):
        """
        Method that is called when the 'WM_DELETE_WINDOW', or 'xing out',
        window event is fired. Default is to destroy the window.
        @params - self
        @returns - None
        """
        self.destroy()

class Root_Win(Gui_Win):
    """
    Class for the Root Window for the GUI.
    This Window contains a 'quit' button, two radio buttons that indicate
    which type of input the user would like to use(manual/file), and an
    'continue' button, which continues according to their choice. It also
    contains a text label for the user. This is a the Root of all other windows,
    and the top eventloop. When other windows are called, this window is hidden.
    """
    def __init__(self, link_cmd):
        """
        Root_Win constructor. Calls Gui_Win's constructor to set up base. Then
        creates the label and the buttons and arranges them properly. Does not
        take a parent object since it is the Root window.

        @params: link_cmd: The command to fire on the user's input. Intended to
                           link UI to other parts of the program.
        @returns: Nothing
        """
        # Call to parent class
        super().__init__(link_cmd)
        self._intro_lbl = ttk.Label(self._frame, text ="Hello! Welcome to " \
                                    "the name pronuncation program!\nPlease " \
                                    "select how you would like to enter names:",
                                    font= ("Arial", 16))
        # buttons
        self._quit_button = ttk.Button(self._frame, text="Quit",
                                       command=self.exit_program)
        self._continue_button = ttk.Button(self._frame, text="Continue",
                                           command=self.next_win)

        # Variable to hold the value for the Radiobuttons
        self._entry_choice = IntVar()
        self._manual_button = ttk.Radiobutton(self._frame, text="Manual Entry",
                                              variable=self._entry_choice,
                                              value=0)
        self._file_button = ttk.Radiobutton(self._frame, text="File Entry",
                                            variable=self._entry_choice,
                                            value=1)


        # Formatting
        self._frame.grid(row=0, column=0)
        self._intro_lbl.grid(row = 0, column = 0, columnspan = 4)
        self._quit_button.grid(row = 1, column = 0)
        self._continue_button.grid(row=1, column=3)
        self._manual_button.grid(row=1, column=1)
        self._file_button.grid(row=1, column=2)

    def next_win(self):
        """
        Method that is called when the continue button is pressed.
        Checks which entry type was choosen, then executes that type accordingly
        @params - self
        @returns - None?
        """
        # Manual Entry
        if self._entry_choice.get() == 0:
            # Create a window for manual entry
            next_window = Manual_Entry_Win(self, self._link_cmd)
            # Hide root window, then call child's mainloop
            self.hide()
            next_window.mainloop()
        # File Entry - Not yet implemented - idea is Filedialog for input file,
        # file dialog for output file. Call to link_func with input
        # Message box/Progress Bar? when complete
        else:
            pass

    def exit_program(self):
        """
        Method kills the program by destroying the root, and for overkill (for
        some reason, without quit you needed to press the button twice)
        calls the quit function to kill the program.
        @params - self
        @returns - None
        """
        self._win.destroy()
        self._win.quit()

    def on_closing(self):
        """
        Method overrides Gui_Win's on_closing, which fires when xed out.
        Calls exit_program method (kills program).
        @params - self
        @returns - None
        """
        self.exit_program()

class Manual_Entry_Win(Gui_Win):
    """
    Class for the window for manually entering names. Child class of Gui_Win.
    Window contains an entry field with a label, and two buttons:
    back, and enter. Back returns user to the root win, and enter calls the
    link_cmd on the input (sends input to processing).
    """
    def __init__(self, parent, link_cmd):
        """
        Constructor for Manual Entry Windows. Calls parent's constructor,
        then sets up the label, entry field, and the enter and back buttons.
        @params - parent: parent window of self
                - link_cmd: the function to call on the input
        @returns - None
        """
        super().__init__(link_cmd, parent)

        # lbl and buttons
        self._lbl = ttk.Label(self._frame, text="Please enter a name: ")
        self._enter_button = ttk.Button(self._frame, text="Enter",
                                        command=self.link)
        self._back_button = ttk.Button(self._frame, text="Back",
                                        command=self.return_top_lvl)

        # Variable for storing the value in the entry field. StringVar is a
        # Tkinter specific class that it uses for this.
        self._user_in = StringVar()
        self._entry_field = ttk.Entry(self._frame, textvariable=self._user_in)

        # Formatting
        self._frame.grid(row=0, column=0)
        self._lbl.grid(row=0, column=0)
        self._entry_field.grid(row=0, column=1)
        self._back_button.grid(row=1, column=0)
        self._enter_button.grid(row=1, column=1)


    def link(self):
        """
        Method is called when the enter button is pressed. If the value in the
        entry field is not blank, converts the value to a regular python string,
        empties the entry field, and places the input into a panda's dataframe.
        This is for standardization with the file entry input method.
        It then calls the provided link_cmd on the dataframe, which then returns
        a result, which is then printed along with user_input, into a messagebox
        Eventually, the message box will be replace to provide more detailed
        output.

        @params - self
        @returns - None?
        """
        user_input = str(self._user_in.get())
        if user_input != "":
            self._user_in.set("")
            in_data = pd.DataFrame([user_input])
            result = self._link_cmd(in_data)
            messagebox.showinfo(message=user_input + ": " + str(result))
        else:
            messagebox.showinfo(message="Please enter something.")

    def return_top_lvl(self):
        """
        Method is called by both on_closing and the 'back' button. Destroys
        self (and closes it's mainloop), then shows the root_win
        @param - self
        @returns - nothing
        """
        self.destroy()
        self._parent.show()

    def on_closing(self):
        """
        Method called when 'xed' out of the window. Calls return_top_lvl
        @param - self
        @returns - nothing
        """
        self.return_top_lvl()

# Non GUI Stuff-----------------------------------------------------------------
def take_input(func):
    """
    take_input checks if there was a filename provided on the command line.
    If so, it calls read_file with the provided cmd line argument.
    Otherwise, it begins manual entry of words/names.
    Each time a word is entered, it is passed to the provided func
    This continues until the user enters nothing.

    Params: func (function) -- function that the input is passed to
    Returns: Nothing
    """
    # Manual Input
    if len(sys.argv) < 2:
        while True:
            user_in = input("Please enter a word/name "\
                            "(Enter nothing to exit): ")
            if user_in == "":
                print("Goodbye!")
                break
            else:
                func(user_in)
    # File input
    else:
        read_file(sys.argv[1], func)

def read_file(filename, func):
    """
    Function reads filename as a csv into a pandas dataframe, then calls the
    provided func function with the dataframe as a parameter

    Params: filename (str) -- filename/path to read in as csv
            func (function) -- function that is called on the dataframe produced
    Returns: Nothing

    """
    # encoding ="UTF-8" needed for IPA chars
    in_file = open(filename, encoding="UTF-8")
    dataframe = pd.read_csv(in_file, sep=",", names=["Word", "IPA"])
    func(dataframe)

def write_dataframe(filename, dataframe):
    """
    Function is a simple wrapper for pandas' DataFrame.to_csv function.
    Will probably be useful enventually when more advanced ui is made

    Params: filename (str) -- filename/path to write dataframe into
            dataframe (pd.DataFrame) -- data to write to file
    Returns: Nothing
    """
    dataframe.to_csv(filename, header=["Word","Pronuncation Rating"])

#------------------------------------------------------------------------------


def main():
    """
    Main just sets up the root window and calls it's mainloop
    """
    root = Root_Win(lambda x: x[0][0])
    root.mainloop()


if __name__ == "__main__":
    main()
