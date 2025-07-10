# BookMyNest

BookMyNest is a hotel booking platform that allows users to search, view, and book hotels, while enabling hotel vendors to manage their listings and bookings. This project is under active development.

---

## 🚀 Features

- User registration, login, and profile management
- Email verification with OTP
- Browse and search hotels
- View hotel details and images
- Book hotels and view booking history
- Vendor registration and login
- Vendor dashboard to manage hotels and bookings
- Add, edit, and upload hotel details and images
- Responsive UI for users and vendors

---

## 🛠️ Technology Stack

- **Backend:** Django (Python)
- **Frontend:** Django Templates (HTML, CSS, JS)
- **Database:** MySql (can be changed)
- **Other:** Bootstrap (Rapid UI Development), Pillow (image handling)

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BNB2006/Hotel.git
   cd Hotel
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file inside the `BookMyNest` directory with the following content:
   ```env
   SECRET_KEY=your-django-secret-key
   DB_NAME=your-database-name
   DB_USER=your-database-username
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=3306
   ```
   > **Note:** Never commit your `.env` file to version control.

5. **Open project:**
   ```bash
   cd BookMyNest
   ```

6. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the app:**
   - User: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

---

## 📁 Folder Structure

```
Hotel/
  BookMyNest/           # Django project root
    accounts/           # User and vendor accounts app
    home/               # Hotel listings, bookings, homepage
    media/              # Uploaded images (hotels, profiles)
    static/             # Static files (CSS, JS, images)
    manage.py           # Django management script
  requirements.txt      # Python dependencies
  README.md             # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request. For major changes, open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 📬 Contact

For questions, suggestions, or support:
- **Email:** balajibandgar26@gmail.com
- **GitHub Issues:** [Open an issue](https://github.com/BNB2006/Hotel/issues)

---

*Happy Booking!*
