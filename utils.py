import hashlib

def bytes_to_str(data):
    if isinstance(data, dict):
        return {bytes_to_str(k): bytes_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [bytes_to_str(i) for i in data]
    elif isinstance(data, bytes):
        return data.decode(errors="replace")
    else:
        return data

def sha1(to_sha1):
    return hashlib.sha1(to_sha1).hexdigest()

def raw_sha1(to_sha1):
    return hashlib.sha1(to_sha1).digest()
