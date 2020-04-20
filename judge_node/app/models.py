from django.db import models


# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '试题类型'

    name = models.CharField(max_length=100, default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Problem(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '试题'

    title = models.CharField(max_length=100, default='', blank=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True)
    difficulty = models.CharField(max_length=50, default='', blank=True)
    content = models.TextField(default='', blank=True)
    deadline = models.DateTimeField(blank=True, null=True, default=None)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'tag': self.tag.name,
            'difficulty': self.difficulty,
            'content': self.content,
            'deadline': self.deadline,
            'create_time': self.create_time
        }

    @property
    def list_view(self):
        return {
            'id': self.id,
            'title': self.title,
            'tag': self.tag.name,
            'difficulty': self.difficulty
        }


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

    @property
    def json(self):
        return {
            'id': self.id,
            'tno': self.tno,
            'name': self.name,
        }


class TClass(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '班级'

    name = models.CharField(max_length=50, default='', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'teacher': self.teacher.json,
        }


class Student(models.Model):
    class Meta:
        verbose_name = verbose_name_plural = '学生'

    sno = models.CharField(max_length=50, default='', blank=True)
    name = models.CharField(max_length=50, default='', blank=True)
    tclass = models.ForeignKey(TClass, on_delete=models.CASCADE, blank=True)
    password = models.CharField(max_length=50, default='', blank=True)

    create_time = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    @property
    def json(self):
        return {
            'id': self.id,
            'sno': self.sno,
            'name': self.name,
            'tclass': self.tclass.json,
        }


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

    @property
    def json(self):
        return {
            'id': self.id,
            'problem': self.problem.json,
            'code': self.code,
            'if_compile': self.if_compile,
            'compile_error': self.compile_error,
            'if_run': self.if_run,
            'run_error': self.run_error,
            'run_seconds': self.run_seconds,
            'memory_used': self.memory_used,
            'create_time': self.create_time
        }


    @property
    def list_view(self):
        return {
            'id': self.id,
            'problem': [self.problem.id, self.problem.title], # return id, title of problem
            'if_compile': self.if_compile,
            'if_run': self.if_run,
            'create_time': self.create_time,
            'run_seconds': self.run_seconds
        }
