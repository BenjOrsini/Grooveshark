import argparse
import csv
import random
import sys
import re
from grooveshark import Grooveshark

tinysong_pattern = re.compile('tinysong.com/(.+)')

def is_url_valid_tinyurl(url):
    regexp_result = tinysong_pattern.search(url)
    return regexp_result != None

def get_tinysong_id_from_url(url):
    return tinysong_pattern.search(url).group(1)



def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="Grooveshark v3 API key")
    parser.add_argument("secret", help="Grooveshark v3 API secret")
    parser.add_argument("login", help="Grooveshark account username")
    parser.add_argument("password", help="Grooveshark account password")
    parser.add_argument("file", help="Input CSV file")
    parser.add_argument("column", help="Column index to find songs (starts at 0)", )
    parser.add_argument("delimiter", help="CSV delimiter character", )
    parser.add_argument("quotechar", help="CSV quotechar character", )
    parser.add_argument("playlist", help="Name of the playlist to create", )
    args = parser.parse_args()

    input_file = args.file
    column_index = int(args.column)
    key = args.key
    secret = args.secret
    login = args.login
    password = args.password
    playlist = args.playlist
    delimiter = args.delimiter
    quotechar = args.quotechar

    urls_ok = []
    urls_ko = []

    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)


        for row in reader:
            url = row[column_index]
            if is_url_valid_tinyurl(url):
                print('.',end="",flush=True)
                urls_ok.append(url)
            else:
                print('X',end="",flush=True)
                urls_ko.append(url)

        print('\n')
        print('Total urls : ' + str(len(urls_ko) + len(urls_ok)))
        print('Urls ok : ' + str(len(urls_ok)))
        print('Urls ko : ' + str(len(urls_ko)))
        print(str(urls_ko))


    shouldContinue = input("Add these " + str(len(urls_ok)) + " songs ? (y/n) : ")

    if(shouldContinue == 'y'):
        print('Connecting to grooveshark.')
        g = Grooveshark(key, secret)

        song_ids_to_add = []

        for url in urls_ok:
            base62 = get_tinysong_id_from_url(url)
            ws_result = g.get_song_id_from_tinysong_base62(base62)
            song_id = ws_result['result']['songID']
            song_ids_to_add.append(song_id)

        print('Randomizing songs.')
        random.shuffle(song_ids_to_add)
        print(song_ids_to_add)

        print('Authenticating user.')
        g.authenticate_user(login, password)

        ws_result = g.get_user_playlists()

        playlists_with_same_name = []
        for pl in ws_result['result']['playlists']:
            if pl['PlaylistName'] == playlist:
                playlists_with_same_name.append(pl['PlaylistID'])

        nb_playlists_with_same_name = len(playlists_with_same_name)

        if nb_playlists_with_same_name > 0:
            choice = input(str(nb_playlists_with_same_name) + " playlist(s) found with the same name. Stop (s) ? Erase them (e) ? Create a new one (c) ?")
            if choice == 'e':
                for playlist_id in playlists_with_same_name:
                    print('Deleting playlist ' + str(playlist_id))
                    g.delete_playlist(playlist_id)
            elif choice != 'c':
                print('Abort.')
                sys.exit(1)

        print('Creating playlist.')
        print(g.create_playlist(playlist, song_ids_to_add))


    else:
        print('Abort.')
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])