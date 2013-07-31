import bleach
from bs4 import BeautifulSoup
from htmltruncate import truncate as htmltruncate

allowed_tags = ['a', 'b', 'p', 'i', 'blockquote', 'span', 'ul', 'li', 'ol',
                'strong', 'pre', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'br', 'span']
allowed_attrs = {
    'a': ['href', 'rel'],
}

allowed_tags_media = list(allowed_tags)
allowed_tags_media += ['iframe', 'object', 'embed', 'img']
allowed_attrs_media = dict(allowed_attrs)
allowed_attrs_media.update({
    'iframe': ['src', 'frameborder', 'width', 'height'],
    'img': ['src', 'alt', 'width', 'height'],
    'embed': ['src', 'type', 'width', 'height'],
    'object': ['data', 'type', 'width', 'height'],
})

allowed_styles = ['text-decoration']

# This is exposed to templates as a template method.
# See ui/template_methods.py
def tinymce_valid_elements(media=True):
    if media:
        tags = allowed_tags_media
        attrs = allowed_attrs_media
    else:
        tags = allowed_tags
        attrs = allowed_attrs
    valid_list = []
    for tag in tags:
        elem = tag
        elem_attrs = attrs.get(tag)
        if elem_attrs:
            tag += '[%s]' % '|'.join(elem_attrs)
        valid_list.append(tag)
    return ','.join(valid_list)

def linkify(input):
    return bleach.linkify(input)

def html_sanitize(input, media=True):
    if media:
        tags = allowed_tags_media
        attrs = allowed_attrs_media
    else:
        tags = allowed_tags
        attrs = allowed_attrs
    text = bleach.clean(input, tags=tags,
                         attributes=attrs,
                         styles=allowed_styles)
    return text

def html_sanitize_preview(input):
    return bleach.clean(input, tags=[], attributes=[], styles=[], strip=True)

def html_to_text(text):
    soup = BeautifulSoup(text)
    text = soup.get_text()
    return text

def truncate(text, length, ellipsis=True):
    text = text[:length]
    if ellipsis and len(text) > length:
        text += '...'
    return text
