"""
Generate the administrator of the neural network, delegated to train/tune the model
"""

import logging
import redis
from crypt import crypt, METHOD_SHA512
from sys import exit

log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Administrator(object):

    def __init__(self, name: str, mail: str, password: str):
        # Identifier will be "name:mail"
        self.name = name
        self.mail = mail
        self.password = password
        self.redis_client = None
        if len(name) < 3 or len(mail) < 3 or len(password) < 5:
            print("Value not allowed! -> {}".format(vars(self)))
            exit(-1)

    def init_redis_connection(self, host, port, db) -> bool:
        log.warning("Initializing a new redis connection")
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        return self.redis_client.ping()

    def validate_password(self) -> bool:
        if len(self.password) < 5:
            log.warning(
                "Password not valid | Password have to be more than 5 characters long")
            return False
        return True

    def verify_user_exist(self) -> bool:
        alredy_exists = self.redis_client.get(self.get_name())
        # Be sure that user does not exists
        return alredy_exists == None

    def remove_user(self) -> bool:
        if not self.verify_user_exist():
            log.warning("User {} does not exists!".format(vars(self)))
            return False
        log.warning("Removing user {} from redis!".format(vars(self)))
        self.redis_client.delete(self.get_name())
        return True

    def add_user(self) -> bool:
        if not self.verify_user_exist():
            log.warning("User {} alredy exist ...".format(vars(self)))
            return False
        if not self.validate_password():
            log.warning("Password not valid")
            return False

        self.password = self.encrypt_password()
        self.redis_client.set(self.get_name(), self.password)
        log.warning("User {} registered!".format(self.get_name()))
        return True

    def encrypt_password(self) -> str:
        if not self.validate_password():
            log.warning("Password [{}] not valid!".format(self.password))
            return ""
        log.warning("Encrypting password for user [{}]".format(self.get_name()))
        psw = crypt(self.password, METHOD_SHA512)
        log.warning("Password -> {}".format(psw))
        return psw

    def get_name(self) -> str:
        return self.name+":"+self.mail


a = Administrator("name", "mail", "password")
a.init_redis_connection("127.0.0.1", "6379", 0)
print(a.remove_user())
print(a.add_user())
