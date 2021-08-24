def sanitize(s: str):
    s = s.strip().upper()
    s = list(s)
    tmp = []
    for i, c in enumerate(s):
        if c != " ":
            tmp.append(c)
        else:
            if s[i - 1] == "'":
                continue
            else:
                tmp.append(c)
    return "".join(tmp)
