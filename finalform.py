import duckdb
import os

def load_db(in_file,table_name,db_path):
    # Connect to Database, EPastore 05/15/2026
    con = duckdb.connect(db_path)

    # Load data into database and close connection, EPastore 05/15/2026
    con.sql(
        f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT *
            FROM read_csv('{in_file}')
        """
    )

    con.close()

def main():
    # Declare Constants, EPastore 05/17/2026
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.join(SCRIPT_DIR,'employee_satisfaction_survey.csv')
    TABLE_NAME = 'employee_satisfaction'
    DB_PATH = os.path.join(SCRIPT_DIR,"my_database.duckdb")

    # Create table in database, EPastore 05/17/2026
    load_db(CSV_FILE,TABLE_NAME,DB_PATH)

    # Connect to the database, EPastore 05/17/2026
    con = duckdb.connect(DB_PATH)

    # Test connection, EPastore 05/17/2026
    print(
    con.sql(
        f"""
            SELECT * FROM {TABLE_NAME} LIMIT 10;
        """))
    
    # Business Question
    # Isolate each employee's most recent response, then count how many employees fall into each satisfaction rating, EPastore 07/03/2026
    # Primary Business Question: How many employees reported satisfaction scores of "1" on their most recent survey responses?

    print(
        con.sql(
            f"""
            WITH latest AS 
            (
                SELECT Email, Satisfaction
                FROM employee_satisfaction
                QUALIFY ROW_NUMBER() OVER (PARTITION BY Email ORDER BY Timestamp DESC) = 1
            )

            SELECT Satisfaction, COUNT(Email) AS Employees
            FROM latest
            GROUP BY Satisfaction;
"""
        )
    )

if __name__ == '__main__':
    main()

