#!/usr/bin/env python3.4

"""
BORIS
Behavioral Observation Research Interactive Software
Copyright 2012-2018 Olivier Friard

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
"""

try:
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *

import math
import csv
import re
import subprocess
import hashlib
import urllib.parse
import sys
import os
import logging
import subprocess
from decimal import *
import math
import datetime
import socket
import numpy as np

from config import *


def bytes_to_str(b):
    """
    Translate bytes to string.
    
    Args:
        b (bytes): byte to convert
    
    Returns:
        str: converted byte
    """

    if isinstance(b, bytes):
        fileSystemEncoding = sys.getfilesystemencoding()
        # hack for PyInstaller
        if fileSystemEncoding is None:
            fileSystemEncoding = "UTF-8"
        return b.decode(fileSystemEncoding)
    else:
        return b


def ffmpeg_recode(video_paths, horiz_resol, ffmpeg_bin):
    """
    recode one or more video with ffmpeg
    
    Args:
        video_paths (list): list of video paths
        horiz_resol (int): horizontal resolution (in pixels)
        ffmpeg_bin (str): path of ffmpeg program
    
    Returns:
        bool: True
    """

    for video_path in video_paths:
        ffmpeg_command = ('"{ffmpeg_bin}" -y -i "{input_}" '
                          '-vf scale={horiz_resol}:-1 -b 2000k '
                          '"{input_}.re-encoded.{horiz_resol}px.avi" ').format(ffmpeg_bin=ffmpeg_bin,
                                                                               input_=video_path,
                                                                               horiz_resol=horiz_resol)
        p = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        p.communicate()

    return True


def convert_time_to_decimal(pj):
    """
    convert time from float to decimal
    
    Args:
        pj (dict): BORIS project
        
    Returns:
        dict: BORIS project
    """

    for obsId in pj[OBSERVATIONS]:
        if "time offset" in pj[OBSERVATIONS][obsId]:
            pj[OBSERVATIONS][obsId]["time offset"] = Decimal(str(pj[OBSERVATIONS][obsId]["time offset"]))
        for idx, event in enumerate(pj[OBSERVATIONS][obsId][EVENTS]):
            pj[OBSERVATIONS][obsId][EVENTS][idx][pj_obs_fields["time"]] = Decimal(str(pj[OBSERVATIONS][obsId][EVENTS][idx][pj_obs_fields["time"]]))

    return pj


def file_content_md5(file_name):
    hash_md5 = hashlib.md5()
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def txt2np_array(file_name, columns_str, substract_first_value, converters = {}, column_converter={}):
    """read a txt file (tsv or csv) and return np array with passed columns
    
    Args:
        file_name (str): path of the file to load in numpy array
        columns_str (str): indexes of columns to be loaded. First columns must be the timestamp. Example: "4,5"
        substract_first_value (str): "True" or "False"
        converters (dict): dictionary containing converters
        column_converter (dict): dcitionary key: column index, value: converter name

    Returns:
        bool: True if data successfullly loaded, False if case of error
        str: error message. Empty if success
        numpy array: data. Empty if not data failed to be loaded

    """
    # check columns
    try:
        columns = [int(x) - 1 for x in columns_str.split(",") ]
    except:
        return False, "Problem with columns {}".format(columns_str), np.array([])
    
    # check converters
    np_converters = {}
    for column_idx in column_converter:
        if column_converter[column_idx] in converters:
            
            conv_name = column_converter[column_idx]
            
            function = """def {}(INPUT):\n""".format(conv_name)
            function += """    INPUT = INPUT.decode("utf-8") if isinstance(INPUT, bytes) else INPUT"""
            for line in converters[conv_name]["code"].split("\n"):
                function += "    {}\n".format(line)
            function += """    return OUTPUT"""

            try:
                exec(function)
            except:
                #print(sys.exc_info()[1])
                return False, "error in converter", np.array([]) 
            
            np_converters[column_idx - 1] = locals()[conv_name]

        else:
            print("converter {} not found".format(converters_param[column_idx]))
            return False, "converter not found", np.array([]) 

    # snif txt file
    with open(file_name) as csvfile:
        buff = csvfile.read(1024)
        snif = csv.Sniffer()
        dialect = snif.sniff(buff)
        has_header = snif.has_header(buff)

    try:
        data = np.loadtxt(file_name,
                          delimiter=dialect.delimiter,
                          usecols=columns,
                          skiprows=has_header,
                          converters=np_converters)
    except:
        return False, sys.exc_info()[1], np.array([])

    # check if first value must be substracted
    if substract_first_value == "True":
        data[:,0] -= data[:,0][0]

    return True, "", data


def versiontuple(version_str):
    """Convert version from text to tuple
    
    Args:
        version_str (str): version
        
    Returns:
        tuple: version in tuple format (for comparison)
    """
    return tuple(map(int, (version_str.split("."))))


def state_behavior_codes(ethogram):
    """
    behavior codes defined as STATE event
    
    Args:
        ethogram (dict): ethogram dictionary
        
    Returns:
        list: list of behavior codes defined as STATE event
    
    """
    return [ethogram[x][BEHAVIOR_CODE] for x in ethogram if "STATE" in ethogram[x][TYPE].upper()]


def get_current_states_by_subject(state_behaviors_codes, events, subjects, time):
    """
    get current states for subjects at given time
    Args:
        state_behaviors_codes (list): list of behavior codes defined as STATE event
        events (list): list of events
        subjects (dict): dictionary of subjects
        time (Decimal): time

    Returns:
        dict: current states by subject. dict of list
    """
    current_states = {}
    for idx in subjects:
        current_states[idx] = []
        for sbc in state_behaviors_codes:
            if len([x[EVENT_BEHAVIOR_FIELD_IDX] for x in events
                                                   if x[EVENT_SUBJECT_FIELD_IDX] == subjects[idx]["name"]
                                                      and x[EVENT_BEHAVIOR_FIELD_IDX] == sbc
                                                      and x[EVENT_TIME_FIELD_IDX] <= time]) % 2: # test if odd
                current_states[idx].append(sbc)

    return current_states


def get_current_points_by_subject(point_behaviors_codes, events, subjects, time, distance):
    """
    get near point events for subjects at given time
    Args:
        point_behaviors_codes (list): list of behavior codes defined as POINT event
        events (list): list of events
        subjects (dict): dictionary of subjects
        time (Decimal): time
        distance (Decimal): distance from time

    Returns:
        dict: current states by subject. dict of list
    """
    current_points = {}
    for idx in subjects:
        current_points[idx] = []
        for sbc in point_behaviors_codes:
            events = [[x[EVENT_BEHAVIOR_FIELD_IDX], x[EVENT_MODIFIER_FIELD_IDX]] for x in events
                                                   if x[EVENT_SUBJECT_FIELD_IDX] == subjects[idx]["name"]
                                                      and x[EVENT_BEHAVIOR_FIELD_IDX] == sbc
                                                      and abs(x[EVENT_TIME_FIELD_IDX] - time) <= distance]
            
            for event in events:
                current_points[idx].append(event)

    return current_points

'''
def get_current_states_modifiers_by_subject(state_behaviors_codes, events, subjects, time):
    """
    get current states and modifiers for subjects at given time
    Args:
        state_behaviors_codes (list): list of behavior codes defined as STATE event
        events (list): list of events
        subjects (dict): dictionary of subjects
        time (Decimal): time

    Returns:
        dict: current state(s) and modifier(s) by subject. dict of list
    """

    current_states = get_current_states_by_subject(state_behaviors_codes, events, subjects, time)
    cm = {}
    for behavior in current_states[subject]:
        for event in events:
            if event[EVENT_TIME_FIELD_IDX] > currentTime:
                break
            if event[EVENT_SUBJECT_FIELD_IDX] == subject:
                if event[EVENT_BEHAVIOR_FIELD_IDX] == behavior:
                    cm[behavior] = event[EVENT_MODIFIER_FIELD_IDX]


    return current_states
'''


def get_ip_address():
    """Get current IP address
    
    Args:
    
    Returns:
        str: IP address
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def check_txt_file(file_name):
    """Extract parameters of txt file (test for tsv csv)
    
    Args:
        filename (str): path of file to be analyzed
        
    Returns:
        dict: 
    """

    # snif txt file
    with open(file_name) as csvfile:
        buff = csvfile.read(1024)
        snif = csv.Sniffer()
        dialect = snif.sniff(buff)

        has_header = snif.has_header(buff)


        logging.debug("dialect.delimiter: {}".format(dialect.delimiter))

    '''data = np.loadtxt(file_name,
                          delimiter=dialect.delimiter,
       #                          usecols=columns,
                          skiprows=has_header  #,
                          #converters=np_converters,
                          )
        

    '''
    
    '''
    # test CSV
    rows_len = []
    with open(file_name, "r") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                if len(row) not in rows_len:
                    rows_len.append(len(row))
                    if len(rows_len) > 1:
                        break
        except:
            return {"error": "Data file error"}

    if len(rows_len) == 1 and rows_len[0] >= 2:
        return {"homogeneous": True, "fields number": rows_len[0], "separator": ","}
    '''
    

    csv.register_dialect("dialect", dialect)
    rows_len = []
    with open(file_name, "r") as f:
        reader = csv.reader(f, dialect="dialect")
        for row in reader:
            logging.debug("row: {}".format(row))
            if not row:
                continue
            if len(row) not in rows_len:
                rows_len.append(len(row))
                if len(rows_len) > 1:
                    break

    # test if file empty
    if not len(rows_len):
        return {"error": "The file is empty"}
    if len(rows_len) == 1 and rows_len[0] >= 2:
        return {"homogeneous": True, "fields number": rows_len[0], "separator": "\t"}
    
    if len(rows_len) > 1:
        return {"homogeneous": False}
    else:
        return {"homogeneous": True, "fields number": rows_len[0]}



'''
def get_set_of_modifiers(text):
    """
    return set of modifiers
    """

    pattern = '~(.*)~'
    match = re.search(pattern, text)
    if match is None:
        return []

    return text[match.start()+1:match.end()-1].split("`")
'''


def extract_frames(ffmpeg_bin, second, currentMedia, fps, imageDir, md5FileName, extension, frame_resize):
    """
    extract frames from media file and save them in imageDir directory
    """

    '''
    ffmpeg_command = '"{ffmpeg_bin}" -ss {second} -loglevel quiet -i "{currentMedia}" -vframes {fps} -qscale:v 2  -vf scale={frame_resize}:-1 "{imageDir}{sep}BORIS@{md5FileName}-{second}_%d.{extension}"'.format(
                    ffmpeg_bin=ffmpeg_bin,
                    second=second,
                    currentMedia=currentMedia,
                    fps=fps,
                    imageDir=imageDir,
                    sep=os.sep,
                    md5FileName=md5FileName,
                    extension=extension,
                    frame_resize=frame_resize
                    )

    '''

    ffmpeg_command = ('"{ffmpeg_bin}" -ss {second_minus1} '
                      '-loglevel quiet '
                      '-i "{currentMedia}" '
                      '-ss 1 '
                      '-frames:v {fps} '
                      '-vf scale={frame_resize}:-1 '
                      '"{imageDir}{sep}BORIS@{md5FileName}-{second}_%d.{extension}"').format(
                    ffmpeg_bin=ffmpeg_bin,
                    second_minus1=second - 1,
                    second=second,
                    currentMedia=currentMedia,
                    fps=fps,
                    imageDir=imageDir,
                    sep=os.sep,
                    md5FileName=md5FileName,
                    extension=extension,
                    frame_resize=frame_resize
                    )

    logging.debug("ffmpeg command: {}".format(ffmpeg_command))

    p = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, error = p.communicate()
    out, error = out.decode("utf-8"), error.decode("utf-8")

    if error:
        logging.debug("ffmpeg error: {}".format(error))


def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def complete(l, max):
    """
    complete list with empty string until len = max
    """
    while len(l) < max:
        l.append("")
    return l


def datetime_iso8601():
    """
    current date time in ISO8601 format
    
    Returns:
        str: date time in ISO8601 format
    """
    return datetime.datetime.now().isoformat().replace("T", "").split(".")[0]


def behavior2color(behavior, behaviors):
    """
    return color for behavior
    """
    return PLOT_BEHAVIORS_COLORS[behaviors.index(behavior)]


def replace_spaces(l):
    return [x.replace(" ", "_") for x in l]


def sorted_keys(d):
    """
    return list of sorted keys of provided dictionary
    """
    return [str(x) for x in sorted([int(x) for x in d.keys()])]


def bestTimeUnit(int):
    """
    Return time in best format

    Keyword argument:
    t -- time (in seconds)
    """
    unit = "s"
    if t >= 60:
        t = t / 60
        unit = "min"
    if t > 60:
        t = t / 60
        unit = "h"
    return t, unit


def intfloatstr(s):
    """
    convert str in int or float or return str
    """

    try:
        val = int(s)
        return val
    except:
        try:
            val = float(s)
            return "{:0.3f}".format(val)
        except:
            return s


def distance(p1, p2):
    """
    distance between 2 points
    """
    x1, y1 = p1
    x2, y2 = p2
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


def angle(p1, p2, p3):
    """
    angle between 3 points (p1 must be the vertex)
    return angle in degree
    """
    return math.acos((distance(p1, p2)**2 + distance(p1, p3)**2 - distance(p2, p3)**2) / (2 * distance(p1, p2) * distance(p1, p3))) / math.pi * 180


def polygon_area(poly):
    """
    area of polygon
    from http://www.mathopenref.com/coordpolygonarea.html
    """
    tot = 0
    for p in range(len(poly)):
        x1, y1 = poly[p]
        n = (p + 1) % len(poly)
        x2, y2 = poly[n]
        tot += x1 * y2 - x2 * y1

    return abs(tot / 2)


def hashfile(fileName, hasher, blocksize=65536):
    """
    return hash of file content
    """
    with open(fileName, 'rb') as afile:
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()


def url2path(url):
    """
    convert URL in local path name
    under windows, check if path name begin with /
    """

    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    # check / for windows
    if sys.platform.startswith('win') and path.startswith('/'):
        path = path[1:]
    return path


def float2decimal(f):
    """
    return decimal value
    """
    return Decimal(str(f))


def time2seconds(time):
    """
    convert hh:mm:ss.s to number of seconds (decimal)
    """
    flagNeg = '-' in time
    time = time.replace("-", "")

    tsplit = time.split(":")

    h, m, s = int(tsplit[0]), int(tsplit[1]), Decimal(tsplit[2])

    if flagNeg:
        return Decimal(- (h * 3600 + m * 60 + s))
    else:
        return Decimal(h * 3600 + m * 60 + s)


def seconds2time(sec):
    """
    convert seconds to hh:mm:ss.sss format
    """
    flagNeg = sec < 0
    sec = abs(sec)

    hours = 0

    minutes = int(sec / 60)
    if minutes >= 60:
        hours = int(minutes / 60)
        minutes = minutes % 60

    secs = sec - hours*3600 - minutes * 60
    ssecs = "%06.3f" % secs

    return "%s%02d:%02d:%s" % ('-' * flagNeg, hours, minutes, ssecs)


def safeFileName(s):
    """
    replace characters not allowed in file name by _
    """
    fileName = s
    notAllowedChars = ['/', '\\']
    for char in notAllowedChars:
        fileName = fileName.replace(char, '_')

    return fileName


def eol2space(s):
    """
    replace EOL char by space for all platforms
    """
    return s.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')


def test_ffmpeg_path(FFmpegPath):
    """
    test if ffmpeg has valid path
    
    Args:
        FFmpegPath (str): ffmepg path to test
        
    Returns:
        bool: True: path found
        str: message
    """

    out, error = subprocess.Popen('"{0}" -version'.format(FFmpegPath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
    logging.debug("test ffmpeg path output: {}".format(out))
    logging.debug("test ffmpeg path error: {}".format(error))

    if (b'avconv' in out) or (b'the Libav developers' in error):
        return False, 'Please use FFmpeg from https://www.ffmpeg.org in place of FFmpeg from Libav project.'

    if (b'ffmpeg version' not in out) and (b'ffmpeg version' not in error):
        return False, "FFmpeg is required but it was not found...<br>See https://www.ffmpeg.org"

    return True, ""


def playWithVLC(fileName):
    """
    play media in filename and return out, fps and has_vout (number of video)
    """

    import vlc
    import time
    instance = vlc.Instance()
    mediaplayer = instance.media_player_new()
    media = instance.media_new(fileName)
    mediaplayer.set_media(media)
    media.parse()
    mediaplayer.play()
    global out
    global fps
    out, fps, result = '', 0, None
    while True:
        if mediaplayer.get_state() == vlc.State.Playing:
            break
        if mediaplayer.get_state() == vlc.State.Ended:
            result = 'media error'
            break
        time.sleep(3)

    if result:
        out = result
    else:
        out = media.get_duration()
    fps = mediaplayer.get_fps()
    nvout = mediaplayer.has_vout()
    mediaplayer.stop()

    return out, fps, nvout


def check_ffmpeg_path():
    """
    check for ffmpeg path
    
    Returns:
        bool: True if ffmpeg path found else False
        str: if bool True returns ffmpegpath else returns error message
    """

    if os.path.isfile(sys.path[0]):  # pyinstaller
        syspath = os.path.dirname(sys.path[0])
    else:
        syspath = sys.path[0]

    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):

        r = False
        if os.path.exists(os.path.abspath(os.path.join(syspath, os.pardir)) + "/FFmpeg/ffmpeg"):
            ffmpeg_bin = os.path.abspath(os.path.join(syspath, os.pardir)) + "/FFmpeg/ffmpeg"
            r, msg = test_ffmpeg_path(ffmpeg_bin)
            if r:
                return True, ffmpeg_bin

        # check if ffmpeg in same directory than boris.py
        if os.path.exists(syspath + "/ffmpeg"):
            ffmpeg_bin = syspath + "/ffmpeg"
            r, msg = test_ffmpeg_path(ffmpeg_bin)
            if r:
                return True, ffmpeg_bin

        # check for ffmpeg in system path
        ffmpeg_bin = "ffmpeg"
        r, msg = test_ffmpeg_path(ffmpeg_bin)
        if r:
            return True, ffmpeg_bin
        else:
            logging.critical("FFmpeg is not available")
            return False, "FFmpeg is not available"

    if sys.platform.startswith("win"):

        r = False
        if os.path.exists(os.path.abspath(os.path.join(syspath, os.pardir)) + "\\FFmpeg\\ffmpeg.exe"):
            ffmpeg_bin = os.path.abspath(os.path.join(syspath, os.pardir)) + "\\FFmpeg\\ffmpeg.exe"
            r, msg = test_ffmpeg_path(ffmpeg_bin)
            if r:
                return True, ffmpeg_bin

        if os.path.exists(syspath + "\\ffmpeg.exe"):
            ffmpeg_bin = syspath + "\\ffmpeg.exe"
            r, msg = test_ffmpeg_path(ffmpeg_bin)
            if r:
                return True, ffmpeg_bin
            else:
                logging.critical("FFmpeg is not available")
                return False, "FFmpeg is not available"

    return False, "FFmpeg is not available"


def accurate_media_analysis(ffmpeg_bin, fileName):
    """
    analyse frame rate and video duration with ffmpeg

    return:
    total number of frames
    duration in ms (for compatibility)
    duration in s
    frame per second
    hasVideo: boolean
    hasAudio: boolean

    if invalid data found:
    return
    -1,
    error_message,
    -1, -1, false, False
    """

    if sys.platform.startswith("win"):
        cmdOutput = "NUL"
    else:
        cmdOutput = "/dev/null"

    command2 = '"{0}" -i "{1}" > {2}'.format(ffmpeg_bin, fileName, cmdOutput)

    p = subprocess.Popen(command2, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    duration, fps, hasVideo, hasAudio = 0, 0, False, False
    try:
        error = p.communicate()[1].decode("utf-8")
    except:
        return int(fps * duration), duration * 1000, duration, fps, hasVideo, hasAudio

    # check for invalid data
    if "Invalid data found when processing input" in error:
        return -1, "Invalid data found when processing input", -1, -1, False, False

    rows = error.split("\n")

    # video duration
    try:
        for r in rows:
            if "Duration" in r:
                duration = time2seconds(r.split('Duration: ')[1].split(',')[0].strip())
                break
    except:
        duration = 0

    # fps
    fps = 0
    try:
        for r in rows:
            if " fps," in r:
                re_results = re.search(', (.{1,10}) fps,', r, re.IGNORECASE)
                if re_results:
                    fps = Decimal(re_results.group(1).strip())
                    break
    except:
        fps = 0

    # check for video stream
    hasVideo = False
    try:
        for r in rows:
            if "Stream #" in r and "Video:" in r:
                hasVideo = True
                break
    except:
        hasVideo = None

    # check for audio stream
    hasAudio = False
    try:
        for r in rows:
            if "Stream #" in r and "Audio:" in r:
                hasAudio = True
                break
    except:
        hasAudio = None

    return int(fps * duration), duration*1000, duration, fps, hasVideo, hasAudio


def behavior_color(colors_list, idx):
    """
    return color with index corresponding to behavior index

    see BEHAVIORS_PLOT_COLORS list in config.py
    """

    return colors_list[idx % len(colors_list)]


class ThreadSignal(QObject):
    sig = pyqtSignal(int, float, float, float, bool, bool, str, str, str)


class Process(QThread):
    """
    process for accurate video analysis
    """
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.filePath = ''
        self.ffmpeg_bin = ''
        self.fileContentMD5 = ''
        self.nPlayer = ''
        self.filePath = ''
        self.signal = ThreadSignal()

    def run(self):
        nframe, videoTime, videoDuration, fps, hasVideo, hasAudio = accurate_media_analysis(self.ffmpeg_bin,
                                                                                            self.filePath)
        self.signal.sig.emit(nframe,
                             videoTime,
                             videoDuration,
                             fps,
                             hasVideo,
                             hasAudio,
                             self.fileContentMD5,
                             self.nPlayer,
                             self.filePath)
