#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Binux <roy@binux.me>

import config
from db.task import TaskDB as _TaskDB
from sqlite3_db.basedb import BaseDB
import db.task 

class TaskDB(_TaskDB, BaseDB):
    def __init__(self, path=config.sqlite3.path):
        self.path = path
        self._execute('''CREATE TABLE IF NOT EXISTS `%s` (
          `id` INTEGER PRIMARY KEY AUTOINCREMENT,
          `tplid` INT UNSIGNED NOT NULL,
          `userid` INT UNSIGNED NOT NULL,
          `disabled` TINYINT(1) NOT NULL DEFAULT 0,
          `init_env` BLOB NULL,
          `env` BLOB NULL,
          `session` BLOB NULL,
          `last_success` INT UNSIGNED NULL,
          `last_failed` INT UNSIGNED NULL,
          `success_count` INT UNSIGNED NOT NULL DEFAULT 0,
          `failed_count` INT UNSIGNED NOT NULL DEFAULT 0,
          `last_failed_count` INT UNSIGNED NOT NULL DEFAULT 0,
          `next` INT UNSIGNED NULL DEFAULT NULL,
          `note` VARCHAR(256) NULL,
          `ctime` INT UNSIGNED NOT NULL,
          `mtime` INT UNSIGNED NOT NULL
        )''' % self.__tablename__)

        for each in ('userid', 'tplid'):
            t = '''CREATE INDEX IF NOT EXISTS `ix_%s_%s` ON %s (%s)''' % (
                self.__tablename__, each, self.__tablename__, each)
            self._execute(t)
            
    def ConvertNewType(self, path=config.sqlite3.path):
        self.path = path
        self._execute("ALTER TABLE `task` ADD `ontimeflg` INT NOT NULL DEFAULT 0")
        self._execute("ALTER TABLE `task` ADD `ontime` VARCHAR(256) NOT NULL DEFAULT '00:10'")            
        return 
        
if __name__ == '__main__':
    d = TaskDB()
    d.ConvertNewType(path=config.sqlite3.path)