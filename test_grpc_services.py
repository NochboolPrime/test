import os
import sys
import grpc
import pytest
import platform


import registration_pb2
import registration_pb2_grpc
import database_pb2
import database_pb2_grpc


if platform.system() != "Windows":
    pytest.exit("Этот тест предназначен для Windows 10", returncode=1)

test_data = {}

@pytest.fixture(scope="module")
def reg_client():
    """Фикстура для подключения к RegistrationService."""
    try:
        channel = grpc.insecure_channel("localhost:50051")
        client = registration_pb2_grpc.RegistrationServiceStub(channel)
        yield client
    finally:
        channel.close()

@pytest.fixture(scope="module")
def db_client():
    """Фикстура для подключения к DatabaseService."""
    try:
        channel = grpc.insecure_channel("localhost:50052")
        client = database_pb2_grpc.DatabaseServiceStub(channel)
        yield client
    finally:
        channel.close()

def test_register_user_success(reg_client):
    request = registration_pb2.RegisterRequest(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password123"
    )
    response = reg_client.RegisterUser(request)
    assert response.success, "User registration failed"
    test_data["user_id"] = response.user_id

def test_register_duplicate_user(reg_client):
    request = registration_pb2.RegisterRequest(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com", 
        password="password123"
    )
    response = reg_client.RegisterUser(request)
    assert not response.success, "Duplicate registration should fail"

def test_get_user(db_client):
    user_id = test_data.get("user_id")
    request = database_pb2.GetUserRequest(user_id=user_id)
    response = db_client.GetUser(request)
    assert response.user.email == "john.doe@example.com", "Email mismatch"

def test_update_user(db_client):
    user_id = test_data.get("user_id")
    request = database_pb2.UpdateUserRequest(
        user_id=user_id,
        new_first_name="Jane"
    )
    response = db_client.UpdateUser(request)
    assert response.success, "User update failed"

def test_delete_user(db_client):
    user_id = test_data.get("user_id")
    request = database_pb2.DeleteUserRequest(user_id=user_id)
    response = db_client.DeleteUser(request)
    assert response.success, "User deletion failed"
    with pytest.raises(grpc.RpcError) as exc_info:
        db_client.GetUser(database_pb2.GetUserRequest(user_id=user_id))
    assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND, "Unexpected error code for deleted user"
