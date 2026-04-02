<div align="center">

# Sistema de Coordinacion de Posgrado

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

Sistema administrativo para la gestion de programas de posgrado del
**Centro de Investigacion en Computacion (CIC) del
Instituto Politecnico Nacional (IPN)**

</div>

---

## Descripcion

SiCoP administra los programas de posgrado del CIC-IPN: Maestria en Ciencias
en Computacion, Doctorado en Ciencias en Computacion y Doctorado Directo en
Ciencias en Computacion. El sistema gestiona profesores, alumnos,
nombramientos, tesis, comites tutoriales y jurados de examen conforme al
Reglamento de Estudios de Posgrado del IPN.

## Tecnologias

- Python 3.12
- Django 5.1
- SQLite
- HTML / CSS

## Estructura del proyecto

```
SiCoP/
├── apps/
│   ├── cuentas/        Autenticacion y control de acceso
│   ├── personas/       Profesores y alumnos
│   ├── programas/      Programas, laboratorios y coordinadores
│   ├── nombramientos/  Nombramientos y tipos
│   ├── tesis/          Tesis, directores, comites y jurados
│   └── historial/      Auditoria de cambios
├── config/             Configuracion de Django
├── scripts/            Datos de prueba
├── static/             Archivos estaticos
└── templates/          Plantillas HTML
```

## Instalacion

```bash
git clone https://github.com/felixrsalinasm/SiCoP.git
cd SiCoP
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations
python manage.py migrate
python scripts/datos_prueba.py
python manage.py runserver
```

Accede en: http://127.0.0.1:8000

## Usuarios de prueba

> Requiere haber ejecutado `python scripts/datos_prueba.py`

| Rol | Usuario | Contrasena |
|---|---|---|
| Django Admin | admin | Admin1234! |
| Administrador | administrador1 | Adm1n1234! |
| Secretaria | secretaria1 | Secr1234! |
| Profesor | profesor1 | Prof1234! |
| Profesor | profesor2 | Prof1234! |