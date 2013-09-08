import tempfile
import os
import sys
from collections import defaultdict
import functools
import subprocess
import tornado.ioloop
import logging

sys.path.append('../')
import settings

styles_bundle = os.path.join(settings.tornado_config['static_path'], 'css/modules_bundle.css')
javascript_bundle = os.path.join(settings.tornado_config['static_path'], 'js/modules_bundle.js')

paths = defaultdict(list)

# Obtain a given file (module_file) from each module.
# Also store the found files in the paths dictionary.
def gather(module_file):
    for module_name in os.listdir(settings.module_dir):
        path = os.path.join(settings.module_dir, module_name)
        if not os.path.isdir(path):
            continue
        module_file_path = os.path.join(path, module_file)
        try:
            f = open(module_file_path, 'r')
            contents = f.read().strip()
            if contents:
                paths[module_file].append(module_file_path)
                yield module_name, contents
        except IOError:
            pass

# Aggregate/bundle the CSS for the modules into the styles_bundle file.
def bundle_styles():
    contents = ["/* %s */\n%s\n" % (n, c) for n, c in gather('main.less')]
    contents = ''.join(contents)
    # Compile and compress the styles
    tmpfd, tmpname = tempfile.mkstemp()
    tmpf = os.fdopen(tmpfd, 'w')
    tmpf.write(contents)
    tmpf.close()
    s = subprocess.Popen(['lessc', '-x', tmpname],
                            stderr=subprocess.STDOUT,
                            stdout=subprocess.PIPE).communicate()[0]
    f = open(styles_bundle, 'w')
    f.write(s)
    f.close()
    os.remove(tmpname)

# Aggregate/bundle the JavaScript for the modules into the javascript_bundle file.
def bundle_javascript():
    contents = ["function %s() {\n%s\n};\n" % (n, c) for n, c in gather('main.js')]
    contents = ''.join(contents)
    # Compile JS
    tmpfd, tmpname = tempfile.mkstemp()
    tmpf = os.fdopen(tmpfd, 'w')
    tmpf.write(contents)
    tmpf.close()
    #s = subprocess.Popen(['uglifyjs', tmpname],
    #                        stderr=subprocess.STDOUT,
    #                        stdout=subprocess.PIPE).communicate()[0]
    #f = open(javascript_bundle, 'w')
    #f.write(s)
    #f.close()
    os.remove(tmpname)


"""
    Watch all the JS and LESS files for changes.
    Re-create the bundles when a change occurs.
"""

def _file_changed(modify_times, path):
    # Check modification time
    try:
        modified = os.stat(path).st_mtime
    except Exception:
        return False
    # First run
    if path not in modify_times:
        modify_times[path] = modified
        return False
    # Check for change since last run
    if modify_times[path] != modified:
        modify_times[path] = modified
        return True
    return False

def _check_styles(modify_times):
    for path in paths['main.less']:
        if _file_changed(modify_times, path):
            logging.info('Rebundling styles...')
            bundle_styles()
            logging.info('Done.')

def _check_javascript(modify_times):
    for path in paths['main.js']:
        if _file_changed(modify_times, path):
            logging.info('Rebundling JavaScript...')
            bundle_javascript()
            logging.info('Done.')

def watch_modules(io_loop, check_time=500):
    modify_times = {}
    callback = functools.partial(_check_styles, modify_times)
    scheduler = tornado.ioloop.PeriodicCallback(callback, check_time, io_loop=io_loop)
    scheduler.start()

    callback = functools.partial(_check_javascript, modify_times)
    scheduler = tornado.ioloop.PeriodicCallback(callback, check_time, io_loop=io_loop)
    scheduler.start()
