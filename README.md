# Requirements
* Docker
* Make
* Python

# Main commands
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
2. Run command `make crun`
3. Open `http://localhost:8000/`, wait 25 seconds, reload the page and observe updated users credit card and address info\

OR

3. Open `http://localhost:8888/` and login with next creds: login `admin@admin.com`, password `admin`
4. Register new server for viewing data with next info:
* Name - `tz`
* In "Connection" tab:
* Host name - `db`
* Username - `tz`
* Password - `tz`
5. Expand `Databases/tz/Schemas/public/Tables/creditinfo`
6. Press on users table and pick view data
7. Wait 25 seconds for updating users credit card and address info

User info updates every 15 seconds, User's credit card and address info updates every 25 seconds.
