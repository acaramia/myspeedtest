import sqlite3
from sqlite3 import Error
from speedtst import speedtest_class as stc
import time

class mydb:

    conn = sqlite3.dbapi2.Connection

    def create_connection(self,db_file=r'../data/logdb.sqlitedb'):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        finally:
            return self.conn
            #if conn:
            #    conn.close()

    def dict_to_field_list(self,fld_dict,prefix='',names_only=False):
        d=[]
        for fl in fld_dict:
            f=fld_dict[fl]
            #print(fl,f,type(f))
            if isinstance(f,dict):
                e=self.dict_to_field_list(f,prefix=fl+"_",names_only=names_only)
                d=d+e
            elif isinstance(f,str):
                e=f"{prefix}{fl}"+ (" text" if not names_only else '')
                d.append(e)
            else:
                e=f"{prefix}{fl}" + (" real" if not names_only else '')
                d.append(e)
        return d

    def dict_to_val_list(self,fld_dict):
        d=[]
        for fl in fld_dict:
            f=fld_dict[fl]
            #print(fl,f,type(f))
            if isinstance(f,dict):
                e=self.dict_to_val_list(f)
                d=d+e
            elif isinstance(f,str):
                e=f
                d.append(e)
            else:
                e=f
                d.append(e)
        return d

    def create_log_table(self):
        c = stc.speedtest_class()
        fld = c.get_st_fields()
        d = self.dict_to_field_list(fld)
        f=','.join(d)
        sql = f"CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY AUTOINCREMENT not null," \
              f"sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL," \
              f" {f})"
        self.create_connection()
        self.conn.execute(sql)
        sql =" delete from log where server_url = 'MOCK_DATA'"
        self.conn.execute(sql)
        self.conn.commit()

    def insert_log(self,row_dict):
        self.create_connection()
        fld = self.dict_to_field_list(row_dict,names_only=True)
        val = self.dict_to_val_list(row_dict)
        val_qm = ['?' for _ in val]
        fld = ','.join(fld)
        val_qm = ','.join(val_qm)
        sql = f"insert into log ({fld}) values ({val_qm})"
        #print(sql,val)
        self.conn.execute(sql,val)
        self.conn.commit()

    def getData(self):
        #stcc = stc.speedtest_class()
        #self.insert_log(stcc.get_data())
        self.create_connection()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        sql="SELECT * FROM log ORDER BY id DESC LIMIT 1"
        curs.execute(sql)
        rows = curs.fetchall()
        rows = [dict(row) for row in rows]
        #for row in rows:
        #    time = str(row[0])
        #    temp = row[1]
        #    hum = row[2]
        curs.close()
        return rows

    def getHistData(self,numSamples=None):
        self.create_connection()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        numSamples=10000
        curs.execute("SELECT * FROM log ORDER BY sqltime DESC LIMIT " + str(numSamples))
        data = curs.fetchall()
        times=[]
        downloads = []
        uploads = []
        pings = []
        for row in reversed(data):
            times.append(row['sqltime'])
            downloads.append(row['download'])
            uploads.append(row['upload'])
            pings.append(row['ping'])
        curs.close()
        print(len(data))
        return times,downloads,uploads,pings

    def select_log(self):
        sql = "select * from log limit 1"

        # This is the important part, here we are setting row_factory property of
        # connection object to sqlite3.Row(sqlite3.Row is an implementation of
        # row_factory)
        self.conn.row_factory = sqlite3.Row
        c = self.conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        rows = [dict(row) for row in rows]
        for row in rows:
            for fld in row:
                print(fld,row[fld])

    def main_loop(self):
        self.create_connection()
        self.create_log_table()
        stcc = stc.speedtest_class()
        sampleFreq = 3*60
        while True:
            self.insert_log(stcc.get_data(real=True))
            time.sleep(sampleFreq)

def test():
    d = mydb()
    d.create_connection()
    d.create_log_table()
    stcc = stc.speedtest_class()
    d.insert_log(stcc.get_data())
    d.select_log()

if __name__ == '__main__':
    #test()
    d=mydb()
    d.main_loop()