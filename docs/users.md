# Documentacion de Users (GAM)

## Objetivo
Este documento explica como usar los controladores de usuarios GAM, como funciona la capa de servicios y cuales son las utilidades internas asociadas.

## Arquitectura

- Controlador HTTP: `app/controllers/gam_user_controller.py`
- Servicio principal (fachada): `app/service/gam/gam_user_service.py`
- Utilidades GAM user (logica core): `app/service/gam/utils/gam_user_utils.py`
- DTOs GAM user: `app/domain/dtos/gam/`
- Enums GAM: `app/domain/enums/gam_command_enum.py`, `app/domain/enums/gam_attribute_enum.py`

Flujo general:
1. El controlador recibe request y valida payload con DTOs.
2. Llama funciones de servicio `GamService.*`.
3. El servicio ejecuta comandos GAM via utilidades.
4. La respuesta se parsea y retorna como DTO (principalmente `GamUserDto`).

---

## Endpoints de Users

Base path: `/gam-user`

### 1) Obtener usuario
- Metodo: `GET /gam-user/{email}`
- Query params:
  - `quick` (bool, opcional, default false)
- Response model: `GamUserDto`

Ejemplo:
```http
GET /gam-user/user@unal.edu.co?quick=false
```

### 2) Actualizacion parcial de usuario
- Metodo: `PATCH /gam-user/{email}`
- Query params:
  - `preview` (bool, opcional, default false)
- Body model: `GamUserUpdateDto`
- Response model: `GamUserDto`

Notas:
- Soporta actualizacion parcial (solo campos enviados).
- `null` no pisa datos porque el payload se normaliza excluyendo nulos.
- Si `preview=true`, se ejecuta comando GAM en modo preview y se devuelve el estado calculado.
- Para listas, el merge soporta operaciones `add`, `remove`, `replace`.
- La operacion para eliminar es `remove` (no `delete`).

#### Input real del PATCH (importante)

Aunque `GamUserUpdateDto` declare algunos campos fijos (`firstname`, `lastname`, etc.),
el DTO tambien permite campos extra por `model_config = ConfigDict(extra="allow")`.

Eso significa que puedes enviar campos dinamicos como `phones`, `addresses`,
`organizations`, `relations`, o cualquier lista del JSON de GAM usando este patron:

```json
{
  "<campo_lista>": {
    "add": [...],
    "remove": [...],
    "replace": [...]
  }
}
```

Reglas:
- `replace`: reemplaza completamente la lista.
- `add`: agrega elementos que no existan.
- `remove`: elimina elementos comparando por `email`, `value`, `name` o igualdad total.
- Si envias `replace`, tiene prioridad sobre `add/remove` para ese campo.

#### Casos de uso de actualizacion de usuario

Caso A - Cambiar solo nombre
```json
{
  "firstname": "Ana",
  "lastname": "Perez"
}
```

Caso B - Agregar telefono
```json
{
  "phones": {
    "add": [
      {"value": "555-1234", "type": "work"}
    ]
  }
}
```

Caso C - Eliminar telefono
```json
{
  "phones": {
    "remove": [
      {"value": "555-1234"}
    ]
  }
}
```

Caso D - Reemplazar toda la lista de telefonos
```json
{
  "phones": {
    "replace": [
      {"value": "3001112233", "type": "mobile"},
      {"value": "6010000000", "type": "work"}
    ]
  }
}
```

Caso E - Cambiar campo escalar y modificar lista en la misma solicitud
```json
{
  "firstname": "Carlos",
  "phones": {
    "add": [
      {"value": "3100000000"}
    ],
    "remove": [
      {"value": "6010000000"}
    ]
  }
}
```

Caso F - Simular sin aplicar cambios (preview)
```http
PATCH /gam-user/user@unal.edu.co?preview=true
```
Con cualquier body valido. Retorna el DTO resultante calculado sin aplicar cambio real.

Ejemplo body:
```json
{
  "firstname": "Ana",
  "lastname": "Perez",
  "phones": {
    "add": [
      {"value": "555-1234"}
    ]
  }
}
```

### 3) Mover usuario de OU
- Metodo: `PATCH /gam-user/{email}/ou`
- Query params:
  - `preview` (bool, opcional, default false)
- Body model: `GamUserOuUpdateDto`
  - `org_unit`
  - `immutableous` (opcional)
- Response model: `GamUserDto`

Ejemplo body:
```json
{
  "org_unit": "/Estudiantes/2026",
  "immutableous": "/Rectorias,/Sistema"
}
```

### 4) Actualizar grupos
- Metodo: `PATCH /gam-user/{email}/groups`
- Body model: `GamUserGroupsUpdateDto`
  - `add` (lista de grupos)
  - `remove` (lista de grupos)
  - `role` (opcional)
- Response model: `GamUserDto`

Ejemplo body:
```json
{
  "add": ["grupo-a@unal.edu.co"],
  "remove": ["grupo-b@unal.edu.co"],
  "role": "owner"
}
```

### 5) Gestionar licencias
- Metodo: `POST /gam-user/{email}/licenses`
- Body model: `GamUserLicensesUpdateDto`
  - `add` (lista de SKUs)
  - `remove` (lista de SKUs)
- Response model: `GamUserDto`

Ejemplo body:
```json
{
  "add": ["google-workspace-enterprise"],
  "remove": ["google-workspace-business"]
}
```

### 6) Consultar cuota
- Metodo: `POST /gam-user/{email}/quota`
- Response model: `GamUserQuotaDto`

### 7) Suspender usuario
- Metodo: `POST /gam-user/{email}/suspend`
- Body model: `GamUserSuspendDto`
  - `suspend` (opcional, default true)
- Response model: `GamUserDto`

Ejemplo body:
```json
{
  "suspend": true
}
```

### 8) Activar usuario
- Metodo: `POST /gam-user/{email}/activate`
- Body model: `GamUserSuspendDto` (opcional)
  - si no llega valor, internamente usa `suspend=false`
- Response model: `GamUserDto`

---

## Como funcionan los servicios

### Servicio fachada
Archivo: `app/service/gam/gam_user_service.py`

Responsabilidad:
- Mantener compatibilidad con metodos historicos de clase.
- Delegar logica real a `gam_user_utils.py`.

Metodos relevantes:
- `get_usuario_dto` -> `info_user`
- `update_user_attributes` -> `update_user_json`
- `update_user_ou` -> `move_user_ou`
- `update_user_groups` -> `update_user_groups`
- `update_user_licenses` -> `manage_licenses`
- `get_user_quota` -> `get_drive_quota`
- `suspend_user` -> `suspend_user`

### Utilidades core
Archivo: `app/service/gam/utils/gam_user_utils.py`

Responsabilidad:
- Construir/ejecutar comandos GAM.
- Parsear salida GAM JSON a DTOs.
- Mezclar patch parcial con estado actual (`merge`) para no perder atributos.

Funciones clave:
- `_run_gam_command(args)`
- `_run_gam_json_command(args)`
- `_load_user_json(email)`
- `parse_user_json(data)` -> `GamUserDto`
- `_merge_user_json(curr, patch)`
- `_normalize_update_payload(json_obj)`

Operaciones de negocio:
- `info_user`
- `update_user_json`
- `move_user_ou`
- `update_user_groups`
- `manage_licenses`
- `get_drive_quota`
- `suspend_user`

---

## Reglas de merge para update parcial

`_merge_user_json` soporta:
- `add/remove/replace` en colecciones.
- Mapeo de campos de conveniencia:
  - `firstname` -> `name.givenName`
  - `lastname` -> `name.familyName`
- Merge superficial de objetos anidados.

Esto evita sobrescribir todo el usuario cuando solo se desea cambiar un atributo.

---

## DTOs usados en Users

DTOs de entrada:
- `GamUserUpdateDto`
- `GamUserOuUpdateDto`
- `GamUserGroupsUpdateDto`
- `GamUserLicensesUpdateDto`
- `GamUserSuspendDto`

DTOs de salida:
- `GamUserDto`
- `GamUserQuotaDto`

Ubicacion: `app/domain/dtos/gam/`

---

## Enums usados

- `GamCommandEnum`: centraliza tokens de comandos GAM (create, update, info, etc.).
- `GamAttributeEnum`: centraliza keys de payload/salida (primaryEmail, skuId, groupEmail, etc.).

Ubicacion:
- `app/domain/enums/gam_command_enum.py`
- `app/domain/enums/gam_attribute_enum.py`

Beneficios:
- Menos strings literales repetidos.
- Menor probabilidad de typos.
- Mejor mantenibilidad.

---

## Errores comunes

1. GAM CLI no instalado o no disponible en PATH.
2. Permisos insuficientes del service account/admin para ejecutar accion.
3. SKU de licencia invalido.
4. OU path invalida.
5. Grupo inexistente al agregar/remover membership.

El controlador responde HTTP 500 con detalle del error capturado.

---

## Recomendaciones operativas

1. Usar `preview=true` antes de cambios masivos en patch y OU.
2. Para updates parciales, enviar solo campos necesarios.
3. Mantener SKUs y grupos en listas limpias, sin duplicados.
4. Si se requieren cambios en mapping de atributos GAM, centralizar en enums y parseadores.
