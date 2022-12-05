#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# API: https://dwz.cn/console/apidoc/v3

import json
import re
import socket
from urllib import parse

import requests
from enum import Enum

SCHEMES = ("http", "https")


class TOV(Enum):
    """
    term of validity
    """
    ONE_YEAR = "1-year"
    LONG_TERM = "long-term"

    @classmethod
    def check(cls, tov):
        """
        check term of validity, raise error when invalid
        :param tov: term of validity
        :return: ValueError
        """
        values = (cls.ONE_YEAR, cls.LONG_TERM)
        if tov not in values:
            raise ValueError("invalid term of validity: {}, expect {}".format(tov, values))


def check_long_url(long_url):
    """
    check long URL, raise error when invalid
    invalid include:
    1. invalid scheme
    2. IP host
    :param long_url:
    :return: ValueError
    """
    url = parse.urlparse(long_url)

    # check scheme
    if url.scheme.lower() not in SCHEMES:
        raise ValueError("invalid scheme: {}, expect {}".format(url.scheme.lower(), SCHEMES))

    # check host
    try:
        # test for IPv4
        socket.inet_pton(socket.AF_INET, url.hostname)
    except socket.error:
        try:
            # test for IPv6
            ipv6 = str.rstrip(str.lstrip(url.hostname, '['), ']')
            socket.inet_pton(socket.AF_INET6, ipv6)
        except socket.error:
            # host isn't IP (expected)
            pass
        else:
            raise ValueError("invalid host in {}, unexpected IPv6 {}".format(long_url, ipv6))
    else:
        raise ValueError("invalid host in {}, unexpected IPv4 {}".format(long_url, url.hostname))


def parse_short_url(short_url: str):
    """
    parse domain and path for short URL
    :param short_url:
    :return: domain, path
    :exception: ValueError
    """
    result = parse.urlsplit(short_url)
    if not result.netloc.endswith("dwz.cn"):
        raise ValueError("invalid short domain: {}".format(result.netloc))
    if not re.match(r"^\w+$", result.path.lstrip("/")):
        raise ValueError("invalid short path: {}".format(result.path))
    return result.netloc, result.path.lstrip("/")


def parse_result(resp):
    """
    simple check for result code in HTTP response
    :param resp: HTTP response
    :return: response body
    :exception: ValueError, RuntimeError
    """
    result = json.loads(resp.text)
    if "Code" not in result:
        raise RuntimeError("Response HTTP Status: ()".format(resp.status_code))
    if result["Code"] != 0:
        raise RuntimeError(result["ErrMsg"])
    return result


class Dwz:
    """
    python code use DWZ API
    """
    schema = "https"
    api_path = "/api/v3/short-urls"

    def __init__(self, token: str, short_domain: str = "dwz.cn"):
        """
        :param token:access token, see https://console.bce.baidu.com/dwz/#/dwz/token
        :param short_domain: domain of DWZ short URL
            default: dwz.cn
            custom: *.dwz.cn
        """
        self.header = {
            "Dwz-Token": token,
            "Content-Language": "zh"
        }
        self.short_domain = short_domain

    def create(self, long_urls, tov: TOV):
        """
        create short URL by list of long URLs with same term of validity
        :param long_urls: long URL list
        :param tov: term of validity, options:
            1-year
            long-term
        :return: json with format:
            [
                {
                    "Code": -1,
                    "LongUrl": "",
                    "ErrMsg": ""
                },
                {
                    "ShortUrl": "",
                    "LongUrl": "",
                }
            ]
        :exception: ValueError, RuntimeError
        """
        # check params
        if len(long_urls) <= 0:
            raise ValueError("no long URL")
        if len(long_urls) > 200:
            raise ValueError("too many long URLs")
        TOV.check(tov)

        # do request
        url = parse.urlunsplit((Dwz.schema, self.short_domain, Dwz.api_path, None, None))
        data = []
        for long_url in long_urls:
            check_long_url(long_url)
            data.append({"LongUrl": long_url, "TermOfValidity": tov.value})
        resp = requests.post(url, headers=self.header, data=json.dumps(data))

        # check result
        result = parse_result(resp)
        return result["ShortUrls"]

    def create_single(self, long_url: str, tov: TOV):
        """
        create short URL for single long URL
        :param long_url:
        :param tov: term of validity, options:
            1-year
            long-term
        :return: short URL
        :exception: ValueError, RuntimeError
        """
        result = self.create([long_url], tov)[0]
        if "Code" in result and result["Code"] != 0:
            raise RuntimeError(result["ErrMsg"])
        return result["ShortUrl"]

    def query(self, short_url: str):
        """
        query origin long URL for short URL
        :param short_url:
        :return: long URL
        :exception: ValueError, RuntimeError
        """
        # do request
        domain, short_path = parse_short_url(short_url)
        url = parse.urlunsplit((Dwz.schema, domain, Dwz.api_path + "/" + short_path, None, None))
        resp = requests.get(url, headers=self.header)

        # check result
        result = parse_result(resp)
        return result["LongUrl"]

    def update(self, short_url: str, long_url: str):
        """
        update short URL
        :param short_url: short URL to be updated
        :param long_url: new target long URL
        :exception: ValueError, RuntimeError
        """
        # do request
        domain, short_path = parse_short_url(short_url)
        url = parse.urlunsplit((Dwz.schema, domain, Dwz.api_path + "/" + short_path, None, None))
        data = {"LongUrl": long_url}
        resp = requests.patch(url, headers=self.header, data=json.dumps(data))
        parse_result(resp)

    def delete(self, short_url: str):
        """
        delete short URL
        :param short_url:
        :exception: ValueError, RuntimeError
        """
        # do request
        domain, short_path = parse_short_url(short_url)
        url = parse.urlunsplit((Dwz.schema, domain, Dwz.api_path + "/" + short_path, None, None))
        resp = requests.delete(url, headers=self.header)
        parse_result(resp)
