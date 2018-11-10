# whatsmyip | myip
[![Build Status](https://travis-ci.org/Ecno92/myip.svg?branch=master)](https://travis-ci.org/Ecno92/myip)
[![pypi release](https://img.shields.io/pypi/v/whatsmyip.svg)](https://pypi.org/project/whatsmyip/)
[![Coverage Status](https://coveralls.io/repos/github/Ecno92/myip/badge.svg?branch=master)](https://coveralls.io/github/Ecno92/myip?branch=master)

## Installation and usage

As a CLI tool:
```
$ pip3 install whatsmyip
$ myip
240.0.0.0
```

As a library:
```
>>> from whatsmyip.ip import get_ip
>>> from whatsmyip.providers import GoogleDnsProvider  # Or any other provider
>>> get_ip(GoogleDnsProvider)
'240.0.0.0'
```


## Supported providers

* Google DNS
* httpbin.org
* Cloudflare
    - DNS
    - HTTP


## Goal of this project

The goal of this project is not to become the best tool to check your IP address. 
In that case I recommend you to use something more simple like:

`curl https://httpbin.org/ip`

I've developed this project to have something simple to experiment with when explorering new ideas or techniques.
