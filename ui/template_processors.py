import tempfile
import os
import sys

sys.path.append('../')
import settings

styles_bundle = os.path.join(settings.tornado_config['static_path'], 'css/modules_bundle.css')
javascript_bundle = os.path.join(settings.tornado_config['static_path'], 'js/modules_bundle.js')

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
                yield module_name, contents
        except IOError:
            pass

def bundle_styles():
    contents = ["/* %s */\n%s\n" % (n, c) for n, c in gather('main.less')]
    contents = ''.join(contents)
    # Compile and compress the styles
    tmpfd, tmpname = tempfile.mkstemp()
    tmpf = os.fdopen(tmpfd, 'w')
    tmpf.write(contents)
    tmpf.close()
    os.system('lessc -x "%s" > "%s"' % (tmpname, styles_bundle))
    os.remove(tmpname)

def bundle_javascript():
    contents = ["function %s() {\n%s\n};\n" % (n, c) for n, c in gather('main.js')]
    contents = ''.join(contents)
    # Compile JS
    tmpfd, tmpname = tempfile.mkstemp()
    tmpf = os.fdopen(tmpfd, 'w')
    tmpf.write(contents)
    tmpf.close()
    os.system('uglifyjs "%s" > "%s"' % (tmpname, javascript_bundle))
    os.remove(tmpname)
