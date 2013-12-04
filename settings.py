"""determines deployment stage and import appropriate settings file"""
import os
import logging

DEPLOYMENT_STAGE = os.environ.get('DEPLOYMENT_STAGE', 'local')

if DEPLOYMENT_STAGE == 'production':
    from server_setup.deployment.prod import *
elif DEPLOYMENT_STAGE == 'staging':
    from server_setup.deployment.staging import *
elif DEPLOYMENT_STAGE == 'test':
    from server_setup.deployment.test import *
else:
    from server_setup.deployment.local import *

print 'using %s settings' % DEPLOYMENT_STAGE
