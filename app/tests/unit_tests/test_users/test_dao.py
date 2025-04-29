import pytest

from app.users.dao import UsersDAO


@pytest.mark.parametrize("user_id, email, is_exist", [
    (1, "john@gmail.com", True),
    (2, "bob@gmail.com", True),
    (4, "email", False)
])
async def test_find_user_by_id(user_id, email, is_exist):
    user = await UsersDAO.find_by_id(user_id)

    if is_exist:
        assert user 
        assert user.id == user_id 
        assert user.email == email 
    else:
        assert not user
