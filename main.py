import json
import sys
from textwrap import wrap
import bencodepy
import hashlib
import requests
import urllib.parse
import socket

def decode_bencode(bencoded_value):
    bc = bencodepy.Bencode()
    return bc.decode(bencoded_value)

def encode_bencode(data):
    bc = bencodepy.Bencode()
    return bc.encode(data)

def sha1(to_sha1):
    return hashlib.sha1(to_sha1).hexdigest()

def bytes_to_str(data):
            if isinstance(data, dict):
                return {bytes_to_str(k): bytes_to_str(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [bytes_to_str(i) for i in data]
            elif isinstance(data, bytes):
                return data.decode(errors='replace')
            else:
                return data

def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value = sys.argv[2].encode()

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #


        # Decode the bencoded value and print it as JSON
        print(json.dumps(bytes_to_str(decode_bencode(bencoded_value))))


    elif command == "info":
        file_name = sys.argv[2]
        with open(file_name, "r+b") as torrent_file:
            bencoded_content = torrent_file.read()

        try:
            if not (bencoded_content.startswith(b'd') or bencoded_content.startswith(b'l')):
                raise ValueError("Invalid bencoded data structure.")

            torrent = decode_bencode(bencoded_content)
            info_bencoded= encode_bencode(torrent[b"info"])
            info_sha1 = sha1(info_bencoded)

            # Get the pieces list as 20-byte chunks
            pieces = torrent[b"info"][b"pieces"]
            pieces_list = [pieces[i:i+20] for i in range(0, len(pieces), 20)]
            pieces_list_sha1 = [piece.hex() for piece in pieces_list]

            print("Tracker URL:", torrent[b"announce"].decode())
            print("Length:", torrent[b"info"][b"length"])
            print("Info Hash:", info_sha1)
            print("Piece Length:", torrent[b"info"][b"piece length"])
            print("Piece Hashes:")
            for i in range(0,len(pieces_list_sha1)):
                print(pieces_list[i])

        except Exception as e:
            print("Error decoding bencoded content:", e)


    elif command == "peers":
        file_name = sys.argv[2]
        with open(file_name, "r+b") as torrent_file:
            bencoded_content = torrent_file.read()

        torrent = decode_bencode(bencoded_content)
        info_bencoded = encode_bencode(torrent[b"info"])
        info_hash = hashlib.sha1(info_bencoded).digest()

        tracker_url = torrent[b"announce"].decode()
        # print(f"Tracker URL: {tracker_url}")

        info_hash_encoded = urllib.parse.quote(info_hash)  #  URL encode
    

        # print(f"Raw info_hash: {info_hash}") 
        # print(f"URL-encoded info_hash: {info_hash}")
        # print(f"left: {torrent[b"info"][b"length"]}")

        params = {
            "info_hash": info_hash,
            "peer_id": "00112233445566778899",
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": torrent[b"info"][b"length"],
            "compact": 1
        }

        response = requests.get(tracker_url, params=params)
        # print(response.content)
        # print(f"response url: {response.url}")
        response_dict= decode_bencode(response.content)
        # print(response_dict)



        peers = response_dict.get(b"peers",b"")
        # print("peers: {peers}")

        for i in range( 0 , len(peers) , 6 ):
            ip=".".join(str(b) for b in peers[i:i+4])
            portarray = peers[i+4:i+6]
            port=  int.from_bytes(portarray)
            print( f"{ip}:{port}" )
    
    elif command == "handshake":
        peer_ip , peer_port = sys.argv[3].split(":")
        file_name = sys.argv[2]
        with open( file_name, "r+b" ) as torrent_file:
            bencoded_content = torrent_file.read()

        torrent = decode_bencode(bencoded_content)
        info_bencoded = encode_bencode(torrent[b"info"])
        info_hash = hashlib.sha1(info_bencoded).digest()

        handshake = bytes([19])+b"BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00" + info_hash + b"00112233445566778899"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer_ip, int(peer_port)))
        sock.send(handshake)
        print(f"Peer ID: {sock.recv(68)[48:].hex()}")
        sock.close()
    
    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()




### GAVE UP ###
# def decode_bencode(bencoded_value):
#     # Handling a string (length-prefixed)
#     if bencoded_value[0:1].isdigit():
#         first_colon_index = bencoded_value.find(b":")
#         if first_colon_index == -1:
#             raise ValueError("Invalid encoded value: No colon found.")
#         length = int(bencoded_value[:first_colon_index])
#         return bencoded_value[first_colon_index + 1:first_colon_index + 1 + length]

#     # Handling an integer (i<value>e)
#     elif bencoded_value[0:1] == b"i" and bencoded_value[-1:] == b"e":
#         return int(bencoded_value[1:-1])

#     # Handling a list (l<list content>e)
#     elif bencoded_value[0:1] == b"l" and bencoded_value[-1:] == b"e":
#         bencoded_list_as_string = bencoded_value[1:-1]
#         bencoded_list = []
#         i = 0
#         while i < len(bencoded_list_as_string):
#             char = bencoded_list_as_string[i:i + 1]

#             # For Integer (handled by checking for "i" at the start)
#             if char == b"i":
#                 end_index = bencoded_list_as_string.find(b"e", i)
#                 if end_index == -1:
#                     raise ValueError("Invalid integer format: missing 'e'.")
#                 bencoded_list.append(decode_bencode(bencoded_list_as_string[i:end_index + 1]))
#                 i = end_index + 1

#             # For String (length-prefixed strings)
#             elif char.isdigit():
#                 first_colon_index = bencoded_list_as_string.find(b":", i)
#                 if first_colon_index == -1:
#                     raise ValueError("Invalid string format: missing colon.")
#                 length = int(bencoded_list_as_string[i:first_colon_index])  # Get the length of the string
#                 bencoded_list.append(bencoded_list_as_string[first_colon_index + 1:first_colon_index + 1 + length].decode())  # Extract and decode the string
#                 i = first_colon_index + 1 + length

#             # For List (recursive parsing for nested lists)
#             elif char == b"l":
#                 # We need to handle nested lists correctly by identifying the corresponding closing "e"
#                 nested_list_end = i
#                 balance = 1  # We already found the opening 'l'
#                 while balance > 0:
#                     nested_list_end += 1
#                     if bencoded_list_as_string[nested_list_end:nested_list_end + 1] == b"l":
#                         balance += 1
#                     elif bencoded_list_as_string[nested_list_end:nested_list_end + 1] == b"e":
#                         balance -= 1
                
#                 # Decode the nested list
#                 bencoded_list.append(decode_bencode(bencoded_list_as_string[i:nested_list_end + 1]))
#                 i = nested_list_end + 1

#             # Handle unexpected characters
#             else:
#                 raise ValueError(f"Unexpected character {char} while decoding list.")

#         return bencoded_list

#     # Handle unsupported types
#     else:
#         raise NotImplementedError("Only strings, integers, and lists are supported at the moment")