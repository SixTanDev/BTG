"""
Unit tests for the UserRepository class.

This module contains unit tests for various methods
in the UserRepository class, which handles operations
related to users, subscriptions, and transactions in the
MongoDB database.
"""

import pytest


@pytest.fixture
def mock_db(mocker):
    """
    Fixture to create a mock of the MongoDB database using pytest-mock.

    Args:
        mocker: The pytest-mock plugin used for creating mocks.

    Returns:
        MagicMock: A mocked instance of the database.
    """
    return mocker.MagicMock()


@pytest.fixture
def user_repo(mock_db):
    """
    Fixture to create an instance of the UserRepository with the mocked database.

    Args:
        mock_db: The mocked database.

    Returns:
        UserRepository: An instance of the UserRepository.
    """
    from btg.repository.user_repository import UserRepository

    return UserRepository(db=mock_db)


def test_has_active_subscription(user_repo, mock_db):
    """
    Test for `has_active_subscription` verifying if a user has
    an active subscription to a specific fund.

    This test mocks the database's `find_one` method and checks
    if the repository returns the correct result when an active
    subscription exists.

    Asserts:
        - The result is True when an active subscription is found.
        - The `find_one` method is called with the correct parameters.
    """
    user_id = "test_user"
    fund_id = "test_fund"
    mock_db.transactions.find_one.return_value = {
        "user_id": user_id,
        "fund_id": fund_id,
        "type": "subscription",
    }

    result = user_repo.has_active_subscription(user_id, fund_id)

    assert result is True
    mock_db.transactions.find_one.assert_called_once_with(
        {"user_id": user_id, "fund_id": fund_id, "type": "subscription"}
    )


def test_find_unique_user(user_repo, mock_db):
    """
    Test for `find_unique_user` verifying the retrieval of a unique user.

    This test mocks the `find_one` method of the `users` collection and checks
    if the repository correctly retrieves the only user in the collection.

    Asserts:
        - The returned user matches the expected user document.
        - The `find_one` method is called once.
    """
    expected_user = {"_id": "test_user", "name": "John"}
    mock_db.users.find_one.return_value = expected_user

    result = user_repo.find_unique_user()

    assert result == expected_user
    mock_db.users.find_one.assert_called_once()


def test_find_all_funds(user_repo, mock_db):
    """
    Test for `find_all_funds` verifying the retrieval of all funds.

    This test mocks the `find` method of the `funds` collection and checks
    if the repository correctly returns all fund documents.

    Asserts:
        - The returned funds match the expected list of fund documents.
        - The `find` method is called with an empty filter.
    """
    expected_funds = [{"_id": "fund1"}, {"_id": "fund2"}]
    mock_db.funds.find.return_value = expected_funds

    result = user_repo.find_all_funds()

    assert result == expected_funds
    mock_db.funds.find.assert_called_once_with({})


def test_find_user(user_repo, mock_db):
    """
    Test for `find_user` verifying the retrieval of a user by their ID.

    This test mocks the `find_one` method of the `users` collection and checks
    if the repository correctly retrieves a user by their unique ID.

    Asserts:
        - The returned user matches the expected user document.
        - The `find_one` method is called with the correct filter.
    """
    user_id = "test_user"
    expected_user = {"_id": user_id, "name": "John"}
    mock_db.users.find_one.return_value = expected_user

    result = user_repo.find_user(user_id)

    assert result == expected_user
    mock_db.users.find_one.assert_called_once_with({"_id": user_id})


def test_find_fund(user_repo, mock_db):
    """
    Test for `find_fund` verifying the retrieval of a fund by its ID.

    This test mocks the `find_one` method of the `funds` collection and checks
    if the repository correctly retrieves a fund by its unique ID.

    Asserts:
        - The returned fund matches the expected fund document.
        - The `find_one` method is called with the correct filter.
    """
    fund_id = "test_fund"
    expected_fund = {"_id": fund_id, "name": "Fund A"}
    mock_db.funds.find_one.return_value = expected_fund

    result = user_repo.find_fund(fund_id)

    assert result == expected_fund
    mock_db.funds.find_one.assert_called_once_with({"_id": fund_id})


def test_update_user_balance_and_transactions(user_repo, mock_db):
    """
    Test for `update_user_balance_and_transactions` verifying the update of
    user balance and insertion of a transaction.

    This test mocks the `update_one` method of the `users` collection and
    the `insert_one` method of the `transactions` collection. It checks if
    the repository correctly updates the balance and logs the transaction.

    Asserts:
        - The user balance is updated with the correct amount.
        - The transaction is inserted into the `transactions` collection.
    """
    user_id = "test_user"
    amount = 100.0
    transaction = {"user_id": user_id, "amount": amount}

    user_repo.update_user_balance_and_transactions(user_id, amount, transaction)

    mock_db.users.update_one.assert_called_once_with(
        {"_id": user_id}, {"$inc": {"balance": amount}}
    )
    mock_db.transactions.insert_one.assert_called_once_with(transaction)


def test_add_subscription(user_repo, mock_db):
    """
    Test for `add_subscription` verifying the insertion of a new subscription.

    This test mocks the `insert_one` method of the `subscriptions` collection
    and checks if the repository correctly inserts a new subscription.

    Asserts:
        - The subscription is inserted into the `subscriptions` collection.
    """
    subscription = {"user_id": "test_user", "fund_id": "test_fund"}

    user_repo.add_subscription(subscription)

    mock_db.subscriptions.insert_one.assert_called_once_with(subscription)


def test_find_last_subscription(user_repo, mock_db):
    """
    Test for `find_last_subscription` verifying the retrieval of the last
    subscription for a user to a specific fund.

    This test mocks the `find_one` method of the `subscriptions` collection
    and checks if the repository correctly retrieves the most recent subscription.

    Asserts:
        - The returned subscription matches the expected subscription document.
        - The `find_one` method is called with the correct filter.
    """
    user_id = "test_user"
    fund_id = "test_fund"
    expected_subscription = {"user_id": user_id, "fund_id": fund_id}
    mock_db.subscriptions.find_one.return_value = expected_subscription

    result = user_repo.find_last_subscription(user_id, fund_id)

    assert result == expected_subscription
    mock_db.subscriptions.find_one.assert_called_once_with(
        {"user_id": user_id, "fund_id": fund_id}
    )


def test_remove_subscription(user_repo, mock_db):
    """
    Test for `remove_subscription` verifying the deletion of a subscription by its ID.

    This test mocks the `delete_one` method of the `subscriptions` collection and
    checks if the repository correctly deletes a subscription.

    Asserts:
        - The subscription is deleted from the `subscriptions` collection.
    """
    subscription_id = "subscription123"

    user_repo.remove_subscription(subscription_id)

    mock_db.subscriptions.delete_one.assert_called_once_with(
        {"subscription_id": subscription_id}
    )


def test_add_transaction(user_repo, mock_db):
    """
    Test for `add_transaction` verifying the insertion of a transaction.

    This test mocks the `insert_one` method of the `transactions` collection and
    checks if the repository correctly inserts a new transaction.

    Asserts:
        - The transaction is inserted into the `transactions` collection.
    """
    transaction = {"user_id": "test_user", "amount": 100.0}

    user_repo.add_transaction(transaction)

    mock_db.transactions.insert_one.assert_called_once_with(transaction)


def test_update_user_balance(user_repo, mock_db):
    """
    Test for `update_user_balance` verifying the update of a user's balance.

    This test mocks the `update_one` method of the `users` collection and checks
    if the repository correctly updates the user's balance.

    Asserts:
        - The user's balance is updated with the correct amount.
    """
    user_id = "test_user"
    amount = 100.0

    user_repo.update_user_balance(user_id, amount)

    mock_db.users.update_one.assert_called_once_with(
        {"_id": user_id}, {"$inc": {"balance": amount}}
    )


def test_get_transactions(user_repo, mock_db):
    """
    Test for `get_transactions` verifying the retrieval of all transactions for a user.

    This test mocks the `find` method of the `transactions` collection and checks
    if the repository correctly retrieves all transactions for a specific user.

    Asserts:
        - The returned transactions match the expected list of transaction documents.
        - The `find` method is called with the correct filter.
    """
    user_id = "test_user"
    expected_transactions = [{"_id": "trans1"}, {"_id": "trans2"}]
    mock_db.transactions.find.return_value = expected_transactions

    result = user_repo.get_transactions(user_id)

    assert result == expected_transactions
    mock_db.transactions.find.assert_called_once_with({"user_id": user_id})
