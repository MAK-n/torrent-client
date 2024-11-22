import requests
import urllib.parse
from bencode import decode_bencode

def get_peers_from_tracker(torrent, info_bencoded, peer_id="00112233445566778899", port=6881):
    info_hash = raw_sha1(info_bencoded)
    tracker_url = torrent[b"announce"].decode()
    
    params = {
        "info_hash": urllib.parse.quote(info_hash),
        "peer_id": peer_id,
        "port": port,
        "uploaded": 0,
        "downloaded": 0,
        "left": torrent[b"info"][b"length"],
        "compact": 1,
    }
    
    response = requests.get(tracker_url, params=params)
    response_dict = decode_bencode(response.content)

    peers = response_dict.get(b"peers", b"")
    peer_list = []
    for i in range(0, len(peers), 6):
        ip = ".".join(str(b) for b in peers[i:i + 4])
        port = int.from_bytes(peers[i + 4:i + 6], byteorder="big")
        peer_list.append(f"{ip}:{port}")
    return peer_list
