import psycopg2

class Postgers:
    def __init__(self):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(database="da2hm7438dn5aa", user="cuzwfpqhggbxjz",
            password="960ec3a4f7e47b2fc14391f3e9772f2f9f4a375b1bfd89d63f3ded32cb07295a",
            host="ec2-3-224-97-209.compute-1.amazonaws.com", port=5432)
        self.cursor = self.connection.cursor()


    # методы для работы с statesTable
    def get_current_state(self, user_id):
        """Получаем состояние пользователя"""
        self.cursor.execute('''SELECT state
                                            FROM statesTable
                                            WHERE user_id = {}'''.format(user_id))

        return self.cursor.fetchall()[0][0]

    def set_state(self, user_id, value):
        """Изменяем состояние"""
        def is_exist_func():
            global is_exist
            self.cursor.execute('''SELECT * FROM statesTable WHERE user_id = {}'''.format(user_id))

            if len(self.cursor.fetchall()) == 0:
                is_exist = False
            else:
                is_exist = True

        is_exist_func()

        if is_exist:
            self.cursor.execute('''UPDATE statesTable
        				  SET state = {0}
        				  WHERE user_id = {1}'''.format(value, user_id))
            self.connection.commit()
        else:

            self.cursor.execute('''INSERT INTO statesTable (user_id, state)
            	VALUES ({0}, {1})'''.format(user_id, value))
            self.connection.commit()


    def get_all_users(self):
        """Получаем все id"""
        self.cursor.execute('''SELECT user_id FROM statesTable''')
        return self.cursor.fetchall()


    # методы для работы с notTable

    def subscribe(self, user_id, not_time, city):
        """Подписываемся на уведомления"""
        def is_exist_func():
            global is_exist2

            self.cursor.execute('''SELECT * FROM notTable WHERE user_id = {}'''.format(user_id))
            if len(self.cursor.fetchall()) == 0:
                is_exist2 = False
            else:
                is_exist2 = True

        is_exist_func() 

        if is_exist2:
            self.cursor.execute('''UPDATE notTable
        				           SET is_sub = True,
                                   city = '{0}',
                                   not_time = '{1}'
        				           WHERE user_id = {2}'''.format(city, not_time, user_id))
            self.connection.commit()
        else:
        	self.cursor.execute('''INSERT INTO notTable (user_id, city, not_time, is_sub)
        	 	                   VALUES ({0}, '{1}', '{2}', True)'''.format(user_id, city, not_time))
        	self.connection.commit()

    def unsubscribe(self, user_id):
        """Отписываемся от уведомлений"""
        self.cursor.execute('''UPDATE notTable
                               SET city = Null,
                               is_sub = False,
                               not_time = Null
                               WHERE user_id = {}'''.format(user_id))
        self.connection.commit()

    def get_sub_users(self):
        """Получение подписанных пользователей"""
        self.cursor.execute('''SELECT user_id
                               FROM notTable
                               WHERE is_sub=True''')
        return self.cursor.fetchall()

    def get_city(self, user_id):
        """Получаем город пользователя"""
        self.cursor.execute('''SELECT city
                               FROM notTable
                               WHERE user_id = {}'''.format(user_id))
        return self.cursor.fetchall()[0][0]

    def get_not_time_list(self, user_id, is_sub):
        """Получение времени уведомление в формате ['5', '30']"""
        self.cursor.execute('''SELECT not_time
						  FROM notTable
						  WHERE user_id = {0} and is_sub = {1}'''.format(user_id, is_sub))
        return self.cursor.fetchall()[0][0].split(':')

    def get_sub_users_in_city(self, city):
        self.cursor.execute('''SELECT city
					  FROM notTable
					  WHERE is_sub = True and city="{}"'''.format(city))
        users_subscribed = self.cursor.fetchall()
        return users_subscribed



db = Postgers()
print(db.set_state(662211080, 3))

