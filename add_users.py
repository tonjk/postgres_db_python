import psycopg2
from psycopg2 import Error

def connect_to_db():
    try:
        # Database connection parameters
        connection = psycopg2.connect(
            host="localhost",
            database="postgres", 
            user="postgres",
            password="admin",
            port="5432"
        )
        return connection
    except (Exception, Error) as error:
        print("Error connecting to PostgreSQL:", error)
        return None

def add_user(connection, name, email):
    try:
        cursor = connection.cursor()
        
        # Insert user query
        insert_query = """
        INSERT INTO users (name, email)
        VALUES (%s, %s) RETURNING id
        """
        cursor.execute(insert_query, (name, email))
        user_id = cursor.fetchone()[0]
        connection.commit()
        print(f"User added successfully. User ID: {user_id}")
        return user_id
        
    except (Exception, Error) as error:
        print("Error adding user:", error)
        return None

def main():
    # Connect to database
    connection = connect_to_db()
    
    if connection:
        try:
            while True:
                # Get user input
                print("\nEnter user details (or press Enter to quit):")
                name = input("Name: ").strip()
                
                if not name:  # Exit if name is empty
                    break
                    
                email = input("Email: ").strip()
                
                # Add user to database
                user_id = add_user(connection, name, email)
                
                if user_id:
                    print(f"Successfully added user {name} with ID {user_id}")
                else:
                    print("Failed to add user")
                    
                continue_adding = input("\nAdd another user? (y/n): ").lower()
                if continue_adding != 'y':
                    break
                    
        finally:
            # Close connection
            connection.close()
            print("\nPostgreSQL connection closed")

if __name__ == "__main__":
    main()
