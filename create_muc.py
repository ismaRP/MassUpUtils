#!/usr/bin/env python3
import xml.etree.ElementTree as ET
# import pandas as pd
import csv
import argparse

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def iter_samples(samples_table):
    for sample in zip(*[samples_table[f] for f in samples_table.keys()]):
        s_dict = {}
        for f, d in zip(samples_table.keys(), sample):
            s_dict[f]=d
        yield s_dict


parser = argparse.ArgumentParser(description='Create MassUp configuration file.')

parser.add_argument('-s', metavar='spectra', type=str, nargs=1, default=None,
                   action='store', dest='spectra_path',
                   help='Path to the spectrum files')
parser.add_argument('-t', metavar='table',type=str, nargs=1, default=None,
                   action='store', dest='table_path',
                   help='Path to the files table')
parser.add_argument('--type', metavar='type',type=str, nargs=1,
                   default='RAW Spectra', action='store', dest='type',
                   help='Path to the files table')
parser.add_argument('-o', metavar='file',type=str, nargs=1,
                   default='config.muc', action='store', dest='out',
                   help='Output xml (.muc) file')

args = parser.parse_args()
spectra_path = args.spectra_path[0]
table_path = args.table_path[0]
outfile = args.out[0]

# samples_table = pd.read_csv(table_path)
samples_table = {}
with open(table_path, 'r', newline='') as table_f:
    header = table_f.readline().rstrip()
    header = header.split(',')
    for f in header:
        samples_table[f] = []
    for row in table_f:
        row = row.rstrip().split(',')
        for f, el in zip(header,row):
            samples_table[f].append(el)


if len(samples_table.keys()) == 3:
    labeled = True
else:
    labeled = False
type = args.type[0]

root = ET.Element('massupdatasetloader')
root.set('labeled', str(labeled).lower())
root.set('type', type)
files = ET.SubElement(root, 'files')
samplenames = ET.SubElement(root, 'samplenames')
filesamplemappings = ET.SubElement(root, 'filesamplemappings')

if labeled:
    classes = ET.SubElement(root, 'classes')
    sampleclassmappings = ET.SubElement(root, 'sampleclassmappings')
    labels = sorted(list(set(samples_table['label'])))
    i=0
    labels_map = {}
    for l in labels:
        labels_map[l] = i
        i += 1
        cl = ET.SubElement(classes, 'class')
        cl.text = l

n=0
for sample in iter_samples(samples_table):
    sample_name = sample['sample name']
    n_reps = int(sample['replicates'])
    samplename = ET.SubElement(samplenames, 'samplename')
    samplename.text = sample_name
    for i in range(1,n_reps+1):
        file = ET.SubElement(files, 'file')
        file.text = spectra_path + sample_name + '_' + str(i) + '.txt.csv'
        filesamplemapping = ET.SubElement(filesamplemappings, 'mapping')
        filesamplemapping.text = str(n)
    if labeled:
        label = sample['label']
        sampleclassmapping = ET.SubElement(sampleclassmappings, 'mapping')
        sampleclassmapping.text = str(labels_map[label])

    n += 1



indent(root)
f = open(outfile, 'w')
f.write(ET.tostring(root, encoding='unicode'))
