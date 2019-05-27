# create retrieve update delete
#
"""
INSERT INTO
    `users`(`id`,`username`,`password`,`email`)
VALUES \
    (2,'','',NULL);

UPDATE `users` SET `username`=? WHERE `_rowid_`='2';
UPDATE `users` SET `password`=? WHERE `_rowid_`='2';
UPDATE `users` SET `email`=? WHERE `_rowid_`='2';
"""

import sqlite3
import config


db_path = config.root + '/novel.sqlite'
class DB:
    def __init__(self,db_path):
        self.conn = sqlite3.connect(db_path)

    def run(self,sql,*args):
        self.conn.execute(sql,*args)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

def create_user():
    db=DB( db_path )
    sql_create='''
    CREATE TABLE IF NOT EXISTS `users` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `username`	TEXT NOT NULL UNIQUE,
        `password`	TEXT NOT NULL,
        `isadmin`	BOOL 
    )
    '''
    sql_insert ='''
    INSERT INTO
        `users`(`username`,`password`,`isadmin`)
    VALUES
        (?,?, ?);    
    '''
    db.run(sql_create)
    db.run(sql_insert,('admin','123456',True))
    db.run(sql_insert,('test01','123456',False))
    db.run(sql_insert,('test02','123456',False))
    db.commit()
    db.close()


def create_book():
    db=DB(db_path)
    sql='''
    CREATE TABLE IF NOT EXISTS `book` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `type`	TEXT NOT NULL,
        `subtype`	TEXT NOT NULL,
        `name`	TEXT NOT NULL,
        `bookid`	TEXT NOT NULL,
        `words`	TEXT,
        `author`	TEXT 
    )
    '''
    db.run(sql)
    db.commit()
    db.close()


def insert_book(l):
    db=DB(db_path)
    sql='''
    INSERT INTO
        `book` (`type`,`subtype`,`name`,`bookid`,`words`,`author`)
    VALUES 
        (?,?,?,?,?,?);
    '''
    for tuple_data in l:
        db.run(sql,tuple_data)
    db.commit()
    db.close()


if __name__ == '__main__':
    create_user()
    create_book()
