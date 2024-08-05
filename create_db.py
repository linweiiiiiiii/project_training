import sqlite3
import os

def create_database():
    # Database file path
    db_path = 'training_bugs.db'
    
    # Delete the database file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Existing database deleted.")

    # Create a new database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Subject table
    cursor.execute('''
    CREATE TABLE Subject (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(90) NOT NULL
    )
    ''')

    # Create Trainer table
    cursor.execute('''
    CREATE TABLE Trainer (
        trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(50) NOT NULL,
        family_name VARCHAR(50) NOT NULL
    )
    ''')

    # Create Training table
    cursor.execute('''
    CREATE TABLE Training (
        t_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_id INTEGER NOT NULL,
        trainer_id INTEGER NOT NULL,
        date_training DATE NOT NULL,
        details VARCHAR(250) NOT NULL,
        FOREIGN KEY (subject_id) REFERENCES Subject(subject_id),
        FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
    )
    ''')

    # Insert initial data for Subject
    cursor.executemany('''
    INSERT INTO Subject (subject_id, name) VALUES (?, ?)
    ''', [
        (1, 'Accounting'),
        (2, 'Construction Blueprint'),
        (3, 'Project Management'),
        (4, 'Software Use'),
        (5, 'Supplier Management')
    ])

    # Insert initial data for Trainer
    cursor.executemany('''
    INSERT INTO Trainer (trainer_id, first_name, family_name) VALUES (?, ?, ?)
    ''', [
        (1, 'Granu', 'Larity'),
        (2, 'Piane', 'Riona'),
        (3, 'Sara', 'Organa'),
        (4, 'Axel', 'Walker')
    ])

    # Insert initial data for Training
    cursor.executemany('''
    INSERT INTO Training (t_id, subject_id, trainer_id, date_training, details) VALUES (?, ?, ?, ?, ?)
    ''', [
        (1, 1, 1, '2017-09-07', 'Creating a robust Financial Report'),
        (2, 2, 2, '2016-02-14', 'Getting Started with Landed House Blueprint'),
        (3, 3, 3, '2018-03-03', 'Managing Project which has gone over the initial budget'),
        (4, 4, 1, '2018-11-09', 'Customization of a Supply Chain Management system'),
        (5, 5, 4, '2018-10-14', 'Dealing with Supplier who keeps increasing their price')
    ])

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database created successfully.")
