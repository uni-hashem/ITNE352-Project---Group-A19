
import requests
import json
import socket
import threading

#to seperate the users data to make every user has his own
thread_data=threading.local()
#urls one for headlines and another for sources
haedline = "https://newsapi.org/v2/top-headlines?apiKey=4411d3bdab63427c91fcef22bed1b3f0"
sources='https://newsapi.org/v2/top-headlines/sources?apiKey=4411d3bdab63427c91fcef22bed1b3f0'

def handle_headline(data):
    '''Function to handle headline data and return a brief list and full list'''
    counter=1
    article_details=[]
    breiflist=[]
    # cheking if the there are headlines retrieved
    if data.get("totalResults")==0:
             breiflist.append("There is no result for this article")
             article_details.append("There is no result for this article")

    for article in data.get("articles", []):
         counter+=1
         source_name = article.get("source", {}).get("name", "No source name available")
         title = article.get("title", "No title available")
         author = article.get("author", "No author available")
         publication_date = article.get("publishedAt", "No publication date available")
         description = article.get("description", "No description available")
         url = article.get("url", "No url available")
         article_details.append({"source_name": source_name, "title": title, "author": author,'url': url, "description": description, "published At":publication_date })
         breiflist=[{"title": a["title"], "author": a["author"], "source_name": a["source_name"]}for a in article_details]
         if counter==16:
             break
    return breiflist,article_details

def handle_requestes(url,filename,prams):
    '''Function to handle requests and save data to file. Returns brief and full list if requested'''
    response = requests.get(url=url,params=prams)
    if response.status_code == 200:
        data = response.json()
        with open(filename, "w") as file:
             json.dump(data, file, indent=4)
             print("[SUCCESS] Data saved to",filename)
        if url==haedline:
            breiflist,article_details = handle_headline(data)

        elif url==sources:
            breiflist,article_details = handle_sources(data)
    else:
        print("[ERROR] Status Code:",response.status_code)
    return breiflist,article_details
            
def handle_sources(data):
    '''function to handle source data and return a brief list and full list'''
    counter=1
    sources_list=[]
    breiflist=[]
    # cheking if the there are sources retrieved
    if data.get("totalResults")==0:
             breiflist.append("There is no result for this article")
             sources_list.append("There is no result for this article")

    for article in data.get("sources", []):
         if article.get("totalResults",False):
             breiflist.append("There is no result for this article")
             sources_list.append("There is no result for this article")
             break
         counter+=1
         source_name = article.get("name", "No source name available")
         country = article.get("country", "No title available")
         Url=article.get("url", "No url available")
         description = article.get("description", "No description available")
         category = article.get("category", "No category available")
         language = article.get("language", "No language available")
         sources_list.append({"source_name": source_name, "country": country, "description": description, "url": Url, "category": category, "language": language })
         breiflist.append({"source_name": source_name})
         if counter==16:
                 break
    return breiflist,sources_list

def handle_params(data):
    '''Function to handle parameters and type of requested data'''
    thread_data.client_data={} #dict for every client
    tp='' #type of requested data
    if data[-2]==115:
        url=sources
        reqby='sources'
    else:
        url=haedline
        reqby='haedline'
    
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
    return prams,url,tp,reqby

def handle_client(conn,adrr):
    '''a function to handle the client request'''
    try:
        while True:
            data = conn.recv(1024)
<<<<<<< HEAD
            # to determine wither its headline request or sources
            if data[-2]==115: # the number is for s in ascii table
                if url in haedline:
                    thread_data.client_data={}
                    torequest=''
                    recdata=''


                url=sources

            elif data[-2]==104: # the number is for h in ascii table
                if url in sources:
                    thread_data.client_data={}  
                    torequest=''
                    recdata=''

                url=haedline 
            

=======
>>>>>>> 84c3c393654106b22f116268bf45bcd90b366370
            if not data:
                print(client_name,'disconnected with address',addr)
                break
            if data.decode()=='quit':
                print(client_name,'disconnected with address',addr)
                conn.close()
                quit()

            prams,url,tp,reqby=handle_params(data)

            if prams=={}: #that means client chose all sources
                print(client_name,"requested all sources")
                filename=client_name+'-'+'all-sources'+'-'+'A19.json'
                
            else:    
                print(client_name,'request by',reqby,'with',tp)
                filename=client_name+'-'+reqby+'-'+tp+'-'+'A19.json'
            breiflist,article_details=handle_requestes(url=url,filename=filename,prams=prams) #request data from newsapi.org 
            results=json.dumps(breiflist)
            if breiflist[0]=='There is no result for this article':
                conn.sendall(results.encode()) #send a massege to client that there is no result and continue
                continue
           
            conn.sendall(results.encode()) #send article details to client
            choise=conn.recv(1024).decode() #receive user's next choise
            conn.sendall(json.dumps(article_details[int(choise)-1]).encode()) #send article details to client) 
                    
    except Exception as e:
        #if there was any error during the procces or the client disconnected unexpectedly
        print(client_name,'disconnected with address',addr)
        


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