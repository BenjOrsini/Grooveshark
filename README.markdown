#Grooveshark Public API V3 Wrapper

This is a pretty simple wrapper for the grooveshark public api. To use it, you'll need an api key and secret pair. You can request this [on their developer site](http://developers.grooveshark.com/api).  


To get started, initialize a session
```
import grooveshark  
grooveshark.init('KEY', 'SECRET')  
```

You can also fill in the KEY and SECRET variables within the script. The initialization would then be :

```
import grooveshark  
grooveshark.init()  
```
  

You can now use the api_call method to make requests. Required parameters are the api method name, and a dictionary of parameters required for that method. For example:  

```
grooveshark.api_call('getSongSearchResults', {'query': 'la vie en rose', 'country': 'USA'})
```  

To make api calls that require user authentication, call the authenticate_user method once:  

```
grooveshark.authenticate_user(username, password)
```  

Because knowing each API method names is tiring, you can use one of those shortcuts methods :
+ get_song_id_from_tinysong_base62
+ get_song_url_from_tinysong_base62
+ create_playlist
+ set_playlist_songs
+ get_playlist
+ get_song_search_results
+ get_stream_key_stream_server

Get stream URL, artist, and title of the most popular song based on query:

```
url, artist, title = grooveshark.get_stream_from_query('kanye west')
```

For more information on the grooveshark API methods and their required parameters, visit the [grooveshark documentation](http://developers.grooveshark.com/docs/public_api/v3/)

#Tinysong API Wrapper

This is a pretty simple wrapper for the tinysong api. To use it, you'll need an api key. You can request this [on their site](http://www.tinysong.com/api).


To get started, initialize the wrapper
```
import tinysong  
tinysong.init('KEY')  
```

You can now use the `api_call` method to search for songs. Required parameter is the query. Optional parameters are the method (`a` `b` or `s`) and the format. For example:  
```
tinysong.api_call('life in the fast lane', method='b', format='json')
```
outputs
```
>> {'ArtistName': 'Eagles', 'SongID': 13856727, 'AlbumID': 1184928, 'Url': 'http://tinysong.com/nwgo', 'AlbumName': 'The Very Best of the Eagles', 'ArtistID': 686, 'SongName': 'Life in the Fast Lane'}
```  
