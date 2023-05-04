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
  self.window_x
  ```
  the x-Position of the displayed Window
  
  ```python
  self.num_values
  ```
  the Amount of values that are currently saved in the array
  
  ```pyhton
  self.max_co2_level
  ```
  the max value that can be displayed in the Graph. Everything above this value will be displayed as the maximum value. The Scaling happens automaticly so don't worry about it
  
  ``python
  self.grapg_color
  ``
  
