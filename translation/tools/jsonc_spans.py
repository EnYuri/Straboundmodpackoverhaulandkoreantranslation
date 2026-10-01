"""Minimal JSONC parser that records source spans for every value.

Supports Starbound-flavoured JSON: // and /* */ comments, trailing commas,
and literal newlines inside strings. Duplicate object keys keep the last
occurrence, matching the game's loader.
"""


class Node:
    __slots__ = ("kind", "start", "end", "children")

    def __init__(self, kind, start, end, children=None):
        self.kind = kind          # 'object' | 'array' | 'string' | 'literal'
        self.start = start        # offset of first char of the value
        self.end = end            # offset just past last char of the value
        self.children = children  # dict for object, list for array, None else


def _skip_ws(text, i, n):
    while i < n:
        c = text[i]
        if c in " \t\r\n":
            i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j == -1 else j + 1
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j == -1 else j + 2
        else:
            break
    return i


def _parse_string(text, i, n):
    # returns end offset just past the closing quote; allows raw newlines
    i += 1
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
        elif c == '"':
            return i + 1
        else:
            i += 1
    raise ValueError("unterminated string")


def _parse_value(text, i, n):
    i = _skip_ws(text, i, n)
    if i >= n:
        raise ValueError("unexpected end of input")
    c = text[i]
    if c == "{":
        start = i
        children = {}
        i += 1
        i = _skip_ws(text, i, n)
        while i < n and text[i] != "}":
            if text[i] != '"':
                raise ValueError(f"expected string key at {i}")
            kend = _parse_string(text, i, n)
            key = _unescape(text[i + 1:kend - 1])
            i = _skip_ws(text, kend, n)
            if text[i] != ":":
                raise ValueError(f"expected ':' at {i}")
            value, i = _parse_value(text, i + 1, n)
            children[key] = value
            i = _skip_ws(text, i, n)
            if i < n and text[i] == ",":
                i = _skip_ws(text, i + 1, n)
        if i >= n:
            raise ValueError("unterminated object")
        return Node("object", start, i + 1, children), i + 1
    if c == "[":
        start = i
        children = []
        i += 1
        i = _skip_ws(text, i, n)
        while i < n and text[i] != "]":
            value, i = _parse_value(text, i, n)
            children.append(value)
            i = _skip_ws(text, i, n)
            if i < n and text[i] == ",":
                i = _skip_ws(text, i + 1, n)
        if i >= n:
            raise ValueError("unterminated array")
        return Node("array", start, i + 1, children), i + 1
    if c == '"':
        end = _parse_string(text, i, n)
        return Node("string", i, end), end
    # literal: number, true, false, null — read to delimiter
    start = i
    while i < n and text[i] not in ",}] \t\r\n":
        i += 1
    return Node("literal", start, i), i


def _unescape(raw):
    out = []
    i = 0
    while i < len(raw):
        if raw[i] == "\\" and i + 1 < len(raw):
            nxt = raw[i + 1]
            if nxt == "u" and i + 5 < len(raw) + 1:
                try:
                    out.append(chr(int(raw[i + 2:i + 6], 16)))
                    i += 6
                    continue
                except ValueError:
                    pass
            out.append({"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f"}.get(nxt, nxt))
            i += 2
        else:
            out.append(raw[i])
            i += 1
    return "".join(out)


def parse_spans(text):
    node, _ = _parse_value(text, 0, len(text))
    return node


def navigate(node, pointer):
    for raw in [p for p in pointer.split("/") if p != ""]:
        part = raw.replace("~1", "/").replace("~0", "~")
        if node.kind == "object":
            node = node.children[part]
        elif node.kind == "array":
            node = node.children[int(part)]
        else:
            raise KeyError(pointer)
    return node
