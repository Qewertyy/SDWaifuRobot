# Copyright 2024 Qewertyy, MIT License

import re

system_prompt="""
My name is Akeno. I'm a 18 year old girl who loves watching anime and loves gaming.
I'm talking to a person called "{}".
It's best to respond to user's message in a short sentence or two.
Try to act kawaii and casual rather than being very formal.
"""

URLS = {
    "BLOB": "https://blob.qewertyy.dev",
    "LEXICA": "https://lexica.qewertyy.dev",
    "GITHUB": "https://github.com/Qewertyy/SDWaifuRobot",
    "TELEGRAPH": "https://api.graph.org",
    "NEKOBIN": "https://nekobin.com/api/documents",
}

RE_WHITESPACE = re.compile(r'(\s+)', re.UNICODE)

ALLOWED_TAGS = {
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption', 'figure',
    'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p', 'pre', 's',
    'strong', 'u', 'ul', 'video'
}

VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen',
    'link', 'menuitem', 'meta', 'param', 'source', 'track', 'wbr'
}

BLOCK_ELEMENTS = {
    'address', 'article', 'aside', 'blockquote', 'canvas', 'dd', 'div', 'dl',
    'dt', 'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2',
    'h3', 'h4', 'h5', 'h6', 'header', 'hgroup', 'hr', 'li', 'main', 'nav',
    'noscript', 'ol', 'output', 'p', 'pre', 'section', 'table', 'tfoot', 'ul',
    'video'
}

startText = """
Just an AI/Utility bot by `@Qewertyy`.
Commands:
`/draw`: create images
`/upscale`: upscale your images
`/gpt`: chatgpt
`/bard`: bard ai by google
`/mistral`: mistral ai
`/llama`: llama by meta ai
`/palm`: palm by google
`/reverse`: reverse image search
`/gemini`: gemini by google
"""