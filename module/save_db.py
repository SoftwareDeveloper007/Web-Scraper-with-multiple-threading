import pymysql

class save_db():
    def __init__(self, configs, patterns):
        DB_HOST = configs['database_host']
        DB_USER = configs['database_user']
        DB_PASSWORD = configs['database_password']
        DB_NAME = configs['database_name']

        self.patterns = patterns

        self.db = pymysql.connect(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

        # prepare a cursor object using cursor() method
        self.cur = self.db.cursor()

    def remove_table(self):
        self.cur = self.db.cursor()
        sql = "DROP TABLE IF EXISTS total_data"
        self.cur.execute(sql)

    def create_table(self):
        self.cur = self.db.cursor()
        sql = "CREATE TABLE IF NOT EXISTS total_data(ID INT(11) PRIMARY KEY AUTO_INCREMENT NOT NULL, URL VARCHAR(255), " \
              "DOMAIN_ VARCHAR(255), Pattern1 INT(11), Pattern2 INT(11), Pattern3 INT(11), Pattern4 INT(11))"
        self.cur.execute(sql)


    def store_data(self, url, domain, pattern1, pattern2, pattern3, pattern4):
        self.cur = self.db.cursor()
        sql = "INSERT INTO total_data(URL, DOMAIN_, Pattern1, Pattern2, Pattern3, Pattern4)" \
              " VALUES (%s, %s, %s, %s, %s, %s);"
        self.cur.execute(sql, (
            url, domain, pattern1, pattern2, pattern3, pattern4))
        self.db.commit()

    def db_close(self):
        self.db.close()