import socket
from utils import raw_sha1

def perform_handshake(peer_ip, peer_port, info_bencoded):
    info_hash = raw_sha1(info_bencoded)
    peer_id = b"00112233445566778899"
    handshake = (
        bytes([19]) + b"BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00" + info_hash + peer_id
    )
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((peer_ip, int(peer_port)))
    sock.send(handshake)
    
    response = sock.recv(68)
    peer_id = response[48:].hex()
    sock.close()
    return peer_id
