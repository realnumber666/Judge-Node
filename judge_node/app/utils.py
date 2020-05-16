import os
import jwt
import datetime
import subprocess
from meta.decorators import APIError

# jwt token使用的参数
secret_key = 'dian_oj_sk'
algorithm = 'HS256'

base_dir = "./"
dir_work = "./submission_code/"

api_error_dictionary = {
    1001: "内容不存在",
    1002: "权限不足",
    1003: "Token校验失败",
    1004: "密码错误",

    2001: "该老师账号不存在",

    3001: "该学生账号不存在",
}


# APIError 只写error code
def return_api_error(code, msg=''):
    if msg:
        raise APIError(code=code, msg=msg)
    else:
        raise APIError(code=code, msg=api_error_dictionary[code])

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
                return {t[0]: [t[1], out]} # {input: [should be, but get]}

        return None


# 生成token
def create_token(user_id, role):
    payload = {
        'iat': datetime.datetime.utcnow(), # 发布时间
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), # 一天后过期
        'data': {
            'role': role,
            'user_id': user_id
        }
    }

    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    token = token.decode("utf-8")

    return token


# 校验token
def check_token(token):
    """
    返回值中的role可能为"student", "teacher"
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
    except Exception as e:
        # 内容被篡改、过期、算法不正确、密钥不正确 => 抛出异常
        raise str(e)
    else:
        res = {
            'user_id': payload['data']['user_id'],
            'role': payload['data']['role']
        }

        return res


def check_teacher_by_token(token):
    from .models import Teacher

    try:
        res = check_token(token)
    except Exception as e:
        return_api_error(1003)

    if res['role'] != 'teacher':
        return_api_error(1002)

    try:
        teacher = Teacher.objects.get(id=res['user_id'])
    except Exception as e:
        return_api_error(2001)

    return teacher


def check_student_by_token(token):
    from .models import Student

    try:
        res = check_token(token)
    except Exception as e:
        return_api_error(1003)

    if res['role'] != 'student':
        return_api_error(1002)

    try:
        student = Student.objects.get(id=res['user_id'])
    except Exception as e:
        return_api_error(2001)

    return student
