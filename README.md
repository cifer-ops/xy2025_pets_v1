# 环境安装
- python=3.7+
- Django = 3.2.7

# 安装方法
- pip install -r requests.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
- python manage.py runserver 
- 浏览器打开 http://127.0.0.1:8000/
- 管理员浏览器打开 http://127.0.0.1:8000/admin
- 管理员账号密码： manage createsuperuser

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