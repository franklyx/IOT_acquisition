#!/usr/bin/env python
# -*-coding:utf-8 -*-

import yaml
import logging
import logging.config
from schedule.consumer.start import consumer


def init_logger():
    filename = "config/logging.yml"
    with open(filename, "r") as f:
        config = yaml.load(f)
    logging.config.dictConfig(config)


def main():
    # init_logger()
    consumer()

if __name__ == '__main__':
    main()
