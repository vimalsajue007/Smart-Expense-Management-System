import mysql.connector
from functools import reduce
from abc import ABC, abstractmethod

#                                           DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vimal@1234",
    database="expense_db"
)

cursor = conn.cursor()

#                                               Abstract Class 
class BaseSystem(ABC):

    @abstractmethod
    def get_details(self):
        pass
    
#                                                User class
class User(BaseSystem):

    def __init__(self, name):
        self.__name = name   

    def create_user(self):
        query = "INSERT INTO users (name) VALUES (%s)"
        cursor.execute(query, (self.__name,))
        conn.commit()
        print("User Added Successfully!")

    def get_details(self):
        print(f"User Name: {self.__name}")
        
class Expense(User):

    def __init__(self, name, amount, category, description, date):
        super().__init__(name)
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date

    #                                             Method Overriding
    def get_details(self):
        print(f"{self.category} | {self.amount} | {self.date}")
        
        
def add_expense(user_id):
    amount = float(input("Enter amount: "))
    category = input("Enter category: ")
    description = input("Enter description: ")
    date = input("Enter date (YYYY-MM-DD): ")

    query = """
    INSERT INTO expenses (user_id, amount, category, description, date)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, amount, category, description, date))
    conn.commit()

    print("Expense Added!")
    
    
def view_expenses(user_id):
    query = """
    SELECT users.name, expenses.amount, expenses.category, expenses.date
    FROM expenses
    JOIN users ON users.user_id = expenses.user_id
    WHERE users.user_id = %s
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    for row in data:
        print(row)

    return data


def filter_expenses(data):
    category = input("Filter by category: ")

    filtered = list(filter(lambda x: x[2] == category, data))

    print("Filtered Data:")
    for i in filtered:
        print(i)

    #date filter
    date = input("Enter date to filter (YYYY-MM-DD): ")
    date_filtered = [x for x in data if str(x[3]) == date]

    print("Date Filter:")
    for i in date_filtered:
        print(i)
        
def total_expense(data):
    amounts = list(map(lambda x: x[1], data))

    total = reduce(lambda a, b: a + b, amounts, 0)

    print("Total Expense:", total)
    
    
def category_spending(data):
    categories = {x[2] for x in data}

    result = {
        cat: sum([x[1] for x in data if x[2] == cat])
        for cat in categories
    }

    print("Category Wise Spending:")
    for k, v in result.items():
        print(f"{k}: {v}")
        
        
def update_expense():
    exp_id = int(input("Enter Expense ID: "))
    amount = float(input("New Amount: "))

    query = "UPDATE expenses SET amount=%s WHERE exp_id=%s"
    cursor.execute(query, (amount, exp_id))
    conn.commit()

    print("Updated!")
    
    
def delete_expense():
    exp_id = int(input("Enter Expense ID: "))

    query = "DELETE FROM expenses WHERE exp_id=%s"
    cursor.execute(query, (exp_id,))
    conn.commit()

    print("Deleted!")
    
    
def monthly_report(user_id):
    query = """
    SELECT MONTH(date), SUM(amount)
    FROM expenses
    WHERE user_id = %s
    GROUP BY MONTH(date)
    """

    cursor.execute(query, (user_id,))
    data = cursor.fetchall()

    print("Monthly Report:")
    for month, total in data:
        print(f"Month {month}: {total}")
        
        
        
def highest_expense(data):
    highest = reduce(lambda a, b: a if a[1] > b[1] else b, data)

    print("Highest Expense:", highest)
    
    
    
def smart_insight(data):
    category_totals = {}

    for d in data:
        category_totals[d[2]] = category_totals.get(d[2], 0) + d[1]

    highest = max(category_totals, key=category_totals.get)

    print(f"You are spending too much on {highest}")
    
    

while True:
    print("\n1.Add User  \n2.Add Expense  \n3.View  \n4.Filter")
    print("5.Total  \n6.Category  \n7.Update  \n8.Delete")
    print("9.Monthly Report  \n10.Highest  \n11.Insight  \n12.Exit")

    choice = int(input("Enter choice: "))

    if choice == 1:
        name = input("Enter name: ")
        u = User(name)
        u.create_user()

    elif choice == 2:
        uid = int(input("Enter user id: "))
        add_expense(uid)

    elif choice == 3:
        uid = int(input("Enter user id: "))
        data = view_expenses(uid)

    elif choice == 4:
        filter_expenses(data)

    elif choice == 5:
        total_expense(data)

    elif choice == 6:
        category_spending(data)

    elif choice == 7:
        update_expense()

    elif choice == 8:
        delete_expense()

    elif choice == 9:
        uid = int(input("Enter user id: "))
        monthly_report(uid)

    elif choice == 10:
        highest_expense(data)

    elif choice == 11:
        smart_insight(data)

    elif choice == 12:
        break