"""
Transfer module for handling money transfers between users.
"""
from database import DatabaseManager
from typing import Tuple, Dict, Optional


class TransferManager:
    """Manage fund transfers between users."""

    def __init__(self):
        """Initialize TransferManager with database connection."""
        self.db = DatabaseManager()
        self.transactions = []

    def check_balance(self, user_id: int, name: str) -> Tuple[bool, str, Optional[int]]:
        """
        Check balance of a user by ID and name.

        Args:
            user_id: User ID
            name: User name

        Returns:
            Tuple of (success: bool, message: str, balance: Optional[int])
        """
        if not user_id or not name:
            return False, "User ID and name are required", None

        balance = self.db.get_user_balance(user_id, name)

        if balance is None:
            return False, f"User with ID {user_id} and name '{name}' not found", None

        return True, f"Balance for {name}: ${balance}", balance

    def transfer_funds(
        self, sender_id: int, sender_name: str, receiver_id: int, amount: int
    ) -> Tuple[bool, str]:
        """
        Transfer funds from one user to another.

        Args:
            sender_id: Sender's user ID
            sender_name: Sender's name
            receiver_id: Receiver's user ID
            amount: Amount to transfer

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validation
        if amount <= 0:
            return False, "Transfer amount must be greater than 0"

        # Get sender details
        sender = self.db.get_user_by_id_and_name(sender_id, sender_name)
        if not sender:
            return False, f"Sender with ID {sender_id} and name '{sender_name}' not found"

        # Get receiver details
        receiver = self.db.get_user_by_id(receiver_id)
        if not receiver:
            return False, f"Receiver with ID {receiver_id} not found"

        sender_balance = sender.get("balance", 0)
        receiver_balance = receiver.get("balance", 0)

        # Check if sender has sufficient balance
        if sender_balance < amount:
            return (
                False,
                f"Insufficient balance. Current balance: ${sender_balance}, Required: ${amount}",
            )

        # Perform transfer
        new_sender_balance = sender_balance - amount
        new_receiver_balance = receiver_balance + amount

        # Update sender balance
        if not self.db.update_balance(sender_id, new_sender_balance):
            return False, "Failed to update sender balance"

        # Update receiver balance
        if not self.db.update_balance(receiver_id, new_receiver_balance):
            # Rollback sender balance if receiver update fails
            self.db.update_balance(sender_id, sender_balance)
            return False, "Failed to update receiver balance. Transaction rolled back"

        # Record transaction
        transaction_record = {
            "sender_id": sender_id,
            "sender_name": sender_name,
            "receiver_id": receiver_id,
            "receiver_name": receiver.get("name"),
            "amount": amount,
            "sender_balance_before": sender_balance,
            "sender_balance_after": new_sender_balance,
            "receiver_balance_before": receiver_balance,
            "receiver_balance_after": new_receiver_balance,
        }
        self.transactions.append(transaction_record)

        return (
            True,
            f"Successfully transferred ${amount} from {sender_name} to {receiver.get('name')}",
        )

    def get_transaction_history(self) -> list:
        """
        Get all transactions history.

        Returns:
            List of transaction records
        """
        return self.transactions

    def print_transaction_details(self, transaction: Dict) -> None:
        """
        Print details of a transaction.

        Args:
            transaction: Transaction dictionary
        """
        print("\n" + "=" * 60)
        print("TRANSACTION DETAILS")
        print("=" * 60)
        print(f"From: {transaction['sender_name']} (ID: {transaction['sender_id']})")
        print(f"To: {transaction['receiver_name']} (ID: {transaction['receiver_id']})")
        print(f"Amount: ${transaction['amount']}")
        print(f"Sender Balance: ${transaction['sender_balance_before']} → ${transaction['sender_balance_after']}")
        print(f"Receiver Balance: ${transaction['receiver_balance_before']} → ${transaction['receiver_balance_after']}")
        print("=" * 60 + "\n")

    def create_account(self, name: str, email: str, initial_balance: int = 0) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new account.

        Args:
            name: User's name
            email: User's email
            initial_balance: Initial account balance (default 0)

        Returns:
            Tuple of (success: bool, message: str, user_id: Optional[int])
        """
        if not name or not email:
            return False, "Name and email are required", None

        if not email or "@" not in email:
            return False, "Invalid email format", None

        if initial_balance < 0:
            return False, "Initial balance cannot be negative", None

        return self.db.create_account(name, email, initial_balance)

    def delete_account(self, user_id: int, confirm_name: str) -> Tuple[bool, str]:
        """
        Delete an account.

        Args:
            user_id: User ID to delete
            confirm_name: Confirmation name to prevent accidental deletion

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not user_id:
            return False, "User ID is required"

        # Get user to verify name
        user = self.db.get_user_by_id(user_id)
        if not user:
            return False, f"User with ID {user_id} not found"

        # Verify confirmation name matches
        if user.get("name") != confirm_name:
            return False, "Name confirmation failed. Account not deleted."

        return self.db.delete_account(user_id)
