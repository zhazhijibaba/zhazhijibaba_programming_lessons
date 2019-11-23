# Modeling and 3D printing rubber gun toy 
  
Here, we tried to design and produce a rubber gun toy.  
<img src="rubber_gun_3.gif" width="250">  
If you pull the trigger, the toy gun would shoot a rubber band.  


#### Design of rubber gun toy  
<img src="rubber_gun_model_new_v4.gif" width="250">   
There are 4 parts for a rubber gun toy:  
(1) The bottom part in green, the main body of the toy gun.  
(2) The top part in blue, the cover of the toy gun.  
(3) The triger part 1 in yellow for horizontal motion.  
(4) The triger part 2 in red to convert horizontal motion of part 1 to vertical motion.  
 

#### Modeling and 3D printed toy  
To make the input model file of bottom part for 3D printing, run the code below:  
```
python make_rubber_gun_bottom.py
```
To make the input model file of top part for 3D printing, run the code below:  
```
python make_rubber_gun_top.py
```
To make the input model file of trigger part for 3D printing, run the code below:  
```
python make_rubber_gun_trigger_part1.py
python make_rubber_gun_trigger_part2.py
```
The resuling 3D prints is showed below:  
<img src="rubber_gun_3d_image.005.jpeg" width="250">  
