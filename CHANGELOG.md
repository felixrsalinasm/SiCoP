# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/).

## [1.2] - 2026-04-02

### Agregado
- Control de acceso por grupos de Django (Administrador, Secretaria, Profesor).
- Permisos explicitos con ContentType y Permission por grupo.
- Context processor para variables de grupo en templates.
- Operaciones de eliminacion en todos los modulos (Profesor, Estudiante, Laboratorio, Programa, Coordinador, Jurado).
- Pagina de error personalizada 500.
- Tesis de Sofia Guerrero en datos de prueba.
- Coordinador de programa en datos de prueba.
- Tipo de nombramiento "Profesor de Posgrado" actualizado.
- CHANGELOG.md y LICENSE.

### Cambiado
- Validaciones de acceso en templates migradas de metodos de rol a context processor de grupos.
- Dashboard con condiciones de acceso corregidas.
- README.md actualizado con descripcion institucional y estructura del proyecto.
- Datos de prueba con get_or_create para idempotencia.

### Corregido
- Condiciones redundantes en templates (es_grupo_admin or es_grupo_admin).
- URLs faltantes para eliminacion de jurado de examen, profesor, estudiante, laboratorio, programa y coordinador.

## [1.1] - 2026-03-25

### Agregado
- Control de acceso por roles con decorador grupo_requerido.
- Exportacion CSV de profesores, estudiantes y nombramientos.
- Historial de cambios con auditoria de IP y usuario.
- Validaciones de negocio del Reglamento IPN en modelos.
- Paginas de error personalizadas 403 y 404.
- Datos de prueba con profesores, alumnos, tesis, comites y jurados.

### Cambiado
- Navegacion con sidebar por rol.

## [1.0] - 2026-03-24

### Agregado
- Estructura inicial del proyecto Django.
- Apps: cuentas, personas, programas, nombramientos, tesis, historial.
- Modelos base: Persona, Profesor, Estudiante, Programa, Laboratorio, Nombramiento, Tesis, DirectorTesis, ComiteTutorial, JuradoExamen.
- Sistema de autenticacion con login y logout.
- Panel de administracion de Django.
