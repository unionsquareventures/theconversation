import bleach
from bs4 import BeautifulSoup
from htmltruncate import truncate as htmltruncate

allowed_tags = ['a', 'b', 'p', 'i', 'blockquote', 'span', 'ul', 'li', 'img',
                'strong', 'pre', 'iframe', 'object', 'embed', 'em', 'h1', 'h2',
                'h3', 'h4', 'h5', 'h6', 'sub', 'sup', 'ol']

allowed_attrs = {
    'a': ['href', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
    'iframe': ['src', 'frameborder', 'width', 'height'],
    'embed': ['src', 'type', 'width', 'height'],
    'object': ['data', 'type', 'width', 'height'],
}
allowed_styles = ['text-decoration']

def linkify(input):
    return bleach.linkify(input)

def html_sanitize(input):
    text = bleach.clean(input, tags=allowed_tags,
                         attributes=allowed_attrs,
                         styles=allowed_styles)
    return text

def html_sanitize_preview(input):
    return bleach.clean(input, tags=[], attributes=[], styles=[], strip=True)

def truncate(text, length, ellipsis=True):
    soup = BeautifulSoup(text)
    text = soup.get_text()
    text = text[:length]
    if ellipsis and len(text) > length:
        text += '...'
    return text
