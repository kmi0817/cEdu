# cEdu

**0. What you need**

- run.py

```
from app import app

if __name__ == '__main__' :
    app.run(debug=True)
```

- venv directory

```
python -m venv [venv name]
pip install Flask
```

**1. How to Start?**

```
# Mac should use python3
python run.py
```

**2. Environments**

```
# Mac should use pip3
pip install Flask
pip install pymongo
pip install python-slugify
```

- use Flask as Server
- use MongoDB as Database

**3. To do**

- [x] 카테고리: 커뮤니티 글 삭제 고치기
- [x] 커뮤니티에서 description 넘치는 것 고치기
- [x] 글 수정 기능 추가
- [x] 회원가입 수정
- [x] 로그인 수정
- [ ] 글 작성 시 이미지 첨부
- [x] 게시글 댓글
- [ ] 회원 정보 수정 및 탈퇴

**4. Reference**

- MongoDB install (MAC) : https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/
- connect and use MongoDB : mongosh
- MongoDB Compass install (MAC) : https://www.mongodb.com/try/download/compass & https://soyoung-new-challenge.tistory.com/95
