import os
import subprocess
base_dir = "./"
dir_work = "./submission_code/"


def compile_code(file_name):
    # build_cmd = {
    #     "gcc": "gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
    # }
    build_cmd = "gcc " + file_name + ".c -o " + file_name
    p = subprocess.Popen(build_cmd, shell=True, cwd=dir_work, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 获取编译错误信息
    out, err = p.communicate()

    # 返回值为0,编译成功
    if p.returncode == 0:
        return True

    raise Exception(err)

def run_code(file_name):
    file_path = os.path.join(dir_work, file_name)
    if os.path.exists(file_path):
        rc, out = subprocess.getstatusoutput(file_path)
        return out


# if __name__ == '__main__':
#     compile_code()
#     run_code()