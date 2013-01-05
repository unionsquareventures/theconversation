import bleach

allowed_tags = ['b', 'p', 'i', 'blockquote', 'span', 'ul', 'li', 'img']
allowed_attrs = {
    '*': ['style', 'class'],
    'a': ['href', 'rel'],
    'img': ['src', 'alt', 'width', 'height'],
}
allowed_styles = ['text-decoration']

def html_sanitize(input):
    return bleach.clean(input, tags=allowed_tags,
                         attributes=allowed_attrs,
                         styles=allowed_styles)

allowed_preview_tags = allowed_tags
allowed_preview_tags.remove('img')
def html_sanitize_preview(input):
    return bleach.clean(input, tags=allowed_preview_tags,
                         attributes=allowed_attrs,
                         styles=allowed_styles, strip=True)

