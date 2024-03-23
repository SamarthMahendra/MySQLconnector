import mysql.connector as mysql

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully.")
        except mysql.Error as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.Error as e:
            print(f"Error executing query: {e}")
            return []

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

class Menu:
    def __init__(self, connector):
        self.connector = connector

    def display_menu(self):
        print("1: Display the spell types")
        print("2: Disconnect from the database and close the application")
        choice = input("Enter your choice: ")
        if choice == '1':
            self.display_spell_types()
        elif choice == '2':
            self.connector.close_connection()
            print("Exiting the application.")
            exit()
        else:
            print("Invalid choice. Please try again.")
            self.display_menu()

    def display_spell_types(self):
        spell_types = self.connector.execute_query("SELECT DISTINCT type_name FROM spell_type")
        print("Spell Types:")
        for spell_type in spell_types:
            print(spell_type[0])
        self.choose_spell_type()

    def choose_spell_type(self):
        spell_type = input("Enter the spell type: ")
        if self.is_valid_spell_type(spell_type):
            self.execute_spell_has_type(spell_type)
        else:
            print("Invalid spell type. Please try again.")
            self.choose_spell_type()

    def is_valid_spell_type(self, spell_type):
        spell_types = [row[0].lower() for row in self.connector.execute_query("SELECT DISTINCT type_name FROM spell_type")]
        return spell_type.lower() in spell_types

    def execute_spell_has_type(self, spell_type):
        result = self.connector.execute_query("CALL spell_has_type(%s)", (spell_type,))
        print("Result set of spell_has_type():")
        for row in result:
            print(row)


def main():
    user = input("Enter the username: ")
    password = input("Enter the password: ")
    database = 'harry_potter'

    connector = DatabaseConnector('localhost', user, password, database)
    connector.connect()

    spell_menu = Menu(connector)
    while True:
        spell_menu.display_menu()

if __name__ == "__main__":
    main()
