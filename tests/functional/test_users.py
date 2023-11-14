# from flask import url_for

# from app.models import User


# def test_user_insert(new_user, client):
#     """Ensure that users can be added to User table and displayed on /list"""
#     test_user = dict(name=new_user.name, email=new_user.email, password=new_user.password)
#     response = client.post("/create", json=test_user, follow_redirects=True)
#     assert response.status_code == 200
#     assert f"{new_user.name}, {new_user.email}".encode("utf-8") in response.data
#     with client:
#         user = User.query.filter_by(name=new_user.name).first()
#         assert user is not None
#         assert user.email == new_user.email


# def test_get_users(client):
#     response = client.get("/list")
#     print(response.data)
#     assert response.status_code == 200
#     assert b"users are:" in response.data
