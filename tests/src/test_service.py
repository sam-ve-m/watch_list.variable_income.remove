# Jormungandr-Onboarding
from src.domain.exceptions import EmailAlreadyExists
from .stub import stub_user_model

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch('src.services.user_register.UserRepository.find_one_by_email')
async def test_when_email_already_exists_then_raises(mock_find_one, user_service):
    with pytest.raises(EmailAlreadyExists):
        await user_service.verify_email_already_exists()


@pytest.mark.asyncio
@patch('src.services.user_register.UserRepository.find_one_by_email', return_value=None)
async def test_when_email_not_in_use_then_return_none_and_continue_execution(mock_find_one, user_service):
    email_in_use = await user_service.verify_email_already_exists()

    assert email_in_use is None


@pytest.mark.asyncio
@patch('src.services.user_register.UserRepository.find_one_by_email', return_value=None)
async def test_when_run_function_then_find_one_was_called(mock_find_one, user_service):
    await user_service.verify_email_already_exists()

    mock_find_one.assert_called_once_with(email='teste@teste.com')


@pytest.mark.asyncio
@patch('src.services.user_register.UserRepository.insert_one_user')
@patch('src.services.user_register.Social.register_user')
@patch('src.services.user_register.Audit.register_user_log')
async def test_when_user_not_exist_then_successfully_register(mock_audit, mock_social, mock_insert_one, user_service):
    success = await user_service.register()

    assert success is True


@pytest.mark.asyncio
@patch('src.services.user_register.UserModel.to_dict', return_value=stub_user_model)
@patch('src.services.user_register.UserRepository.insert_one_user')
@patch('src.services.user_register.Social.register_user')
@patch('src.services.user_register.Audit.register_user_log')
async def test_when_user_not_exist_then_mocks_was_called(mock_audit, mock_social, mock_insert_one, mock_user, user_service):
    await user_service.register()

    mock_user.assert_called_once_with()
    mock_audit.assert_called_once()
    mock_social.assert_called_once()
    mock_insert_one.assert_called_once()
