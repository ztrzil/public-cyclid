from coinbits.client import BitcoinClient
from coinbits.protocol.serializers import GetBlocks

connection_success = False

class MyClient(BitcoinClient):
    def message_received(self, message_header, message):
        print ("Got a message:", message_header.command, message)
        super(MyClient, self).message_received(message_header, message)

    def send_message(self, message):
        print ("Sending a message:", str(message))
        super(MyClient, self).send_message(message)

    def connected(self):
        global connection_success
        hash = int('00000000000000000f69e991ee47a3536770f5d452967ec7edeb8d8cb28f9f28', 16)
        gh = GetBlocks([hash])
        self.send_message(gh)
        connection_success = True

    def handle_inv(self, message_header, message):
        print ("Got some inventory:", message)


def main():
  global connection_success

  # Connect to bitcoin network
  try:
    MyClient("bitcoin.sipa.be").loop()
  except Exception as e:
    print(e)

  return connection_success


if __name__ == '__main__':
  main()  
