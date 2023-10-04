#!/usr/bin/env python
import rospy
from std_msgs.msg import Int32
import numpy as np, cv2
from screeninfo import get_monitors
from time import gmtime, strftime

class subscriber:    
    def __init__(self):

        # In ROS, nodes are uniquely named. If two nodes with the same
        # name are launched, the previous one is kicked off. The
        # anonymous=True flag means that rospy will choose a unique
        # name for our 'listener' node so that multiple listeners can
        # run simultaneously.
        rospy.init_node('co2_graph', anonymous=True)

        rospy.Subscriber("/cjt/co2", Int32, grph.addValue)

        # spin() simply keeps python from exiting until this node is stopped
        rospy.spin()

class graph:
    def __init__(self):
        self.graph_height = 250
        self.window_height = self.graph_height + 50
        self.window_x = 0
        self.num_values = 0
        self.max_co2_level = 35000
        self.graph_color = (0,125,250)
        self.scale_color = (255,255,255)
        self.pix_between_value = 10

        for m in get_monitors():
            if(m.is_primary):
                self.window_width = m.width
                self.window_y = m.height - self.window_height

        self.disc_factor = self.graph_height / self.max_co2_level
        self.values = []
        self.scaled_image = np.zeros((self.window_height,self.window_width,3),dtype=np.uint8)

        self.drawScale()
    def drawScale(self):
            hor_lines = 2 + 3  #2 + the desired numer of horizontal lines
            hor_line_factor = int(self.graph_height/(hor_lines-1))

            self.vert_lines = 1 + 10 #1 + the desired amount of vertical lines
            self.vert_line_factor = int(self.window_width/(self.vert_lines))

            cv2.line(self.scaled_image,(0,self.graph_height),(self.window_width,self.graph_height),self.scale_color,2)

            for i in range(1,hor_lines):
                cv2.line(self.scaled_image,(0,i*hor_line_factor),(self.window_width,i*hor_line_factor),self.scale_color,1)
                value = str(int(self.max_co2_level - ((i*hor_line_factor)/self.disc_factor))) + 'ppm'
                cv2.putText(self.scaled_image,value,(5,i*hor_line_factor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)
                cv2.putText(self.scaled_image,value,(self.window_width - 90,i*hor_line_factor-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)

            for i in range (1,self.vert_lines):
                cv2.line(self.scaled_image,(i*self.vert_line_factor,self.graph_height),(i*self.vert_line_factor,self.graph_height + 10),self.scale_color,1)

    def addValue(self,data):
        value = data.data

        if(self.num_values < int(self.window_width/self.pix_between_value)):
            self.values.append((value,strftime("%M.%S", gmtime()))) 
            self.num_values += 1    
        else:
            for i in range(self.num_values-1):
                self.values[i] = self.values[i+1]   #assign each value of the array to the slot in front of it
            self.values[self.num_values-1] = (value,strftime("%M.%S", gmtime()))

        self.drawGraph() 

    def drawGraph(self):
        blank_image = self.scaled_image.copy()

        last_value = self.values[0][0]
        for i in range(self.num_values):
            pix_x = i*self.pix_between_value
            pix_y = int(self.graph_height - self.values[i][0] * self.disc_factor)

            last_pix_x = (i-1)*self.pix_between_value
            last_pix_y = int(self.graph_height - last_value * self.disc_factor)
            
            if(last_value >= self.max_co2_level):
                last_pix_y = 0
            if(self.values[i][0] >= self.max_co2_level):
                pix_y = 0 
            
            #print('pix_y:',pix_x,'last_pix_y:',last_pix_y,'value:',self.values[i][0],'last_value:',last_value)

            blank_image[pix_y][pix_x] = self.graph_color
            cv2.line(blank_image,(pix_x,pix_y),(last_pix_x,last_pix_y),self.graph_color,1)

            last_value = self.values[i][0]

        for i in range(1,self.vert_lines):
            index = int((i*self.vert_line_factor)/self.pix_between_value)
            if(self.num_values > index):
                cv2.putText(blank_image,str(self.values[index][1]),(i * self.vert_line_factor - 23,self.graph_height + 30),cv2.FONT_HERSHEY_SIMPLEX,0.5,self.scale_color,1)

        cv2.imshow('CO₂ Graph', blank_image), cv2.waitKey(3)
        cv2.moveWindow('CO₂ Graph',self.window_x,self.window_y-40)
        #blank_image = self.scaled_image

if __name__ == '__main__':
    grph = graph()
    sub = subscriber()