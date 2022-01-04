#NAME: KIRAN VENKATESH KULKARNI
#ID: 1001848434

import socket #import socket for socket connection
import time #importing time for getting date, time of file modification
import pickle #importing pickle to send python objects
import os #importing os for accessing the files in the directory
import socket #import socket for socket connection
import time #importing time for getting date, time of file modification
import pickle #importing pickle to send python objects
import os #importing os for accessing the files in the directory
from watchdog.observers import Observer  #observer to observe file changes
from watchdog.events import FileSystemEventHandler #file handler to monitor events
from dirsync import sync #dirsync to synchronize two folders
import threading #thread to serve the client when requested and another thread to synchronize the contents of the folder


HEADERSIZE=100 #initializing headersize for the message length

servers=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and TCP connection
servers.bind((socket.gethostname(),7444)) #binding ip with port number
servers.listen(5)#queue of 5 if it starts getting to filled up

def threadFunc():
    class Watcher:

        def __init__(self, directory, handler=FileSystemEventHandler()):
            self.observer = Observer() #constructor to initialize the observer
            self.handler = handler
            self.directory = directory #constructor to initialize the directory

        def run(self):
            self.observer.schedule(
                self.handler, self.directory, recursive=True)
            self.observer.start() #starting the observer
            print("\nWatcher Running in {}/\n".format(self.directory)) #prints the directory which the watcher is watching
            try:
                while True:
                    time.sleep(1) #checks for changes every one second
            except: 
                self.observer.stop() #stops when the user stops it
            self.observer.join()
            print("\nWatcher Terminated\n")


    class MyHandler(FileSystemEventHandler):
        def __init__(self):
            self.observer = Observer()
            self.pause=False

        def on_any_event(self, event):
            
            if(event.event_type=="created"):
                print(event)
                sync('./directory_a','./directory_b','sync') #if file is created in directory a, it synchronizes and creates the file in b
                sync('./directory_b','./directory_a','sync')

            #if the file is modified we get the file name in directory a and modify accordingly in directory b
            elif(event.event_type=='moved'):
                if not self.pause:
                    #print(event)
                    a=str(event)
                    a=a.split('\\')
                    print(a)
                    a=a[2][:-27]
                    print(a+" has been renamed")
                    files = os.listdir('./directory_a')
                    os.chdir('./directory_a')
                    for f in files:
                        if(f==a):
                            os.remove(str(a))
                    self.pause=False
                    os.chdir('..')
                    sync('./directory_b','./directory_a','sync')
                    #sync('./directory_b','./directory_a','sync')

            #if the file is deleted we get the file name deleted in directory a and delete it in directory b
            elif(event.event_type=="deleted"):
                if not self.pause:
                    self.pause=True
                    
                    #sync('./directory_a','./directory_b','sync')
                    #sync('./directory_b','./directory_a','sync')
                    #print(os.listdir('./directory_a'))
                    a=str(event)
                    a=a.split('\\')
                    a=a[-1][:-2]
                    print(a+'.txt file has been deleted')
                    files = os.listdir('./directory_a')
                    os.chdir('./directory_a')
                    for f in files:
                        if(f==a):
                            os.remove(str(a))
                    self.pause=False
                    os.chdir('..')

            elif(event.event_type=="modified"):
                print(event)
                sync('./directory_a','./directory_b','sync') #if file is created in directory a, it synchronizes and creates the file in b
                sync('./directory_b','./directory_a','sync')   
    w = Watcher('./directory_b', MyHandler()) #start the watcher by calling my handler class
    w.run()

def main():
    # Create a Thread with a function without any arguments
    th = threading.Thread(target=threadFunc)
    # Start the thread
    th.start()
    # Print some messages on console
    
    while True:
        servera_socket,address=servers.accept() #accepting the connection
        print(f"Connection from {address} has been established!") #printing the connection has been established on the server terminal

        cur=os.getcwd()
        path='./directory_b' #directory_b folder in the project folder
        #https://stackoverflow.com/questions/67099229/list-all-files-available-in-server-directory-in-client-computer-using-python-soc
        files = os.listdir(path) #listing the files in path
        list={} #dictionary to hold file names as key and size, modified time as values
        os.chdir(path) #changing the directory to directory_a folder
        for f in files:
            #https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
            kb=(os.path.getsize(f))/1024 #getting the file size and converting it to kb by dividing it by 1024
            list[f]=str(round(kb,3)) +" KB           " #rounding off to 3 decimals and adding the string KB as the value to the dictionary whereas the key is the file name
            list[f]=list[f]+time.ctime(os.path.getmtime(f)) #adding the time to the value to get file modified date and time
            


        msg=pickle.dumps(list) #converting the dictionary into pickle in order to send to the client
        msg=bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8")+msg #sending the message-dictionary to the client using utf-8 encoding
        os.chdir(cur)
        servera_socket.send(msg) #sending the dictionary objecvt to client
        
    # Wait for thread 



if __name__ == '__main__':
   main()

    
        