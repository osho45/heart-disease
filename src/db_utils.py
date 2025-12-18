import sqlite3
import pandas as pd
import os

def create_normalized_db(csv_path, db_path):
    """
    Reads a CSV file and creates a normalized SQLite database.
    Schema includes separate lookup tables for categorical features
    and a main exams table.
    """
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Read Raw Data
    df = pd.read_csv(csv_path)
    
    # Generate Patient IDs (assuming one row per patient for this dataset)
    df['patient_id'] = range(1, len(df) + 1)
    
    # 2. Extract Lookup Tables
    # CP
    cp_values = sorted(df['cp'].unique())
    cursor.execute("CREATE TABLE lookup_cp (cp_code INTEGER PRIMARY KEY, description TEXT)")
    cursor.executemany("INSERT INTO lookup_cp (cp_code, description) VALUES (?, ?)", 
                       [(int(x), f"cp_{x}") for x in cp_values])
                       
    # RestECG
    restecg_values = sorted(df['restecg'].unique())
    cursor.execute("CREATE TABLE lookup_restecg (restecg_code INTEGER PRIMARY KEY, description TEXT)")
    cursor.executemany("INSERT INTO lookup_restecg (restecg_code, description) VALUES (?, ?)", 
                       [(int(x), f"restecg_{x}") for x in restecg_values])
                       
    # Slope
    slope_values = sorted(df['slope'].unique())
    cursor.execute("CREATE TABLE lookup_slope (slope_code INTEGER PRIMARY KEY, description TEXT)")
    cursor.executemany("INSERT INTO lookup_slope (slope_code, description) VALUES (?, ?)", 
                       [(int(x), f"slope_{x}") for x in slope_values])
                       
    # Thal
    thal_values = sorted(df['thal'].unique())
    cursor.execute("CREATE TABLE lookup_thal (thal_code INTEGER PRIMARY KEY, description TEXT)")
    cursor.executemany("INSERT INTO lookup_thal (thal_code, description) VALUES (?, ?)", 
                       [(int(x), f"thal_{x}") for x in thal_values])

    # 3. Create Patients Table
    # Storing Age and Sex separately
    cursor.execute('''
        CREATE TABLE patients (
            patient_id INTEGER PRIMARY KEY,
            age INTEGER,
            sex INTEGER
        )
    ''')
    patients_data = df[['patient_id', 'age', 'sex']].drop_duplicates()
    patients_data.to_sql('patients', conn, if_exists='append', index=False)
    
    # 4. Create Exams Table (The Main Table)
    cursor.execute('''
        CREATE TABLE exams (
            exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            cp INTEGER,
            trestbps INTEGER,
            chol INTEGER,
            fbs INTEGER,
            restecg INTEGER,
            thalach INTEGER,
            exang INTEGER,
            oldpeak REAL,
            slope INTEGER,
            ca INTEGER,
            thal INTEGER,
            target INTEGER,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id),
            FOREIGN KEY(cp) REFERENCES lookup_cp(cp_code),
            FOREIGN KEY(restecg) REFERENCES lookup_restecg(restecg_code),
            FOREIGN KEY(slope) REFERENCES lookup_slope(slope_code),
            FOREIGN KEY(thal) REFERENCES lookup_thal(thal_code)
        )
    ''')
    
    # Prepare exams data
    exams_cols = ['patient_id', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                  'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target']
    exams_data = df[exams_cols]
    exams_data.to_sql('exams', conn, if_exists='append', index=False)
    
    conn.commit()
    conn.close()
    print(f"Database created at {db_path}")

def load_data_from_db(db_path):
    """
    Reconstructs the training dataframe from the normalized SQLite database.
    """
    conn = sqlite3.connect(db_path)
    
    query = '''
        SELECT 
            p.age, p.sex,
            e.cp, e.trestbps, e.chol, e.fbs, e.restecg, 
            e.thalach, e.exang, e.oldpeak, e.slope, e.ca, e.thal, 
            e.target
        FROM exams e
        JOIN patients p ON e.patient_id = p.patient_id
    '''
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
