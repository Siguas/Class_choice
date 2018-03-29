#!/usr/bin/env python
#-*- coding:utf-8 -*-
#Author:SiWen
import os
import sys
import shelve
from config import settings
from modules.school import School


class Main(object):
    def __init__(self):
        pass

    def run(self):
        while True:
            print('''_______欢迎进入选课系统_______
                            1.学生视图
                            2.讲师视图
                            3.学校视图
                            q.返回主界面''')
            user_choice = input('请输入您的选择：')
            if user_choice == '1':
                Manage_student()
            if user_choice == '2':
                Manage_teacher()
            if user_choice == '3':
                Manage_school()
            if user_choice == 'q':
                print('您已退出系统，返回主界面')
                break
            else:
                print('请输入正确选项')


class Manage_school(object):
    # 学校视图
    def __init__(self):
        if os.path.exists(settings.school_db_file + '.dat'):
            self.school_db = shelve.open(settings.school_db_file)  # 打开数据库
            self.run_manage()
            self.school_db.close()  # 关闭数据库

        else:
            print('初始化数据库')
            self.initialize_school()
            self.run_manage()
            self.school_db.close()

    def initialize_school(self):
        self.school_db = shelve.open(settings.school_db_file)
        self.school_db['北京'] = School('中国*北京', '北京')
        self.school_db['上海'] = School('中国*上海', '上海')

    def run_manage(self):
        while True:
            for key in self.school_db:
                print('学校名称：', key)
            school_choice = input('请选择学校名称：').strip()
            self.school_choice = school_choice
            if school_choice in self.school_db:
                self.school_obj = self.school_db[school_choice]

                while True:
                    print("\n欢迎来到老男孩%s校区\n"
                          "添加课程 add_course\n"
                          "增加班级 add_class\n"
                          "招聘讲师 add_teacher\n"
                          "查看课程 check_course\n"
                          "查看班级 check_class\n"
                          "查看讲师 check_teacher\n"
                          "退出程序 exit" % self.school_obj.school_name)
                    user_func = input('请输入要进行的操作：').strip()
                    if hasattr(self, user_func):
                        getattr(self, user_func)()
            else:
                print('Please input right school name')

    def add_course(self):
        course_name = input('请输入课程名称').strip()
        course_price = input('请输入课程价格').strip()
        course_time = input('请输入课程3'
                            '周期').strip()
        if course_name in self.school_obj.school_course:
            print('课程已存在')
            self.school_obj.create_course(course_name, course_price, course_time)
            print("课程更新完成")
        else:
            self.school_obj.create_course(course_name, course_price, course_time)
            print("课程添加成功")

        self.school_db.update({self.school_choice: self.school_obj})

    def add_teacher(self):
        teacher_name = input('请输入讲师名字').strip()
        teacher_salary = input('请输入讲师工资').strip()
        teacher_class = input('请输入讲师的班级').strip()
        if teacher_class in self.school_obj.school_class:
            class_obj = self.school_obj.school_class[teacher_class]
            if teacher_name not in self.school_obj.school_teacher:
                self.school_obj.create_teacher(teacher_name, teacher_salary, teacher_class.class_obj)
                print('新讲师聘用成功')
            else:
                self.school_obj.update_teacher(teacher_name, teacher_salary, teacher_class.class_obj)
                print('讲师信息更新成功')
        else:
            print('关联课程不存在，请输入正确班级')
        self.school_db.update({self.school_choice: self.school_obj})  # 更新数据库

    def add_class(self):
        class_name = input('请输入班级名称').strip()
        course_name = input('请输入开设课程').strip()
        if class_name not in self.school_obj.school_class:
            if course_name in self.school_obj.school_course:
                course_obj = self.school_obj.school_course[course_name]
                self.school_obj,creat_class(class_name,course_obj)
                self.school_db.update({self.school_choice: self.school_obj})  # 更新数据库
                print('课程添加成功')
            else:
                print ('系统错误，课程不存在')
        else:
            print('系统错误，班级已存在')

    def check_course(self):
        self.school_obj.show_course()

    def check_class(self):
        self.school_obj.show_class()

    def check_teacher(self):
        self.school_obj.show_teacher()

    def exit(self):
        self.school_db.close()
        sys.exit("\033[32;1m欢迎下次使用学员管理系统\033[0m")
class Manage_teacher(object):
    def __init__(self):
        if os.path.exists(settings.school_db_file + ".dat"):  # shelve会生成三个文件，其中有.dat结尾
            self.school_db = shelve.open(settings.school_db_file)  # 打开学校数据库文件
            self.run_manage()  # 运行管理视图
            self.school_db.close()  # 关闭数据库文件
        else:
            print("\033[31;1m数据库文件不存在，请先创建学校\033[0m")
            exit()

    def run_manage(self):
        print('欢迎进入讲师视图')
        for key in self.school_db:
            print("学校名称：", key)
        choice_school = input("\33[34;0m输入选择学校名:\33[0m").strip()
        self.school_choice = choice_school
        if self.school_choice in self.school_db:
            self.school_obj = self.school_db[choice_school]
            teacher_name = input('请输入讲师姓名')
            while True:
                if teacher_name in self.school_obj.school_teacher:
                    print('''欢迎进入讲师视图
                            查看班级 check_class
                            退出     exit''')
                    user_func = input('请选择所需操作')
                    if hasattr(self,user_func):
                        getattr(self,user_func)()

                else:
                    print('教师不存在')
                    break

    def check_class(self, teacher_name):
        self.school_obj.show_teacher_classinfo(teacher_name)

    def exit(self, *args):
        self.school_db.close()
        sys.exit("\033[32;1m欢迎下次使用学员管理系统\033[0m")

class Manage_student(object):
    def __init__(self):
        if os.path.exists(settings.school_db_file + ".dat"):  # shelve会生成三个文件，其中有.dat结尾
            self.school_db = shelve.open(settings.school_db_file)  # 打开学校数据库文件
            self.run_manage()  # 运行管理视图
            self.school_db.close()  # 关闭数据库文件
        else:
            print("\033[31;1m数据库文件不存在，请先创建学校\033[0m")
            exit()

    def run_manage(self):
        print('欢迎来到学员视图')
        school_choice = input('请选择学校')
        if school_choice in self.school_db:
            self.school_choice = school_choice
            self.school_obj = self.school_db[school_choice]
            student_name = input('''\033[34;0m输入学生的姓名：\033[0m''').strip()
            student_age = input('''\033[34;0m输入学生的年龄：\033[0m''').strip()
            self.school_obj.show_class_course()
            class_choice = input('''\033[34;0m输入上课的班级：\033[0m''').strip()
            if class_choice in self.school_obj.school_class:
                self.school_obj.create_student(student_name, student_age, class_choice)
                self.school_db.update({self.choice_school: self.school_obj})  # 更新数据库数据
                print("\33[32;1m学生注册成功\33[0m")
            else:
                print("\33[31;1m系统错误：输入的班级不存在\33[0m")
        else:
            print("\33[31;1m系统错误：输入的学校不存在\33[0m")
