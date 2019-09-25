# Calculating pi and e in Euler's Identity

#### calculate pi using Monte Carlo sampling
The area of a circle A is:  
<img src="https://latex.codecogs.com/svg.latex?\Large&space;A={\pi}r^2" title="\Large A={\pi}r^2" />  
So we can compute pi by:  
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\pi=4\frac{N_{circle}}{N_{square}}" title="\Large \pi=4\frac{N_{circle}}{N_{square}}" />              
where N is the number of sample points
```
python compute_pi_monte_carlo.py
```
calculate pi using Monte Carlo sampling with turtle graphics
```
python compute_pi_monte_carlo_turtle.py
```
<img src="mc_pi.gif" width="250">

calculate pi using Monte Carlo with numpy for speed-up
```
python compute_pi_monte_carlo_np.py
```
#### calculate pi using math

compute pi using Nilakantha series  
<img src="https://latex.codecogs.com/svg.latex?\Large&space;\pi=3+\frac{4}{2\times3\times4}-\frac{4}{4\times5\times6}+\frac{4}{6\times7\times8}-\frac{4}{8\times9\times10}+\dots" title="\Large \pi=3+\frac{4}{2\times3\times4}-\frac{4}{4\times5\times6}+\frac{4}{6\times7\times8}-\frac{4}{8\times9\times10}+\dots" />  
with the module decimal for high precision float number  
```
python compute_pi_monte_carlo_np.py
```
#### calculate e using math
Euler's number e, the base of natural logs
e is the sum of this infinite series:  
<img src="https://latex.codecogs.com/svg.latex?\Large&space;e=\frac{1}{0!}+\frac{1}{1!}+\frac{1}{2!}+\frac{1}{3!}+\frac{1}{4!}+\dots" title="\Large e=\frac{1}{0!}+\frac{1}{1!}+\frac{1}{2!}+\frac{1}{3!}+\frac{1}{4!}+\dots" />
```
python compute_e.py
```
High precision version using the module decimal for high precision float number 
```
python compute_e_high_precision.py
```
