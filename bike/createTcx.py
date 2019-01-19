#!/usr/bin/env python3

import argparse
import os
import re
import xml.etree.ElementTree

def main():
    parser = argparse.ArgumentParser(description='Create Garmin TCX workout files')
    parser.add_argument('--Source', '-s', type=str, metavar='directory', help='Source directory with FTP in directory name', required=True)
    parser.add_argument('--Power', '-p', type=int, metavar='number', help='The desired FTP', required=True)
    args = parser.parse_args()

    source = args.Source
    ftp = args.Power

    if not os.path.isdir(args.Source):
        print('{} is not a directory'.format(source))
        return

    ftpRegex = re.match('[^0-9]+([0-9]+)(.*)', source)
    if ftpRegex is None:
        print('Could not find original ftp in directory name {}'.format(source))
        return

    originalFtp = ftpRegex.groups()[0]
    folderText = ftpRegex.groups()[1]
    destination = '{}{}'.format(ftp, folderText)

    source = os.path.abspath(source)
    sourceParent = os.path.abspath(os.path.join(source, '..'))
    destination = os.path.join(sourceParent, destination)

    if os.path.isdir(destination):
        print('{} already exists'.format(destination))
        return

    os.mkdir(destination)

    print('Creating {}'.format(destination))
    print('From source {}'.format(source))
    print('Converting FTP from {} to {}'.format(originalFtp, ftp))
    scaler = int(ftp) / int(originalFtp)

    xml.etree.ElementTree.register_namespace('', 'http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2')
    xml.etree.ElementTree.register_namespace('nsworkout', 'http://www.garmin.com/xmlschemas/WorkoutExtension/v1')
    xml.etree.ElementTree.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    for tcxFile in os.listdir(source):
        if os.path.splitext(tcxFile)[1] == '.tcx':
            fullFilePath = os.path.join(source, tcxFile)
            tree = xml.etree.ElementTree.parse(fullFilePath)
            root = tree.getroot()
            for powerZone in root.iter('{http://www.garmin.com/xmlschemas/WorkoutExtension/v1}PowerZone'):
                for lowHigh in powerZone:
                    for value in lowHigh:
                        ftpToChange = int(value.text)
                        newFtp = int(round(ftpToChange * scaler))
                        value.text = str(newFtp)

            xmlText = xml.etree.ElementTree.tostring(root, encoding='unicode')
            xmlText = xmlText.replace('_{}'.format(originalFtp), '_{}'.format(ftp))
            xmlText = xmlText.replace('<nsworkout:', '<')
            xmlText = xmlText.replace('</nsworkout:', '</')
            xmlText = xmlText.replace('<Steps>', '<Steps xmlns="http://www.garmin.com/xmlschemas/WorkoutExtension/v1">')
            fullFilePath = os.path.join(destination, tcxFile)
            fullFilePath = fullFilePath.replace('_{}'.format(originalFtp), '_{}'.format(ftp))
            with open(fullFilePath, 'w') as textFile:
                textFile.write(xmlText)

    print('Done!')

if __name__ == '__main__':
    main()