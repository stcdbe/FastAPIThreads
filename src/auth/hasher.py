import bcrypt


class Hasher:
    @staticmethod
    def gen_psw_hash(psw: str) -> str:
        return (bcrypt.hashpw(password=psw.encode(), salt=bcrypt.gensalt())).decode()

    @staticmethod
    def verify_psw(psw: str, hashed_psw: str) -> bool:
        return bcrypt.checkpw(password=psw.encode(), hashed_password=hashed_psw.encode())
