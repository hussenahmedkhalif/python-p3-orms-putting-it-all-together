import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
        CREATE TABLE IF NOT EXISTS dogs (
            id INTEGER PRIMARY KEY,
            name TEXT,
            breed TEXT
        )
        ''')
        CONN.commit()



    @classmethod
    def drop_table(cls):
        CURSOR.execute('''
        DROP TABLE IF EXISTS dogs
        ''')
        CONN.commit()

    def save(self):
        CURSOR.execute('''
        INSERT INTO dogs (name, breed) 
        VALUES (?, ?)
        ''', (self.name, self.breed))
        
        # Update the instance's id with the last inserted id
        self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls, name, breed):
        # Create a new Dog instance and save it to the database
        dog = cls(name, breed)
        dog.save()
        return dog
    
    @classmethod
    def new_from_db(cls, row):
        # The row is expected to be in the format: (id, name, breed)
        dog_id, name, breed = row
        return cls(name, breed, dog_id)
    
    @classmethod
    def get_all(cls):
        # Query to select all records from the dogs table
        sql = "SELECT * FROM dogs"
        rows = CURSOR.execute(sql).fetchall()
        
        # Convert each row to a Dog instance using new_from_db() and return as a list
        return [cls.new_from_db(row) for row in rows]
    
    @classmethod
    def find_by_name(cls, name):
        # Query to select a record from the dogs table based on the name
        sql = "SELECT * FROM dogs WHERE name = ? LIMIT 1"
        row = CURSOR.execute(sql, (name,)).fetchone()
        
        # If a row is found, convert it to a Dog instance using new_from_db() and return it
        if row:
            return cls.new_from_db(row)
        else:
            return None  # Return None if no record is found
    
    @classmethod
    def find_by_id(cls, id):
        # SQL query to find a dog by its ID
        sql = "SELECT * FROM dogs WHERE id = ? LIMIT 1"
        row = CURSOR.execute(sql, (id,)).fetchone()
        
        # Check if the row is found
        if row:
            # Convert the row to a Dog instance using new_from_db()
            return cls.new_from_db(row)
        return None
    
    @classmethod
    def find_or_create_by(cls, name, breed):
        # Query the database to find a dog with the given name and breed
        sql = "SELECT * FROM dogs WHERE name = ? AND breed = ? LIMIT 1"
        row = CURSOR.execute(sql, (name, breed)).fetchone()
        
        # If a dog is found, return it as a Dog instance
        if row:
            return cls.new_from_db(row)
        
        # If no dog is found, create a new dog and save it to the database
        new_dog = cls.create(name, breed)
        return new_dog
    
    def update(self):
        # Ensure the dog instance has an id (it must have been saved to the database)
        if self.id is None:
            raise ValueError("Dog must be saved to the database before updating.")

        # SQL query to update the record in the database
        sql = '''
        UPDATE dogs 
        SET name = ?, breed = ?
        WHERE id = ?
        '''
        CURSOR.execute(sql, (self.name, self.breed, self.id))
        CONN.commit()

