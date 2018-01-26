#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""随机密码生成和密码加密模块"""

import re
import random
import hashlib


class Encryption:
    """生成随机码"""

    @staticmethod
    def generate_randauid(strs='-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
                          size=64):
        auid = ''
        while size > 0:
            auid = auid + random.choice(strs)
            size = size - 1

        return auid

    @staticmethod
    def generate_randsalt(strs='0123456789abcdefghijklmnopqrstuvwxyz', size=8):
        salt = ''
        while size > 0:
            salt = salt + random.choice(strs)
            size = size - 1

        return salt

    @staticmethod
    def generate_randatms(strs='0123456789', size=8):
        salt = ''
        while size > 0:
            salt = salt + random.choice(strs)
            size = size - 1

        return salt

    """加密"""

    @staticmethod
    def generate_password(pswd, salt):
        return hashlib.md5(
            'AL.pswd:' + hashlib.md5(str(pswd) + '#' + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def generate_smscode(code):
        return hashlib.md5(
            'AL.smscode:' + hashlib.md5(str(code) + '#').hexdigest()).hexdigest()

    @staticmethod
    def generate_authword(atms, salt):
        return hashlib.md5(
            'AL.auth:' + hashlib.md5(str(atms) + '$' + str(salt)).hexdigest()).hexdigest()

    @staticmethod
    def chk_is_user_name(name):
        return 3 < len(name) < 32 and re.match('^[A-Za-z0-9](?:[-_]?[A-Za-z0-9]+)+$', name)

    @staticmethod
    def chk_is_user_pswd(pswd):
        return len(pswd) >= 6

    @staticmethod
    def chk_is_user_mail(mail):
        return 3 < len(mail) < 64 and re.match(
            '^[^@\\.]+(?:\\.[^@\\.]+)*@[^@\\.]+(?:\\.[^@\\.]+)+$', mail)

    @staticmethod
    def chk_is_not_null(word):
        return 3 < len(word) < 64

    @staticmethod
    def chk_user_if_perm(user):
        if user.role_id in (1, 2):
            return user
        else:
            return False

    @staticmethod
    def chk_user_is_live(user):
        return Encryption.chk_user_if_perm(user)

    @staticmethod
    def chk_user_is_root(user):
        return Encryption.chk_user_if_perm(user)
