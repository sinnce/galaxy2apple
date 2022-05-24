import os
import glob
import hashlib
import imghdr
from changeFileTime import changeTime
from tqdm import tqdm
class Hashchk:
    def __init__(self):
        self._hashes = []

    def __call__(self, filename):
        with open(filename, 'rb') as f:
            bindata = f.read()
            fhash = hashlib.md5(bindata).hexdigest()
        try:
            self._hashes.index(fhash)
            return fhash # 중복
        except:
            self._hashes.append(fhash)

def main(root_path:str="C:/Users/user/Pictures/galaxy note 10/"):
    # subdirs = glob.glob('./**/', recursive=True)

    log_path = '../log'
    os.chdir(root_path)
    os.mkdir(log_path)
    hashchk = Hashchk()

    def fwrite(fname, list):
        fullpath = os.path.join(log_path, fname)
        with open(fullpath, 'a') as f:
            for line in list:
                f.write(line+os.linesep)

    for (root, directories, files) in os.walk(root_path):
        print('-----------------------------------------')
        print(f'entering {root}, {len(files)} files found')
        nonimglist = []
        timenotchangedlist = []
        duplicatedlist = []
        if root.endswith('Cache'):
            print('skip ipod cache directories')
            break
        for file in tqdm(files):
            # for every img file
            fpath = os.path.join(root, file)
            if imghdr.what(fpath) is not None:
                # hash 중복 체크
                duphash = hashchk(fpath)
                if duphash is not None:
                    duplicatedlist.append(fpath)
                # file 시간 변경
                if changeTime(fpath) == -1:
                    timenotchangedlist.append(fpath)
            else:
                nonimglist.append(fpath)

        if len(timenotchangedlist) != 0:
            print(f'{len(timenotchangedlist)}files cannot change time')
            fwrite('notchanged_files.txt', timenotchangedlist)
        if len(duplicatedlist) != 0 or len(nonimglist) != 0:
            print(f'{len(duplicatedlist)} duplicated files found. {len(nonimglist)} files considered as not image')
            fwrite('duplicated_files.txt', duplicatedlist)
            fwrite('nonimage_files.txt',nonimglist)

if __name__ == '__main__':
    # main("C:/Users/user/Desktop/test/")
    main()
