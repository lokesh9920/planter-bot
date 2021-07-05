# planter-bot
This is a planter bot developed for IIT Bombay competition

## Storing the final files in git for reference

## Planter bot is a robot developed from scratch on Raspberry pi. The coding part is done in python programming language, and the final task is achieved by using image processing extensively. 

# Task in detail: 
* The project aims at simulating automating farming. 
* The robot should use a camera module and traverse a black line.
* Some color markers (different colors) are placed alongside the path.
* The robot, while traversing, should detect the shape and color of the color marker. 
* Upon detecting the shape, color of the marker, the robot should select appropriate seedling image as mapped in ["Input Table.csv"](https://github.com/lokesh9920/planter-bot/blob/master/Input%20Table.csv) file. 
* The robot after selecting the seedling , that image should be blended on appropriate field on ["plantation.png"](https://github.com/lokesh9920/planter-bot/blob/master/Plantation.png)image.
* All the above tasks should be achieved in best possible time. 
* The final image looks like ["p_final.png"](https://github.com/lokesh9920/planter-bot/blob/master/p_final.png). 
* The program can be run from [task4-main.py](https://github.com/lokesh9920/planter-bot/blob/master/task4-main.py) file (runnable only on Raspbery pi due to harware I/O dependency)
* The raspberry pi has camera module, motors attached to it to facilitate it's movement.
