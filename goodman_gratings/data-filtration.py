import os
import glob
import re
import datetime
import pandas as pd
import numpy as np

data_location = '/user/simon/data/soar/instrument_configs'

def select_file(path):
    oldest = ''
    oldest_file = ''
    for _file in os.listdir(path):
        with open(os.path.join(path, _file), mode='rb') as _setup:
            for _line in _setup.readlines():
                if b'SUBMIT' in _line:
                    _line = str(_line.split(b': ')[1].rstrip(), 'utf-8')
                    # print(re.sub('[\ ]', '', _line))
                    _time = datetime.datetime.strptime(re.sub('[\ ]', '', _line), '%Y-%m-%d.%H:%M:%S')
                    if oldest == '':
                        oldest = _time
                        oldest_file = os.path.join(path, _file)
                    else:
                        if oldest < _time:
                            oldest = _time
                            oldest_file = os.path.join(path, _file)
                    # print(_time)
    # print('Oldest: {} file: {}'.format(oldest, oldest_file))
    return oldest_file

def extract_info(selected_file):
    all_data = []
    with open(selected_file, mode='rb') as _setup:
        all_lines = _setup.readlines()
        semester = ''
        start_date = ''
        for _line in all_lines:

            _line = _line.strip(b'\n')
            if b'SEMESTER:' in _line:
                # print(_line)
                semester = _line.split(b':')[1]
                semester = str(semester, 'utf-8')
                semester = re.sub('[ ]', '', semester)
                # print(semester)

            if b'STARTDATE:' in _line and start_date == '':
                # print(_line)
                start_date = str(_line, 'utf-8')
                start_date = start_date.strip(' ')
                start_date = start_date.split(':')[1]
                start_date = re.sub(' ', '', start_date)
                # print(selected_file)
                # print(start_date)
            if b'GRATINGS:' in _line:
                # print(_line)
                gratings = _line.split(b':')[1:]
                if len(gratings) == 1:
                    gratings = str(gratings[0], 'utf-8')
                    gratings = re.sub('Red', '', gratings)
                    gratings = re.sub('Blue', '', gratings)
                    gratings = re.sub('l/mm', '', gratings)
                    gratings = re.sub('lines/mm', '', gratings)
                    gratings = re.sub('500nm', '', gratings)
                    gratings = re.sub('620nm', '', gratings)
                    gratings = re.sub('620 nm', '', gratings)
                    gratings = re.sub('mm\^-1', '', gratings)
                    gratings = re.sub('\(([^\)]+)\)', '', gratings)
                    gratings = re.sub('&', ',', gratings)
                    gratings = re.sub('&', ',', gratings)
                    gratings = re.sub(';', ',', gratings)
                    gratings = re.sub('and', ',', gratings)
                    gratings = re.sub('0.45" slit', '', gratings)
                    gratings = re.sub('\(\)', '', gratings)
                    if 'N/A' not in gratings:
                        gratings = re.sub('/', ',', gratings)
                    for subs in ['m1', 'm2', 'M1', 'M2', 'm3', 'M3', 'm4', 'M4']:
                        gratings = re.sub(subs, '', gratings)
                    gratings = re.sub('[a-zA-z_. \+/-]', '', gratings)
                    print(gratings, len(gratings))
                    if len(gratings) > 1:
                        # print(selected_file)
                        if gratings == '4006001200':
                            gratings = '400,600,1200'
                        if gratings == '400600':
                            gratings = '400,600'
                        if gratings == '600300':
                            gratings = '600,300'
                        if gratings == '600930':
                            gratings = '600,930'
                        if gratings == '4001200':
                            gratings = '400,1200'
                        if gratings == '6001200':
                            gratings = '600,1200'


                        for grating in gratings.split(','):
                            if grating in ['300', '400', '600', '930', '1200', '1800', '2100', '2400', '']:
                                # [print(selected_file)]
                                # print('{} {} {}'.format(start_date, grating, semester))
                                all_data.append((start_date, grating, semester))
                            else:
                                pass
                                # print(selected_file)
                                # print(_line)
                                # print(repr(grating))
                else:
                    print('Error in {:s}'.format(selected_file))
                    print(gratings)
                # print(re.sub('[a-z/\\\\ ]', '', gratings))
            # else:
        return all_data



all_data = []
for _datadir in sorted(glob.glob(os.path.join(data_location, '????-??-??*'))):

    if os.path.isdir(_datadir):
        n_files = len(os.listdir(_datadir))
        if n_files == 1:
            # print('OK')
            full_file = os.path.join(data_location, _datadir, os.listdir(_datadir)[0])
            # useful_data = extract_info(full_file)
        elif n_files > 1:
            full_file = select_file(path=_datadir)

        else:
            print('No files in {}'.format(_datadir))
        useful_data = extract_info(selected_file=full_file)
        if useful_data != []:
            all_data.extend(useful_data)
    else:
        pass
# print(all_data)

df = pd.DataFrame(data=all_data, columns=['date', 'grating', 'semester'])

np.savetxt(r'/user/simon/documentation/soar/general_documentation/goodman_gratings/all_gratings.txt', df.values, fmt='%s')

# # print(df)
#
# for semester in ['2018A', '2018B', '2019A']:
#     selected = df[(df.semester == semester)]
#     print(selected)
#     selected.hist(column='grating', bins=7)