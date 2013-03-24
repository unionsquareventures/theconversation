import bleach

allowed_tags = ['a', 'b', 'p', 'i', 'blockquote', 'span', 'ul', 'li', 'img', 'strong', 'pre']
allowed_attrs = {
    '*': ['style', 'class'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
}
allowed_styles = ['text-decoration']

def linkify(input):
    return bleach.linkify(input)


def html_sanitize(input):
    return bleach.clean(input, tags=allowed_tags,
                         attributes=allowed_attrs,
                         styles=allowed_styles)

allowed_preview_tags = list(allowed_tags)
allowed_preview_tags.remove('img')
def html_sanitize_preview(input):
    return bleach.clean(input, tags=[], attributes=[], styles=[], strip=True)

