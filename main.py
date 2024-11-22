import sys
import json
from bencode import decode_bencode, encode_bencode
from tracker import get_peers_from_tracker
from handshake import perform_handshake
from utils import bytes_to_str

def main():
    command = sys.argv[1]

    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        print(json.dumps(bytes_to_str(decode_bencode(bencoded_value))))

    elif command == "info":
        file_name = sys.argv[2]
        with open(file_name, "r+b") as torrent_file:
            bencoded_content = torrent_file.read()
        
        torrent = decode_bencode(bencoded_content)
        info_bencoded = encode_bencode(torrent[b"info"])
        print("Tracker URL:", torrent[b"announce"].decode())
        print("Length:", torrent[b"info"][b"length"])
        print("Piece Length:", torrent[b"info"][b"piece length"])

    elif command == "peers":
        file_name = sys.argv[2]
        with open(file_name, "r+b") as torrent_file:
            bencoded_content = torrent_file.read()
        
        torrent = decode_bencode(bencoded_content)
        info_bencoded = encode_bencode(torrent[b"info"])
        peers = get_peers_from_tracker(torrent, info_bencoded)
        for peer in peers:
            print(peer)

    elif command == "handshake":
        peer_ip, peer_port = sys.argv[3].split(":")
        file_name = sys.argv[2]
        with open(file_name, "r+b") as torrent_file:
            bencoded_content = torrent_file.read()

        torrent = decode_bencode(bencoded_content)
        info_bencoded = encode_bencode(torrent[b"info"])
        peer_id = perform_handshake(peer_ip, peer_port, info_bencoded)
        print(f"Peer ID: {peer_id}")

    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
