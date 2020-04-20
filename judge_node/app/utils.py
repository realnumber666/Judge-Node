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

def run_code(ts, file_name):
    # 依次运行每一个测试用例，对比输入输出
    # 一旦发现输入输出不同则退出循环，记录提交记录，返回错误的输出和应有输出
    file_path = os.path.join(dir_work, file_name)
    if os.path.exists(file_path):
        for t in ts:
            rc, out = subprocess.getstatusoutput(file_path+' '+t[0])
            if out != t[1]:
                return {t[0]: [t[1], out]} # [should be, but get]

        return None



# if __name__ == '__main__':
#     compile_code()
#     run_code()