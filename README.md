# sam
This is the program that will from the sam robot. 
It is modular for the components on the robot.

If you would like to add a module: 

- make a class in the modules folder and extend the class SamModule.

- Make sure you add the module to the mods list within SamControl.init_mods().
If this mod is an arduino mod, you don't have to do anything further within SamControl. 

- If it is the camera, there needs to be a new listening port and code added in the main function, as I notated already, to make sure 
SamControl reads the information properly.

- Construct your file using the functions defined in SamModule. 
Many of these files will be called automatically. More documentation is in SamModule.

- If you have any questions, please ask! I can also fix code as needed.