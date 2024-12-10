import socket,json,signal,sys
def handle_interrupt(signal, frame):
    '''to handle an interrupt signal from the user'''
    print("\nCaught interrupt signal. Closing connection.")
    client_socket.close()
    sys.exit(0)
signal.signal(signal.SIGINT, handle_interrupt)


# Define server host and port
HOST = 'localhost'  # Server's hostname or IP address
PORT = 12345        # Port used by the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientname=input('Enter Your Name: ')
clientname=clientname.strip() # Remove the trailing and leading spaces from the name string
# Check if the client name is empty
if clientname=='':
     clientname = 'Unknown'
try:
    # Connect to the server
    client_socket.connect((HOST, PORT))
    client_socket.sendall(clientname.encode())
    print("Connected to the server.")
    while True:
        print("1 - search by headlines")
        print("2 - List of sources")
        print("3 - Quit")
        x=int(input("choise your option "))
        if x==1:
                print('1 - search for kewyords ')
                print('2 - search by catagory ')
                print('3 - search for country ')
                print('4 - list all new headlines ')
                print('5 - Back to main menue')

                y=int(input("choise your option "))
                if y==1:
                    keyword = input("Enter your keyword: ")
                    client_socket.sendall((keyword+'h1').encode())
                elif y==2:
                    print('Available categories are: business, general, health, science, sports, technology')
                    category = input("Enter your category: ")
                    client_socket.sendall((category+'h2').encode())
                elif y==3:
                    print('Available countries are: au, ca, jp, ae, sa, kr, us, ma')
                    country = input("Enter your country: ")
                    client_socket.sendall((country+'h3').encode())
                elif y==4:
                    client_socket.sendall('h4'.encode())
                elif y==5:
                     continue
                else:
                     print("Invalid option. Please choose a valid option.") 
                     continue
        if x==2: 
                    print('1 - list all sources by category ')
                    print('2 - list all sources by country ')
                    print('3 - list all sources by languege ')
                    print('4 - list all sources ')
                    print('5 - Back to main menu')
                    y=int(input('choise your option '))
                    if y==1:
                        print('Available categories are: business, general, health, science, sports, technology')
                        category = input("Enter your category: ")
                        client_socket.sendall((category+'s1').encode())
                    elif y==2:
                        print('Available countries are: au, ca, jp, ae, sa, kr, us, ma')
                        country = input("Enter your country: ")
                        client_socket.sendall((country+'s2').encode())
                    elif y==3:
                        print('Available languages are: en, ar')
                        language = input("Enter your language: ")
                        client_socket.sendall((language+'s3').encode())
                    elif y==4:
                        client_socket.sendall('s4'.encode())
                    elif y==5:
                         continue
                    else:
                        print("Invalid option. Please choose a valid option.") 
                        continue
        if x==3:
             client_socket.sendall('quit'.encode())
             break
        elif x>3 or x<1: #force the client to chose valid option
             print("Invalid option. Please choose a valid option.")
             continue
        
        recived=client_socket.recv(4000)
        results=json.loads(recived.decode('utf-8'))
        if results[0]=='There is no result for this article':
             print('\n','='*50)
             print(results[0])
             print('='*50,'\n')
             client_socket.sendall
             continue
        c=1
        for headline in results:
            print('\n',c,':')
            print('='*40)
            print(json.dumps(headline,indent=4))
            print('='*40)
            if c==len(results) or c==15:
                break
            c+=1
        print('Enter the number of record you want to view: ')
        choice=int(input())
        while choice<=0 or choice>len(results):
             print('Invalid option. Enter the number of record you want to view: ')
             choice=int(input())
        client_socket.sendall(str(choice).encode())
        recived=client_socket.recv(4000)
        results=json.loads(recived.decode('utf-8'))
        print('\n','='*50)
        print(json.dumps(results,indent=4))
        print('='*50,'\n')
except Exception as e:
     print("connection closed")
finally:
    client_socket.close()