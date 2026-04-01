<div align="center">

# Sistema de Coordinación de Posgrado

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![PEP8](https://img.shields.io/badge/code%20style-PEP%208-brightgreen?style=for-the-badge)

Sistema administrativo para la gestion de programas de posgrado del
**Centro de Investigacion en Computacion (CIC) del
Instituto Politecnico Nacional (IPN)**

</div>

---

## Modulos

- **Personas** — Gestion de profesores y estudiantes
- **Programas** — MCC, DCC, DDCC
- **Nombramientos** — Distinciones academicas con exportacion CSV
- **Tesis** — Directores, Comites Tutoriales y Jurados
- **Roles** — Administrador, Secretaria, Profesor
- **Historial** — Auditoria automatica de cambios con IP y usuario

## Requisitos

- Python 3.12+
- pip

## Instalacion

```
git clone https://github.com/felixrsalinasm/SiCoP.git
cd SiCoP
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python scripts/datos_prueba.py
python manage.py runserver
```

Accede en: http://127.0.0.1:8000

## Usuarios de Prueba

> Requiere haber ejecutado scripts/datos_prueba.py

| Rol | Usuario | Contrasena |
|---|---|---|
| Superusuario | admin | Admin1234! |
| Administrador | administrador1 | Adm1n1234! |
| Secretaria | secretaria1 | Secr1234! |
| Profesor | profesor1 | Prof1234! |
| Profesor | profesor2 | Prof1234! |