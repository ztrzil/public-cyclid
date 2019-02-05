import json
import ethereum
import external
import httpserver_80
import httpserver_8000
import mail
import raw_sockets
import shell
import socks
import tcp
import udp
import whoami

json_file = 'resources/service_restrictions.json'
scripts = ['tcp.py', 'udp.py', 'raw_sockets.py', 'shell.py', 'external.py',
'httpserver_80.py', 'httpserver_8000.py', 'mail.py', '', '', '', 'socks.py',
'']

def read_file(filename):
  with open(json_file, 'r') as fp:
    d = json.load(fp)
  return d

def get_entry(d, uuid):
  for entry in d[1:]:
    if entry['UUID'] == uuid:
      print(entry)
      return entry
  return None

def run_scripts(entry):
  if entry['TCP'] != 'N':
    print('Checking TCP...')
    rv = tcp.main()
    print('TCP test returned ' + str(rv))
  else:
    print('Skipping TCP')
  if entry['UDP'] != 'N':
    print('Checking UDP...')
    rv = udp.main()
    print('UDP test returned ' + str(rv))
  else:
    print('Skipping UDP')
  if entry['Raw Sockets/Forge Packets'] != 'N':
    print('Checking Raw Sockets/Forging Packets...')
    # call script from module
  else:
    print('Skipping Raw Sockets/Forging Packets')
  if entry['Output of `whoami`/`id`'] != 'N':
    print('Checking access to shell...')
    # call script from module
    print('Checking output of `whoami`/`id`...')
    # call script from module
  else:
    print('Skipping test for access to shell')
  if entry['Externally Reachable'] != 'N':
    print('Checking if externally reachable...')
    # call script from module
  else:
    print('Skipping check for external reachability')
  if entry['Host a Server'] != 'N':
    print('Checking ability to host a server on port 80...')
    # call script from module
    print('Checking ability to host a server on port 8000...')
    # call script from module
  else:
    print('Skipping test to host a server')
  if entry['Send Email'] != 'N':
    print('Checking if email can be sent...')
    # call script from module
  else:
    print('Skipping test to see if email can be sent')
  if entry['Seed Bittorrent File'] != 'N':
    print('Checking if torrent can be seeded...')
    # call script from module
  else:
    print('Skipping test to see if torrent can be seeded')
  if entry['Reach BTC P2P Network'] != 'N':
    print('Attempting to reach BTC P2P network...')
    # call script from module
  else:
    print('Skipping test to reach BTC P2P network')
  if entry['Reach ETH P2P Network'] != 'N':
    print('Attempting to reach ETH P2P network...')
    # call script from module
  else:
    print('Skipping test to reach ETH P2P network')
  if entry['Run SOCKS Proxy'] != 'N':
    print('Attempting to run SOCKS Proxy...')
    # call script from module
  else:
    print('Skipping test to run SOCKS Proxy')
    # call script from module
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

  run_scripts(entry)



d = read_file(json_file)
from_file_select_scripts(d, 'uuid.txt')
