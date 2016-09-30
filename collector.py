import os
import re


def find_eaters():
    params = (
        'VmSwap',
        'Pid',
        'Name',
        'Ppid'
    )



    PROC = '/proc'
    dir_list = []
    for i in os.listdir(PROC):
        if re.match('\d+', i):
            dir_list.append(i)
    swap_eaters = {}
    for i in dir_list:
        proc_path = os.path.join(PROC, i, 'status')
        proc_file = open(proc_path)
        proc_info = proc_file.readlines()
        proc_file.close()
        if 'VmSwap' in ''.join(proc_info):
            proc_dic = {}
            for j in proc_info:
                k, v = j.split(':')
                if k not in params:
                    continue
                if k == 'VmSwap':
                    k = 'VmSwap (kB)'
                    v = int(v.replace('kB', '').strip()) # for normal sorting
                    proc_dic.update({k: v})
                    # import ipdb; ipdb.set_trace()

                else:
                    proc_dic.update({k: v.strip()})
            swap_eaters.update({i: proc_dic})
    return swap_eaters

# for i in:

if __name__ == '__main__':
    eaters = find_eaters()
    import ipdb; ipdb.set_trace()
