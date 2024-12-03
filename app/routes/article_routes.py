from flask import Blueprint, request, jsonify
from services.article import ArticleService
from schemas.article import ArticleCreate, ArticleUpdate
from db.db_session import get_db
from utils.jwt_decorator import jwt_required

article_bp = Blueprint("article", __name__, url_prefix="/article")
session = next(get_db())


@article_bp.route("/<uuid:article_id>")
def get_article(article_id):
    article_service = ArticleService(session)
    article = article_service.get_article(article_id)
    
    return jsonify({
        "id": article_id,
        "owner_id": article.owner_id,
        "title": article.title,
        "content": article.content,
    })


@article_bp.route("/all")
def get_all_articles():
    article_service = ArticleService(session)
    articles = article_service.get_all_articles()
    articles = [
        {
            "id": article.id,
            "owner_id": article.owner_id,
            "title": article.title,
            "content": article.content,
        } for article in articles
    ]
    
    return jsonify(articles)


@article_bp.route("/", methods=["POST"])
@jwt_required
def create_article():
    data = request.json
    article = ArticleCreate(**data)
    article_service = ArticleService(session)
    article = article_service.create_article(article, request.current_user)
    
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content,
    })


@article_bp.route("/<uuid:article_id>", methods=["DELETE"])
@jwt_required
def delete_article(article_id):
    article_service = ArticleService(session)
    article_service.delete_article(article_id, request.current_user)
    
    return jsonify({"message": "Article deleted"})


@article_bp.route("/<uuid:article_id>", methods=["PUT"])
@jwt_required
def update_article(article_id):
    data = request.json
    article = ArticleUpdate(**data)
    article_service = ArticleService(session)
    article = article_service.update_article(article_id, article, request.current_user)
    
    return jsonify({
        "id": article.id,
        "title": article.title,
        "content": article.content,
    })


@article_bp.route("/search")
def search_article():
    text = request.json.get("text")
    article_service = ArticleService(session)
    articles = article_service.find_article_by_text(text)
    articles = [
        {
            "id": article.id,
            "owner_id": article.owner_id,
            "title": article.title,
            "content": article.content,
        } for article in articles
    ]
    
    return jsonify(articles)
