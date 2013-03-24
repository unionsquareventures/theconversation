import os
import sys

from fabric.api import *

def prod():
    env.deployment_stage = 'production'
    env.user = 'ubuntu'
    env.hosts = [
        '23.21.41.77'
    ]

def staging():
    env.deployment_stage = 'staging'
    env.user = 'ubuntu'
    env.hosts = [
        '54.225.158.156',
    ]

def deploy():
    deploy_path = '/data/apps/usv'
    run('sudo mkdir -p %s' % deploy_path)
    run('sudo chmod -R 777 %s' % deploy_path)
    local('find . -name "*.pyc" -exec rm -rf {} \;')
    local('scp -r -i ../usv.pem *'
                        ' ubuntu@%s:%s' % (env.hosts[0], deploy_path))
    with cd(deploy_path):
        clean = lambda x: x.replace('/', '\\\\/').replace('"', '\\\\"')

        # Switch settings to production
        initial = 'DEPLOYMENT_STAGE = "local"'
        new = 'DEPLOYMENT_STAGE = "%s"' % env.deployment_stage
        run('sed -i "s/%s/%s/g" %s' % (clean(initial), clean(new), "settings.py"))

        # Switch Prod config
        initial = "server_address = 'insert_address_here'"
        new = "server_address = 'https://%s'" % env.hosts[0]
        run('sed -i "s/%s/%s/g" %s' % (clean(initial),
                                        clean(new),
                                        "server_setup/deployment/prod.py"))

        # Restart server processes
        run('sudo supervisorctl restart usv:*')
