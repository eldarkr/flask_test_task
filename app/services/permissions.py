from schemas.user import UserGet
from schemas.enums import UserRole
from schemas.article import ArticleGet


class Permissions:
    @staticmethod
    def can_manage_all(current_user: UserGet) -> bool:
        return current_user.role == UserRole.ADMIN

    @staticmethod
    def can_edit_other_articles(current_user: UserGet) -> bool:
        return current_user.role in {UserRole.ADMIN, UserRole.EDITOR}

    @staticmethod
    def can_manage_own_articles(current_user: UserGet, article: ArticleGet) -> bool:
        return current_user.role == UserRole.ADMIN or current_user.id == article.owner_id
