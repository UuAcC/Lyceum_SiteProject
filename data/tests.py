from requests import get, post, delete

print(get('http://localhost:8000/api/bands').json())
print()
print(get('http://localhost:8000/api/bands/2').json())
print()
print(get('http://localhost:8000/api/bands/999').json())
print()
print(get('http://localhost:8000/api/bands/q').json())
print()
print(post('http://localhost:8000/api/bands').json())
print()
print(post('http://localhost:8000/api/bands',
           json={'name': 'Пивоеды',
                 'genre': 'Панк',
                 'created_date': '01.01.2024'}).json())
print()
print(delete('http://localhost:8000/api/bands/3').json())
