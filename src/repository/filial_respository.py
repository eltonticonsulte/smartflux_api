# -*- coding: utf-8 -*-


class FiliaryRepository:
    def __init__(self):
        pass

    def create_user(self, user: UserReciver):
        self.log.debug(f"create_user {user}")
        db_user = Filial(
            name=user.username,
            description=user.description,
            token_api=self.genetate_token(),
            password_hash=user.password,
        )
        try:
            self.data_base.create_device(db_user)
        except IntegrityError:
            raise ExceptionUserNameExists(user.username)

    def genetate_token(self):
        return str(uuid4())
