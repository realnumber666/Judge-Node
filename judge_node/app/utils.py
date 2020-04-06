import os
import subprocess
dir_work = "./"


def compile():
    # build_cmd = {
    #     "gcc": "gcc main.c -o main -Wall -lm -O2 -std=c99 --static -DONLINE_JUDGE",
    # }
    build_cmd = "gcc main.c -o main"
    p = subprocess.Popen(build_cmd, shell=True, cwd=dir_work, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # 获取编译错误信息
    out,err = p.communicate()

    # 返回值为0,编译成功
    if p.returncode == 0:
        return True

    print(err,out)
    return False

def run():
    if os.path.exists('./main'):
        rc, out = subprocess.getstatusoutput('./main')
        print(rc, out)


if __name__ == '__main__':
    compile()
    run()