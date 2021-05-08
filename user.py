import socket
SERVER_IP = '127.0.0.1'
SERVER_PORT = 9091
LOGIN_MSG = "Please enter the password:"
LOGIN_ERROR = "Invalid password!"
RECV_SIZE = 1024*8
def printMenu():
    '''
    This function prints the menu according to the project protocol
    Input: none
    Output: none
    '''
    print("-----------------\nchoose an option:")
    print("1 - Albums list")
    print("2 - Songs list in the Album")
    print("3 - Song`s length")
    print("4 - Song`s lyrics")
    print("5 - Song`s album")
    print("6 - Search a song by name")
    print("7 - Seacrh a song by lyrics")
    print("8 - Album`s year")
    print("9 - Exit")
    print("For option 1 or 9 syntax: <option>")
    print("For option 2-8 syntax: <option>&<name>")

def selectOption():
    answer = input("Your choice:") #gets the input
    print('*' * 20)
    return answer # return it

def printFormat(ans):
    print(ans.decode())# prints the answer from the server
    print('*' * 20)

def takePass():
    try: 
        ans = input(LOGIN_MSG).encode() #gets the input of the user and encodes it
        return ans
    except KeyboardInterrupt: #if the user types Ctrl + C in cmd it wont crash
        print("KeyboardInterrupt - Error")

def socketprog():
        while (1):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.connect((SERVER_IP, SERVER_PORT))
                    sock.sendall(takePass())
                    startMsg = sock.recv(RECV_SIZE).decode()#prints the users welcome msg
                    print(startMsg) #prints the users welcome msg
                    if(startMsg == LOGIN_ERROR):
                        break
                    else:
                        printMenu()
                    while (1):
                        try:
                            #printMenu() -> can be added if you want to always display the menu (i prefer to not)
                            option = selectOption()
                            sock.sendall(option.encode()) #sends to the server the user`s input
                            answer = sock.recv(RECV_SIZE) # gets the output according to the protocol
                            printFormat(answer)
                            if option == '9':  #if user`s option is to Quit
                                return 0 #stop the program
                        except KeyboardInterrupt as r: #if the user types Ctrl + C in cmd it wont crash
                            print("KeyboardInterrupt - Error", r) 
            except (ConnectionResetError, EOFError, ConnectionAbortedError,Exception) as e:
                print("Error:", e)
                return 0
if __name__ == "__main__":
        socketprog()