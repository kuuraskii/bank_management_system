"""
Main CLI interface for the bank management system.
"""
from transfer import TransferManager
from database import DatabaseManager


def display_menu():
    """Display main menu options."""
    print("\n" + "=" * 60)
    print("BANK MANAGEMENT SYSTEM")
    print("=" * 60)
    print("1. Check Balance")
    print("2. Transfer Funds")
    print("3. Create Account")
    print("4. Delete Account")
    print("5. View All Users")
    print("6. View Transaction History")
    print("7. Exit")
    print("=" * 60)


def check_balance_option(transfer_manager):
    """Handle balance check option."""
    try:
        user_id = int(input("Enter User ID: "))
        name = input("Enter Name: ").strip()

        success, message, balance = transfer_manager.check_balance(user_id, name)
        print("\n" + message)
        if success:
            print(f"Balance: ${balance}")
    except ValueError:
        print("Invalid User ID. Please enter a number.")
    except Exception as e:
        print(f"Error: {e}")


def transfer_funds_option(transfer_manager):
    """Handle fund transfer option."""
    try:
        sender_id = int(input("Enter Sender ID: "))
        sender_name = input("Enter Sender Name: ").strip()
        receiver_id = int(input("Enter Receiver ID: "))
        amount = int(input("Enter Amount to Transfer: "))

        success, message = transfer_manager.transfer_funds(
            sender_id, sender_name, receiver_id, amount
        )

        if success:
            print(f"\n✓ {message}")
            # Show transaction details
            if transfer_manager.transactions:
                transfer_manager.print_transaction_details(transfer_manager.transactions[-1])
        else:
            print(f"\n✗ {message}")

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error: {e}")


def create_account_option(transfer_manager):
    """Handle account creation option."""
    try:
        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()
        
        balance_input = input("Enter Initial Balance (default 0): ").strip()
        initial_balance = int(balance_input) if balance_input else 0

        success, message, user_id = transfer_manager.create_account(name, email, initial_balance)

        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")

    except ValueError:
        print("Invalid input. Please enter valid numbers for balance.")
    except Exception as e:
        print(f"Error: {e}")


def delete_account_option(transfer_manager):
    """Handle account deletion option."""
    try:
        user_id = int(input("Enter User ID to Delete: "))
        confirm_name = input("Enter the account holder's name to confirm deletion: ").strip()

        # Show warning
        print("\n" + "!" * 60)
        print("WARNING: This action cannot be undone!")
        print("!" * 60)
        confirm = input("Are you sure you want to delete this account? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Deletion cancelled.")
            return

        success, message = transfer_manager.delete_account(user_id, confirm_name)

        if success:
            print(f"\n✓ {message}")
        else:
            print(f"\n✗ {message}")

    except ValueError:
        print("Invalid User ID. Please enter a number.")
    except Exception as e:
        print(f"Error: {e}")


def view_all_users_option():
    """Handle view all users option."""
    db = DatabaseManager()
    users = db.get_all_users()

    if not users:
        print("\nNo users found in database.")
        return

    print("\n" + "=" * 80)
    print(f"{'ID':<5} {'Name':<25} {'Email':<30} {'Balance':<15}")
    print("=" * 80)

    for user in users:
        user_id = user.get("id", "N/A")
        name = user.get("name", "N/A")
        email = user.get("email", "N/A")
        balance = user.get("balance", 0)

        print(f"{user_id:<5} {name:<25} {email:<30} ${balance:<14}")

    print("=" * 80)


def view_transaction_history_option(transfer_manager):
    """Handle view transaction history option."""
    transactions = transfer_manager.get_transaction_history()

    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n" + "=" * 100)
    print("TRANSACTION HISTORY")
    print("=" * 100)

    for i, transaction in enumerate(transactions, 1):
        print(f"\nTransaction {i}:")
        transfer_manager.print_transaction_details(transaction)


def main():
    """Main function to run the CLI."""
    transfer_manager = TransferManager()

    print("\n" + "=" * 60)
    print("Welcome to Bank Management System")
    print("=" * 60)

    while True:
        display_menu()
        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            check_balance_option(transfer_manager)
        elif choice == "2":
            transfer_funds_option(transfer_manager)
        elif choice == "3":
            create_account_option(transfer_manager)
        elif choice == "4":
            delete_account_option(transfer_manager)
        elif choice == "5":
            view_all_users_option()
        elif choice == "6":
            view_transaction_history_option(transfer_manager)
        elif choice == "7":
            print("\nThank you for using Bank Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
