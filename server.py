
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
    
def response(selected_option, user_input,filename):
    try:
        # Retrieve data once when the server starts
        with open(filename, 'r') as ofile:
            info = json.load(ofile)

        selected_info = "."
        for news in info:
            # Process flight data based on the selected option
            if selected_option == '1':
                if news['flight_status'] == 'landed':
                    selected_info += f"***Here are your required information about arrived flights ✅***\n"
                    selected_info += f"\n"  
                    selected_info += f"Flight IATA code: {news['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {news['departure']['airport']}\n"
                    selected_info += f"Arrival Time: {news['arrival']['estimated']}\n"
                    selected_info += f"Arrival Terminal: {news['arrival']['terminal']}\n"
                    selected_info += f"Arrival Gate: {news['arrival']['gate']}\n"
                    selected_info += "\n"
                    selected_info += "=====================================\n"
            elif selected_option == '2':
                if news['arrival']['delay'] is not None:
                    selected_info += f"***Here are your required information about delayed flights ⏱️***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {news['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {news['departure']['airport']}\n"
                    selected_info += f"Original departure Time: {news['departure']['actual']}\n"
                    selected_info += f"Estimated Arrival Time: {news['arrival']['estimated']}\n"
                    selected_info += f"Arrival terminal: {news['departure']['terminal']}\n"
                    selected_info += f"delay : {news['arrival']['delay']}\n"
                    selected_info += f"Arrival Gate: {news['arrival']['gate']}\n"
                    selected_info += "\n"
                    selected_info += "=====================================\n"
            elif selected_option == '3':
                if news['departure']['iata'] == user_input:
                    selected_info += f"***Required information about specific airport/city 👇***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {news['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {news['departure']['airport']}\n"
                    selected_info += f"Original departure Time: {news['departure']['actual']}\n"
                    selected_info += f"Estimated Arrival Time: {news['arrival']['estimated']}\n"
                    selected_info += f"Arrival Gate: {news['arrival']['gate']}\n"
                    selected_info += f"Departure Gate: {news['departure']['gate']}\n"
                    selected_info += f"flight_status: {news['flight_status']}\n"
                    selected_info += "\n"
                    selected_info += "=====================================\n"
            elif selected_option == '4':
                if news['flight']['iata'] == user_input:
                    selected_info += f"***Here are your required information about this flight 📅***\n"
                    selected_info += f"\n"
                    selected_info += f"Flight IATA code: {news['flight']['iata']}\n"
                    selected_info += f"Departure Airport: {news['departure']['airport']}\n"
                    selected_info += f"Departure Gate: {news['departure']['gate']}\n"
                    selected_info += f"Departure terminal: {news['departure']['terminal']}\n"
                    selected_info += f"Arrival airport: {news['arrival']['airport']}\n"
                    selected_info += f"Arrival Gate: {news['arrival']['gate']}\n"
                    selected_info += f"Arrival terminal: {news['arrival']['terminal']}\n"
                    selected_info += f"flight_status: {news['flight_status']}\n"
                    selected_info += f"scheduled Departure time: {news['departure']['scheduled']}\n"
                    selected_info += f"scheduled arrival time: {news['arrival']['scheduled']}\n"
                    selected_info += "=====================================\n"
    except FileNotFoundError:
        selected_info = "Error: File not found."
    except json.JSONDecodeError:
        selected_info = "Error: Unable to decode JSON file."
    except Exception as e:
        selected_info = f"An unexpected error occurred: {str(e)}"
        
    return selected_info


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
                data = response.json()
                with open('aa.json', "w") as file:
                     json.dump(data, file, indent=4)
                     print("[SUCCESS] Data saved to 'posts.json'")
                article_details = []
                if url==haedline:
                # iterate over the articles and print their details
                   

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
                            print(formatted_date)
                            article_details.append({"source_name": source_name, "title": title, "author": author,'url': url, "description": description, "published At":formatted_date })
                            breiflist=[{"title": article_details["title"], "author": a["author"], "published-day": a["published-day"], "published-time": a["published-time"]}for a in article]
                            results=json.dumps(breiflist)
                            conn.sendall(results.encode())
                    else:
                        print("[ERROR] No article data found")
                        conn.sendall(b'No articles found')
                elif url==sources:
                     for article in data.get("articles", []):
                        source_name = article.get("source", {}).get("name", "No source name available")
                        title = article.get("title", "No title available")
                        author = article.get("author", "No author available")

                        article_details.append({"source_name": source_name, "title": title, "author": author })

               
                nameoffile=client_name+' '+torequest+' '+recdata+' '+'A19'
                nameoffile=re.sub("\s+", "_",nameoffile)
                
               
            else:
                print("[ERROR] Status Code:",response.status_code)
            


            
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