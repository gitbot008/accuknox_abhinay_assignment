Deployed link of assignment on render with debug=True so that it can be tested from django provided forms itself.

Link- https://accuknox-abhinay-assignment.onrender.com

Note-All functional apis are under the sub-route of "api/" and i have also added the redoc and swagger documentations for clarity.



# To test the setup in local env
 - Navigate to the directory with docker-compose file.
 - run <docker compose up --build>  

# API Documentation


### Sign Up View:
- **URL:** `/api/signup/`
- **Method:** POST
- **Description:** Allows users to sign up by providing their details including email, username, and password.
- **Request Data:**
  - email (string): User's email address.
  - username (string): User's username.
  - password (string): User's password.
- **Response:**
  - Success (201 Created):
    ```json
    {
        "message": "User Created Successfully",
        "data": {
            "id": 1,
            "email": "example@example.com",
            "username": "example"
        }
    }
    ```
  - Error (400 Bad Request): If there are validation errors in the provided data.

### Login View:
- **URL:** `/api/login/`
- **Method:** POST
- **Description:** Allows users to log in by providing their email and password.
- **Request Data:**
  - email (string): User's email address.
  - password (string): User's password.
- **Response:**
  - Success (200 OK):
    ```json
    {
        "message": "Login Successfull",
        "tokens": {
            "access": "<access_token>",
            "refresh": "<refresh_token>"
        }
    }
    ```
  - Error (Unauthorized 401): If the provided credentials are invalid.

### User List and Creation View:
- **URL:** `/api/users/`
- **Method:** GET, POST
- **Description:** Allows authenticated users to view and create other users' profiles.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can access this endpoint.
- **GET Response:** Returns a list of all users' profiles.
- **POST Request Data:**
  - email (string): User's email address.
  - username (string): User's username.
  - date_of_birth (date): User's date of birth.
- **POST Response:** Returns the newly created user's profile.
- **Error (401 Unauthorized):** If the user is not authenticated.

### User Detail View:
- **URL:** `/api/users/<user_id>/`
- **Method:** GET, PUT, DELETE
- **Description:** Allows authenticated users to view, update, and delete a specific user's profile.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can access this endpoint.
- **GET Response:** Returns the specified user's profile.
- **PUT Request Data:** Updates the user's profile details.
- **DELETE Response:** Deletes the specified user's profile.
- **Error (401 Unauthorized):** If the user is not authenticated.

### Friend Request Create View:
- **URL:** `/api/friend-requests/`
- **Method:** POST
- **Description:** Allows authenticated users to send friend requests to other users.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can send friend requests.
- **Request Data:**
  - receiver_id (integer): ID of the user to whom the friend request is sent.
- **Response:** Returns a success message if the friend request is sent successfully.
- **Error (400 Bad Request):** If the receiver_id is not provided or invalid.

### Friend Request List View:
- **URL:** `/api/friend-requests/`
- **Method:** GET, POST
- **Description:** Allows authenticated users to view and create friend requests.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can access this endpoint.
- **GET Response:** Returns a list of all friend requests sent by the authenticated user.
- **POST Request Data:** Sends a new friend request.
- **Error (401 Unauthorized):** If the user is not authenticated.

### Email API View:
- **URL:** `/api/send-email/`
- **Method:** GET
- **Description:** Sends an email to the specified recipient.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can access this endpoint.
- **Request Parameters:**
  - product_id (integer): ID of the product being reviewed.
  - emreceiver (string): Email address of the recipient.
  - article_title (string): Title of the article being reviewed.
  - article_link (string): Link to the article being reviewed.
- **Response:** Returns a success message if the email is sent successfully.
- **Error (500 Internal Server Error):** If there is an issue sending the email.

### Friend Request Accept and Reject Views:
- **URL:** `/api/friend-requests/accept/` and `/api/friend-requests/reject/`
- **Method:** POST
- **Description:** Allows authenticated users to accept or reject friend requests.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can accept or reject friend requests.
- **Request Data:**
  - friend_request_id (integer): ID of the friend request to accept or reject.
- **Response:** Returns a success message if the friend request is accepted or rejected successfully.
- **Error (400 Bad Request):** If the friend_request_id is not provided or invalid.

### User Search View:
- **URL:** `/api/user-search/`
- **Method:** GET
- **Description:** Allows authenticated users to search for other users by email or username.
- **Authentication:** Basic Authentication
- **Permissions:** Only authenticated users can search for other users.
- **Request Parameters:**
  - keyword (string): Search keyword to find users by email or username.
- **Response:** Returns the user's profile if a match is found. If multiple matches are found, returns an error message.

### Cookie feature JWT Token Endpoints:

### Obtain JWT Access Token:
- **URL:** `/api/jwt/create/`
- **Method:** POST
- **Description:** Allows users to obtain a JWT access token by providing valid credentials (email and password).
- **Request Data:**
  - username (string): User's username or email address.
  - password (string): User's password.
- **Response:**
  - Success (200 OK):
    ```json
    {
        "access": "<access_token>",
        "refresh": "<refresh_token>"
    }
    ```
  - Error (401 Unauthorized): If the provided credentials are invalid.

### Refresh JWT Access Token:
- **URL:** `/api/jwt/refresh/`
- **Method:** POST
- **Description:** Allows users to obtain a new JWT access token by providing a valid refresh token.
- **Request Data:**
  - refresh (string): User's refresh token.
- **Response:**
  - Success (200 OK):
    ```json
    {
        "access": "<new_access_token>"
    }
    ```
  - Error (401 Unauthorized): If the provided refresh token is invalid or expired.

### Verify JWT Access Token:
- **URL:** `/api/jwt/verify/`
- **Method:** POST
- **Description:** Allows users to verify the authenticity of a JWT access token.
- **Request Data:**
  - token (string): User's JWT access token.
- **Response:**
  - Success (200 OK): If the access token is valid.
  - Error (401 Unauthorized): If the access token is invalid or expired.

These JWT endpoints provide additional features for user authentication and session management using JSON Web Tokens.


These APIs provide essential functionalities for managing user accounts, sending friend requests, and communicating with other users on a social media platform.


**Make sure to use the email as username in the django pop-up authentication form not the username;> and password as password as it is**
