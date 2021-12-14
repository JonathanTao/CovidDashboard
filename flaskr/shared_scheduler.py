'''
    The tasks of this file are as follows:
        - create an instance of a scheduler which will be used across other files
'''



import sched
import time



scheduler = sched.scheduler(time.time, time.sleep) #creates an instance of a scheduler which will be used across other files