import hashlib
import hmac
from urllib import request

import simplejson


KEY = ''  # fill in with your key
SECRET = ''  # fill in with your secret
API_URL = 'https://api.grooveshark.com/ws3.php?sig='
SESSION_ID = ''
ENCODING = 'utf-8'
country = {'ID': 221, 'CC1': 0, 'CC2': 0, 'CC3': 0, 'CC4': 0, 'DMA': 0, 'IPR': 0}

def signature(data):
    secret_bytes = bytes(SECRET, encoding=ENCODING)
    data_bytes = data.encode(encoding=ENCODING)
    sig = hmac.new(secret_bytes, data_bytes)
    return sig.hexdigest()

def user_token(username, password):
    hash_pass = hashlib.md5(password.encode(ENCODING)).hexdigest()
    token = hashlib.md5(str.encode(username.lower() + hash_pass, ENCODING))
    return token.hexdigest()


def api_call(method, parameters=None):
    data = {}
    data['method'] = method
    data['parameters'] = parameters
    data['header'] = {'wsKey': KEY}
    if method != 'startSession':
        data['header']['sessionID'] = SESSION_ID
    
    data_str = simplejson.dumps(data)
    data_bytes = data_str.encode(encoding=ENCODING)
    sig = signature(data_str)
    req = request.Request(API_URL + sig, data=data_bytes)
    response = request.urlopen(req).read()
    
    return simplejson.loads(response)
    
        
def init(key='', secret=''):
    ''' Create session'''
    if key and secret:
        global KEY
        global SECRET
        KEY = key
        SECRET = secret
    response = api_call('startSession')    
    if response['result']['success'] == True:
        global SESSION_ID
        SESSION_ID = response['result']['sessionID']
    else:
        raise APIError(simplejson.dumps(response['errors']))
        

def authenticate_user(username, password):
    if SESSION_ID == '':
        raise Exception("You need to create a session before you authenticate that session with a username and password")
    else:
        token = user_token(username, password)
        response = api_call('authenticateUser', {'username': username.lower(), 'token': token})
        return response


def get_song_url_from_tinysong_base62(base62):
    '''
    :param base62: a base62 identifier fetched from http://www.tinysong.com/
    :return: a response with the song url
    '''
    results = api_call('getSongURLFromTinysongBase62', {'base62': base62})
    return results


def get_song_search_results(query, limit=10):
    ''' Perform a song search '''
    results = api_call('getSongSearchResults', {'query': query, 'country':country, 'limit': limit})
    return results

def get_stream_key_stream_server(songID):
    ''' Get stream URL from songID '''
    results = api_call('getStreamKeyStreamServer', {'songID': songID, 'country':country})
    return results

def get_stream_from_query(query):
    ''' Get stream URL of the most popular song from query '''
    results = get_song_search_results(query)
    songs = results['result']['songs']
    if len(songs) == 0:
        return None, None, None
    
    song = songs[0]
    songID = song['SongID']
    artistName = song['ArtistName']
    songName = song['SongName']
    results = get_stream_key_stream_server(songID)
    url = results['result']['url']
    return url, artistName, songName

class APIError(Exception):
    
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr("There was a problem with your API request: " + self.message)


# if __name__ == '__main__':
#     init()
#     url, artist, title = get_stream_from_query('kanye west')
#     print url, artist, title
