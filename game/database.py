import mysql.connector
import os
from dotenv import load_dotenv


class Database():
    
    """
    This function will read from .env file the required variables used to interact with the mysql database
    """

    def __init__(self):
        load_dotenv()
        self.host = os.getenv('HOST_DB')
        self.port = os.getenv('PORT_DB')
        self.user = os.getenv('USER_DB')
        self.password = os.getenv('PASSWORD_DB')
        self.database = os.getenv('DATABASE')

    """
    This function will connect to the mysql database
    """
        
    def __connect__(self): 
        self.db = mysql.connector.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.db.cursor()

    """
    This function will disconnect to the mysql database
    """

    def __disconnect__(self):
        self.db.disconnect()

    """
    This function fill execute the commit transaction on the db. It's required when inserting values in the tables
    """

    def __commit__(self):
        self.db.commit()

    """
    This function will return a list of words given the name of the tag 
    """

    def get_words_by_tag(self, tag):
        self.__connect__()
        sql = "SELECT wordname FROM `words` WHERE id IN (SELECT `id-words` FROM `tags-words` WHERE `id-tags` IN (SELECT id FROM tags WHERE tagname = %s))"
        self.cursor.execute(sql, [tag])
        # the db returns a list of tuples, with this magic we will translate it to a list of words
        result = [(lambda x: x[0])(row)for row in self.cursor.fetchall()]
        self.__disconnect__()
        return result
    
    """
    This function will insert a tag and a language in the db
    """

    #still to test
    def add_tag(tag, lang): # check if already present in the db before inserting
        self.__connect__()
        sql = "INSERT INTO `tags` (`id`, `tagname`, `lang`, `modifiable`) VALUES (NULL, %s, %s, '1')"
        value = [(tag, lang)]
        self.cursor.execute(sql, value)
        self.__commit__()
        self.__disconnect__()
    
    """
    This function will check if a tag is already present in the db [TO TEST]
    """

    def exists_tag(tag):
        self.__connect__()
        sql = "SELECT * FROM `tags` WHERE `tagname` LIKE %s "
        self.cursor.execute(sql, [tag])
        result = self.cursor.fetchone()
        self.__disconnect__()
        return not result # check is the result is empty

    """
    This function will check if a word is already present in the db [TO TEST]
    """

    def exists_word(word):
        self.__connect__()
        sql = "SELECT * FROM `words` WHERE `wordname` LIKE %s "
        self.cursor.execute(sql, [word])
        result = self.cursor.fetchone()
        self.__disconnect__()
        return not result # check is the result is empty

    """
    This function will return the id of a word [WIP]
    """

    def get_word(word):
        self.__connect__()
        sql = "SELECT wordname FROM `words` WHERE id IN (SELECT `id-words` FROM `tags-words` WHERE `id-tags` IN (SELECT id FROM tags WHERE tagname = %s))"
        self.cursor.execute(sql, [tag])
        # the db returns a list of tuples, with this magic we will translate it to a list of words
        result = [(lambda x: x[0])(row)for row in self.cursor.fetchall()]
        self.__disconnect__()
        return result

    """
    This function will insert a word or a list of words in the db and will bind it with the tag [WIP]
    """

    def add_word(words, tag):
        self.__connect__()
        for word in words:
            sql = "INSERT INTO `words` (`id`, `tagname`, `lang`, `modifiable`) VALUES (NULL, %s, %s, '1')"
            value = [(tag, lang)]
            self.cursor.execute(sql, value)
            self.__commit__()
            self.__disconnect__()


