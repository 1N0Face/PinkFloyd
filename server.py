import data
import socket
import hashlib        
LISTEN_PORT = 9091
SERVER_IP = ''
WELCOME = "Welcome Pink Floyd fan, im Pink-server, nice to meet you!"
LOGIN_ERROR = "Invalid password!"
QUIT_OPT = "Bye Bye!"
ELSE_OPT = "Unknown command"
NO_INPUT = "Error: not found!"
PASSWORD = '1b90c0c0a52a5ad7643e34c95a79b7af'
RECV_SIZE = 1024*8
def loginCheck(toCheck):
    '''
    This function checks if password is correct by hash
    Input: the user's input (str)
    Output: 1 if the password is correct 0 if not
    '''
    if(str(PASSWORD) == str(toCheck.hexdigest())):
        return 1
    else:
        return 0

def commandAnalyze(msg):
    '''
    This function takes the users input and analyze it according to the protocol
    Input: msg
    Output: none
    '''
    name = ""
    totalAlbums, dataDict = data.createDict() # creates the dict
    if msg.find('&') != -1:
        option = msg[:msg.find('&')] # if he chose option 2-7 the input was: <option>&<name> so it takes only the chosen option
        name = msg[msg.find('&')+1:] #takes the name: <option>&<name of someting>
    else:
        option = msg # if the chosen option was 1 or 8 the input was: <option>
    if not name and option != '9' and option != '1': #checks if the name is null and the option are not 1 or 9
        return -1,NO_INPUT
    if option == '1':
        return 1,data.getAlbums(dataDict,totalAlbums)# removes the # in each index of the albums list and makes it string
    elif option == '2':
        return 2,data.getSongsInAlbum(dataDict,name, totalAlbums)
    elif option == '3':
        return 3,data.getSongLength(dataDict,name, totalAlbums)
    elif option == '4':
        return 4,data.getSongWords(dataDict,name, totalAlbums)
    elif option == '5':
        return 5,data.getAlbumBySong(dataDict,name, totalAlbums)
    elif option == '6':
        return 6,data.songSearchByWord(dataDict,name, totalAlbums)
    elif option == '7':
        return 7,data.songSearchByLyrics(dataDict,name, totalAlbums)
    elif option == '8':
        return 8,data.GethAlbumsYear(dataDict,name, totalAlbums)
    elif option == '9' and msg.find('&') == -1: #if the option is '9' and it wasnt in the format: 9&<name>
        return 0,QUIT_OPT
    else:
        return 9,ELSE_OPT

def serverSide():
    flag = 1 #sets the flag as a true
    while (flag != 0): #the flag is instead of checking if the user`s choice is to quit
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
                listen_socket.bind(('',LISTEN_PORT)) 
                listen_socket.listen(1)
                client_soc, client_adress = listen_socket.accept()
                passInput = hashlib.md5(client_soc.recv(1024)) # hashlib.md5 to check the passInput
                flag = loginCheck(passInput)
                if flag == 1:
                    client_soc.sendall(WELCOME.encode()) #sends the welcome msg to the user
                else:
                    client_soc.sendall(LOGIN_ERROR.encode()) #sends an error msg if the password is wrong
                while (flag != 0):
                    client_msg = client_soc.recv(RECV_SIZE).decode() # the users choice to the menu
                    print("New user command:\n" + client_msg) #prints the choice 
                    flag,msg = commandAnalyze(client_msg) # the flag is checking the input, the msg is according to the users choice
                    client_soc.sendall(msg.encode()) #sends the result according to users choice
        except (ConnectionResetError, EOFError, ConnectionAbortedError) as e:
            print("Error:", e)

if __name__ == "__main__":
    serverSide()