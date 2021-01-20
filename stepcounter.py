import json
import pymysql
import pymysql.cursors


def read_database_config(db_config_path):
    try:
        with open(db_config_path) as f:
            return json.load(f)
    except Exception as exc:
        raise Exception("Please add configuration file " + db_config_path) from exc 


class DatabaseConnection:
    DB_CONFIG_PATH = "stepcounter_database_config.json"
    CONFIG = read_database_config(DB_CONFIG_PATH)

    def __init__(self, user):
        self.user = user
        self.cnx = pymysql.connect(
            cursorclass=pymysql.cursors.DictCursor,
            user=self.CONFIG["username"],
            password=self.CONFIG["password"],
            host=self.CONFIG["host"],
            port=self.CONFIG["port"],
            database=self.CONFIG["database"],
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def close(self):
        self.cnx.close()

    def get_number_of_steps_after(self, date):
        with self.cnx.cursor() as cursor:
            cursor.execute(
                """SELECT SUM(`number_of_steps`) FROM `steps`
                WHERE `username` = %s AND `date_of_walk` >= %s""",
                (self.user, date),
                )
            response = cursor.fetchone()
            return int(set(response.values()).pop())

    def add_steps(self, number_of_steps, date):
        with self.cnx.cursor() as cursor:
            cursor.execute(
                """INSERT INTO `steps` (`username`, `number_of_steps`, `date_of_walk`)
                VALUES (%s, %s, %s)""",
                (self.user, number_of_steps, date),
                )
        self.cnx.commit()
