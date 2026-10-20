# Aprobación: interoperabilidad del token en ReqFlow

## Estado

Spec y arquitectura aprobadas por el usuario el 2026-10-20. Implementación no autorizada en esta etapa.

## Hallazgo aprobado

El formato JWT emitido por el backend de autenticación no coincide con el formato de token esperado por la API de requisitos, por lo que el flujo de autenticación integrado puede fallar al acceder a endpoints protegidos.

## Decisiones aprobadas

- Mantener el JWT actual firmado con HS256.
- Configurar el secreto compartido fuera del código fuente.
- Validar explícitamente la firma, el algoritmo HS256 y la expiración.
- Rechazar solicitudes no autenticadas o con token inválido con HTTP `401` y el mensaje genérico exacto `ocurrio un error`.
- Preservar el contrato vigente de `POST /auth/login`, el esquema `Authorization: Bearer <token>` y rutas, métodos y respuestas exitosas de los endpoints protegidos.

## Alcance protegido

La aprobación cubre la interoperabilidad entre el backend de autenticación y la API de requisitos para:

- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/summary`
- `POST /api/requirements`
- `GET /api/backend-health`

## Pruebas previstas

- Token válido emitido por el login aceptado por los endpoints protegidos.
- Tokens inválidos, malformados o expirados rechazados con HTTP `401` y el mensaje acordado.
- Contratos de rutas, métodos y respuestas exitosas preservados.

## Registro de ejecución

No se realizaron cambios de código, configuración o pruebas. No se crearon issues. La implementación queda pendiente de una solicitud explícita.
