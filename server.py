
import requests
import json
import socket
import threading
import re
from datetime import datetime

#to seperate the users data to make every user has his own
thread_data=threading.local()
haedline = "https://newsapi.org/v2/top-headlines?apiKey=4411d3bdab63427c91fcef22bed1b3f0"
sources='https://newsapi.org/v2/top-headlines/sources?apiKey=4411d3bdab63427c91fcef22bed1b3f0'

def requested_data(data,type,torequest,recdata):

    if torequest=='':
        torequest=type
    else:
        torequest+=' , '+type
    if recdata=='':
        recdata=data
    else:
        recdata+=' , '+data

    return [recdata,torequest]
    

def handle_client(conn,adrr):
    '''a function to handle the client request'''
    thread_data.client_data={} #dict for every client
    url=''
    torequest=''
    recdata=''
    tp=''
    try:
        while True:
            data = conn.recv(1024)
            # to determine wither its headline request or sources
            if data[-2]==115: # the number is for s in ascii table
                if url==haedline:
                    thread_data.client_data={}
                    torequest=''
                    recdata=''


                url=sources

            elif data[-2]==104: # the number is for h in ascii table
                if url==sources:
                    thread_data.client_data={}  
                    torequest=''
                    recdata=''

                url=haedline 
            

            if not data:
                break
            '''distinguish between the choise of client'''
            if data[-2:]==b'h1':
                thread_data.client_data['q']=data[:-2].decode()
                tp='keywords'
                
            elif data[-2:]==b'h2' or data[-2:]==b's1':
                thread_data.client_data['category']=data[:-2].decode()
                tp='category'
                
            elif data[-2:]==b'h3'or data[-2:]==b's2':
                thread_data.client_data['country']=data[:-2].decode()
                tp='country'
            elif data[-2:]==b's3':
                thread_data.client_data['language']=data[:-2].decode()
                tp='language'
            elif data[-2:]==b'h4':
                 thread_data.client_data['country']='us'
                    
            
            cdata=requested_data(data[:-2].decode(),tp,torequest,recdata)
            recdata=cdata[0]
            torequest=cdata[1]
            
            prams={}
            #move the client info to prameter dict (if chosen)
            if 'q' in thread_data.client_data:
                prams['q']=thread_data.client_data['q']
            if 'category' in thread_data.client_data:
                prams['category']=thread_data.client_data['category']
            if 'country' in thread_data.client_data:
                prams['country']=thread_data.client_data['country']
            if 'language' in thread_data.client_data:
                prams['language']=thread_data.client_data['language']
            
            print(client_name,'request by',torequest,'with',recdata)
            
            response = requests.get(url=url,params=prams)
            print(response.url)
            if response.status_code == 200:
                nameoffile=client_name+' '+torequest+' '+recdata+' '+'A19.json'
                nameoffile=re.sub("\s+", "_",nameoffile)
                data = response.json()
                with open(nameoffile, "w") as file:
                     json.dump(data, file, indent=4)
                     print("[SUCCESS] Data saved to",nameoffile)
                article_details = []
                breiflist = []
                if url==haedline:
                # iterate over the articles and save their details 
                    for article in data.get("articles", []):
                        
                            source_name = article.get("source", {}).get("name", "No source name available")
                            title = article.get("title", "No title available")
                            author = article.get("author", "No author available")
                            publication_date = article.get("publishedAt", "No publication date available")
                            description = article.get("description", "No description available")
                            url = article.get("url", "No url available")
                            tobject =datetime.strptime(publication_date, "%Y-%m-%dT%H:%M:%SZ")
                            formatted_date =tobject.strftime("%b %d %Y, %I:%M %p")
                            # Convert the date and time to a more readable format
                            article_details.append({"source_name": source_name, "title": title, "author": author,'url': url, "description": description, "published At":formatted_date })
                            breiflist=[{"title": a["title"], "author": a["author"], "published-At": a["published At"]}for a in article_details]
                   
                elif url==sources:
                     for article in data.get("sources", []) and  range(15):
                        source_name = article.get("name", "No source name available")
                        country = article.get("country", "No title available")
                        Url=article.get("url", "No url available")
                        description = article.get("description", "No description available")
                        category = article.get("category", "No category available")
                        language = article.get("language", "No language available")
                        article_details.append({"source_name": source_name, "country": country, "description": description, "url": Url, "category": category, "language": language })
                        breiflist.append({"source_name": source_name, "country": country, "description": description, "url": Url, "category": category, "language": language})
            else:
                print("[ERROR] Status Code:",response.status_code)
            
             
            results=json.dumps(breiflist)
            conn.sendall(results.encode()) #send article details to client
                    
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
    client_name=conn.recv(100).decode()
    print(client_name,'has connected with address',addr)
    thread=threading.Thread(target=handle_client,args=(conn,addr))
    thread.start()