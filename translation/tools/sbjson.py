# Lenient Starbound JSON loader: strips // and /* */ comments outside
# strings, escapes literal CR/LF inside strings, drops trailing commas.
# Only chr()-based escapes so the file survives transport unharmed.
import json, re

BS = chr(92)
CR = chr(13)
LF = chr(10)


def parse_sb(raw):
    if isinstance(raw, bytes):
        s = raw.decode('utf-8', errors='replace')
    else:
        s = raw
    out = []
    i, n, ins = 0, len(s), False
    while i < n:
        c = s[i]
        if c == '"' and (i == 0 or s[i - 1] != BS):
            ins = not ins
            out.append(c)
            i += 1
            continue
        if not ins and c == '/' and i + 1 < n and s[i + 1] == '/':
            while i < n and s[i] != LF:
                i += 1
            continue
        if not ins and c == '/' and i + 1 < n and s[i + 1] == '*':
            i += 2
            while i + 1 < n and not (s[i] == '*' and s[i + 1] == '/'):
                i += 1
            i += 2
            continue
        if ins and c == CR:
            out.append(BS + 'r')
            i += 1
            continue
        if ins and c == LF:
            out.append(BS + 'n')
            i += 1
            continue
        if ins and ord(c) < 32:
            out.append(BS + 'u%04x' % ord(c))
            i += 1
            continue
        out.append(c)
        i += 1
    body = ''.join(out)
    body = re.sub(r',(\s*[}\]])', r'\1', body)
    return json.loads(body)


def ptr_get(doc, ptr):
    cur = doc
    for t in ptr.lstrip('/').split('/'):
        if isinstance(cur, list):
            try:
                cur = cur[int(t)]
            except (ValueError, IndexError):
                return None
        elif isinstance(cur, dict):
            if t not in cur:
                return None
            cur = cur[t]
        else:
            return None
    return cur
