# making change for commit to trigger build
import json
import ethereum
import external
import httpserver_80
import httpserver_8000
import mail
#import raw_sockets
import shell
import socks
import tcp
import udp
import whoami

json_file = 'resources/service_restrictions.json'

def read_file(filename):
  with open(json_file, 'r') as fp:
    d = json.load(fp)
  return d

def get_entry(d, uuid):
  for entry in d[1:]:
    if entry['UUID'] == uuid:
      return entry
  return None

def print_details(entry):
  print('Running scripts for ', entry['Service Name'])
  print('Find the ToS at ', entry['ToS Link'])
  print('Prohibited Uses:')
  if len(entry['Prohibited Uses']) == 0:
    print('None\n')
  else:
    print(entry['Prohibited Uses'] + '\n')

def run_scripts(entry):
  if entry['TCP'] != 'N':
    print('Checking TCP...')
    try:
      rv = tcp.main()
      print('TCP test returned ' + str(rv))
    except:
      print('ERROR during TCP test')
  else:
    print('Skipping TCP')
  # UDP
  if entry['UDP'] != 'N':
    print('Checking UDP...')
    try:
      rv = udp.main()
      print('UDP test returned ' + str(rv))
    except:
      print('ERROR during UDP test')
  else:
    print('Skipping UDP')
  # Raw Sockets
  if entry['Raw Sockets/Forge Packets'] != 'N':
    print('Checking Raw Sockets/Forging Packets...')
    try:
      raw_sockets.main() 
    except:
      print('ERROR during Raw Sockets/Forge Packets test')
  else:
    print('Skipping Raw Sockets/Forging Packets')
  # Shell and whoami/id
  if entry['Output of `whoami`/`id`'] != 'N':
    print('Checking access to shell...')
    try:
      rv = shell.main() 
      print('Shell access test returned ' + str(rv))
    except:
      print('ERROR during shell access test')
    print('Checking output of `whoami`/`id`...')
    try:
      who, id_out = whoami.main() 
      print('`whoami` result: {} `id` result: {}'.format(who, id_out))
    except:
      print('ERROR during `whoami`/`id` test')
  else:
    print('Skipping test for access to shell')
  # Externally Reachable
  if entry['Externally Reachable'] != 'N':
    print('Checking if externally reachable...')
    try:
      rv = external.main() 
      print('External Reachability test returned ' + str(rv))
    except:
      print('ERROR during external reachability test')
  else:
    print('Skipping check for external reachability')
  # Host http server
  if entry['Host a Server'] != 'N':
    print('Checking ability to host a server on port 80...')
    # call script from module
    try:
      rv = httpserver_80.main()
      print('Http server on port 80 test returned ' + str(rv))
    except:
      print('ERROR during attempt to host http server on port 80')
    print('Checking ability to host a server on port 8000...')
    # call script from module
    try:
      rv = httpserver_8000.main()
      print('Http server on port 8000 test returned ' + str(rv))
    except:
      print('ERROR during attempt to host http server on port 8000')
  else:
    print('Skipping test to host a server')
  if entry['Send Email'] != 'N':
    print('Checking if email can be sent...')
    # call script from module
    try:
      rv = mail.main()
      print('Mail test returned ' + str(rv))
    except:
      print('ERROR during mail test')
  else:
    print('Skipping test to see if email can be sent')
  # Seed bittorrent file
  if entry['Seed Bittorrent File'] != 'N' and False: # DEBUG: skip this test until bittorrent seeding is working
    print('Checking if torrent can be seeded...')
    # call script from module
    try:
      rv = seed.main()
      print('Bittorrent seed test returned ' + str(rv))
    except:
      print('ERROR during bittorrent seed test')
  else:
    print('Skipping test to see if torrent can be seeded')
  # Bitcoin network connection test
  if entry['Reach BTC P2P Network'] != 'N' and False: # DEBUG: skipping test until code is written for it
    print('Attempting to reach BTC P2P network...')
    # call script from module
    try:
      #rv = 
      print('BTC connection test returned ' + str(rv))
    except:
      print('ERROR during BTC connection test')
  else:
    print('Skipping test to reach BTC P2P network')
  # Ethereum network connection test
  if entry['Reach ETH P2P Network'] != 'N':
    print('Attempting to reach ETH P2P network...')
    # call script from module
    try:
      rv = ethereum.main()
      print('Ethereum connection test returned ' + str(rv))
    except:
      print('ERROR during Ethereum connection test')
  else:
    print('Skipping test to reach ETH P2P network')
  # SOCKS proxy test
  if entry['Run SOCKS Proxy'] != 'N':
    print('Attempting to run SOCKS Proxy...')
    # call script from module
    try:
      rv = socks.main()
      print('SOCKS Proxy test returned ' + str(rv))
    except:
      print('ERROR during SOCKS Proxy test')
  else:
    print('Skipping test to run SOCKS Proxy')
  # Scanning/scraping. TODO: Are we planning on making a script for this catagory??
  if entry['Scanning'] != 'N':
    pass


def interactive_select_scripts(d):
  uuid = input('Input the UUID of the service being tested: ')
  try:
    int(uuid)
  except:
    print('Expected integer input corresponding to the UUID of the service \
    being tested. Refer to the Cyclid Google Sheet for a mapping of UUIDs to \
    service')
    return
  entry = get_entry(d, uuid)
  if entry == None:
    print('Failed to find entry for the entered UUID. Refer to the Cyclid \
    Google Sheet for a mapping of UUIDs to service.')
    return

  run_scripts(entry)


def from_file_select_scripts(d, filename):
  with open(filename, 'r') as fp:
    uuid = fp.readline().strip('\n')
  try:
    int(uuid)
  except:
    print('Expected integer input corresponding to the UUID of the service \
    being tested. Refer to the Cyclid Google Sheet for a mapping of UUIDs to \
    service')
    return
  entry = get_entry(d, uuid)
  if entry == None:
    print('Failed to find entry for the entered UUID. Refer to the Cyclid \
    Google Sheet for a mapping of UUIDs to service.')
    return

  print_details(entry)
  run_scripts(entry)


d = read_file(json_file)
from_file_select_scripts(d, 'uuid.txt')
