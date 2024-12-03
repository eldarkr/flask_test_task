from app.services.permissions import Permissions


def test_can_manage_all(admin_user, editor_user, regular_user):
    assert Permissions.can_manage_all(admin_user)
    assert not Permissions.can_manage_all(editor_user)
    assert not Permissions.can_manage_all(regular_user)

def test_can_edit_other_articles(admin_user, editor_user, regular_user):
    assert Permissions.can_edit_other_articles(admin_user)
    assert Permissions.can_edit_other_articles(editor_user)
    assert not Permissions.can_edit_other_articles(regular_user)

def test_can_manage_own_articles(admin_user, editor_user, regular_user, article):
    assert Permissions.can_manage_own_articles(admin_user, article)
    assert not Permissions.can_manage_own_articles(editor_user, article)
    assert Permissions.can_manage_own_articles(regular_user, article)
