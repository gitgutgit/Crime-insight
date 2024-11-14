import psycopg2
import toml

config = toml.load("secrets.toml")
DB_URL = config["database"]["DB_URL"]

def reset_crime_sequence():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    # Crime 테이블의 현재 최대 Crime_id 값 가져오기
    cursor.execute("SELECT MAX(Crime_id) FROM Crime")
    max_crime_id = cursor.fetchone()[0]

    # Crime_id 시퀀스를 최대 Crime_id 값 이후로 재설정
    if max_crime_id is not None:
        cursor.execute(f"ALTER SEQUENCE crime_crime_id_seq RESTART WITH {max_crime_id + 1};")
        print(f"Crime_id 시퀀스가 {max_crime_id + 1}로 재설정되었습니다.")
    else:
        print("Crime 테이블에 데이터가 없으므로 시퀀스 재설정이 필요하지 않습니다.")

    conn.commit()
    cursor.close()
    conn.close()

# 시퀀스 재설정 함수 실행
reset_crime_sequence()
