import hashlib
def encrpt(content,entype='md5'):
    if entype == 'md5':
        h = hashlib.md5()
    else:
        h = hashlib.sha512()
    h.update(content)
    print(h.hexdigest())
    #print(h.digest_size,h.block_size)

encrpt(b'132469')
