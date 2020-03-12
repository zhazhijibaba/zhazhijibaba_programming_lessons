# Data analysis for COVID-19 outbreak 
The data of COVID-19 confirmed cases are fitted to SIR model. The SIR model is also validated with 2003 SARS data.
Trend of COVID-19 outbreak is predicted by SIR model.

#### The data of total confirmed cased, China VS oversea 
First, we compared the total confirmed cases for China v.s. oversea. 
The code to fit the data to SIR model and to draw the plots:  
```
python analysis_covid_2019.py
```
<img src="wuhan_china_vs_oversea_raw_data1.jpeg" width="250">  
The red points represents the total confirmed cases in China.  
The blue points represents the total confirmed cases outside China.  

#### SIR model prediction of final confirmed cases 
Then the data are feeded to SIR model, the prediction was made.  
<img src="wuhan_china_vs_oversea_SIR_fitting_data1.jpeg" width="250">  
The red points represents the total confirmed cases in China.  
The blue points represents the total confirmed cases outside China.  
The red dashed line is the prediction for China based on SIR model.  
The blue dashed line is the prediction for Oversea based on SIR model.  
The final confirmed cased oversea will reach to 400K in 120 days from the outbreak.  

#### SIR Model validattion on 2003 SARS data 
The code to fit the data to SIR model and to draw the plots:  
```
python analysis_sars_2003_fit_SIR.py
```
<img src="SARS_SIR_fitting_data1.jpeg" width="250">  
The green points represents the total confirmed cases of 2003 SARS all over the world.  
The red dashed line is the prediction based on SIR model.  
We can see the model matched the data very well.

#### The ways to fight COVID-19 based on SIR Model 
The explanation of SIR model
<img src="SIR_model.jpeg" width="250">  
The yellow cup represents the susceptible people.  
The red cup represents the infected people.  
The green cup represents the recovered people.  
According to the model, the three major ways to fight the virus are: quarantine, vaccine, and specific medicine.  
Since we don't have caccine and specific medicine, the only thing we can do is quarantine.  
Obviously, China did a great job for quaratine than other countries.


The green cup represents the recovered people.  
