#NAME: KIRAN VENKATESH KULKARNI
#ID: 1001848434

import socket #import socket for socket connection
import pickle #importing pickle to send python objects
HEADERSIZE = 100 #initializing headersize for the message length
import os
import sys
#socket connection is established using ipv4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234)) #connecting with server a
#receive message(dictionary) from the server a and print it
#https://www.youtube.com/watch?v=8A4dqoGL62E
cur=os.getcwd()
path='C:/Users/Kiran/Desktop/Myproj/directory_a'
input=sys.argv #to ge the lock/unlock command from the user
#print(input)
if(len(input)>=2): # to check if the client wants to lock or just obtain the query freom the server
    argument=input[1:]
    from os import listdir #to list the directory content
    from os.path import isfile, join 
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    file=onlyfiles[int(argument[1][-1])] #to get the command after python command
else:
    argument=['NONE']


from stat import S_IREAD, S_IWRITE, S_IRGRP, S_IROTH
if(argument[0]=='-lock'):
    os.chdir(path)    
    os.chmod(file, S_IREAD|S_IRGRP|S_IROTH) #to change the permission of the file to write only

elif(argument[0]=='-unlock'):
    os.chdir(path)
    os.chmod(file, S_IWRITE|S_IRGRP|S_IROTH) #to unlock the file and set the permission to write only

elif(argument[0]=='NONE'):
    while True: #while the connection is active
        full_message = b''
        new_message = True
        while True: #while we have a new message from server a receive it
            msg = s.recv(10000000)
            if not msg: break
            #print(msg)
            if new_message:
                msglen = int(msg[:HEADERSIZE]) #get the length of the message until declared header size
                new_message = False #change new message to false as we have already received it


            full_message += msg #add the message received to the existing full message
            #print(len(full_message)-HEADERSIZE, msglen)
            if len(full_message)-HEADERSIZE == msglen: #check if the entire message has been received
                d=pickle.loads(full_message[HEADERSIZE:]) #load the entire message into dictionary d
                #print(d)
                for k,v in d.items(): #iterating keys and values of dictionary which are file names and date, file size 
                    ls=v.split() #splitting the string to only get file modified size and day of modification
                    length=len(k) #length of file size
                    os.chdir('C:/Users/Kiran/Desktop/Myproj/directory_a')
                    
                    if(os.access(k, os.W_OK)):
                        print('{:<12}'.format(k) +'{:>19}'.format(ls[0])+ls[1]+"    "+ls[4]+"-"+ls[2]) #printing the formatted strings(file name, modified day and file size)
                        
                    else:
                        print('{:<12}'.format(k) +'{:>19}'.format(ls[0])+ls[1]+"    "+ls[4]+"-"+ls[2]+"     "+"<locked>") #printing the formatted strings(file name, modified day and file size)
                        

                new_message = True #new message is set to true to receive the next new message
                full_message=b'' #full message is cleared inorder to add the new received message to full message

# print(file)
# #if(argument[0]=='-lock'):

# print(os.getcwd())
# print(argument)
# # data=input('enter index of file you want to lock or unlock')
# # dos=data.split(' ')
# # keys=list(d.keys())
# # file_name=keys[int(dos[0])]
# # os.chdir(path)
# # os.chmod(str(file_name), 0o777)
# # os.chdir(cur)
# # print(os.getcwd())

            
            
            
