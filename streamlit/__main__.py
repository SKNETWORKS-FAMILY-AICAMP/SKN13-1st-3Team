import subprocess
import sys

# def install_requirements():
#     print("필요한 패키지 설치 중...")
#     subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "pymysql", "folium", "streamlit-folium"], check=True)

def main():
    # 필요한 패키지 설치
    # install_requirements()
    
    # 대시보드 실행
    print("\n=== 대시보드 실행 중... ===")
    subprocess.run(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    main() 