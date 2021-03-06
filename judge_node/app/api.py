import os
import time
from .utils import *
from .models import *
from meta.decorators import api, APIError, comments, errors, params, returns

"""Judge"""
@api
def submit(user_id, problem_id, code):
    # TODO 校验user_id
    # 找到该学生和该题
    student = Student.objects.get(id=user_id)
    problem = Problem.objects.get(id=problem_id)
    subm = Submission.objects.create(student=student, problem=problem)
    subm.code = code

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
        # 若编译失败，记录提交记录，返回失败原因
        subm.if_compile = False
        subm.compile_error = str(e)
        return str(e)

    subm.if_compile = True

    # 根据题号从数据库中获得测试用例
    ts = Testcase.objects.filter(problem__id=problem_id)
    testcase = []
    for t in ts:
        i = t.input
        o = t.output
        testcase.append([i, o])

    # result存在，即代表有错误
    result = run_code(testcase, file_name)

    if result:
        # 若失败，记录对比结果
        subm.if_run = False
        subm.run_error = str(result)
    else:
        # 若全部运行通过，记录运行时间
        subm.if_run = True

    subm.save()

    # 返回结果
    return result


"""Problem"""
@api
def problem_list(user_id=1, tag=''):
    # TODO: 校验user_id
    if not tag:
        p_list = Problem.objects.all()
    else:
        t = Tag.objects.get(name=tag)
        p_list = Problem.objects.filter(tag=t)

    return [p.list_view for p in p_list]


@api
def problem(user_id, problem_id):
    # TODO: 校验user_id
    try:
        p = Problem.objects.get(id=problem_id)
    except Exception as e:
        return_api_error(1001, str(e))

    return p.json


"""Submission"""
@api
def submission_list(user_id='', problem_id=''):
    student = Student.objects.get(id=user_id)
    problem = Problem.objects.get(id=problem_id)

    submissions = Submission.objects.filter(student=student, problem=problem)

    return [subm.list_view for subm in submissions]


@api
def submission(user_id, submission_id):
    student = Student.objects.get(id=user_id)
    try:
        subm = Submission.objects.get(id=submission_id, student=student)
    except Exception as e:
        return_api_error(1001, str(e))

    if subm:
        return subm.json
    else:
        return_api_error(1001)


"""General User"""
@api
def create_teacher(tno, name, pwd):
    t = Teacher.objects.create(tno=tno,name=name,password=pwd)

    # TODO create token then return it
    return t.json


@api
def create_class(name, teacher_id):
    t = Teacher.objects.get(id=teacher_id)
    c = TClass.objects.create(name=name, teacher=t)

    return c.json


@api
def create_student(sno, name, class_id, pwd):
    c = TClass.objects.get(id=class_id)
    s = Student.objects.create(sno=sno, name=name, tclass=c, password=pwd)

    # TODO create token then return it
    return s.json


@api
def login(_type, no, pwd):
    if _type == "student":
        student = Student.objects.filter(sno=no)
        if not student.exists():
            return_api_error(3001)
        else:
            student = student.first()
            if pwd == student.password:
                token = create_token(student.id, 'student')
                return token
            else:
                return_api_error(1004)

    if _type == "teacher":
        teacher = Teacher.objects.filter(tno=no)
        if not teacher.exists():
            return_api_error(2001)
        else:
            teacher = teacher.first()
            if pwd == teacher.password:
                token = create_token(teacher.id, "teacher")
                return token
            else:
                return_api_error(1004)