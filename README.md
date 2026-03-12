# Sistema de Coordinación de Posgrado (SiCoP) - CIC-IPN

Bienvenido al repositorio oficial del **Sistema de Coordinación de Posgrado (SiCoP)**, un sistema web administrativo diseñado desde cero para el Centro de Investigación en Computación (CIC) del Instituto Politécnico Nacional (IPN) de México.

## Descripción del Sistema

**SiCoP** es una plataforma orientada a la gestión integral de programas de posgrado (maestrías y doctorados) del CIC-IPN. Automatiza, valida y documenta procesos académicos basados rigurosamente en el **Reglamento de Estudios de Posgrado del IPN**, cubriendo:

- **Personas**: Gestión completa de profesores (con grado y laboratorio) y estudiantes (con matrícula y generación).
- **Programas**: Administración de programas de posgrado (MCC, MCIC, MCyTIAyCD, DCC, DCyTIAyCD) y laboratorios.
- **Roles y Accesos**: Sistema seguro de autenticación con 4 perfiles principales (Administrador, Coordinador, Secretaría, Profesor).
- **Academia y Tesis**: Control estricto de restricciones institucionales (máximo 2 directores de tesis activos por alumno, máximo 4 alumnos simultáneos por director). Conformación de Comités Tutoriales y Jurados de Examen.

Todo el desarrollo se encuentra realizado en **Python** & **Django** con cumplimiento estricto del estándar PEP-8.

## Requisitos Previos

Asegúrese de contar con las siguientes herramientas en su entorno:

- **Python 3.12** o superior
- **pip** (Manejador de paquetes de Python)
- **Git** (Opcional, para versionamiento y clonación)

## Instalación y Despliegue Local

Siga los siguientes pasos para ejecutar SiCoP en su máquina local:

1. **Clonar el repositorio**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd SiCoP
   ```

2. **Crear y activar el entorno virtual**
   ```bash
   # En Windows
   python -m venv venv
   venv\Scripts\activate

   # En Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones de la base de datos**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Cargar los datos de prueba (Opcional)**
   El sistema incluye un script idempotente que poblará la base de datos con laboratorios, programas, catálogos, y usuarios pre-configurados:
   ```bash
   python scripts/datos_prueba.py
   ```

6. **Iniciar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
   El sistema estará disponible en [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usuarios de Prueba

Si ejecutó el paso de `datos_prueba.py`, podrá ingresar al sistema con los siguientes usuarios (distintos roles para probar las vistas):

| Rol / Perfil | Usuario | Contraseña |
| --- | --- | --- |
| **Coordinador** | `coordinador1` | `Coord1234!` |
| **Secretaría** | `secretaria1` | `Secr1234!` |
| **Profesor 1** | `profesor1` | `Prof1234!` |
| **Profesor 2** | `profesor2` | `Prof1234!` |

*(Nota: Todos los accesos se prueban en la ruta redirigida de `/cuentas/login/` automáticamente si ingresa al index del sistema).*

## Pruebas Automatizadas

El sistema cuenta con un set de pruebas de integración para validar reglas de negocio. Para ejecutarlas:
```bash
python manage.py test apps --verbosity=2
```

## Créditos

Sistema desarrollado para el **Centro de Investigación en Computación (CIC)** del **Instituto Politécnico Nacional (IPN)**. Construido con arquitectura limpia en Django, enfocado en resiliencia y automatización de validaciones.
