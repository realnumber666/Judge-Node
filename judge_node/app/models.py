from django.db import models


# Create your models here.
class PType(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '试题类型'

    name = models.CharField(max_length=100, default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Problem(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '试题'

    type = models.ForeignKey(PType, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, default='', blank=True)
    content = models.TextField(default='', blank=True)
    deadline = models.DateTimeField(blank=True, null=True, default=None)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Testcase(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '测试用例'

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True)
    no = models.IntegerField(default=1)
    input = models.TextField(default='', blank=True)
    output = models.TextField(default='', blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Teacher(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '老师'

    tno = models.CharField(max_length=50, default='', blank=True)
    name = models.CharField(max_length=50, default='', blank=True)
    password = models.CharField(max_length=50, default='', blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class TClass(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '班级'

    name = models.CharField(max_length=50, default='', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Student(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '学生'

    sno = models.CharField(max_length=50, default='', blank=True)
    name = models.CharField(max_length=50, default='', blank=True)
    tclass = models.ForeignKey(TClass, on_delete=models.CASCADE, blank=True)
    password = models.CharField(max_length=50, default='', blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Submission(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '提交记录'

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)

    code = models.TextField(default='', blank=True)
    if_compile = models.BooleanField(default=True, blank=True)
    compile_error = models.TextField(default='', blank=True)
    if_run = models.BooleanField(default=True, blank=True)
    run_error = models.TextField(default='', blank=True)

    run_seconds = models.IntegerField(default=1)
    memory_used = models.IntegerField(default=1)

    create_time = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
