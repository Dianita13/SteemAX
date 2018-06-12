#!/usr/bin/python3

import pymysql
from screenlogger.screenlogger import Msg

class DB:


    def __init__(self, dbuser, dbpass, dbname):
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbname = dbname
        self.msg = Msg()



    def sanitize(self, *args):
        alist = []
        for v in args:
            if v:
                alist.append(pymysql.escape_string(v))
        return alist



    def open_db(self):
        ''' opens a database connection
        '''
        self.db = pymysql.connect("localhost",
                                    self.dbuser,
                                    self.dbpass,
                                    self.dbname)
        self.cursor = self.db.cursor()


    def get_results(self, sql, *args):
        ''' Gets the results of an SQL statement
        '''
        self.open_db()
        cleanargs = self.sanitize(args) or None
        try:
            self.cursor.execute(sql, cleanargs)
            self.dbresults = self.cursor.fetchall()
        except Exception as e:
            self.msg.error_message(e)
            self.dbresults = False
            self.db.rollback()
            return False
        else:
            return len(self.dbresults)
        finally:
            self.db.close()



    def commit(self, sql, *args):
        ''' Commits the actions of an SQL 
        statement to the database
        '''
        self.open_db()
        cleanargs = self.sanitize(args) or None
        try:
            self.cursor.execute(sql, cleanargs)
            self.db.commit()
        except Exception as e:
            self.msg.error_message(e)
            self.db.rollback()
            return False
        else:
            return True
        finally:
            self.db.close()



# Run as main

if __name__ == "__main__":

    db = DB("bigbird", "Snook_Nook_33", "bot_memory")
    db.get_results("SELECT * FROM turtlebotmem;")
    for a in db.dbresults:
        print (str(a[0]) + " " + str(a[1]) + " " + str(a[2]))




# EOF

