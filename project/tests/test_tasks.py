from unittest.mock import patch, call

from worker import create_task, face_recognition_task,redis_key_clean_up_task


def test_home(test_app):
    response = test_app.get("/")
    assert response.status_code == 200

def test_face_recognition(test_app):
    response = test_app.get("/face_recognition")
    assert response.status_code == 200

def redis_key_clean_up(test_app):
    response = test_app.get("/redis_key_clean_up")
    assert response.status_code == 200

def test_task():
    assert create_task.run(1)
    assert create_task.run(2)
    assert create_task.run(3)


@patch("worker.face_recognition_task.run")
def test_face_recognition_task(mock_run):
    assert face_recognition_task.run(1)
    face_recognition_task.run.assert_called_once_with(1)

@patch("worker.redis_key_clean_up_task.run")
def test_redis_key_clean_up_task(mock_run):
    assert redis_key_clean_up_task.run(1)
    redis_key_clean_up_task.run.assert_called_once_with(1)
