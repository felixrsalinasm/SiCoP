<div align="center">

# SiCoP — Sistema de Coordinación de Posgrado

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![PEP8](https://img.shields.io/badge/code%20style-PEP%208-brightgreen?style=for-the-badge)
![Tests](https://img.shields.io/badge/tests-11%20passed-success?style=for-the-badge)

Sistema web administrativo para la gestión integral de programas de posgrado del Centro de Investigación en Computación CIC — Instituto Politécnico Nacional.
</div>

---

## ¿Qué es SiCoP?
SiCoP automatiza, valida y documenta los procesos académicos del posgrado del CIC-IPN con base en el Reglamento de Estudios de Posgrado del IPN, cubriendo desde la gestión de personas y programas hasta el control estricto de tesis y comités tutoriales.

## Módulos
- Personas: gestión de profesores y estudiantes
- Programas: gestión de los cinco programas MCC, MCIC, MCyTIAyCD, DCC y DCyTIAyCD
- Nombramientos: gestión de distinciones académicas
- Tesis: control de directores (máximo 2 por alumno), comités y jurados
- Roles: perfiles de Administrador, Coordinador, Secretaría y Profesor

## Requisitos
- Python 3.12+
- pip

## Instalación
1. Clonar el repositorio desde https://github.com/felixrsalinasm/SiCoP.git
2. Crear y activar entorno virtual en Windows con `venv\Scripts\activate` y en Linux/Mac con `source venv/bin/activate`
3. Instalar dependencias con `pip install -r requirements.txt`
4. Aplicar migraciones con `python manage.py makemigrations` y `python manage.py migrate`
5. Cargar datos de prueba opcionales con `python scripts/datos_prueba.py`
6. Iniciar servidor con `python manage.py runserver`

http://127.0.0.1:8000

## Usuarios de Prueba
Nota: Requiere `datos_prueba.py` ejecutado previamente.

| Usuario | Contraseña |
|---|---|
| coordinador1 | Coord1234! |
| secretaria1 | Secr1234! |
| profesor1 | Prof1234! |
| profesor2 | Prof1234! |

## Pruebas Automatizadas
`python manage.py test apps --verbosity=2`

11 pruebas de integración cubriendo autenticación, permisos por rol, validaciones de negocio y restricciones de tesis.