**Problem Statement**: Great Fitness has recently expanded into a network of 15 gyms within California. Each gym has approximately 200 members, 8 basketball courts and members are able to reserve basketball courts at Great Fitness gyms. The Great Fitness owners recognized the need to create a database management system to track court reservations.

**Database Outlines**

**Gyms:** Represent a Great Fitness gym
- **gym_ID:** PK, int, auto_increment, unique, not NULL
- **location:** VARCHAR, not NULL
- **email:** VARCHAR, not NULL
- **opening_time:** TIME, not NULL
- **closing_time:** TIME, not NULL
- **Relationships:** M:N with Members, 1:M with Courts

**Courts:** Represent courts within a gym
- **court_ID:** PK, int, unique, auto_increment, not NULL
- **gym_ID:** FK
- **court_name:** VARCHAR, unique, not NULL
- **Relationships:** M:1 with Gyms, 1:M with Reservations

**Reservations:** Represent reservations made by gym members
- **reservation_ID:** PK, int, unique, auto_increment, not NULL
- **court_ID:** FK
- **member_ID:** FK
- **reservation_start:** DATETIME, not NULL
- **reservation_end:** DATETIME, not NULL
- **paid:** TINYINT
- **Relationships:** M:1 with Courts, M:1 with Members

**Members:** Represents gym members making the reservations
- **member_ID:** PK, int, unique, auto_increment, not NULL
- **first_name:** VARCHAR, unique, not NULL
- **last_name:** VARCHAR, unique, not NULL
- **age:** int, not NULL
- **email:** VARCHAR, unique, not NULL
- **gender:** CHAR, unique, not NULL
- **Relationships:** 1:M with Reservations, M:N with GymMemberships

**GymMemberships:** Intersection table for the M:M relationship between Gyms and Members table
- **gym_memberships_ID:** PK
- **gym_ID:** FK
- **member_ID:** FK
- **paid:** TINYINT
- **Relationships:** M:1 with Gyms, M:1 with Members
