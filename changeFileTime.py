import re
import os
from datetime import datetime
from ctypes import windll, wintypes, byref

def getTimefromFilename(filename:str):

    pat1 = re.compile('(20\d{2})[_-]?(\d{2})[_-]?(\d{2})[_\s-]?(\d{2})[_-]?(\d{2})[_-]?(\d{2})?')
    pat2 = re.compile('1\d{12}')
    res1 = re.findall(pat1, filename)
    #handle err
    if len(res1) != 0:
        try:
            castedres = [int(elem) for elem in res1[0]]
        except:
            print(f'{filename} valueerror')
            return None, -1
        time = datetime(*castedres)
        utime = time.timestamp()
        return utime, None
    else:
        res2 = re.findall(pat2, filename)
        # handle err
        if len(res2) != 0:
            utime = int(res2[0])
            return utime, None
        else:
            return None, -1

# from exif import Image
#
# file = os.path.join(path, filename)
# with open(file, "rb") as palm_1_file:
#     image = Image(palm_1_file)
# print(image.has_exif)


def changeFileTime(filename, utime):
    # Convert Unix timestamp to Windows FileTime using some magic numbers
    # See documentation: https://support.microsoft.com/en-us/help/167296
    timestamp = int((utime * 10000000) + 116444736000000000)
    ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)

    # Call Win32 API to modify the file creation date
    handle = windll.kernel32.CreateFileW(filename, 256, 0, None, 3, 128, None)
    windll.kernel32.SetFileTime(handle, byref(ctime), None, None)
    windll.kernel32.CloseHandle(handle)

def changeTime(filename):
    utime, err = getTimefromFilename(filename)
    if err is not None:
        return -1
    else:
        changeFileTime(filename, utime)
        return 0
