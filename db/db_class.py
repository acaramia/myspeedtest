import sqlite3
from sqlite3 import Error
from speedtst import speedtest_class as stc

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
        sql = f"CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY AUTOINCREMENT, {f})"
        self.create_connection()
        self.conn.execute(sql)

    def insert_log(self,row_dict):
        self.create_connection()
        fld = self.dict_to_field_list(row_dict,names_only=True)
        val = self.dict_to_val_list(row_dict)
        val_qm = ['?' for _ in val]
        fld = ','.join(fld)
        val_qm = ','.join(val_qm)
        sql = f"insert into log ({fld}) values ({val_qm})"
        print(sql,val)
        self.conn.execute(sql,val)
        self.conn.commit()

    def select_log(self):
        sql = "select * from log"
        rows = self.conn.execute(sql)
        for row in rows:
            print(row)


d = mydb()
d.create_connection()
d.create_log_table()
stcc = stc.speedtest_class()
d.insert_log(stcc.get_data())
d.select_log()