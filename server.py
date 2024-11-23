
import requests
import json
import socket
import threading

#to seperate the users data to make every user has his own
thread_data=threading.local()
haedline = "https://newsapi.org/v2/top-headlines?"
sources='https://newsapi.org/v2/top-headlines/sources?'

def handle_client(conn,adrr):
    '''a function to handle the client request'''
    print("connected to client at", addr)
    thread_data.client_data={} #dict for every client
    try:
        while True:
            data = conn.recv(1024)
            print(data[-2])
            # to determine wither its headline request or sources
            if data[-2]==115: # the number is for s in ascii table
                url=sources
            elif data[-2]==104: # the number is for h in ascii table
                url=haedline
            if not data:
                break
            '''distinguish between the choise of client'''
            if data[-2:]==b'h1':
                thread_data.client_data['q']=data[:-2].decode()
            elif data[-2:]==b'h2' or data[-2:]==b's1':
                thread_data.client_data['category']=data[:-2].decode()
            elif data[-2:]==b'h3'or data[-2:]==b's2':
                thread_data.client_data['country']=data[:-2].decode()
            elif data[-2:]==b's3':
                thread_data.client_data['languege']=data[:-2].decode()
            
            prams={'apiKey':'69252012c3fb4382afcf446fa407a866'}
            #move the client info to prameter dict (if chosen)
            if 'q' in thread_data.client_data:
                prams['q']=thread_data.client_data['q']
            if 'category' in thread_data.client_data:
                prams['category']=thread_data.client_data['category']
            if 'country' in thread_data.client_data:
                prams['country']=thread_data.client_data['country']
            if 'languege' in thread_data.client_data:
                prams['language']=thread_data.client_data['languege']
            
            response = requests.get(url=url,params=prams)
            print(response.url)
            
            if response.status_code == 200:
                data = response.json()
                 # Save data to a file
                with open("posts.json", "w") as file:
                     json.dump(data, file, indent=4)
                     print("[SUCCESS] Data saved to 'posts.json'")
            else:
                print(f"[ERROR] Status Code: {response.status_code}")

            
    except Exception as e:
        #if there was any error during the procces
        print("connection closed")
        print(e)
        


#define a socket and starting tcp conection
server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)
print("the server is listening on localhost port 12345")

#accept connection from clients ans start thread
while True:
    conn,addr=server_socket.accept()
    thread=threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()