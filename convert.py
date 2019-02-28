import json

test_map = {
    'TCP': ['tcp'],
    'UDP': ['udp'],
    'Raw Sockets/Forge Packets': ['raw_sockets'],
    'Output of `whoami`/`id`': ['whoami'],
    'Externally Reachable': ('external',),
    'Host a Server': ['httpserver_80', 'httpserver_8000'],
    'Send Email': ['mail'],
    'Seed Bittorrent File': ['seed'],
    'Reach BTC P2P Network': ['bitcoin'],
    'Reach ETH P2P Network': ['ethereum'],
    'Run SOCKS Proxy': ['socks'],
}


attr_map = {
    "UUID": "uuid",
    "Service Name": "name",
    "Can Use": "can_use",
    "ToS Link": "tos",
    "Type": "type",
    "Prohibited Uses": "prohibited_uses",
    "Comment": "comment",
}


with open('services.json', 'r') as f:
    services = json.load(f)[1:]

out_services = []

for service in services:
    if service['Can Use'].upper() == 'Y':
        new_service = {}
        for old_name, new_name in attr_map.items():
            new_service[new_name] = service[old_name]
        new_service['tests'] = []
        
        for old_test, new_tests in test_map.items():
            if service[old_test].upper() == 'Y' or service[old_test].strip() == '':
                new_service['tests'] += new_tests

        out_services.append(new_service)


with open('new_services.json', 'w') as f:
    json.dump(out_services, f)

