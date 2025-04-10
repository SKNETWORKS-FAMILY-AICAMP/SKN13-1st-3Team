import pandas as pd

connection =  pymysql.connect(host ="192.168.0.45",
                                    port:3306,
                                    user ="3team",
                                    password:str="1111",
                                    db = "gas_station",
                                    charset = "utf8",
                                    )

#sql 쿼리 실행하여 데이터 가져오기
query ="SELECT * FROM gas_station"
df = pd.read_sql(query, connection)

#연결종료
connection.close()

#데이터 확인
print(df.head())#처음 5개행 출력
print(df.info()) #데이터 프레임 정보출력
