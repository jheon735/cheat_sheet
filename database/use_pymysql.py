import pymysql

def get_add_from_db(dname, result):
    db = pymysql.connect(host='ip', user='username', passwd='password', db='db name', charset='utf8')

    cursor = db.cursor()
    sql = f"SELECT 항목1, 항목2, 항목3 from 테이블이름 where collect_data_name='{dname}'"  # db테이블 가져오기
    cursor.execute(sql)
    data1, data2, data3, data4 = cursor.fetchall()[0]  #테이블의 모든 자료 가져오기

    sql = "INSERT %s (ftime, arc_dir, arc_fname) VALUES('%s', '%s', '%s' ) " % (tablename, ftime, arc_dir, self.sfname)
    cursor.execute(sql)
    db.commit()

    db.close()