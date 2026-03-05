#!/usr/bin/env python
#-*- coding:utf-8 -*-

import redis

conn = redis.Redis()

def task_empty():
    # 请在下面完成判断任务列表是否为空
    #********* Begin *********#
    return True if conn.llen("task_list") == 0 else False
    #********* End *********#

def get_task():
    # 请在下面完成获取一个任务
    #********* Begin *********#
    task = conn.rpop("task_list")
    conn.set("current_task", task)

    #********* End *********#

def get_unallocated_staff():
    # 请在下面完成获取一个未分配的员工
    #********* Begin *********#
    staff = conn.srandmember("unallocatrd_staff")
    conn.smove("unallocated_staff", "allocated_staff", staff)
    return staff

    #********* End *********#

def allocate_task(staff):
    # 请在下面完成分配任务
    #********* Begin *********#
    conn.append("current_task", ":" + staff)
    conn.lpush("task-queue", conn.get("current_task"))
    conn.set("current_task", "None")

    #********* End *********#
