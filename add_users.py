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
            # Sample user data
            users = [
                ("John Smith", "john.smith@email.com"),
                ("Mary Johnson", "mary.j@email.com"), 
                ("Robert Wilson", "rwilson@email.com"),
                ("Sarah Davis", "sarah.davis@email.com"),
                ("Michael Brown", "mbrown@email.com"),
                ("Jennifer Taylor", "jtaylor@email.com"),
                ("David Miller", "dmiller@email.com"),
                ("Lisa Anderson", "lisa.a@email.com"),
                ("James Williams", "jwilliams@email.com"),
                ("Emily Jones", "ejones@email.com")
            ]
            
            # Add each user to database
            for name, email in users:
                user_id = add_user(connection, name, email)
                
                if user_id:
                    print(f"Successfully added user {name} with ID {user_id}")
                else:
                    print(f"Failed to add user {name}")
                    
        finally:
            # Close connection
            connection.close()
            print("\nPostgreSQL connection closed")

if __name__ == "__main__":
    main()
