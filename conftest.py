import pytest
import mysql.connector
from mysql.connector import Error

@pytest.fixture(scope="session")
def my_conftest_test():
    print('mysql_connection fixtureee')
    conn = None
    try:
        conn = mysql.connector.connect(
            host='35.229.171.142',
            user='sfqat_superadmin_qa',  # 'qat_readonly',
            password='dL72QF1Ia4',  # 'NTZ6Wt3tzqCp4k7v',
            port=3306,
            database='GB_Qat'
            # !!this is DATABASEname(GB_Qat) in mysql , not the connectionName on mysql workbench....
        )
        yield conn
    except Error as err:
        pytest.fail(f"MySQL connection error: {err}")
    finally:
        print('mysql at finally')
        if conn and conn.is_connected():
            print('going to close the mysql connection')
            conn.close()