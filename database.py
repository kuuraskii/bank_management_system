
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from typing import Dict, Optional, List, Tuple


class DatabaseManager:
    """Manage database operations with Supabase."""

    def __init__(self):
        """Initialize Supabase client."""
        self.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.table_name = "users"  # Using public.users table

    def get_user_by_id_and_name(self, user_id: int, name: str) -> Optional[Dict]:
        """
        Get user from database by ID and name.

        Args:
            user_id: User ID
            name: User name

        Returns:
            User dictionary or None if not found
        """
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .eq("id", user_id)
                .eq("name", name)
                .execute()
            )

            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Get user from database by ID only.

        Args:
            user_id: User ID

        Returns:
            User dictionary or None if not found
        """
        try:
            response = (
                self.client.table(self.table_name)
                .select("*")
                .eq("id", user_id)
                .execute()
            )

            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None

    def get_user_balance(self, user_id: int, name: str) -> Optional[int]:
        """
        Get balance of a user.

        Args:
            user_id: User ID
            name: User name

        Returns:
            Balance or None if user not found
        """
        user = self.get_user_by_id_and_name(user_id, name)
        if user:
            return user.get("balance", 0)
        return None

    def update_balance(self, user_id: int, new_balance: int) -> bool:
        """
        Update user balance in database.

        Args:
            user_id: User ID
            new_balance: New balance amount

        Returns:
            True if successful, False otherwise
        """
        try:
            response = (
                self.client.table(self.table_name)
                .update({"balance": new_balance})
                .eq("id", user_id)
                .execute()
            )

            if response.data:
                return True
            return False
        except Exception as e:
            print(f"Error updating balance: {e}")
            return False

    def get_all_users(self) -> List[Dict]:
        """
        Get all users from database.

        Returns:
            List of user dictionaries
        """
        try:
            response = self.client.table(self.table_name).select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching all users: {e}")
            return []

    def create_account(self, name: str, email: str, initial_balance: int = 0) -> Tuple[bool, str, Optional[int]]:
        """
        Create a new account in database.

        Args:
            name: User's name
            email: User's email
            initial_balance: Initial account balance (default 0)

        Returns:
            Tuple of (success: bool, message: str, user_id: Optional[int])
        """
        try:
            # Check if email already exists
            existing = (
                self.client.table(self.table_name)
                .select("*")
                .eq("email", email)
                .execute()
            )

            if existing.data and len(existing.data) > 0:
                return False, f"Email {email} already exists", None

            # Create new account
            response = (
                self.client.table(self.table_name)
                .insert({"name": name, "email": email, "balance": initial_balance})
                .execute()
            )

            if response.data and len(response.data) > 0:
                user_id = response.data[0].get("id")
                return True, f"Account created successfully for {name} with ID {user_id}", user_id
            return False, "Failed to create account", None

        except Exception as e:
            return False, f"Error creating account: {e}", None

    def delete_account(self, user_id: int) -> Tuple[bool, str]:
        """
        Delete an account from database.

        Args:
            user_id: User ID to delete

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Check if user exists
            user = self.get_user_by_id(user_id)
            if not user:
                return False, f"User with ID {user_id} not found"

            # Delete user
            response = (
                self.client.table(self.table_name)
                .delete()
                .eq("id", user_id)
                .execute()
            )

            return True, f"Account for {user.get('name')} (ID: {user_id}) deleted successfully"

        except Exception as e:
            return False, f"Error deleting account: {e}"
