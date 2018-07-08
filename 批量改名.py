import os
import re

RE_NAME = "Sashow@subpig.net@Disc.\d+\.(.+)"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    # [0]代表只walk第0层
    os_walk = list(os.walk(BASE_DIR))
    files = os_walk[0][2]
    for file_name in files:
        if file_name.endswith("py"): continue
        new_name = re.findall(RE_NAME, file_name)
        if new_name:
            print(new_name)
            new_name = new_name[0]
            old_file = os.path.join(BASE_DIR, file_name)
            new_file = os.path.join(BASE_DIR, new_name)
            try:
                os.rename(old_file, new_file)
            except:
                pass
