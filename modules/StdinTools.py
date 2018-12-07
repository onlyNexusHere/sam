from .SamModule import SamModule
import time
import sys
import traceback
import serial.tools.list_ports
import curses


class StdinTools(SamModule):
    """
    Module for stdin functions. Not overly nessecary, but use this as a reference.
    """

    stdin_cmds = {}

    r1 = False
    r1_started = False
    r1_past_1 = False
    r1_starty = 0.0

    r2 = False
    r2_past_1 = False
    r2_starty = 0.0

    # Variables for curses
    cur_key = ""
    quit = False
    stdscr = None

    ml = 0
    mr = 0
    # Art by Max Strandberg
    car = r"""
    ____
 __/  |_\_
|  _     _``-.
'-(_)---(_)--'"""
    car_location = 0

    def __init__(self, kargs):
        super().__init__(module_name="StdinTools", is_local=True, identi=">", **kargs)

        self.sam.listening_to[sys.stdin] = self._process_stdin

        self.stdin_cmds = {"modules": (lambda str_args: self.show_mods(),
                                       "View the modules"),

                           "set": (lambda str_args: self.set_var(str_args),
                                   "Use command to set certain SAM variables, such as 'set arduino /dev/usb000'"),

                           "request": (lambda str_args: self.request_module(str_args),
                                       "Use this command to talk to the modules. 'request <mod_name> txt'"),

                           "help": (lambda str_args: self.show_help(),
                                    "Use this command to see the help text"),

                           "h": (lambda str_args: self.show_help(),
                                 "Same as 'help'"),

                           "status": (lambda str_args: self.show_status(),
                                      "Get the status of the Arduino"),

                           "send": (lambda str_args: self.send_message(str_args),
                                    "Send a string to the arduino"),

                           "findarduino": (lambda str_args: self.find_arduino(),
                                           "Re-find the arduino"),

                           "curses": (lambda str_args: self.run_curses(),
                                           "Interactive robot control"),

                           "debug": (lambda str_args: self.toggle_debug(str_args),
                                     "Change debugging to true or false"),

                           "wait": (lambda str_args: self.wait(str_args),
                                    "Change debugging to true or false"),

                           "run": (lambda str_args: self.run_file(str_args),
                                    "Run lines in a file"),

                           "echo": (lambda str_args: self.echo(str_args),
                                    "Echo a string"),

                           "quit": (lambda str_args: self.sam.request_quit(),
                                    "Quit the program"),

                           "exit": (lambda str_args: self.sam.request_quit(),
                                    "Same as quit")
                           }

    def _process_stdin(self, response):
        str_rsv = sys.stdin.readline()

        self.debug_run(print, "got message: " + str_rsv)

        try:
            self.message_received(str_rsv)
        except Exception as e:
            print("Exception found in stdin module for message received --> "+str(e.__doc__)+"\n" + str(e))

    def message_received(self, message):
        if message.strip() == "":
            return

        message_arg = message.strip().split(" ")

        self.debug_run(print, "Function requested: " + message_arg[0])

        func_to_run, _ = self.stdin_cmds.get(message_arg[0], (None, None))

        if func_to_run is None:
            self.write_to_stdout("Cannot find command " + message_arg[0] + ". Use help to get help.")
        else:
            func_to_run(message_arg[1:])

    def find_arduino(self):
        self.sam.find_arduino()

    def toggle_debug(self, str_args):
        self.debug_run(print, "Toggling debugging, msg is " + str_args[0])
        if str_args[0].strip() == "true":
            self.sam.debug = True
        elif str_args[0].strip() == "false":
            self.sam.debug = False
        else:
            self.write_to_stdout("Cannot change debugging to " + str(str_args[0]))

    def show_mods(self):
        self.write_to_stdout(str([n for n in {**self.sam.arduino_modules, **self.sam.local_modules}.keys()]))

    def set_var(self, str_args):
        if len(str_args) == 2:
            if str_args[0].lower() == 'arduino':
                try:
                    serial.Serial(str_args[1], timeout=1, baudrate=115200)
                except Exception as e:
                    self.debug_run(self.write_to_stdout, "Could not connect to arduino: " + e.__doc__ + "\n" + str(e))
            else:
                self.write_to_stdout("Only setting arduino path is available")
        else:
            self.write_to_stdout("Need two arguments.")

        # TODO sam listening list is affected, fix is...

    def show_help(self):

        print("\n".join([cmd + " --> \n\t" + comment for cmd, (_, comment) in self.stdin_cmds.items()]))

    def show_status(self):
        to_print = "\n"

        if self.arduino is not None:
            to_print = to_print + "\tArduino is: " + self.sam.arduino.port + "\n"
        else:
            to_print = to_print + "\tArduino is not detected." + "\n"

        to_print = to_print + "\tDebugging is " + str(self.sam.debug) + "\n"

        to_print = to_print + "\tBroken modules: " + str(self.sam.broken_module_on_wait)

        self.write_to_stdout(to_print)

    def send_message(self, str_args):
        self.sam.send(" ".join(str_args))

    def request_module(self, str_args):

        get_mod = {**self.sam.arduino_modules, **self.sam.local_modules}.get(str_args[0])
        if get_mod is None:
            self.write_to_stdout("Cannot retrieve module named " + str_args[0])

        else:
            try:
                get_mod.stdin_request(" ".join(str_args[1:]))
            except Exception as e:
                self.write_to_stdout("Cannot run request for module " + get_mod.name + "\n" + str(e))
                traceback.print_tb(e.__traceback__)

    def wait(self, str_args):
        if len(str_args) > 0 and str_args[0].isdigit():
            time.sleep(int(str_args[0]))

    def echo(self, str_args):
        self.write_to_stdout(" ".join(str_args))

    def run_file(self, str_args):
        if str_args is None or len(str_args) < 1 or str_args[0].strip() == "":
            self.write_to_stdout("Cannot open file")
            return

        to_run = open(str_args[0], 'r', encoding='utf-8')

        line_to_read = to_run.readline()
        while line_to_read is not "":

            if line_to_read.strip() != "":
                # Ignore empty lines
                self.message_received(line_to_read.strip())
                # Keeps file reading from being non-blocking
                self.sam.process_sockets()

            line_to_read = to_run.readline()

    def follow(self, routine):
        if routine == 'r1':
            self.r1 = not self.r1
            if self.r1:
                self.sam['camera'].stdin_request('start')
                self.write_to_stdout("Starting r1")
            else:
                self.sam['camera'].stdin_request('stop')
                self.sam['motor'].stdin_request('stop')
        elif routine == 'r2':
            self.r2 = not self.r2
            if self.r2:
                self.sam['camera'].stdin_request('start')
                self.write_to_stdout("starting r2")
            else:
                self.sam['camera'].stdin_request('stop')
                self.sam['motor'].stdin_request('stop')

    def on_wait(self):
        pass

    def _init_curses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        self.stdscr.keypad(True)
        curses.curs_set(False)
        self.stdscr.nodelay(True)

    def _end_curses(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        self.quit = True

    def draw(self, stdscr):
        # Clear screen

        self.cur_key = self.stdscr.getch()

        curses.flushinp()

        self.stdscr.clear()

        title = "INTERACTIVE MODE"
        subtitle = "Press 'q' to quit."
        subtitle_1 = "Press arrow keys and space bar to control robot."
        speed_l = "Left wheel: " + str(self.ml)
        speed_r = "Right wheel: " + str(self.mr)

        self.stdscr.addstr(0, int((curses.COLS-1)/2)-int(len(title)/2), title, curses.A_STANDOUT)
        self.stdscr.addstr(2, int((curses.COLS-1)/2)-int(len(subtitle)/2), subtitle)
        self.stdscr.addstr(4, int((curses.COLS-1)/2)-int(len(subtitle_1)/2), subtitle_1)

        self.stdscr.addstr(6, 0, str(curses.LINES - 1) + ", " + str(curses.COLS - 1))

        self.stdscr.addstr(10, 0, str(self.cur_key))

        self.stdscr.addstr(11, 0, speed_l)
        self.stdscr.addstr(12, 0, speed_r)

        for y, line in enumerate(self.car.splitlines(), curses.LINES-5):
            # self.stdscr.addstr(20,0, self.car)
            self.stdscr.addstr(y, int(self.car_location)%(curses.COLS - 15), line)

        self.car_location += (self.ml + self.mr)/100

        if self.cur_key == ord('q'):
            self._end_curses()
            print("end")
        elif self.cur_key == curses.KEY_LEFT:
            self.ml += 20
        elif self.cur_key == curses.KEY_RIGHT:
            self.mr += 20
        elif self.cur_key == curses.KEY_UP:
            self.ml += 20
            self.mr += 20
        elif self.cur_key == curses.KEY_DOWN:
            self.ml -= 20
            self.mr -= 20
        elif self.cur_key == ord(' '):
            if self.ml == 0 and self.mr == 0:
                self.ml = 60
                self.mr = 60
            else:
                self.ml = 0
                self.mr = 0

        # Adjust the actual speed of the robot
        a_l, a_r = self.sam['motor'].current_speed
        if a_l != self.ml or a_r != self.mr:
            self.sam['motor'].send(str(self.ml) + " " + str(self.mr))

        time.sleep(0.1)

    def run_curses(self):
        self._init_curses()
        while not self.quit:
            curses.wrapper(self.draw)


