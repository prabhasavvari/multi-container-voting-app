import redis
import psycopg2
import time
import sys
import os

def connect_to_db():
    """Attempt to establish a secure link to the PostgreSQL database vault"""
    db_password = os.getenv("DB_PASSWORD")

    while True:
        try:
            conn = psycopg2.connect(
                host="postgres",
                database="voting_db",
                user="prabhas",
                password=db_password
            )
            return conn
        except psycopg2.OperationalError:
            print("Database vault not ready yet. Retrying in 2 seconds...")
            time.sleep(2)

def main():
    print("Backend Worker initialized successfully! Watching the cache room...")
    
    # 1. Connect to the high-speed Redis cache room
    r = redis.Redis(host="redis", port=6379, socket_timeout=2)
    
    # 2. Connect to the permanent PostgreSQL database vault
    db_conn = connect_to_db()
    cursor = db_conn.cursor()
    
    # 3. Create the SQL data storage table structure if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id SERIAL PRIMARY KEY,
            vote VARCHAR(10) NOT NULL
        );
    """)
    db_conn.commit()

    # 4. Infinite looping automation loop: Process votes instantly
    while True:
        try:
            # Check the Redis cache keys for cats and dogs
            for team in ['cats', 'dogs']:
                # Pull the count out of the cache room
                count = r.get(team)
                if count and int(count) > 0:
                    # Clear the vote out of the temporary cache queue bucket
                    r.decr(team)
                    
                    # Log the vote permanently inside the PostgreSQL database table
                    cursor.execute("INSERT INTO votes (vote) VALUES (%s);", (team,))
                    db_conn.commit()
                    print(f"Worker Success: Moved 1 vote for '{team}' from Cache to Database Vault!")
                    sys.stdout.flush() # Force print out to terminal instantly
        except Exception as e:
            print(f"Worker Error: Connection drop detected. Details: {e}")
            sys.stdout.flush()
        
        time.sleep(1) # Sleep for 1 second before checking the cache loop again

if __name__ == "__main__":
    main()
