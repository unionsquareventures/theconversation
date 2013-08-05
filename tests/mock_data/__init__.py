import os
import codecs

def mock_data(type, id, attribute):
    file_path = '%s/%s/%s.txt' % (type, id, attribute)
    cur_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(cur_path, file_path)
    f = codecs.open(file_path, 'r', encoding='utf-8')
    text = f.read()
    return text
