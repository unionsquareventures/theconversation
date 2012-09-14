"""determines deployment stage and import appropriate settings file"""
import os

DEPLOYMENT_STAGE = "local"
if os.path.exists("deployment_stage"):
    DEPLOYMENT_STAGE = open("deployment_stage").read().strip()

if DEPLOYMENT_STAGE == 'production':
    from server_setup.deployment.prod import *
elif DEPLOYMENT_STAGE == 'staging':
    from server_setup.deployment.staging import *
elif DEPLOYMENT_STAGE == 'beta':
    from server_setup.deployment.beta import *
else:
    from server_setup.deployment.local import *

print 'using %s settings' % DEPLOYMENT_STAGE
