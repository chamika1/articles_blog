# Tech Blog Platform

A modern, responsive tech blog platform built with Flask and MongoDB, featuring a sleek UI with animated elements and a full content management system.

![Tech Blog Screenshot](https://image.pollinations.ai/prompt/tech_blog_website?width=800&height=400&nologo=true)

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [User Actions](#user-actions)
  - [Admin Setup & Features](#admin-setup--features)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Articles](#articles)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Features

-   🔐 **User Authentication**: Secure registration, login, and session management using JWT.
-   👤 **User Profiles**: Basic user profiles with randomized avatars.
-   ✍️ **Article Management**: Create, read, update, and delete (CRUD) operations for articles.
-   📝 **Rich Text Editor**: Integrated editor for easy content creation and formatting.
-   🖼️ **Image Upload**: Functionality to upload and associate images with articles (via ImageBB).
-   🎨 **Modern UI**: Responsive design built with Tailwind CSS, suitable for various devices.
-   ✨ **Animations**: Subtle background animations using Three.js.
-   🌙 **Dark Mode**: Aesthetically pleasing dark theme design.
-   🔍 **Search & Filtering**: Functionality to search and filter articles.
-   👑 **Admin Dashboard**: Dedicated interface for administrators to moderate content and manage users (basic).

## Tech Stack

-   **Backend**: Python 3 with Flask Framework
-   **Database**: MongoDB (NoSQL)
-   **Authentication**: JSON Web Tokens (JWT)
-   **Frontend**: HTML, CSS, JavaScript
-   **UI Framework**: Tailwind CSS
-   **Background Effects**: Three.js
-   **Image Hosting Integration**: ImageBB API

## Installation

### Prerequisites

-   Python 3.8 or higher
-   `pip` (Python package installer)
-   MongoDB instance (local or cloud-based like MongoDB Atlas)
-   Git

### Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/chamika1/articles_blog.git](https://github.com/chamika1/articles_blog.git)
    cd articles_blog
    ```

2.  **Create and activate a virtual environment:**
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**
    * Create a `.env` file in the project root directory.
    * *(Optional but recommended: Copy `env.example` to `.env` if you create an example file).*
    * Add the following variables, replacing the placeholder values with your actual credentials:
        ```dotenv
        MONGO_URI=your_mongodb_connection_string  # e.g., mongodb://localhost:27017/techblogdb or mongodb+srv://...
        JWT_SECRET_KEY=your_strong_jwt_secret_key # Use a long, random, secure string
        IMAGEBB_API_KEY=your_imagebb_api_key      # Get this from [imagebb.com](https://www.google.com/search?q=imagebb.com)
        ```

## Usage

### Running the Application

1.  **Start the Flask development server:**
    ```bash
    python app.py
    ```
2.  Open your web browser and navigate to `http://127.0.0.1:5000` (or the address provided in the console).

### User Actions

-   **Register:** Navigate to `/register` to create a new user account.
-   **Login:** Navigate to `/login` to sign in with your credentials.
-   **Create Article:** Once logged in, go to `/articles/new`. Use the rich text editor and image upload features.
-   **View Articles:** Browse all published articles at `/articles`.
-   **Manage Your Articles:** View, edit, or delete your own articles via their detail pages.

### Admin Setup & Features

1.  **Assign Admin Role:** After creating a regular user account, run the following command in your terminal (while the virtual environment is active) from the project root directory:
    ```bash
    python make_admin.py <user_email_address>
    ```
    Replace `<user_email_address>` with the email of the user you want to make an admin (e.g., `python make_admin.py admin@example.com`).

2.  **Admin Capabilities:** Logged-in admin users can:
    * Access the admin dashboard at `/admin`.
    * Edit or delete *any* article on the platform.
    * (Potentially) Manage user accounts (depending on implementation details).

## API Endpoints

The following API endpoints are available:

### Authentication

-   `POST /api/auth/register`: Register a new user.
    -   *Body*: Requires `username`, `email`, `password`.
-   `POST /api/auth/login`: Authenticate a user and receive a JWT.
    -   *Body*: Requires `email`, `password`.

### Articles

*Authentication (JWT Bearer Token in `Authorization` header) is required for POST, PUT, DELETE methods and image upload.*

-   `GET /api/articles`: Retrieve a list of all articles.
-   `GET /api/articles/<article_id>`: Retrieve a single article by its ID.
-   `POST /api/articles`: Create a new article.
    -   *Body*: Requires `title`, `content`, etc.
-   `PUT /api/articles/<article_id>`: Update an existing article.
    -   *Body*: Contains fields to update (`title`, `content`, etc.).
-   `DELETE /api/articles/<article_id>`: Delete an article.
-   `POST /api/articles/upload-image`: Upload an image file.
    -   *Body*: Expects image data (e.g., multipart/form-data).

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please report any bugs or suggest features by opening an issue on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (assuming you have a LICENSE file in your repo).

## Author

-   **Chamika Rasanjana**