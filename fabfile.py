import os
import sys

from fabric.api import *

env.user = 'ubuntu'
env.hosts = [
    'ec2-54-234-57-239.compute-1.amazonaws.com'
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
        new = 'DEPLOYMENT_STAGE = "production"'
        run('sed -i "s/%s/%s/g" %s' % (clean(initial), clean(new), "settings.py"))

        # Switch Prod config
        initial = "server_address = 'insert_address_here'"
        new = "server_address = 'https://ec2-54-234-57-239.compute-1.amazonaws.com'"
        run('sed -i "s/%s/%s/g" %s' % (clean(initial),
                                        clean(new),
                                        "server_setup/deployment/prod.py"))

        run('sudo mkdir -p ../usv_ssl')
        run('sudo cp -r ../usv/* ../usv_ssl')
        run('sudo chmod -R 777 ../usv_ssl')
        with cd('/data/apps/usv_ssl'):
            # Switch Prod port for SSL
            initial = "server_port = 80"
            new = "server_port = 443"
            run('sed -i "s/%s/%s/g" %s' % (clean(initial),
                                            clean(new),
                                            "server_setup/deployment/prod.py"))

        # Restart server processes
        run('sudo supervisorctl restart usv_group:*')
