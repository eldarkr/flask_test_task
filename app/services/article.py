from sqlalchemy.orm import Session
from pydantic.types import UUID4

from services.permissions import Permissions
from schemas.article import ArticleCreate, ArticleGet
from schemas.user import UserGet
from db.models import Article


class ArticleService:
    def __init__(self, session: Session):
        self.session = session
        
    def get_article(self, article_id: UUID4) -> ArticleGet:
        return self.session.get(Article, article_id)
        
    def create_article(self, article_data: ArticleCreate, current_user: UserGet) -> ArticleGet:
        article = Article(**article_data.model_dump())
        article.owner_id = current_user.id
        self.session.add(article)
        self.session.commit()
        return article
    
    def delete_article(self, article_id: UUID4, current_user: UserGet):
        article_to_delete = self.get_article(article_id)
        if not Permissions.can_manage_own_articles(current_user, article_to_delete):
            raise PermissionError("You don't have permission to delete article")
        article = self.get_article(article_id)
        self.session.delete(article)
        self.session.commit()
        return article
    
    def update_article(self, article_id: UUID4, article_data: ArticleCreate, current_user: UserGet) -> ArticleGet:
        article = self.get_article(article_id)
        if not Permissions.can_manage_own_articles(current_user, article) \
            or not Permissions.can_edit_other_articles(current_user):
            raise PermissionError("You don't have permission to update article")
        article.update(article_data.model_dump())
        self.session.commit()
        return article
