from remanager_back.database.user_extra import UserExtra


def get_user_extra_by_login(login: str) -> UserExtra:
    extra = UserExtra.objects().get(login=login)
    return extra


def create_user_extra(login: str) -> UserExtra:
    extra = UserExtra()
    extra.login = login
    extra.save()
    return extra
