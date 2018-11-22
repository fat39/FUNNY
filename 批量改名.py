# 之前写的
# import os
# import re
# 
# RE_NAME = "Sashow@subpig.net@Disc.\d+\.(.+)"
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 
# if __name__ == '__main__':
#     # [0]代表只walk第0层
#     os_walk = list(os.walk(BASE_DIR))
#     files = os_walk[0][2]
#     for file_name in files:
#         if file_name.endswith("py"): continue
#         new_name = re.findall(RE_NAME, file_name)
#         if new_name:
#             print(new_name)
#             new_name = new_name[0]
#             old_file = os.path.join(BASE_DIR, file_name)
#             new_file = os.path.join(BASE_DIR, new_name)
#             try:
#                 os.rename(old_file, new_file)
#             except:
#                 pass

# 后来写的
import os
import re

class F():
    @classmethod
    def get_obj(cls,args):
        obj = cls()
        translate = {0: "zero", 1: "first", 2: "second", 3: "third", 4: "forth",5:"fifth",6:"sixth"}
        for idx,arg in enumerate(args):
            setattr(obj,translate[idx],arg)
            # print(obj.__dict__)
        return obj

def file_rename(target_dir, re_filename, new_file_format, check_name=True):
    os_walk = os.walk(target_dir)
    for file_name in next(os_walk)[2]:
        res = re_filename.findall(file_name)
        if res:
            res = res[0]
            obj = F.get_obj(res)
            new_file_name = new_file_format.format(obj=obj)
            if check_name:
                print(res,new_file_name)
            else:
                new_file_path = os.path.join(target_dir, new_file_name)
                old_file_path = os.path.join(target_dir, file_name)
                os.rename(old_file_path, new_file_path)


if __name__ == '__main__':
    target_dir = "D:\下载\迅雷下载\头文字D.Initial.D\Initial.D_Stage5"
    re_filename = re.compile("Initial D Fifth Stage - (.{2}).(mkv)")
    new_file_format = "{obj.zero}集 头文字D 第5季.{obj.first}"
    file_rename(target_dir,re_filename,new_file_format,check_name=True)