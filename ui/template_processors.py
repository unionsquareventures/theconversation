import settings
import tempfile
import os

module_dir = os.path.join(settings.tornado_config['template_path'], '_modules')
styles_bundle = os.path.join(settings.tornado_config['static_path'], 'css/modules_bundle.css')
javascript_bundle = os.path.join(settings.tornado_config['static_path'], 'js/modules_bundle.js')

def gather(module_file):
    for module_name in os.listdir(module_dir):
        path = os.path.join(module_dir, module_name)
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
    print "CSS"
    contents = ["/* %s */\n%s\n" % (n, c) for n, c in gather('main.css')]
    contents = ''.join(contents)
    print contents
    # Compile and compress the styles
    tmpfd, tmpname = tempfile.mkstemp()
    tmpf = os.fdopen(tmpfd, 'w')
    tmpf.write(contents)
    tmpf.close()
    os.system('lessc -x "%s" > "%s"' % (tmpname, styles_bundle))
    os.remove(tmpname)

def bundle_javascript():
    print "JS"
    contents = ["function %s() {\n%s\n};\n" % (n, c) for n, c in gather('main.js')]
    contents = ''.join(contents)
    print contents

