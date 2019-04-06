#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

import uuid, os


def custom_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    return filename


class Reader(models.Model):
    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='读者')
    name = models.CharField(max_length=16, verbose_name='姓名')
    phone = models.CharField(max_length=100, unique=True, verbose_name='电话')
    max_borrowing = models.IntegerField(default=5, verbose_name='可借数量')
    balance = models.FloatField(default=0.0, verbose_name='余额')
    photo = models.ImageField(blank=True, default='default.jpg', upload_to=custom_path, verbose_name='头像')

    STATUS_CHOICES = (
        (0, 'normal'),
        (-1, 'overdue')
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

    ISBN = models.CharField(max_length=13, primary_key=True, verbose_name='ISBN')
    title = models.CharField(max_length=128, verbose_name='书名')
    author = models.CharField(max_length=32, verbose_name='作者')
    press = models.CharField(max_length=64, verbose_name='出版社')

    description = models.CharField(max_length=1024, default='', verbose_name='详细')
    price = models.CharField(max_length=20, null=True, verbose_name='价格')

    category = models.CharField(max_length=64, default=u'文学', verbose_name='分类')
    cover = models.ImageField(blank=True, default='default.jpg', upload_to=custom_path, verbose_name='封面')
    index = models.CharField(max_length=16, null=True, verbose_name='索引')
    location = models.CharField(max_length=64, default=u'图书馆1楼', verbose_name='位置')
    quantity = models.IntegerField(default=1, verbose_name='数量')

    def __str__(self):
        return self.title + self.author


class Borrowing(models.Model):
    class Meta:
        verbose_name = '借阅'
        verbose_name_plural = '借阅'

    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='ISBN')
    date_issued = models.DateField(verbose_name='借出时间')
    date_due_to_returned = models.DateField(verbose_name='应还时间')
    date_returned = models.DateField(null=True, verbose_name='还书时间')
    amount_of_fine = models.FloatField(default=0.0, verbose_name='欠款')

    def __str__(self):
        return '{} 借了 {}'.format(self.reader, self.ISBN)


class Demand(models.Model):
    class Meta:
        verbose_name = '读者需求'
        verbose_name_plural = '读者需求'
    choices = [
        ('checking', '审核中'),
        ('accepted', '已接受申请'),
        ('refused', '拒绝申请'),
        ('bought', '图书已购买')
    ]
    msg = models.CharField(max_length=100, default='请求正在审核,工作人员会在三个工作日内给出答复。')
    status = models.CharField(max_length=100, choices=choices, default='checking')
    # reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='读者')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    book_name = models.CharField(max_length=100, verbose_name='书名')
    book_author = models.CharField(max_length=100, verbose_name='作者')
    note = models.TextField(verbose_name='备注')

    def __str__(self):
        return self.book_name
