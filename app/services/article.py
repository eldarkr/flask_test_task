from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.sql import update
from pydantic.types import UUID4

from db.models import Article
from services.permissions import Permissions
from schemas.article import ArticleCreate, ArticleGet
from schemas.user import UserGet


class ArticleService:
    def __init__(self, session: Session):
        self.session = session
        
    def get_article(self, article_id: UUID4) -> ArticleGet:
        return self.session.get(Article, article_id)
    
    def get_all_articles(self) -> list[ArticleGet]:
        return self.session.query(Article).all()
        
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
                and not Permissions.can_edit_other_articles(current_user):
            raise PermissionError("You don't have permission to update article")
        query = (
            update(Article)
            .where(Article.id == article_id)
            .values(**article_data.model_dump(exclude_none=True))
            .returning(Article)
        )
        result = self.session.execute(query).scalar()
        self.session.commit()
        return result

    def find_article_by_text(self, text: str) -> list[ArticleGet]:
        query = self.session.query(Article).filter(
            or_(Article.title.ilike(f"%{text}%"), Article.content.ilike(f"%{text}%"))
        )
        return query.all()