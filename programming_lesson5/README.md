# Modeling and 3D printing coin sorter with gravity well funnel 
This toy is to sort coins and show the gravity well.  

#### Modeling and 3D printed coin sorter  
First, we make a 3D model of coin sorter by running  
```
python make_coin_sorter_version5.py
```
<img src="coin_sort_3d_model.001.jpeg" width="250">  
The 3D printed coin sorter is as below  
<img src="coin_sorter_2.gif" width="250">  

#### Modeling and 3D printed gravity well funnel  
First, we make a 3D model of gravity well funnel and coin launcher by running  
```
make_funnel.py  
make_funnel_stand.py  
make_funnel_launcher.py  
```
<img src="coin_sort_3d_model.002.jpeg" width="250">  
The 3D printed coin sorter is as below  
<img src="coin_sorter_3.gif" width="250">  

#### sorting coins  
<img src="coin_sorter_7.gif" width="250">  
The sorter can quickly separate different coins according to their size.  
<img src="coin_sorter_8.gif" width="250">  
The coins are collected by the cylinder collectors.

#### Motion in gravity well  
<img src="coin_sorter_4.gif" width="250">  
Coins can stay in different orbits based on their speed and launching angle.  
<img src="coin_sorter_5.gif" width="250">  
If the launching angle is too wide, the coin will fly away from the funnel.  
<img src="coin_sorter_6.gif" width="250">  
If the launching angle is good, the coin will stay at smaller orbit with the speed decreasing and eventually drop to the hole at bottom. 
