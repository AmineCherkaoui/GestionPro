# GestionPro

**GestionPro** is a business management web application built with **Django**.  
It allows users to manage:

- 🧾 Clients & Suppliers  
- 📦 Products & Services  
- 📄 Invoices, Quotes, and Purchase Orders (with PDF generation)

It also includes a **Settings page** where users can define key **company configurations** such as name, address, contact info, logo, and other defaults used across documents.

This project was developed during an internship at **OPTIMA TIC** as a real-world solution for managing business operations more efficiently.

---

## 🚀 Features

- Full CRUD for clients, suppliers, products, and services
- Invoice, quote, and purchase order creation
- PDF generation for all official documents
- MySQL as the backend database
- Easy setup with Docker and Docker Compose

---

## 🧰 Tech Stack

- **Backend:** Django (Python)
- **Database:** MySQL
- **PDF Generation:**  WeasyPrint
- **Containerization:** Docker, Docker Compose
- **Environment Configuration:** `.env` file

---

## ⚙️ Installation with Docker

You can install and run this project easily using Docker.

### 1. Clone the repository

```bash
git clone https://github.com/AmineCherkaoui/GestionPro.git
cd GestionPro
```

### 2. Configure environment variables

Copy the provided environment template file and customize it:

```bash
cp .env.prod.example .env.prod
```

Then edit `.env.prod` with your own values:

```ini
#Replace with your secret key
DJANGO_SECRET_KEY=SECRET_KEY

#Replace with your ip address or domain name
DJANGO_ALLOWED_HOSTS=localhost


# Change also the DB infos.
DATABASE_ENGINE=mysql
DATABASE_NAME=db_name
DATABASE_USERNAME=db_username
DATABASE_PASSWORD=db_password
DATABASE_HOST=db
DATABASE_PORT=3306
MYSQL_DATABASE: db_name
MYSQL_USER: db_username
MYSQL_PASSWORD: db_password
MYSQL_ROOT_PASSWORD: db_root_password
```

> ⚠️ Make sure your `SECRET_KEY` is secure.

---

### 3. Build and start the containers

```bash
docker-compose up --build
```

This will:
- Build the Django app with MySQL DB container
- Launch the development server on [http://localhost](http://localhost)

---

## 🙋‍♂️ Author

Created during internship at **OPTIMA TIC**  
By **Amine Cherkaoui**
[🔗 LinkedIn](https://linkedin.com/in/aminecherkaoui) • 


