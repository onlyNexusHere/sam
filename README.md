# sam
This is the program that will from the sam robot. 
It is modular for the components on the robot.

If you would like to add a module: 

- make a class in the modules folder and extend the class SamModule.

- Make sure you add the module to the mods list within SamControl.init_mods(), and import your module (in the 5th line of SamControls)
If this mod is an arduino mod, you don't have to do anything further within SamControl. 

- Construct your file using the functions defined in SamModule. 
Many of these files will be called automatically. More documentation is in SamModule.

- If you have any questions, please ask! I can also fix code as needed.


SamModule API:

    self.arduino: Serial
        links to the serial object for the arduino. May be None if there is no arduino connected. Pl
     
    self.sam: Sam
        This is the link to the sam object.
        
    self.sam.debug: Boolean
        If you want to print something only in debugging mode, then chcek this boolean.
        
    self.name: String
        This is the name of the module for debugging purposes.
        
    self.identifier: String
        This is the string that indicates that this module should be run. Can only be one word.
        
    self.is_local_to_pi
        If the socket goes to something on the pi, then it is true. If the module is for a device on the arduino, then it is false.
        
    self.log_file
        The log file!
        
    self.__init__(kargs)
        Initialize the object!
        
    self.message_received(self, message)
        This function is message_received when the arduino sends a message from the module to the pi.
        Message does not include the identifier sent by the arduino
        
    self.stdin_request(self, message):
        This function is message_received when the terminal is used to request a specific module to do something.
        This string removes the 'request mod_name' from the front.
        
    self.on_wait(self):
        This runs at least every .5 seconds at least.
        This method can be used to request an update regularily.
        
    self.write_to_stdout(self, string_to_write):
        Use this method to print to the terminal running the program on the pi.
        Use this in place of print().
        
    self.log_to_file(self, string_to_log):
        Use this to write to the logging file.
       
    self.send(self, msg):
        Use this function to send a message to the arduino.
        Adds the identifier
