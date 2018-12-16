# sam
This is the program that will from the sam robot. 
It is modular for the components on the robot.


The code will compile on a Mac machine as well as a Raspberry Pi B. For full functionality, it must be run on a Pi, connected to an Arduino Uno and a camera. On the arduino, we have a ping sensor, two motors for wheels, quadratures, and a motor shield.

The code for the arduion is located within SamControl_Arduino/SamControl_Arduino.ino.


- To run the main program:

python SamControl.py

Flags are also supported, such as --arduino "arduino location", --help, --debug, and --logging-file "File Location". 

Once the program is started, use the command line interface for basic commands. Type "help" to see the options.

Each module also has it's own commands, but you will have to look through the code to figure out what they are. To send a command to a module type: "request module_id command" where module id is the identi variable assigned to that module. For example, "request motor straight" will make the robot motors start moving forward. "request ir" should give you the current x, y, and heading of the robot (if there is an arduino to give back information). "request map status" will give you information on the programmed route: if you have a current location set on the map createed within sam control, and if you set a path, and if the robot is currently trying to navigate the path.


- To run the camera file:

python test_vision_socket.py

This file can only be run on a Pi, and it will gather information about a road and send the information to socket 5005, which will be picked up by the pi. We ran this program in the background.



DEVELOPMENT:

If you would like to add a module: 

- make a class in the modules folder and extend the class SamModule.

- Make sure you add the module to the mods list within SamControl.init_mods(), and import your module (in the 5th line of SamControls)
If this mod is an arduino mod, you don't have to do anything further within SamControl. 

- Construct your file using the functions defined in SamModule. 
Many of these files will be called automatically. More documentation is in SamModule.

- If you have any questions, please ask! I can also fix code as needed.


SamModule API:

You can define these functions in the module:   
        
    self.__init__(kargs)
        Initialize the object! See other modules for how to use this.
        
    self.message_received(self, message)
        This function is message_received when the arduino sends a message from the module to the pi.
        Message does not include the identifier sent by the arduino
        
    self.stdin_request(self, message):
        This function is message_received when the terminal is used to request a specific module to do something.
        This string removes the 'request mod_name' from the front.
        
    self.on_wait(self):
        This function is called very .2 seconds or faster.
        This method can be used to request an update regularily.
        
You can use these functions and variables:

    self.arduino: Serial
        links to the serial object for the arduino. May be None if there is no arduino connected. Pl
     
    self.sam: Sam
        This is the link to the sam object.
    
    self.sam[NAME_OF_ID]
        Name of ID is a string.
        Get the module that matches the id with NAME_OF_ID. Returns the module or None.
    
    self.sam.debug: Boolean
        If you want to print something only in debugging mode, then chcek this boolean.
    
    self.sam.request_quit()
        use this to request that the full program quit.
        
    self.name: String
        This is the name of the module for debugging purposes.
        
    self.identifier: String
        This is the string that indicates that this module should be run. Can only be one word.
        
    self.is_local_to_pi
        If the socket goes to something on the pi, then it is true. If the module is for a device on the arduino, then it is false.
        
    self.log_file
        The log file! May be None.
        
    self.debug_run(func, func_args):
        Use this method to run somthing only in debugging mode. One example:
        "self.debug_run(self.write_to_stdout, "Failed!!")
        
    self.write_to_stdout(self, string_to_write):
        Use this method to print to the terminal running the program on the pi.
        Use this in place of print().
        
    self.log_to_file(self, string_to_log):
        Use this to write to the logging file.
       
    self.send(self, msg):
        Use this function to send a message to the arduino.
        Adds the identifier   
        
        

   
