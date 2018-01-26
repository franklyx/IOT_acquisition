#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
tools.jwtserializer
~~~~~~~~~~~~~~~~~~~

token,和rf_tokend的生成和验证的功能模块
"""
import time

from tools.cfgparser import parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature, BadData


def genTokenSeq(user_id, user_role, expires):
    """
    生成token码
    :param user_id: 用户id
    :param user_role: 用户角色
    :param expires: 有效期
    :return: 成功返回token
    """
    s = Serializer(
        secret_key=parser.secret_key_token,
        salt=parser.auth_salt,
        expires_in=expires)
    timestamp = time.time()
    return s.dumps(
        {'user_id': user_id,
         'user_role': user_role,
         'iat': timestamp})


def genRfTokenSeq(user_id, user_role, expires):
    """
    生成rf_token
    :param user_id: 用户id
    :param user_role: 用户角色
    :param expires: 有效期
    :return: 成功返回rf_token
    """
    s = Serializer(
        secret_key=parser.secret_key_rf_token,
        salt=parser.auth_salt,
        expires_in=expires)
    timestamp = time.time()
    return s.dumps(
        {'user_id': user_id,
         'user_role': user_role,
         'iat': timestamp})


def tokenAuth(token):
    """
    token验证模块
    验证token的正确性，有效性，以及是否被修改
    :param token: token码
    :return: 通过返回 [userId, roleId, msg]
            未通过返回 None, None, msg]
    """
    s = Serializer(
        secret_key=parser.secret_key_token,
        salt=parser.auth_salt)
    try:
        data = s.loads(token)
    except SignatureExpired:
        msg = 'token expired'
        return [None, None, msg]
    except BadSignature, e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                # the token is tampered.
                msg = 'token tampered'
                return [None, None, msg]
        msg = 'badSignature of token'
        return [None, None, msg]
    except:
        msg = 'wrong token with unknown reason'
        return [None, None, msg]
    if ('user_id' not in data) or ('user_role' not in data):
        msg = 'illegal payload inside'
        return [None, None, msg]
    msg = 'user(' + data['user_id'] + ') logged in by token.'
    userId = data['user_id']
    roleId = data['user_role']
    return [userId, roleId, msg]


def RftokenAuth(rf_token):
    """
    rf_token验证模块
    验证rf_token的正确性，有效性，以及是否被修改
    :param rf_token: rf_token码
    :return: 通过返回用户名，用户角色，和最新的token的列表
             未通过返回[None, None, msg]
    """
    s = Serializer(
        secret_key=parser.secret_key_rf_token,
        salt=parser.auth_salt)
    try:
        data = s.loads(rf_token)
    except SignatureExpired:
        msg = 'token expired'
        return [None, None, msg]
    except BadSignature, e:
        encoded_payload = e.payload
        if encoded_payload is not None:
            try:
                s.load_payload(encoded_payload)
            except BadData:
                # the token is tampered.
                msg = 'token tampered'
                return [None, None, msg]
        msg = 'badSignature of token'
        return [None, None, msg]
    except:
        msg = 'wrong token with unknown reason'
        return [None, None, msg]
    if ('user_id' not in data) or ('user_role' not in data):
        msg = 'illegal payload inside'
        return [None, None, msg]
    userId = data['user_id']
    role = data['user_role']
    result = [userId, role, genTokenSeq(user_id=userId, user_role=role, expires=7200)]
    return result
