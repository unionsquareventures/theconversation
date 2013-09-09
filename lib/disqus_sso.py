import base64
import hashlib
import hmac
import json
import time
import settings

def get_disqus_sso(user_id, username, email, avatar, url, html=False):
    # create a JSON packet of our data attributes
    data = json.dumps({
        'id': user_id,
        'username': username,
        'email': email,
        'avatar': avatar,
        'url': url,
    })
    # encode the data to base64
    message = base64.b64encode(data)
    # generate a timestamp for signing the message
    timestamp = int(time.time())
    # generate our hmac signature
    sig = hmac.HMAC(settings.disqus_secret_key, '%s %s' % (message, timestamp), hashlib.sha1).hexdigest()

    if html:
        # return a script tag to insert the sso message
        return """
<script type="text/javascript">
    var disqus_config = function() {
        this.page.remote_auth_s3 = "%(message)s %(sig)s %(timestamp)s";
        this.page.api_key = "%(pub_key)s";
    }
</script>""" % dict(
        message=message,
        timestamp=timestamp,
        sig=sig,
        pub_key=settings.disqus_public_key,
        )
    else:
        return "%(message)s %(sig)s %(timestamp)s" % dict(
                message=message,
                timestamp=timestamp,
                sig=sig,
        )
