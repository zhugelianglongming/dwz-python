#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# API: https://dwz.cn/console/apidoc/v3

import json
import re
import requests
from urllib import parse


def _check_tov(tov):
    """
    :param tov: term of validity
    :return: ValueError
    """
    if tov not in ("1-year", "long-term"):
        raise ValueError("invalid term of validity")


def parse_short_url(short_url):
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


class Dwz:
    """
    python code use DWZ API
    """
    schema = "https"
    api_path = "/api/v3/short-urls"

    def __init__(self, token, short_domain="dwz.cn"):
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

    def create(self, long_urls, tov):
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
        _check_tov(tov)

        # do request
        url = parse.urlunsplit((Dwz.schema, self.short_domain, Dwz.api_path, None, None))
        data = []
        for long_url in long_urls:
            data.append({"LongUrl":long_url,"TermOfValidity":tov})
        resp = requests.post(url, headers=self.header, data=json.dumps(data))

        # check result
        result = json.loads(resp.text)
        if "Code" not in result:
            raise RuntimeError("Response HTTP Status: ()".format(resp.status_code))
        if result["Code"] != 0:
            raise RuntimeError(result["ErrMsg"])
        return result["ShortUrls"]

    def create_single(self, long_url, tov):
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

    def query(self, short_url):
        """
        query origin long URL for short URL
        :param short_url:
        :return: long URL
        :exception: ValueError, RuntimeError
        """
        # do request
        domain, short_path = parse_short_url(short_url)
        url = parse.urlunsplit((Dwz.schema, domain, Dwz.api_path+"/"+short_path, None, None))
        resp = requests.get(url, headers=self.header)

        # check result
        result = json.loads(resp.text)
        if "Code" not in result:
            raise RuntimeError("Response HTTP Status: {}".format(resp.status_code))
        if result["Code"] != 0:
            raise RuntimeError(result["ErrMsg"])
        return result["LongUrl"]

    def delete(self, short_url):
        """
        delete short URL
        :param short_url:
        :exception: ValueError, RuntimeError
        """
        # do request
        domain, short_path = parse_short_url(short_url)
        url = parse.urlunsplit((Dwz.schema, domain, Dwz.api_path+"/"+short_path, None, None))
        resp = requests.delete(url, headers=self.header)

        # check result
        result = json.loads(resp.text)
        if "Code" not in result:
            raise RuntimeError("Response HTTP Status: ()".format(resp.status_code))
        if result["Code"] != 0:
            raise RuntimeError(result["ErrMsg"])