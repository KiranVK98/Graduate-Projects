#NAME: KIRAN VENKATESH KULKARNI
#ID: 1001848434

import socket #import socket for socket connection
import time #importing time for getting date, time of file modification
import pickle #importing pickle to send python objects
import os #importing os for accessing the files in the directory
from watchdog.observers import Observer #observer to observe file changes
from watchdog.events import FileSystemEventHandler #file handler to monitor events
from dirsync import sync #dirsync to synchronize two folders
import threading #thread to serve the client when requested and another thread to synchronize the contents of the folder
HEADERSIZE=100 #initializing headersize for the message length
#initiating the connection between the client and the server a
#https://www.youtube.com/watch?v=Lbfe3-v7yE0

#path ='/Users/Kiran/Desktop/directory_a'
path='./directory_a' #path to directory a
serv_path='./directory_b' #path to directory b
cur=os.getcwd() 
print(cur)
servers=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #ipv4 and TCP connection
servers.bind((socket.gethostname(),1234)) #binding ip with port number
servers.listen(5) #queue of 5 if it starts getting to filled up
clientsocket=0
source='C:/Users/Kiran/Desktop/Myproj/directory_a'
destination='C:/Users/Kiran/Desktop/Myproj/directory_b'


def serverb_connect():
        #connecting to server b to get the contents of the files
        #https://www.youtube.com/watch?v=8A4dqoGL62E
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #establishing ipv4 and tcp connection with server b
        s.connect((socket.gethostname(), 7444)) #connecting with server b
        while True: 
            sorted_d={} #dictionary that contains sorted file names of server b
            full_message = b'' 
            new_message = True
            while True: #while we have a new message from server b receive it
                msg = s.recv(16)
                if new_message:
                    msglen = int(msg[:HEADERSIZE]) #get the length of the message until declared header size
                    new_message = False #change new message to false as we have already received it

                full_message += msg #add the message received to the existing full message

                if len(full_message)-HEADERSIZE == msglen: #check if the entire message has been received
                    d=pickle.loads(full_message[HEADERSIZE:]) #load the entire message into dictionary d
                    sorted_d = dict( sorted(d.items(), key=lambda x: x[0].lower()) ) #https://stackoverflow.com/questions/24728933/sort-dictionary-alphabetically-when-the-key-is-a-string-name
                    #sorted_d contains the sorted file names of server b as key and and file size, date modified, time as value 
                    new_message = True #new message is set to true to receive the next new message
                    full_message=b'' #full message is cleared inorder to add the new received message to full message

                    return sorted_d #return dictionary of sorted file names of server b

def threadFunc():
    class Watcher:

        def __init__(self, directory, handler=FileSystemEventHandler()): 
            self.observer = Observer()  #constructor to initialize the observer
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
                    files = os.listdir(destination)
                    os.chdir('./directory_b')
                    for f in files:
                        if(f==a):
                            os.remove(str(a))
                    self.pause=False
                    os.chdir('..')
                    sync(source,destination,'sync')
                    #sync('./directory_b','./directory_a','sync')

            #if the file is deleted we get the file name deleted in directory a and delete it in directory b
            elif(event.event_type=="deleted"):
                if not self.pause:
                    self.pause=True
                    print(event)
                    #sync('./directory_a','./directory_b','sync')
                    #sync('./directory_b','./directory_a','sync')
                    #print(os.listdir('./directory_a'))
                    a=str(event)
                    a=a.split('\\')
                    a=a[-1][:-2]
                    print(a+'.txt file has been deleted')
                    files = os.listdir(destination)
                    os.chdir(destination)
                    for f in files:
                        if(f==a):
                            os.remove(str(a))
                    self.pause=False
                    os.chdir('..')

            elif(event.event_type=="modified"):
                print(event)
                sync(source,destination,'sync') #if file is created in directory a, it synchronizes and creates the file in b
                sync(destination,source,'sync') 
    w = Watcher('./directory_a', MyHandler()) #start the watcher by calling my handler class
    w.run() 

def main():
    # Create a Thread with a function without any arguments
    th = threading.Thread(target=threadFunc)
    # Start the thread
    th.start()
    # Print some messages on console
    
    while True:
    
        clientsocket,address=servers.accept() #accept the connection from the client
        print(f"Connection from {address} has been established!")
    
        #https://stackoverflow.com/questions/67099229/list-all-files-available-in-server-directory-in-client-computer-using-python-soc
        files = os.listdir(path) #list the directories of server a
        list={} #dictionary that contains file name, size, time of server a_directory files
        os.chdir(path) #changing the current working directory to that of directory_a folder
        for f in files:
            
            #to convert to kilobytes
            kb=(os.path.getsize(f))/1024 #divide the size by 1024 to convert the file size to KB
            list[f]=str(round(kb,3)) +" KB           " #add the rounded value with string KB
            #https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
            list[f]+=time.ctime(os.path.getmtime(f)) #get the file modified date and time 

        
        server_b_sorted=serverb_connect() #connect with server b by calling the method serverb_connect
        comb_servers_data={**list,**server_b_sorted} #combine dictionaries of directory_a and directory_b
        comb_servers_data = dict( sorted(comb_servers_data.items(), key=lambda x: x[0].lower()) ) #sort the files of directory a and directory b wrt first letter

        msg=pickle.dumps(comb_servers_data) #convert the dictionary to pickle inorder to send it to the client
        msg=bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8")+msg #encode the message with utf-8 encoding

        clientsocket.send(msg) #send the encoded message to the client
        os.chdir(cur)
    # Wait for thread 



if __name__ == '__main__':
   sync('./directory_a','./directory_b','sync') #synchronize two directories when we start server a
   sync('./directory_b','./directory_a','sync')
   main()

