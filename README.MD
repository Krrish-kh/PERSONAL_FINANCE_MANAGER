# Personal Finance Manager

## Overview
This Personal Finance Manager is a Python-based application that helps users manage their finances, track income and expenses, set savings goals, and visualize their financial data. It uses SQLite for data storage and matplotlib for generating graphs.

## Features

### User Management
1. **Sign Up**: New users can create an account with a username and password.
2. **Login**: Existing users can log in using their credentials.
3. **Recent Logins**: The system remembers recent logins for quick access.
4. **Password Recovery**: Users can reset their password using a security question.
5. **Delete Account**: Users can delete their account and all associated data.

### Financial Management
1. **Add Income**: Users can record their income.
2. **Add Expense**: Users can log their expenses along with the purpose.
3. **View Expenses**: Users can see a list of their recorded expenses.
4. **Set Savings Goal**: Users can set a target savings amount.
5. **Check Savings**: Users can view their current savings status and progress towards their goal.

### Reporting and Visualization
1. **View Income vs Expense Graph**: A bar chart comparing total income and expenses.
2. **View Donut Chart**: A pie chart showing the proportion of expenses to savings.
3. **View Savings Bar Chart**: A bar chart displaying the total savings.
4. **View Full Report**: A comprehensive report including all financial data and graphs.

### Additional Features
1. **Latest Finance Updates**: Redirects users to the Financial Times website for current financial news.
2. **Data Persistence**: All user data is stored in an SQLite database for future access.

## Technical Details
- **Language**: Python
- **Database**: SQLite
- **Libraries Used**:
  - `sqlite3` for database operations
  - `matplotlib` for graph generation
  - `hashlib` for password hashing

## How to Use
1. Run the script and choose from the interface menu options:
   - Sign Up
   - Log In
   - Exit
2. After logging in, use the working menu to access various features:
   - Manage income and expenses
   - Set and check savings goals
   - View financial reports and graphs
   - Access latest finance updates
   - Logout or delete account

## Security
- Passwords are hashed using SHA-256 before storing in the database.
- The application includes a basic password recovery system using security questions.

## Future Improvements
- Implement more detailed categorization for expenses
- Add support for multiple currencies!
- Enhance the user interface with a graphical UI
- Implement data export features for backup purposes

---

This Personal Finance Manager is designed to help individuals take control of their finances by providing easy-to-use tools for tracking, analyzing, and visualizing their financial data.
