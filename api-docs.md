# e-commerce-monolith Endpoints Documentation

### User Section

> To generate OTP for login

```sh
POST api/auth/mobile-login/
{
    "phone_number" : <phone_number>
}
Response{
    "message": "OTP is sent. Please check your Phone message box",
    "data": {
        "Status": "Success",
        "Details": <otp_session_id>
    }
}
```

> To verify OTP for login

```sh
POST api/auth/login-verify-otp/
{
    "phone_number" : "+913131313131",
    "otp" : "123456",
    "otp_session_id" : "dc8ee5a9-7258-4327-bdf5-adbee969e54f",
}
Response{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEwNjgwMDkwLCJpYXQiOjE3MDkzODQwOTAsImp0aSI6ImM0NGE4MDZmNzYxNDRmMDZiM2NmMzE3MzAxZDBkMmY1IiwidXNlcl9pZCI6M30.VsZAdC0rsCQ-aZHHMaH6hvMU4bHcPPI9edUceAEcOUE",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMTk3NjA5MCwiaWF0IjoxNzA5Mzg0MDkwLCJqdGkiOiIwNDlmNTg1N2E4OTE0YjU0YmMyOGFmYTI1NzI1NjIyYiIsInVzZXJfaWQiOjN9.5xELp0qSz1r0p7VHTqf8eZTxIw4vvgYcxELbz73rQ_0",
    "user": {
        "uid": "c9f58274-eb4c-4a13-bdd5-346b0dfd4832",
        "email": null,
        "first_name": "",
        "last_name": "",
        "full_name": " ",
        "city": "Jind",
        "state": "rajasthan",
        "profile_photo": null,
        "phone_number": "+916262626262",
        "addresses": [
            {
                "created": "2023-06-15T14:46:32.943854+05:30",
                "modified": "2023-06-15T14:46:32.943876+05:30",
                "uid": "b9aa7803-a623-46f5-a586-5c6d032a1f07",
                "address_line_1": "D-95",
                "address_line_2": "",
                "landmark": null,
                "city": "Udaipur",
                "state": "Rajasthan",
                "pincode": 302023,
                "country": "India",
                "is_default": true,
                "user": 41
            }
        ]
    }
}
```

> To get user info

```sh
GET  api/auth/user-info/

Response{
    "uid": "c9f58274-eb4c-4a13-bdd5-346b0dfd4832",
    "email": null,
    "first_name": "",
    "last_name": "",
    "phone_number": "+916262626262",
    "profile_photo": null,
    "city": "jaipur",
    "state": "rajasthan",
    "registered_at": "2024-03-02T12:25:27.281455Z",
    "date_of_birth": null
}
```

> To update user details

```sh
PATCH  api/auth/user/

{
    "city" : <city>,
}

Response{
    "uid": "c9f58274-eb4c-4a13-bdd5-346b0dfd4832",
    "email": null,
    "first_name": "",
    "last_name": "",
    "full_name": " ",
    "city": "Jind",
    "state": "rajasthan",
    "profile_photo": null,
    "phone_number": "+916262626262"
}
```

> To logout User
```sh

POST api/auth/logout/
{
  "refresh" : <refresh_token>
}
Response{
    "detail": "Successfully logged out."
}
```

> To get new access token
```sh

POST api/auth/token/refresh/
{
  "refresh" : <refresh_token>
}
Response{
    "access": <new_access_token>,
    "access_token_expiration": <date and time>
}
```
