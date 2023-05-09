<h1 align="center">Shortify</h1>

# 📃 About

**Shortify** is a web application built with the **Flask** framework and **Flask-RESTful**, this application is supposed
to help
people shorten long URLs for later use. To implement this idea, both the web version of the site and the API interface
were created.
> The project was created for educational purposes.

# 🔥 Features

* **Rest API**
* **JWT token authentication**
* **Shortening long URLs**
* **Registration / Authorization**
* **User profile**
* **Profile editing**
* **Tests**

# 💽 Local: Development
1. Clone or download the repository.
2. Create a virtual environment and install requirements from requirements.txt file. 
3. Create an .env file or rename .env.dist to .env and populate it with all the variables in the .env.dist file.
4. Make migrations:
   * `flask db migrate`
   * `flask db upgrade`
5. Run development server:
    * `flask run`
