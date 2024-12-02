from pydantic import BaseModel, UUID4


class ArticleBase(BaseModel):
    owner_id: UUID4
    
    
class ArticleCreate(BaseModel):
    title: str
    content: str
    
    
class ArticleGet(ArticleCreate):
    id: UUID4
