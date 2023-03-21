from sqlite3 import connect
from cachetools import cached, MRUCache
from os.path import join

class SQLiteDatabase(): 
    user_info_keys = [
            "id", 
            "username", 
            "name", 
            "age", 
            "preferred_age_min",
            "preferred_age_max",
            "gender",
            "preferred_gender",
            "bio",
        ]

    def __init__(self, db_path, queries_path):
        self.conn = connect(db_path)
        self.queries_path = queries_path
        self.__init_tables()

    def __init_tables(self): 
        cursor = self.conn.cursor()
        users_table_q = self.__get_from_file("users_table_q")

        cursor.executescript(users_table_q)
    
    def create_user(self, info):
        try: 
            ordered_values = [info[key] for key in self.user_info_keys]
        except KeyError as err: 
            return 
        
        create_user_q = self.__get_from_file("create_user_q")
        cursor = self.conn.cursor()
        cursor.execute(create_user_q, tuple(ordered_values))
        self.conn.commit()

        return self.get_user(info["id"])

    def get_user(self, id): 
        cursor = self.conn.cursor()
        get_user_q = self.__get_from_file("get_user_q")

        res = cursor.execute(get_user_q, (id,))
        info = res.fetchone()

        if info is None: 
            return None
        
        return dict(zip(self.user_info_keys, info))

    @cached(MRUCache(16))
    def __get_from_file(self, name): 
        filename = f'{name}.sql'
        query_path = join(self.queries_path, filename)

        with open(query_path) as file: 
            content = file.read()

            if len(content) == 0: 
                return None 
            
            return content

    