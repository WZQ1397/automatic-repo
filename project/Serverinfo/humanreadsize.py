# python day 28
# author zach.wang
def humanize_bytes(bytesize, precision=2):
    abbrevs = (
        (10**15, 'PB'),
        (10**12, 'TB'),
        (10**9, 'GB'),
        (10**6, 'MB'),
        (10**3, 'KB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f%s' % (precision, float(bytesize) / factor, suffix)