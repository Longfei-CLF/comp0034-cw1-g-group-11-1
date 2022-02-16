[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-f059dc9a6f8d3a56e377f745f24479a46679e63a5d9fe6f495e02850cd0d8118.svg)](https://classroom.github.com/online_ide?assignment_repo_id=6689081&assignment_repo_type=AssignmentRepo)
# COMP0034 Coursework 1

# Introduction

Volcano eruption is a natural disaster that hard to predict. Without any forecast or contingency plan, volcano eruption might cause tremendous losses to society and humans. However, scientist can make a probability estimation with sufficient long-period eruption data set. (Turner et al., 2007) Thus, in the project, some dimensions such as the number of eruptions, the duration of the eruption and the volcano eruption index (VEI) are presented by visualizing the eruption data. ***This visualization design could help scientist to predict the possibility of volcano eruptions by using two sets of plot***. The first section is a general overview of the volcanoes around the world. The second section is about more specific plot that used to predict the eruption.


# Overview of the volcanos around the world

In Fig.1, all volcanoes were highlighted on a world map. Since this is only a general graph, our **target audience** includes a wide range of people such as geologists, volcano enthusiasts, and local government. Moreover, this graphic design was intended to answers general information about volcanoes such as the total number of eruptions, average eruption duration, and VEI (how large the eruption is). They could play around with this graph to see the distribution of volcanoes. Also, the audience could use select boxes to filter the countries and volcanoes they want to look into. In order to position the volcano, we need longitude and latitude from the dataset and the corresponding volcano name on that coordinate. 

This design can be understood by the majority of people without expert knowledge which is appropriate for a wide range of audiences. Using the small blue spot to represent the volcano makes the audience easy to see and select them by moving the cursor.

<div align=center><img width="75%" height="75%" src="https://github.com/ucl-comp0035/comp0034-cw1-g-group-11-1/blob/master/Fig/Fig1.png"/></div>
<div align=center> [Fig.1]: Distribution of volcanos all over the world </div> <br />

Combine with the world map graph, more information was provided as shown in Fig.2. Thus, this graph was designed to answer more professional questions. When the audience selects a volcano, the plot on the right side shows the number of eruptions in a period of time. Moreover, they can adjust the time period by sliding the bottom icon. The number of eruptions versus eruptions years could be used to predict the activity of the volcano (Venzke, 2013). This is essential when scientists want to predict the eruption of a specific volcano. Using the line plot expresses the difference between each eruption better. The audience is able to compare the peak value easily from the plot. What is more, the sliding icon has simplified the operations for the audience. They don’t need to put specific starting years or times. Instead, sliding makes the section of the time period much easier. <br />
 



<div align=center><img width="75%" height="75%" src="https://github.com/ucl-comp0035/comp0034-cw1-g-group-11-1/blob/master/Fig/Fig2.png"/></div>
<div align=center>[Fig.2]: Number of Eruptions over the year </div>


  
# Eruption prediciton 

The second set of plots were designed for eruption predictions. Our **target audience** is volcanologist and geologists who intended to predict the volcano or continental plate activities. To plot this graph, VEI, position of the volcano, and Eruption years were needed. In Fig.3, this plot was design to indicate the VEI in a specific year.  In geography, a large amount of severe volcano eruptions can be caused by unusually plate movement, in which will cause earthquake, flooding to the edge of the continental plate. Fig.3 could provide a clear view of all the VEI in a specific year. Geologist could use these informations to predict the further movement of the plate. More importantly, this forecast could reduce the losses to societies and human. In addition, VEI was represented by a gradient ramp spot, the warmer the color, means the eruption is severe to the neighboring areas. This color design helped scientist to identify the VEI in a more obvious way compare with numbers. From this graph, volcanologist can easily see the trend of VEI of a region which they could build model based on this graph. Furthermore, using the world map to position the eruptions could help scientist to see the density of eruptions. This design helped scents to identify the region that they should pay more attention to. 


<div align=center><img width="75%" height="75%" src="https://github.com/ucl-comp0035/comp0034-cw1-g-group-11-1/blob/master/Fig/Fig.3.png"/> </div>
<div align=center>[Fig.3]: Volcano Eruption Index in a specific year </div> <br />

In Fig.4, other information on volcanoes has been designed for predicting the eruption. The data needed is eruption durations and a sum of eruptions at each year. In order to obtain the sum of eruptions, we have written a program to sum the eruptions number per year from our dataset. Our target audiences are volcanologists or geologists who were investigating the frequency of the volcano eruption and eruption prediction. In volcanology, the number of eruptions and durations is a key factor that is used to predict volcano activities. If there is a sudden change of eruption numbers that lasts for a long period, it is evidence that the volcano has released its lava and gas. More importantly, it won’t have the same scale of eruption within 5-10 years. (Turner et al., 2007) This visualization design will be made into a scattered-dot plot in which the size of the dot is corresponding to the eruption duration. Moreover, the x-axis is the Eruption year and the y-axis is the number of eruptions. Thus, this plot can help scientists to identify the eruption scale in a specific period. Also, the frequency of eruptions can be represented by the density of the dots. This design aid scientist to identify the eruption density in a more visualized way.  <br />

<div align=center><img width="75%" height="75%" src="https://github.com/ucl-comp0035/comp0034-cw1-g-group-11-1/blob/master/Fig/Fig.4.png"/> </div>
<div align=center> [Fig.4]: Number of Eruptions and Durations </div>


# Evaluation

### The strength of this design: 

We have used different sets of charts to answer the audience’s questions. Each chart has a specific question to answer and show our audience better-visualized data. Moreover, the color and style of the plot are concise which is appropriate to the target audiences. 

### Weakness: 

However, most of the plot was made for professional use. General information about the volcano is lacking, such as the introduction of the volcano. Also, for a professionally used chart, we could make more complex callback functions that make the audience gather the data easily. 

### How to improve: 

Add more callback functions to the chart. Also, find more data to increase our dataset. For instance, we can add links to each of the volcanoes which will lead the audience to find more specific information. 



# Weekly Report  

### Report 1 

#List what you completed or made progress on this week 

For the project, we investigate the visual design technics for the coursework. Also, research into relationship between visualized data and graphing.

#List what you plan to do next week 

Build a brief structure for the CW and find a suitable CSS stylesheet. 

### Report 2

#List what you completed or made progress on this week 

Create a suitable directory structure and find suitable CSS stylesheet. Also, add Html element to the CW.

#List what you plan to do next week 

Considering the design technics that suitable for this project.

### Report 3

#List what you completed or made progress on this week 

Creating chart in the dash app which could answer the qeustiones from target audience. 

Moreover, change the color of the background and chart.

#List what you plan to do next week 

Plot more charts and Style the chart with respect to the design


### Report 4

#List what you completed or made progress on this week 

Add callback functions to the graph and other functions that suitable for answering the questions. 


#List what you plan to do next week (for the coursework project):

Debuging and writing readme for the CW.




# Bibliography

[1] Turner, M.B., Cronin, S.J., Bebbington, M.S. et al. Developing probabilistic eruption forecasts for dormant volcanoes: a case study from Mt Taranaki, New Zealand. Bull Volcanol 70, 507–515 (2008). https://doi.org/10.1007/s00445-007-0151-4

[2] Venzke, E., 2013. Global Volcanism Program | How do scientists forecast eruptions?. [online] Smithsonian Institution | Global Volcanism Program. Available at: <https://volcano.si.edu/faq/index.cfm?question=eruptionforecast#:~:text=Scientists%20use%20a%20wide%20variety,and%20changes%20in%20gravity%20and> [Accessed 13 February 2022].

[3] Society, N., n.d. Plate Tectonics and Volcanic Activity. [online] National Geographic Society. Available at: <https://www.nationalgeographic.org/article/plate-tectonics-volcanic-activity/> [Accessed 14 February 2022].
