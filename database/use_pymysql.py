import pymysql

def get_add_from_db(dname, result):
    db = pymysql.connect(host='ip', user='username', passwd='password', db='db name', charset='utf8')

    cursor = db.cursor()
    sql = f"SELECT 항목1, 항목2, 항목3 from 테이블이름 where collect_data_name='{dname}'"  # db테이블 가져오기
    sql = "INSERT %s (ftime, arc_dir, arc_fname) VALUES('%s', '%s', '%s' ) " % (tablename, ftime, arc_dir, self.sfname)
    cursor.execute(sql)
    met, add, sdir, sfname = cursor.fetchall()[0]

    if result=='add':
        return add[0:add.find(':')]
    elif result=='path':
        return add[add.find(':')+1:]
    elif result=='sdir':
        return sdir
