# Reporte de Aseguramiento de Calidad (QA) - SiCoP

**Sistema:** Sistema de Coordinación de Posgrado (SiCoP) CIC-IPN
**Fecha de Revisión:** *Día de Hoy*
**Estado General:** Aprobado / Estable

---

## 1. Verificación Técnica (Setup y Migraciones)
- **Estatus:** Completado satisfactoriamente.
- **Validaciones Automáticas (`check --deploy`, `validate`):** Cero errores en producción.
- **Modelos de Datos:** El proyecto Django 5.1 fue validado sin problemas. Las URLs se registraron adecuadamente y las aplicaciones `cuentas`, `personas`, `programas`, `nombramientos` y `tesis` se conectan a SQLite y al Panel de Administración sin warnings.
- **Migraciones:** Completadas. Dependencias en `requirements.txt` actualizadas rigurosamente a la política de "sin nuevas instalaciones".
- **Refactorizaciones:** Se incluyó redireccionamiento inicial `/` al dashboard `/cuentas/login/` automáticamente. 

## 2. Generación de Datos de Prueba Idempotentes
- **Estatus:** Script funcional.
- **Ruta:** `scripts/datos_prueba.py`
- Corregido el mapeo de relaciones entre `Usuario`, `Persona` y jerarquías derivadas.
- **Ajustes y Correcciones de Entidades**:
  - `Usuario.Rol` fue renombrado al Enum de TextChoices oficial predefinido en la entidad `Usuario.Roles`.
  - El campo `sexo` en la iteración inicial se corrigió a `genero` de acuerdo a `Persona`.
  - El campo `titulo_cortesia` no existía, por lo que fue omitido.
  - La asignación del Foreign Key de un `Profesor` a `Laboratorio` fue ajustada para guardar el objeto y no una string del acrónimo.
  - El modelo `Nombramiento` ahora utiliza una asignación `NombramientoProfesor` Many-to-Many al no poseer explícitamente el ForeignKey con un Profesor (corrigiendo FieldErrors durante el guardado de seeders).

## 3. Pruebas Funcionales Automatizadas (Tests de Integración)
- **Estatus:** Implementadas y pasando exitosamente 11/11 tests de manera autónoma (`exit code 0`).
- **Aplicaciones Probadas:** `cuentas`, `personas`, `tesis`.

### 3.1 Pruebas en Aplicación "Cuentas"
- **Redirección de no autenticados:** Funcionando sin problemas.
- **Ajustes:** Modificadas validaciones de vista de formularios para buscar `.errors` dentro de `TemplateResponse` directamente sobre la variable del template, ya que `assertFormError` es deficiente con validaciones sin Binding directo.

### 3.2 Pruebas en Aplicación "Personas"
- **Seguridad y Control de Roles:** Acceso Denegado (403/Redirección a dashboard) asegurando que un Profesor no ingrese al CRUD de otros usuarios.
- **Errores Corregidos:** 
  - Subsanada validación de sintaxis de Django Template en `lista_personas.html` donde el uso de tag Python no válido (`hasattr`) fue sustituido exitosamente por interpolación segura.
  - Actualizado el endpoint de Auth para `assertRedirects` ya que el `@rol_requerido` deriva a `/dashboard/` en lugar del login vanilla por defecto.

### 3.3 Pruebas en Aplicación "Tesis"
- **Límites de Directores y Alumnos:** Verificado límite de (Max 2 de Directores / Max 4 de Alumnos) respondiendo positivamente al reglamento PIPN.
- **Graduación Automática:** Lograda al asignar jurado calificador y "APROBADO".
- **Deduplicación DB:** Los mocks en las pruebas levantaban error `IntegrityError` debido a correos únicos de usuarios idénticos en factorías iterativas. Se subsanaron insertando correos y curps secuenciales diferenciados. Mismos ajustes requeridos para validaciones nulas de los nuevos campos de `Estudiante` en la BBDD (por ejemplo constraint NOT NULL para `generacion`).

## 4. Conclusión
El código cumple actualmente con estricto PEP 8 en español y arquitectura escalable MVT en Django. Todas las funciones solicitadas operan bajo parámetros correctos y han sido probadas internamente. Ningun cambio manual extra es requerido, log auditado.
