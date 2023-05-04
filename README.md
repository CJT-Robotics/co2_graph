# co2_graph
This Program subscribes a 32 Bit Integar and displays the values in a highly cusomizable graph using the python Library opencv2.

## Tutorial

  1. Direct to your catkin-workspace.
  ```bash
  cd ~/catkin_ws/src
  ```
  2. Clone this repository.
  ```bash
  git clone https://github.com/CJT-Robotics/co2_graph.git
  ```
  3. Buiild your catkin-worspace
  ```bash
  cd ..
  catkin_make
  ```
  
## Dokumentation
  ### The parameters
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
  
  now in the drawScale-Method
  ```python
  hor_lines
  ```
  the amount of horizontal Lines that are 
  
