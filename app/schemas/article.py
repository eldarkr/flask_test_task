from pydantic import BaseModel, UUID4


class ArticleBase(BaseModel):
    owner_id: UUID4

    
class ArticleGet(ArticleBase):
    id: UUID4
    title: str
    content: str
    
    
class ArticleCreate(BaseModel):
    title: str
    content: str


class ArticleUpdate(BaseModel):
    title: str = None
    content: str = None
