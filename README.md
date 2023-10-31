# co2_graph
This Program subscribes a 32 Bit Integar and displays the values in a highly customizable graph using the python Library opencv2.

## Tutorial

  1. Direct to your catkin-workspace.
  ```bash
  cd ~/catkin_ws/src
  ```
  2. Clone this repository.
  ```bash
  git clone https://github.com/CJT-Robotics/co2_graph.git
  ```
  3. Build your catkin-worspace
  ```bash
  cd ..
  catkin_make
  ```
  
## The parameters
  ```python
  self.graph_height
  ```
  the height of the Graph in px
  
  ```python
  self.window_height
  ```
  the height of the Window. Adds some pixels at the bottom to make room for time staps of the values
  
  ```python
  self.num_values
  ```
  the Amount of values that are currently saved in the array
  
  ```pyhton
  self.max_co2_level
  ```
  the max value that can be displayed in the Graph. Everything above this value will be displayed as the maximum value. The Scaling happens automaticly so don't worry about it
  
  ```python
  self.graph_color
  ```
  the color of the Graph in the BGR-format
  
  ```python
  self.scale_color
  ```
  the color of the Scale in the BGR-format
  
  ```python
  self.pix_between_value
  ```
  the x-spacing between two values in the displayed Graph in px

  ```python
  for m in get_monitors():
    if(m.is_primary):
      self.window_width = m.width
  ```
  sets the width of the displayed window according to the the width of your primary monitor. If you have more than one Monitor connected and want the graph to be displayed at the second monitor, just add a ```not``` in front of ```m.is_primary``` so that it reads ```if(not m.is_primary):```. In case you use more than two monitors and want the Window to be displayed at the third (or higher) Monitor you have to add the line ```print(m.name)``` below the line ```for m in get_monitors():```. When you execute the node you get a list of the names of the monitors afterwards you can remove the added line again and change ```if(m.is_primary):``` to ```if(m.name == <the Name of the desired Monitor>):```
  
  ```python
  self.window_x
  ```
  the x-Position of the displayed Window. Is set automatically so display the window in the bottom of the screen
  
  ```python
  self.window_y
  ```
  the y-Position of the displayed Window. Is set automatically so display the window in the bottom of the screen
  
  ```pyhton
  self.disc_factor
  ```
  the factor the added values get multiplied with, also known as the y-dilation of the Graph 
  
  ```python
  self.values
  ```
  the array the imported values are saved in. It's two Dimensional: 1. Slot: the value as int  2.Slot: the timestamp when the value is added. Beispiel value[index][0] = value; value[index][1] = timestamp
  
  ```pyhton
  self.scaled_image
  ```
  the image that has the scale on it 
  
  ### now in the drawScale-Method
  ```python
  hor_lines
  ```
  the amount of horizontal Lines that are drawn in the scaling-image. The value must be 2 higher than the desited amount of lines
  
  ```pyhton
  hor_line_factor
  ```
  the distance between two lines in px
  
  ```python
  self.vert_lines
  ```
  the amount of timestamps in the graph. Must be one higher than the desired amount
  
  ```python
  self.vert_line_factor
  ```
  the distance between two timestamps in px
  
## The Code Explained
  ### The "main-Method":
  ```python
  if __name__ == '__main__':
    grph = graph()
    sub = subscriber()
  ```
  This block of code is executed when the Program is launched.
  
  ```python
  grph = graph()
  ```
  initializes an object of the class graph that is called grph
  
  ```python
  sub = subscriber()
  ```
  initializes an object of the class subscriber that is called sub
  
  ### class subscriber:
  #### __init__ - Method:
  this Method runs, when an object of this class is created 
  ```python
  rospy.init_node('co2_graph', anonymous=True)
  ```
  inits the ```co2_graph``` ROS_node that will be named unique due to the ```anonymous=True``` Flag. The Unique name is important as ROS doesn't allow multiple nodes to have the same names. If this would happen, the older node would be closed.
  
  ```python
  rospy.Subscriber("/cjt/co2", Int32, grph.addValue)
  ```
  subscribes to the topic ```/cjt/co2``` this might be different depending on your ROS_Namespace. to Check the name of your topic, start the node that publishes the co2-values and type ```rostopic list```. The ```Int32``` means, that the node will only react to published messages that have the type ```Int32```. ```grph.addValue``` is the name of the Function that is called if a Message of the right datatype is recieved. In this case the ```addValue``` Method is located in the class graph, what is indicated by the prefix ```grph.```, that is the name of the Object initialized before.

  ```python
  rospy.spin()
  ```
  keeps python from exiting the program until the node is stopped.
  
  ### class graph:
  #### __init__ - Method:
  this Method runs, when an Object of this class is created
  this Method declares the Parameters needed for thr Graph. It also starts the procces of drawing the scale to the image
  
  ```python
  for m in get_monitors():
    if(m.is_primary):
      self.window_width = m.width
      self.window_y = m.height - self.window_height
  ```
  this loops through all monitors connected and checks if the current monitor is the primary one. If this is the case, the parameters are set according to the specs of the Monitor
  
  #### draw-Scale - Method:

  this Method draws the Axes and the Scaling of the Graph
  
  ```python
  cv2.line(self.scaled_image,(0,self.graph_height),(self.window_width,self.graph_height),self.scale_color,2)
  ```
  uses opencv2 to draw the horizontal line that seperates the the are of the graph and the area where the timestamps are displayed. The Parameters given are:
  - ```self.scaled_image```: the image in which the line is drawn
  - ```(0,self.graph_height)```: the start position of the line as Tupel
  - ```(self.window_width,self.graph_height)```: the end postion of the line as Tupel
  - ```self.scale_color```: the color of the line as Tupel in the BGR format
  - ```2```: the Thickness of the line

  ``` python
  for i in range(1,hor_lines):
    cv2.line(self.scaled_image,(0,i*hor_line_factor),(self.window_width,i*hor_line_factor),self.scale_color,1)
    value = str(int(self.max_co2_level - ((i*hor_line_factor)/self.disc_factor))) + 'ppm'
    cv2.putText(self.scaled_image,value,(5,i*hor_line_factor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)
    cv2.putText(self.scaled_image,value,(self.window_width - 90,i*hor_line_factor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)
  ```
  this loops through the amount of horizontal lines set before. the y-value of the lines is calculated by multiplying the index with the distance between the lines that was set as a Parameter. The x-values are both sides of the window.
  
  ```python
  cv2.line(self.scaled_image,(0,i*hor_line_factor),(self.window_width,i*hor_line_factor),self.scale_color,1)
  ```
  draws the horizontal line. For explanation of the Parameters see above.
  
  ```
  value = str(int(self.max_co2_level - ((i*hor_line_factor)/self.disc_factor))) + 'ppm'
  ```
  calculates the value that is used to label the line just drawn. This is done by calculation the distance to the top of the image in px, this distance is convertet to ppm and substracted from the max co2 level. At the end the unit ppm is added.
  
  ```python
  cv2.putText(self.scaled_image,value,(5,i*hor_line_factor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)
  cv2.putText(self.scaled_image,value,(self.window_width - 90,i*hor_line_factor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)
  ```
  places the calculated value on the lines. The Parameters given are:
  - ```self.scaled_image```: the image that the text is put to
  - ```value```: the text that is put in the Image. Must be a String
  - ```(self.window_width - 90,i*hor_line_factor-5)```: The bottom-left position of the Text as Tupel
  - ```cv2.FONT_HERSHEY_SIMPLEX```: the font of the text
  - ```0.5```: the scale of the text
  - ```self.scale_color```: the color of the text as Tupel in the BGR format
  - ```1```: the line_thicknes of the text
  
  ```python
  for i in range (1,self.vert_lines):
    cv2.line(self.scaled_image,(i*self.vert_line_factor,self.graph_height),(i*self.vert_line_factor,self.graph_height + 10),self.scale_color,1)
  ```
  draws small vertical lines that indicate the position of the timestamps. This is done by looping though the number of verical lines set before and multipy the index with the amount of pixels between the lines. 

#### addValue - Method  

the Method that subscribes the topic of the Value that is to be listed in the Graph, in this case to co2 Level.

```value = data.data```: save the subscribed value to a loval variable to work with it

```python
   if(self.num_values < int(self.window_width/self.pix_between_value)):
            self.values.append((value,strftime("%M.%S", gmtime()))) 
            self.num_values += 1 
```
When the array is not full yet, the recieved value is added at the and of the array and the variable to keep track of the amount of values is increased

``` python
else:
            for i in range(self.num_values-1):
                self.values[i] = self.values[i+1]   #assign each value of the array to the slot in front of it
            self.values[self.num_values-1] = (value,strftime("%M.%S", gmtime()))
```
When the max amount of values is reached, all values stored in the array are put in the slot before them and the received message is put in the last slot
  
```self.drawGraph()``` repaints the Graph with refreshed values

#### drawGraph - Method

draws the Graph into the Image that already contains axes and measures

```blank_image = self.scaled_image.copy()``` copies the Image that the scaling can be reused
```last_value = self.values[0][0] ``` saves the last value. this value is important for a connecting line between the points

```for i in range(self.num_values):``` loop through all saved values

```python
pix_x = i*self.pix_between_value
pix_y = int(self.graph_height - self.values[i][0] * self.disc_factor)
```
calculate the coordinates of the current value

```python
last_pix_x = (i-1)*self.pix_between_value
last_pix_y = int(self.graph_height - last_value * self.disc_factor)
```
calculate the coordinates of the previous value

```python
if(last_value >= self.max_co2_level):
    last_pix_y = 0
  if(self.values[i][0] >= self.max_co2_level):
    pix_y = 0
```
set the y_position to the upper edge of the window when the value is higher than the set threshold

```blank_image[pix_y][pix_x] = self.graph_color``` paint the pixel to the image
```cv2.line(blank_image,(pix_x,pix_y),(last_pix_x,last_pix_y),self.graph_color,1)``` add a connection line in between pixels
```last_value = self.values[i][0]``` refresh last value

```python
for i in range(1,self.vert_lines):
  index = int((i*self.vert_line_factor)/self.pix_between_value)
  if(self.num_values > index):
    cv2.putText(blank_image,str(self.values[index][1]),(i * self.vert_line_factor - 23,self.graph_height + 30),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)
```
puts the timestamps of the corresponding values below the vertical lines 

```python
cv2.imshow('CO₂ Graph', blank_image), cv2.waitKey(3)
cv2.moveWindow('CO₂ Graph',self.window_x,self.window_y-40)
```
display the image at a predefined position 

