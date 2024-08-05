# Requirements
* Poetry
* Docker
* Make
* Python

# Main commands
Installing packages
```
make poetry
```

Formatting the code
```
make format
```

Run project
```
make run
```

Clean run project (rebuild and run)
```
make crun
```

# First step

1. Rename `.env.example` file to `.env`
2. Run command `make poetry`
3. Run command `make run`
4. Open `http://localhost:8888/` and login with next creds: login `admin@admin.com`, password `admin`
5. Register new server for viewing data with next info:
* Name - `tz`
* In "Connection" tab:
* Host name - `db`
* Username - `tz`
* Password - `tz`
6. Expand `Databases/tz/Schemas/public/Tables/users`
7. Press on users table and pick view data
8. Wait 25 seconds for updating users credit card and address info

User info updates every 15 seconds, User's credit card and address info updates every 25 seconds.