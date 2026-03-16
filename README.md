<div align="center">

# SiCoP — Sistema de Coordinación de Posgrado

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![PEP8](https://img.shields.io/badge/code%20style-PEP%208-brightgreen?style=for-the-badge)
![Tests](https://img.shields.io/badge/tests-21%20passed-success?style=for-the-badge)

Sistema web administrativo para la gestión integral
de programas de posgrado del
**Centro de Investigación en Computación (CIC)
— Instituto Politécnico Nacional**

</div>

---

## ¿Qué es SiCoP?

SiCoP automatiza, valida y documenta los procesos
académicos del posgrado del CIC-IPN con base en el
Reglamento de Estudios de Posgrado del IPN, cubriendo
desde la gestión de personas y programas hasta el
control estricto de tesis, comités tutoriales y
auditoría de cambios.

## Módulos

- **Personas** — Gestión de profesores y estudiantes
- **Programas** — MCC, MCIC, MCyTIAyCD, DCC, DCyTIAyCD
- **Nombramientos** — Distinciones académicas con exportación CSV
- **Tesis** — Directores, Comités Tutoriales y Jurados
- **Roles** — Administrador, Coordinador, Secretaría, Profesor
- **Historial** — Auditoría automática de cambios con IP y usuario
- **Exportación CSV** — Compatible con Excel
- **Admin personalizado** — Panel con filtros y acciones

## Requisitos

- Python 3.12+
- pip

## Instalación

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

| Rol | Usuario | Contraseña |
|---|---|---|
| Coordinador | coordinador1 | Coord1234! |
| Secretaría | secretaria1 | Secr1234! |
| Profesor | profesor1 | Prof1234! |
| Profesor | profesor2 | Prof1234! |

## Pruebas Automatizadas

```
python manage.py test apps --verbosity=2
```