import hashlib
import hmac
from urllib import request

import simplejson


class Grooveshark:
    API_URL = 'https://api.grooveshark.com/ws3.php?sig='
    ENCODING = 'utf-8'
    COUNTRY = {'ID': 221, 'CC1': 0, 'CC2': 0, 'CC3': 0, 'CC4': 0, 'DMA': 0, 'IPR': 0}

    def __init__(self, key='', secret=''):
        ''' Create session'''
        if key and secret:
            self.key = key
            self.secret = secret
        response = self.api_call('startSession', add_session_id=False)
        if response['result']['success'] == True:
            self.session_id = response['result']['sessionID']

    def signature(self, data):
        secret_bytes = bytes(self.secret, encoding=Grooveshark.ENCODING)
        data_bytes = data.encode(encoding=Grooveshark.ENCODING)
        sig = hmac.new(secret_bytes, data_bytes)
        return sig.hexdigest()

    def user_token(self, username, password):
        hash_pass = hashlib.md5(password.encode(Grooveshark.ENCODING)).hexdigest()
        token = hashlib.md5(str.encode(username.lower() + hash_pass, Grooveshark.ENCODING))
        return token.hexdigest()


    def api_call(self, method, parameters=None, add_session_id=True):
        data = {}
        data['method'] = method
        data['parameters'] = parameters
        data['header'] = {'wsKey': self.key}
        if add_session_id:
            data['header']['sessionID'] = self.session_id

        data_str = simplejson.dumps(data)
        data_bytes = data_str.encode(encoding=Grooveshark.ENCODING)
        sig = self.signature(data_str)
        req = request.Request(Grooveshark.API_URL + sig, data=data_bytes)
        response = request.urlopen(req).read()

        response_json = simplejson.loads(response)

        if 'errors' in response_json:
            raise APIError(simplejson.dumps(response_json['errors']))

        return simplejson.loads(response)


    ############CORE#################

    def add_user_library_songs_ex(self, song_ids):
        return self.api_call('addUserLibrarySongsEx', {'songIDs': song_ids})

    def get_user_library_songs(self, page=1, limit=10):
        return self.api_call('getUserLibrarySongs', {'limit': limit, 'page': page})

    def removeUserLibrarySongs(self, song_ids, album_ids, artist_ids):
        return self.api_call('removeUserLibrarySongs', {'songIDs': song_ids, 'albumIDs': album_ids, 'artistIDs':artist_ids})

    def getUserPlaylistsSubscribed(self):
        return self.api_call('getUserPlaylistsSubscribed')

    def getUserPlaylists(self):
        return self.api_call('getUserPlaylists')

    def delete_playlist(self, playlist_id):
        return self.api_call('deletePlaylist', {'playlistID':playlist_id})

    def getUserPlaylistsByUserID(self):
        return self.api_call('getUserPlaylistsByUserID')

    def authenticate_user(self, username, password):
        if self.session_id == '':
            raise Exception(
                "You need to create a session before you authenticate that session with a username and password")
        else:
            token = self.user_token(username, password)
            response = self.api_call('authenticateUser', {'username': username.lower(), 'token': token})
            return response


    def get_song_id_from_tinysong_base62(self, base62):
        '''
        :param base62: a base62 identifier fetched from http://www.tinysong.com/
        :return: a response with the song id
        '''
        result = self.api_call('getSongIDFromTinysongBase62', {'base62': base62})
        return result


    def get_song_url_from_tinysong_base62(self, base62):
        '''
        :param base62: a base62 identifier fetched from http://www.tinysong.com/
        :return: a response with the song url
        '''
        result = self.api_call('getSongURLFromTinysongBase62', {'base62': base62})
        return result


    def create_playlist(self, name, song_ids):
        return self.api_call('createPlaylist', {'name': name, 'songIDs': song_ids})


    def set_playlist_songs(self, playlist_id, song_ids):
        return self.api_call('setPlaylistSongs', {'playlistID': playlist_id, 'songIDs': song_ids})


    def get_playlist(self, playlist_id, limit=10):
        return self.api_call('getPlaylist', {'playlistID': playlist_id, 'limit': limit})

    def get_playlist_info(self, playlist_id):
        return self.api_call('getPlaylistInfo', {'playlistID': playlist_id})

    def get_song_search_results(self, query, limit=10):
        ''' Perform a song search '''
        results = self.api_call('getSongSearchResults',
                                {'query': query, 'country': Grooveshark.COUNTRY, 'limit': limit})
        return results

    def get_stream_key_stream_server(self, songID):
        ''' Get stream URL from songID '''
        results = self.api_call('getStreamKeyStreamServer', {'songID': songID, 'country': Grooveshark.COUNTRY})
        return results

    def get_stream_from_query(self, query):
        ''' Get stream URL of the most popular song from query '''
        results = self.get_song_search_results(query)
        songs = results['result']['songs']
        if len(songs) == 0:
            return None, None, None

        song = songs[0]
        songID = song['SongID']
        artistName = song['ArtistName']
        songName = song['SongName']
        results = self.get_stream_key_stream_server(songID)
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
