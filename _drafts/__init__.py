from os import listdir
for dir_name in listdir(__file__[:-11]):
    if len(dir_name) >= 4 and dir_name[:2] == dir_name[-2:] == '__':
        continue
    if len(dir_name) and dir_name[-3:] == '.py':
        dir_name = dir_name[:-3]
        if len(dir_name) >= 4 and dir_name[:2] == dir_name[-2:] == '__':
            continue
        else:
            exec('from .' + dir_name + ' import *')
    else:
        try:
            exec('from ' + dir_name + ' import *')
        finally:
            pass
