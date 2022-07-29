import psycopg2
import bcrypt

connection = psycopg2.connect("dbname=niceities")
cursor = connection.cursor()

cursor.execute("INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s);", ('test1', 'test1@gmail.com', bcrypt.hashpw(b"letmein", bcrypt.gensalt()).decode()))


cursor.execute("""
INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s);
""",("test2", "test2@gmail.com", bcrypt.hashpw(b"letmein", bcrypt.gensalt()).decode()))

connection.commit()


cursor.execute("""
INSERT INTO sentences (user_id, sentence) 
VALUES (%s, %s);
""", (1, "Test Sentence 1"))
cursor.execute("""
INSERT INTO sentences (user_id, sentence, likes) VALUES (%s, %s, %s);
""", (2, "Test Sentence 2", 3))
cursor.execute("""
INSERT INTO sentences (user_id, sentence, likes) VALUES (%s, %s, %s);
""", (1, "Test Sentence 3", 10))

connection.commit()

connection.close()