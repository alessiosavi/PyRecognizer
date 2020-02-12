# -*- coding: utf-8 -*-
import logging

import bcrypt
import redis

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

    def init_redis_connection(self, host: str = "0.0.0.0", port: str = "6379", db: int = 0) -> bool:
        log.warning("Initializing a new redis connection")
        self.redis_client = redis.Redis(host=host, port=port, db=db)
        try:
            health_check = self.redis_client.ping()
        except redis.exceptions.ConnectionError:
            health_check = False
            log.warning("Connection not established!")
        return health_check

    @staticmethod
    def validate_password(password) -> bool:
        if len(password) < 5:
            log.warning(
                "Password not valid | Password have to be more than 5 characters long")
            return False
        return True

    def retrieve_password(self) -> str:
        if self.redis_client is None:
            log.warning("Redis connection is not initialized")
            return ""
        return self.redis_client.get(self.get_name())

    def verify_user_exist(self) -> bool:
        """
        Verify that an user is already registered.
        True -> Already exist
        False -> New user
        """
        already_exists = self.retrieve_password()
        # Be sure that user does not exists
        return already_exists is not None

    def remove_user(self) -> bool:
        if not self.verify_user_exist():
            log.warning("User {} does not exists!".format(vars(self)))
            return False
        log.warning("Removing user {} from redis!".format(vars(self)))
        self.redis_client.delete(self.get_name())
        return True

    def add_user(self) -> bool:
        if self.verify_user_exist():
            log.warning("User {} already exist or db is not reachable ...".format(vars(self)))
            return False
        if not self.validate_password(self.password):
            log.warning("Password not valid")
            return False

        log.warning("Encrypting password -> {}".format(self.password))
        self.password = self.encrypt_password(str(self.password))
        log.warning("Password encrypted {}".format(self.password))
        self.redis_client.set(self.get_name(), self.password)
        log.warning("User {} registered!".format(self.get_name()))
        return True

    def verify_login(self, password: str) -> bool:
        if not self.verify_user_exist():
            log.warning("User {} does not exists!".format(vars(self)))
            return False
        if not self.validate_password(password):
            log.warning("Password {} is not valid!".format(password))
            return False

        # Retrieve password from DB
        psw = self.retrieve_password()
        return self.check_password(password, psw)

    def get_name(self) -> str:
        # return self.name+":"+self.mail
        return self.mail

    @staticmethod
    def encrypt_password(plain_text_password: str) -> str:
        # Hash a password for the first time
        #   (Using bcrypt, the salt is saved into the hash itself)
        return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

    @staticmethod
    def check_password(plain_text_password: str, hashed_password: str) -> bool:
        # Check hashed password. Using bcrypt, the salt is saved into the hash itself
        log.warning("Comparing plain: {} with hashed {}".format(
            plain_text_password, hashed_password))
        check = bcrypt.checkpw(plain_text_password, hashed_password)
        if check:
            log.debug("Password match, user logged in!")
        else:
            log.debug("Password mismatch, user NOT logged in!")
        return check
