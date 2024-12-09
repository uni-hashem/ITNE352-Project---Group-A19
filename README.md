# Multithreaded News Client/Server Information System
___
## Project Description

A client-server system that exchanges information about current news where the user requests for news headlines and sources from the server through filters such as keyboards, category, and country. The server then fetches the data from the API and send the requested information to the client.
___
## Semester

First semester of 2024/2025.
___
## Group

* Group Number: A19

* Course Code: ITNE352/ITCE320

* Section Number: 01

* Students Names: HASHEM SAEED ABDULLA ALKHANAIZI, ABDULLAH MOHAMMAD ISHTIAQ AFRIDI

* Students IDs: 202203100, 202200767
___
## Table of Contents

1- [Requirements](#requirements)

2- [How to](#how-to)

3- [The Scripts](#the-scripts)

4- [Additional Concepts](#additional-concepts)

5- [Acknowledgments](aAcknowledgments)

6- [Conclusion](#conclusion)
___
## Requirements

1- Install the latest verion of Python from Python's official website, which is: https://www.python.org/downloads/

2- Install the required packages to run the project by running the following command in command prompt:

pip install requests 

3- Clone the repository from GitHub and run it on Virtual Studio code  
___
## How to

1- Open two terminal windows, one for the client and one for the server

2- Navigate to the directory where the client and sierver files are in terminal

3- Start the server side first to make it ready to receive requests by running the script:

python server.py 

4- Start the client side next and connect to the already running server using the script:

python client.py

5- The client side of the terminal window would ask you to input some information and choose from the menu, interact with it and retrieve the data.
___
## The Scripts

---
## Additional concepts

1- Threading.local:

2- Multithreading: The server script uses the threading module to handle several client connections at once. The server may handle requests from several clients simultaneously thanks to this multithreading technique. By giving every client connection its own thread. Using multithreading. the server increases it's efficiency in sending the requested data to clients 

3- Object-Oriented Programming:
___
## Acknowledgments

* News provided and used in this project was taken from NewsAPI

* The usage of GitHub made sharing of the project very easy

* A big thanks to Dr. Mohammad A. Almeer for teaching us and guiding us on the project and throughtout the course as a whole.
___
## Conclusion

---
