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
