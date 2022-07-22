<div id="top"></div>


<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

![coverage-shield]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="https://www.pngall.com/wp-content/uploads/2016/04/Banana-Free-Download-PNG.png" alt="Logo" width="140" height="140">
  </a>

<h3 align="center">Banana API</h3>

  <p align="center">
    Simple Flask API
    <br />
    <a href="https://github.com/Glico21/BananaAPI/issues">Report Bug</a>
    ·
    <a href="https://github.com/Glico21/BananaAPI/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is BananaAPI. A project to demonstrate a possible configuration of a simple API project in Flask.
Allows you to work with bananas by CRUD. Uses [SQLAlchemy ORM](https://www.sqlalchemy.org) and [Marshmallow](https://marshmallow.readthedocs.io/) as a serializer to interact with the database.
The project is based on the [tutorial by Leonardo Giordani](https://www.thedigitalcatonline.com/blog/2020/07/05/flask-project-setup-tdd-docker-postgres-and-more-part-1/).
All API development is done via TDD. 

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
* [![Docker][Docker]][Docker-url]
* [![Nginx][Nginx]][Nginx-url]
* [![Gunicorn][Gunicorn]][Gunicorn-url]
* [![Pytest][Pytest]][Pytest-url]

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

* Install [Docker](https://docs.docker.com/install/) on your machine.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com//Glico21/BananaAPI.git
   ```
2. Use [virtual environments](https://docs.python.org/3/tutorial/venv.html) and install all necessary requirements
   ```sh
   pip install -r requirements/development.txt
   ```
3. Also you need to build the container
   ```sh
   ./manage.py compose build web
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
The API can work in three modes. In development, production and testing modes.

### Development
Development mode runs the application as a separate container, independent of the database, which is also in a separate container.
It uses separate development server specific environment variables.

You can run development mode by this command
   ```sh
   ./manage.py compose up
   ```
This command will start the application on localhost [0.0.0.0:5000](http://0.0.0.0:5000).

After that, you need to migrate to initialize all the necessary tables for the database.
   ```sh
   ./manage.py flask db migrate -m "Some message"
   ```
And upgrade
   ```sh
   ./manage.py flask db upgrade
   ```
You can check out the [available endpoints](https://github.com/Glico21/BananaAPI/edit/main/README.md#endpoints-list) and see how it all works.

### Production
Production mode also runs the application in a separate container, but it can be scalable by nginx and gunicorn.

You can run production server by this command
   ```sh
   APPLICATION_CONFIG="production" ./manage.py compose up
   ```
If you want scale application for N containers you should use this command
   ```sh
   APPLICATION_CONFIG="production" ./manage.py compose up --scale web=N
   ```

### Testing
You can run separate tests for the application. To do this, run the following command.
   ```sh
   ./manage.py test
   ```
A separate database is used for the tests, which is cleared automatically after each test is performed.




<!-- Endpoints -->
## Endpoints list
| URL/Method | GET | POST | PATCH | DELETE |
| --- | --- | --- | --- | --- |
| `/` | Return `Hello, World!` |
| `/users` | Return count of users in database |
| `/bananas` | Return all banana objects | Create a banana object |
| `/palms` | Return all palms objects | Create a palm object |
| `/bananas/<id>` | Return a specific banana object | | Update a banana object | Delete a banana object |
| `/palms/<id>` | Return a specific palm object | | Update a palm object | Delete a palm object |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

In the future it is planned to develop this project a little bit.

- [x] Add a palm tree model, which will be linked to the banana model.
- [ ] Add more fields for the banana
- [ ] Expand user model
- [ ] Add simple authorization and access rights

See the [open issues](https://github.com/Glico21/BananaAPI/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- CONTACT -->
## Contact me

Boyko Dmitriy - 21glicodin@gmail.com

Project Link: [https://github.com/Glico21/BananaAPI](https://github.com/Glico21/BananaAPI)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org!
/basic-syntax/#reference-style-links -->
[coverage-shield]: https://user-images.githubusercontent.com/70241079/179604459-0774c04b-b73b-471a-8383-77bf9adf5b4d.svg
[contributors-shield]: https://img.shields.io/github/contributors/Glico21/BananaAPI.svg?style=for-the-badge
[contributors-url]: https://github.com/Glico21/BananaAPI/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Glico21/BananaAPI.svg?style=for-the-badge
[forks-url]: https://github.com/Glico21/BananaAPI/network/members
[stars-shield]: https://img.shields.io/github/stars/Glico21/BananaAPI.svg?style=for-the-badge
[stars-url]: https://github.com/Glico21/BananaAPI/stargazers
[issues-shield]: https://img.shields.io/github/issues/Glico21/BananaAPI.svg?style=for-the-badge
[issues-url]: https://github.com/Glico21/BananaAPI/issues
[license-shield]: https://img.shields.io/github/license/Glico21/BananaAPI.svg?style=for-the-badge
[license-url]: https://github.com/Glico21/BananaAPI/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/boyko-dmitry
[Flask]: https://img.shields.io/badge/flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-0f1b2e?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1
[PostgreSQL-url]: https://www.postgresql.org/
[Docker]: https://img.shields.io/badge/Docker-35495E?style=for-the-badge&logo=docker&logoColor=2496ED
[Docker-url]: https://www.docker.com/
[Nginx]: https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white
[Nginx-url]: https://www.nginx.com/
[Gunicorn]: https://img.shields.io/badge/Gunicorn-5d636e?style=for-the-badge&logo=gunicorn&logoColor=499848
[Gunicorn-url]: https://gunicorn.org/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=ded821
[Python-url]: https://www.python.org/
[Pytest]: https://img.shields.io/badge/Pytest-white?style=for-the-badge&logo=pytest&logoColor=0A9EDC
[Pytest-url]: https://docs.pytest.org/
