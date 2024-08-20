import hashlib

def int_to_bytes(i):
    byte_length = (i.bit_length() + 7) // 8
    return i.to_bytes(byte_length, 'little')

def do_hash(data):
    h = hashlib.sha256()
    h.update(data)
    return h.digest()

def full_domain_hash(data, target_length):
    tl_bytes = target_length // 8
    digest_size = hashlib.sha256().digest_size
    ncycles = (tl_bytes // digest_size) + 1
    out = bytearray()
    for i in range(ncycles):
        out.extend(do_hash(data + int_to_bytes(i)))
    return bytes(out[:tl_bytes])

def digest(data, parameters):
    hashed = full_domain_hash(data, parameters['L'])
    i = int.from_bytes(hashed, byteorder='little') % parameters['p']
    return pow(i, (parameters['p'] - 1) // parameters['q'], parameters['p'])
