# Jormungandr-Onboarding
from src.services.watch_list import UserService
from .stub import stub_user_params

# Third party
from pytest import fixture


@fixture(scope="function")
def user_service():
    setup_service_instance = UserService(user_params=stub_user_params)
    return setup_service_instance
