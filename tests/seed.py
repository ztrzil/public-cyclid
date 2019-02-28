import sys
import time
import libtorrent as lt

#Create torrent
fs = lt.file_storage()
lt.add_files(fs, "./random.txt")
t = lt.create_torrent(fs)
t.add_tracker("udp://tracker.openbittorrent.com:80/announce", 0)
t.set_creator('libtorrent %s' % lt.version)
t.set_comment("Random bytes")
tracker_list = ['udp://public.popcorn-tracker.org:6969/announce',

'http://182.176.139.129:6969/announce',
 
'http://5.79.83.193:2710/announce',
 
'http://91.218.230.81:6969/announce',

'udp://tracker.ilibr.org:80/announce',
 
'http://atrack.pow7.com/announce',
 
'http://bt.henbt.com:2710/announce',
 
'http://mgtracker.org:2710/announce',
 
'http://mgtracker.org:6969/announce',
 
'http://open.touki.ru/announce.php',
 
'http://p4p.arenabg.ch:1337/announce',
 
'http://pow7.com:80/announce',
 
'http://retracker.krs-ix.ru:80/announce',
 
'http://secure.pow7.com/announce',
 
'http://t1.pow7.com/announce',
 
'http://t2.pow7.com/announce',
 
'http://thetracker.org:80/announce',

'udp://tracker.coppersurfer.tk:6969/announce',

'udp://tracker.open-internet.nl:6969/announce',

'udp://tracker.leechers-paradise.org:6969/announce',

'udp://tracker.internetwarriors.net:1337/announce',

'udp://tracker.opentrackr.org:1337/announce',

'udp://9.rarbg.to:2710/announce',

'udp://exodus.desync.com:6969/announce',

'udp://explodie.org:6969/announce',

'udp://tracker.tiny-vps.com:6969/announce',

'udp://thetracker.org:80/announce',

'udp://ipv4.tracker.harry.lu:80/announce',

'udp://tracker1.wasabii.com.tw:6969/announce',

'udp://tracker.torrent.eu.org:451/announce,'

'udp://tracker.port443.xyz:6969/announce',

'udp://tracker.dler.org:6969/announce',

'udp://open.stealth.si:80/announce',

'udp://open.demonii.si:1337/announce',

'udp://denis.stalker.upeer.me:6969/announce',

'udp://bt.xxx-tracker.com:2710/announce',

'http://open.acgnxtracker.com:80/announce'
]

for tracker in tracker_list:
    t.add_tracker(tracker, 0)

lt.set_piece_hashes(t, ".")
torrent = t.generate()    
f = open("mytorrent.torrent", "wb")
f.write(lt.bencode(torrent))
f.close()

#Seed torrent
ses = lt.session()
ses.listen_on(6881, 6891)
h = ses.add_torrent({'ti': lt.torrent_info('mytorrent.torrent'), 'save_path': '.', 'seed_mode': True}) 
print ("Total size: " + str(h.status().total_wanted))
print ("Name: " + h.name())
while True:
    s = h.status()
    state_str = ['queued', 'checking', 'downloading metadata', \
      'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']

    print('\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s' % \
      (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, s.num_peers, state_str[s.state]))
    sys.stdout.flush()

    time.sleep(1)