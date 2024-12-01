import socket,json

# Define server host and port
HOST = 'localhost'  # Server's hostname or IP address
PORT = 12345        # Port used by the server

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientname=input('Enter your name: ')
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
            while True:
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
                    category = input("Enter your category: ")
                    client_socket.sendall((category+'h2').encode())
                elif y==3:
                    country = input("Enter your country: ")
                    client_socket.sendall((country+'h3').encode())
                elif y==4:
                    client_socket.sendall('h4'.encode())
                elif y==5:
                    break
                else:
                        print("Invalid option. Please choose a valid option.")
                recived=client_socket.recv(4000)
                results=json.loads(recived.decode('utf-8'))
                print(results)

        if x==2:
            while True:                
                    print('1 - list all sources by category ')
                    print('2 - list all sources by country ')
                    print('3 - list all sources by languege ')
                    print('4 - list all sources ')
                    print('5 - Back to main menu')
                    y=int(input('choise your option '))
                    if y==1:
                        category = input("Enter your category: ")
                        client_socket.sendall((category+'s1').encode())
                    elif y==2:
                        country = input("Enter your country: ")
                        client_socket.sendall((country+'s2').encode())
                    elif y==3:
                        language = input("Enter your language: ")
                        client_socket.sendall((language+'s3').encode())
                    elif y==4:
                        client_socket.sendall('s4'.encode())
                    elif y==5:
                        break
                    else:
                        print("Invalid option. Please choose a valid option.")
                    recived=client_socket.recv(4000)
                    results=json.loads(recived.decode('utf-8'))
                    print(results)

except ConnectionRefusedError:
    print("Connection to the server failed.")
finally:
    client_socket.close()