DATABASE_PATH = "Pink_Floyd_DB.txt"
def getLyrics(song):
    '''
    This function gives the lyrics of the song that is given as an input.
    Input: song name (*Name), str type
    Output the lyrics list
    '''
    count = 0
    flag = 0
    lyrics = list()
    with open(DATABASE_PATH, "r") as dbfile:
        for line in dbfile:
            if song == line[:line.find(':')]: # if it reaches the line with the chosen album
                    flag = 1 
            if flag == 1:
                if (line.find('*') != -1 and count > 0): #its used to not reach the next song
                    break
                else:
                    if (line.find('*') != -1):
                        start = line.replace(":", "", 6)  #The lyrics start in the same line with the song's name after 7 ':' but i leave 1 ':' for the next action...
                        lyrics.append(start[start.find(":")+1:-1]) # the ':' that left helps me to find the start of the lyrics
                    else:
                        if (line.find('#') == -1): # checks if it wont get to the new album line
                            lyrics.append(line[:-1]) # adds the lyrics without the \n
                count +=1
        return lyrics

def createDict():
    '''
    This function creates the dictionary that will help us to get the needed information from
    Input: none
    Output total albums amount (int), the created dictionary (dict)
    The format of the dict:
    d = {'album1': {'name': '', year: '', 'songs': [], 'words': [[each song's words have their own list]], 'length': []},
        {'album2': {'name': '', year: '', 'songs': [], 'words': [[each song's words have their own list]], 'length': []}}
    .......
    The index in the songs list will be the same index in words and in length.
    '''
    pinkFloyd = dict()
    i = 1 # serves as an index for the album key, starts from 1
    with open(DATABASE_PATH, "r") as temp:
        for line in temp:
            if '#' in line: #if the line contains an album name in it
                albumName = line[:line.find(':')] #gets the albumName with # at the start exmp: #The Piper At The Gates Of Dawn
                year = line[line.find(':')+2:-1] #gets the year the album was written in
                album = 'album{}'.format(i) # each album will have a key album1...
                pinkFloyd[album] = {'name': albumName, 'year': year, 'songs': [], 'words': [], 'length': []} #creates the dict for each album[i]
                i += 1 
            elif '*' in line: #if the line contains a song name in it
                songName = line[:line.find(':')] #gets the song name with * at the start exmp: *Lucifer Sam
                pinkFloyd[album].setdefault("words",[]).append(getLyrics(songName)) #we use here this func to do: 'words': [[lyrics1][lyrics2]]...
                temp = line.replace(':','',3) # helps to get each song length
                songLength = temp[temp.find(':')+1:temp.find('::')] #gets the song length
                pinkFloyd[album].setdefault("songs",[]).append(songName) # adds the song name to a list as a value for a "songs" key
                pinkFloyd[album].setdefault("length",[]).append(songLength) # adds the song name to a list as a value for a "length" key
        return i,pinkFloyd

def getAlbums(data, albumCount):
    '''
    This function gives the albums using the dict.
    Input: data(dict), total amount of albums (int)
    Output: the albums(str)
    '''
    ans = []
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i) # its a dict in dict so each dict starts as a value to a album[i] key
        ans.append(data[key1]['name'][1:]) #adds the album name withoud the '#'
    return '\n'.join(ans)

def getSongsInAlbum(data, albumName, albumCount):
    '''
    This function gives the song in the album using the dict.
    Input: data(dict), album name(str), total amount of albums (int)
    Output: the songs in the album (str)
    '''
    ans = []
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i)
        if data[key1]['name'][1:] == albumName: #checks if the dict has the albumName under the key 'name'
            for songName in data[key1]['songs']: #for each song in the songs list
                ans.append(songName[1:])
    checkOutput(ans)
    return '\n'.join(ans)

def getSongLength(data,songName ,albumCount):
    '''
    This function gives the song length using the dict.
    Input: data(dict), album name(str), total amount of albums (int)
    Output: the songs in the album (str)
    '''
    ans = "Error: not found!" # it will change if it will find the song length
    index = 0
    if songName[0] != '*':
        songName = '{}{}'.format('*',songName) #makes the song in the syntax: *Name
    for i in range(1,albumCount): # for album1 key, album2 key, album3 key....
        key1 = 'album{}'.format(i)
        if songName in data[key1]['songs']:
            index = data[key1]['songs'].index(songName)
            ans = data[key1]['length'][index]
    return ans
    
def getSongWords(data,songName,albumCount):
    '''
    This function gives the song's lyrics using the dict.
    Input: data(dict), song name(str), total amount of albums (int)
    Output: the lyrics(str)
    '''
    ans = "Error: not found!"
    index = 0
    songName = '{}{}'.format('*',songName)#makes the song in the syntax: *Name
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i)
        if songName in data[key1]['songs']: # if the song in the list of the songs
            index = data[key1]['songs'].index(songName) # saves the index of from the songs list
            ans = '\n'.join(data[key1]['words'][index]) # using the index here because the index in songs, words, length is the same
    return ans

def getAlbumBySong(data,songName,albumCount):
    '''
    This function gives the album of the song.
    Input: data(dict), song name(str), total amount of albums(int)
    Output: the album(str)
    '''
    ans = "Error: not found!"
    songName = '{}{}'.format('*',songName)
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i)
        if songName in data[key1]['songs']:
            ans = data[key1]['name'][1:] # the key name has the album name
    return ans

def songSearchByWord(data,word,albumCount):
    '''
    This function searches the song if it has the chosen word in the song`s name.
    Input: data(dict), word(str), total amount of albums(int)
    Output: the song or the songs(str)
    '''
    ans = []
    word = word.lower()
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i)
        for song in data[key1]['songs']:
            if word in song.lower(): # if the song name contains the word
                ans.append(song[1:])
    checkOutput(ans)
    return '\n'.join(ans)

def songSearchByLyrics(data,word,albumCount):
    '''
    This function searches the song if it has the chosen word in the lyrics of the song.
    Input: data(dict), word(str), total amount of albums(int)
    Output: the song or the songs(str)
    '''
    word = word.lower()
    j = 0
    ans = []
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i)
        for lyrics in data[key1]['words']: # for each list in words
            for item in lyrics: # for each line in the words
                if word in item.lower(): #if the word is in the line
                    ans.append(data[key1]['songs'][j][1:]) # adds the song name by the index j
            j += 1
            if(j == len(data[key1]['songs'])):
                j = 0 #the index is zero, we want the index for each album
    checkOutput(ans)
    return '\n'.join(list(dict.fromkeys(ans)))

def GethAlbumsYear(data,albumName,albumCount):
    '''
    This function gets the year of the album
    Input: data(dict), album name (str), total amount of albums(int)
    Output: none
    '''
    ans = "Error: not found!"
    for i in range(1,albumCount):
        key1 = 'album{}'.format(i)
        if data[key1]['name'][1:].lower() == albumName.lower(): #if the album is found
            ans = data[key1]['year'] # takes the year value
    return ans

def checkOutput(answer):
    if not answer: #if the answer in none
        answer.append("Error: not found!")

if __name__ == "__main__":
    pass