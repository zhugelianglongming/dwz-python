#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# API: https://dwz.cn/console/apidoc/v3

import requests
import json


class Dwz:
    """
    python code use DWZ API
    """
    api_path = "/api/v3/short-urls"

    def __init__(self, token, short_domain="dwz.cn"):
        """
        :param token:access token, see https://console.bce.baidu.com/dwz/#/dwz/token
        :param short_domain: domain of DWZ short URL
            default: dwz.cn
            custom: *.dwz.cn
        """
        self.header = {"Dwz-Token": token}
        self.short_domain = short_domain

    def create(self, long_urls, tov):
        """
        create short URL by list of long URLs with same term of validity
        :param long_urls: long URL list
        :param tov: term of validity, options:
            1-year
            long-term
        :return: json with format:
        {
            "Code": 0,
            "ShortUrls": [
                {
                    "Code": 0,
                    "ShortUrl": "",
                    "LongUrl": "",
                    "ErrMsg": ""
                }
            ],
            "ErrMsg": ""
        }
        :exception: ValueError
        """
        # check params
        if len(long_urls) <= 0:
            raise ValueError("no long URL")
        if len(long_urls) > 200:
            raise ValueError("too many long URLs")
        if tov not in ("1-year", "long-term"):
            raise ValueError("invalid term of validity")

        url = "https://{}{}".format(self.short_domain, Dwz.api_path)
        data = []
        for long_url in long_urls:
            data.append({"LongUrl":long_url,"TermOfValidity":tov})
        resp = requests.post(url, headers=self.header, data=json.dumps(data))
        return json.loads(resp.text)

    def query(self, short_path):
        """
        query origin long URL by short URL path
        :param short_path: path in short URL
        :return: json with format:
        {
            "Code": 0,
            "LongUrl": "",
            "ErrMsg": ""
        }
        """
        url = "https://{}{}/{}".format(self.short_domain, Dwz.api_path, short_path)
        resp = requests.get(url, headers=self.header)
        return json.loads(resp.text)

    def delete(self, short_path):
        """
        delete short URL
        :param short_path: path in short URL
        :return: json with format:
        {
            "Code": 0,
            "ErrMsg": ""
        }
        """
        url = "https://{}{}/{}".format(self.short_domain, Dwz.api_path, short_path)
        resp = requests.delete(url, headers=self.header)
        return json.loads(resp.text)
