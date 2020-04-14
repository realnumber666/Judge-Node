import os
import time
from .utils import *
from meta.decorators import api, APIError, comments, errors, params, returns

@api
def submission(user_id, problem_id, code):
    # 把代码保存到本地（函数结束前记得删除）
    timestamp = str(int(time.time()))
    file_name = timestamp + "_" +str(user_id) + "_" + str(problem_id)  # 不带路径，不带.c的纯文件名
    file_path = os.path.join(dir_work, file_name) + ".c" # 带路径，带.c的全路径名

    c_file = open(file_path, "a")
    c_file.write(code)
    c_file.close()

    # 编译代码
    try:
        compile_code(file_name)
    except Exception as e:
        return str(e)

    # 若编译失败，记录提交记录，返回失败原因


    # 根据题号从数据库中获得测试用例
    result = run_code(file_name)

    # 依次运行每一个测试用例，对比输入输出
    # 一旦发现输入输出不同则退出循环，记录提交记录，返回错误的输出和应有输出

    # 若全部运行通过，记录运行时间

    # 返回结果
    return result