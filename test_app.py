import pytest
from app import app, mongo
from bson.objectid import ObjectId


class FakeCollection:
    def __init__(self):
        self.items = []

    def find(self):
        return list(self.items)

    def find_one(self, query):
        for item in self.items:
            if item.get("_id") == query.get("_id"):
                return item
        return None

    def insert_one(self, data):
        new_data = dict(data)
        if "_id" not in new_data:
            new_data["_id"] = ObjectId()
        self.items.append(new_data)

        class InsertResult:
            inserted_id = new_data["_id"]

        return InsertResult()

    def update_one(self, query, update):
        for item in self.items:
            if item.get("_id") == query.get("_id"):
                item.update(update.get("$set", {}))
                break

    def delete_one(self, query):
        self.items = [item for item in self.items if item.get("_id") != query.get("_id")]


class FakeDB:
    def __init__(self):
        self.students = FakeCollection()


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/test_student_db"

    fake_db = FakeDB()
    fake_db.students.insert_one({
        "_id": ObjectId("66fddff25f4b5f6a0a123456"),
        "name": "Test Student",
        "email": "test@student.com",
        "course": "Flask"
    })
    mongo.db = fake_db

    with app.test_client() as test_client:
        yield test_client


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Test Student" in response.data


def test_add_student(client):
    data = {"name": "New User", "email": "new@user.com", "course": "Python"}
    response = client.post('/add', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"New User" in response.data


def test_update_student(client):
    student_id = "66fddff25f4b5f6a0a123456"
    data = {"name": "Updated Name", "email": "updated@student.com", "course": "Updated Course"}
    response = client.post(f'/update/{student_id}', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Updated Name" in response.data


def test_delete_student(client):
    student_id = str(mongo.db.students.insert_one({
        "name": "Temp User",
        "email": "temp@user.com",
        "course": "Temp Course"
    }).inserted_id)

    response = client.get(f'/delete/{student_id}', follow_redirects=True)
    assert response.status_code == 200
    assert b"Temp User" not in response.data
