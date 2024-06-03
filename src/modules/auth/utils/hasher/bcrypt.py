import bcrypt

from src.modules.auth.utils.hasher.base import AbstractHasher


class BcryptHasher(AbstractHasher):
    def gen_psw_hash(self, psw: str) -> str:
        return (bcrypt.hashpw(password=psw.encode(), salt=bcrypt.gensalt())).decode()

    def verify_psw(self, psw_to_check: str, hashed_psw: str) -> bool:
        return bcrypt.checkpw(password=psw_to_check.encode(), hashed_password=hashed_psw.encode())
