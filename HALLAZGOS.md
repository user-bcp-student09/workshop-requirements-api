# Hallazgos pendientes — Workshop Requirements API

Los siguientes hallazgos están pendientes de revisión humana. Son candidatos; no representan aprobación de cambios ni autorización para implementarlos.

## H-01 — El cliente puede elegir el propietario de tareas y resúmenes

- **Estado:** CANDIDATO
- **Evidencia:** `app/main.py:96` usa el parámetro `owner` si se proporciona; `app/main.py:110` permite obtener el propietario del cuerpo de creación.
- **Impacto:** Las operaciones pueden consultar o asignar tareas para un propietario distinto de la identidad autenticada.
- **Prioridad propuesta:** Alta (P1), si se requiere aislamiento de datos por usuario.
- **Contrato potencialmente afectado:** `GET /api/tasks`, `GET /api/summary` y `POST /api/tasks`; propietario asociado a la identidad autenticada.
- **Cómo validarlo:** Con dos identidades ficticias y datos aislados, comprobar que una identidad no pueda consultar tareas/resúmenes de la otra ni crear tareas en su nombre modificando `owner`.

## H-02 — Valores de entrada concatenados en consultas SQL

- **Estado:** CANDIDATO
- **Evidencia:** `app/main.py:97` concatena `requested_owner` en la consulta de tareas; `app/main.py:111` concatena campos del cuerpo en la inserción; `app/main.py:120` concatena `requested_owner` en la consulta del resumen.
- **Impacto:** Valores de solicitud con caracteres especiales pueden alterar el comportamiento de las consultas o provocar errores.
- **Prioridad propuesta:** Alta (P1), por afectar datos usados en consultas de lectura y escritura.
- **Contrato potencialmente afectado:** Filtros y campos de entrada de `GET /api/tasks`, `GET /api/summary` y `POST /api/tasks`.
- **Cómo validarlo:** Añadir pruebas con entradas ficticias que contengan comillas y verificar que se traten como valores literales, sin alterar el alcance de las consultas ni causar errores.

## H-03 — La carga usa el nombre recibido y lee el archivo completo

- **Estado:** CANDIDATO
- **Evidencia:** `app/main.py:136` forma la ruta de destino a partir de `file.filename`; `app/main.py:137-138` lee todo el contenido y lo escribe sin aplicar límites de tamaño en este flujo.
- **Impacto:** Un nombre no controlado podría escapar del directorio destinado a cargas; un archivo grande podría consumir memoria excesiva.
- **Prioridad propuesta:** Alta (P1) para el control de ruta; Media (P2) para límite de tamaño.
- **Contrato potencialmente afectado:** `POST /api/requirements`, reglas de nombre, tamaño y ubicación de archivos aceptados.
- **Cómo validarlo:** En pruebas aisladas con un directorio temporal, comprobar que nombres con componentes de ruta no escriban fuera del directorio y que archivos por encima del límite acordado se rechacen.

## Aprobación

- **Estado de aprobación:** Aprobado.
- **Hallazgos aprobados:** H-01, H-02 y H-03.
- **Decisión / comentarios:** Aprobado.
- **Aprobador:** Juan Carlos.
- **Fecha:** 20/10/2026.
