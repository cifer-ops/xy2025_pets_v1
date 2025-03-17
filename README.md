#Environmental installation- python=3.7+
- Django = 3.2.7

# Installation method- pip install -r requests.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
- python manage.py runserver 
- Browser open http://127.0.0.1:8000/- Admin browser open http://127.0.0.1:8000/admin- Administrator account password: manage createsuperuser
```mermaid
erDiagram
    UserProfile ||--o{PetsInfo} : "owns"
    UserProfile ||--o{Collect} : "collects"
    UserProfile ||--o{Adoption} : "adopts"
    PetsType ||--o{PetsInfo} : "classifies"
    PetsInfo ||--o{Collect} : "collected"
    PetsInfo ||--o{Adoption} : "adopted"

    UserProfile {
      int id PK
    }
    PetsType {
      int id PK
      char name
      datetime updated
      datetime create_time
    }
    PetsInfo {
      int id PK
      image showimg
      char name
      text intro
      char area
      int age
      char status
      datetime updated
      datetime create_time
    }
    Collect {
      int id PK
      datetime updated
      datetime create_time
    }
    Adoption {
      int id PK
      char status
      datetime updated
      datetime create_time
    }
```