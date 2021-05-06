import subprocess as subp
import csv
import re

proc_list = list()
thread_count = 0

data_file = open('data.csv', 'r')

for count, row in enumerate(csv.reader(data_file, delimiter=',')):
    if count != 0:
        name = re.sub(r'"', '', row[12])
        name = re.sub(r'\\', '', name)
        song_id = row[6]
        artist_arr = row[1][2:len(row[1]) - 2]
        artist_names = list()
        if "," in artist_arr:
            artist_arr = re.split(r"['|\"], ['|\"]", artist_arr)
            for artist in artist_arr:
                artist_names.append(artist)
        else:
            artist_names.append(artist_arr)
            
        if thread_count > 49:
            for proc in proc_list:
                out, err = proc.communicate()
                text = out.decode()
                if len(text) > 0 :
                    print(text.strip())
            proc_list = list()
            thread_count = 0
            
        proc_list.append(subp.Popen(["python", "musicbrainzgetter.py", song_id, artist_names[0], name], stdout=subp.PIPE, stdin=subp.PIPE))
        thread_count +=1

for proc in proc_list:
    out, err = proc.communicate()
    text = out.decode()
    if len(text) > 0 :
        print(text.strip())
