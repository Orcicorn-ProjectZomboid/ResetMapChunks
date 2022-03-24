# =============================================================================
#   This class is designed to be used as an import for additional projects.
#    It allows for simple console and log outputs without having to define
#    or code a lot of properties.  Simply instantiate the object and then
#    you are free to log.add("My Message") as many entries as you need
# =============================================================================
#   PRE-REQUISITES
#       1:  Python3                         apt install python3
# =============================================================================

from datetime import datetime                       # Get current time & date


class NewLog:

    # -------------------------------------------------------------------------
    # CONSTRUCTOR -------------------------------------------------------------
    # -------------------------------------------------------------------------

    def __init__(self, console_width=65, save_log=False,
                 save_path="log.log"):
        """
        Initialization for the Log Class that can take some optional
         arguments for configuration purposes.

        Args:
            console_width (int): Max width for console output.
             Defaults to 65.
            save_log (bool): Save output to a file?.
             Defaults to False.
            save_path (str, optional): Path and filename to save the
             logfile to. Defaults to "log.log".
        """
        # Save Settings
        self.console_width = console_width
        self.save_log = save_log
        self.save_path = save_path
        self.tree_view = False
        self.tree_view_indent = ">"
        self.custom_time = False
        self.custom_time_string = "%H:M%M:S"
        # If Saving, Start a new logfile
        if self.save_log is True:
            try:
                with open(self.save_path, 'w') as log_file:
                    log_file.close()
            except Exception:
                print('ERROR OPENING LOGFILE')

    # -------------------------------------------------------------------------
    # PRIVATE METHODS ---------------------------------------------------------
    # -------------------------------------------------------------------------

    def __print_to_log(self, message):
        """
        A Private function that handles the actual output of log
         messages to both the console and the optiona log file.

        Args:
            Message (str): The message to output to the console & log
        """
        if self.save_log is True:
            with open(self.save_path, 'a') as log_file:
                log_file.write(f"{message}\n")
                log_file.close()
        if self.tree_view is True:
            message_reversed = message[::-1]
            message_reversed = message_reversed.replace(
                                    self.tree_view_indent,
                                    '^\u2574\u2514', 1)
            message = message_reversed[::-1]
            message = message.replace(self.tree_view_indent, '    ')
            message = message.replace('^', self.tree_view_indent)
        print(message)

    # -------------------------------------------------------------------------
    # PUBLIC METHODS ----------------------------------------------------------
    # -------------------------------------------------------------------------

    def add(self, message, header=False):
        """
        Adds a message to the console and log file.

        Args:
            message (str): The message to add to the console & log
            header (bool, optional): If True, append -'s to the end of
             the message to form a line break. Defaults to False.
        """
        if self.custom_time is False:
            time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        else:
            time = datetime.now().strftime(self.custom_time_string)
        if header is True:
            line_width = self.console_width - (1+len(time)+2+len(message)+1)
            line = f" {'-' * line_width}"
        else:
            line = ''
        self.__print_to_log(f"[{time}] {message}{line}")

    def add_header(self, message):
        """
        Adds a console & logfile header message.
        Shorthand for add(Message,True)

        Args:
            message (str): The message to write as a header
        """
        self.add(message, True)

    def use_custom_strftime(self, strftime="%H:%M:%S"):
        """
        Allows the setting of a custom strftime string for log output

        Args:
            strftime (str): An strftime string. Defaults "%H:%M:%S".
        """
        self.custom_time = True
        self.custom_time_string = strftime

    def disable_treeview(self):
        """Disables the tree_view ascii conversion"""
        self.tree_view = False

    def enable_treeview(self, indentation=">"):
        """
        Enables the conversion of indentation to ASCII tree view chars

        Args:
            indentation (str): What character should be changed into a
             tree view indendtation? Defaults to ">".
        """
        self.tree_view = True
        self.tree_view_indent = indentation

    def linebreak(self):
        """Draws a console width linebreak using equal signs.
        """
        self.__print_to_log("=" * self.console_width)

    def timestamp(self, ISO8601=True):
        """
        Outputs a line enclosed timestamp that is most commonly used at
         the start of a log file as well as at the absolute end.

        Args:
            ISO8601 (bool, optional): Use ISO8601 format, otherwise use
             locale. Defaults to True.
        """
        self.linebreak()
        if ISO8601 is True:
            self.__print_to_log(f"{datetime.now().astimezone().isoformat()}")
        else:
            self.__print_to_log(f"{datetime.now().strftime('%c')}")
        self.linebreak()
