# Torrent Client

This is a work-in-progress BitTorrent client written in Python. The client provides basic functionality for parsing `.torrent` files, communicating with trackers, discovering peers, and initiating the BitTorrent handshake. The code is modularized for better readability and future expansion.

- **Bencode Parsing:** Decodes and encodes bencoded data structures.
- **Torrent Info Extraction:** Extracts metadata, including tracker URLs, file length, piece hashes, and info hash.
- **Tracker Communication:** Sends GET requests to HTTP trackers and retrieves peer information.
- **Peer Handshake:** Establishes a connection with peers and performs the BitTorrent handshake.

## Usage
Run the client using the following commands:

1. **Decode bencoded data:**
   ```bash
   python main.py decode "<bencoded-string>"
   ```

2. **Extract torrent info:**
   ```bash
   python main.py info <path-to-torrent-file>
   ```

3. **Discover peers via tracker:**
   ```bash
   python main.py peers <path-to-torrent-file>
   ```

4. **Perform a handshake with a peer:**
   ```bash
   python main.py handshake <path-to-torrent-file> <peer-ip:port>
   ```

## Dependencies
- `bencodepy`
- `requests`


## TODO
- Implement peer-to-peer data exchange.
- Add support for multiple trackers.
- Handle advanced protocol features (e.g., DHT, PEX).
- Improve error handling and logging.

---