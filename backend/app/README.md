## ✅ **ZONES API** `/api/zones`

### `GET /api/zones/`

**Descripción**: Listar todas las zonas
**Requiere**: Token de usuario o admin
**Respuesta esperada**:

```json
[
  {
    "id": 1,
    "name": "Zona 1",
    "location": "150px 220px",
    "area": 43.25,
    "status": "ENABLED",
    "sensor": {
      "id": 1,
      "serial_number": "SN-123",
      "status": "ACTIVE"
    },
    "fan": {
      "id": 1,
      "serial_number": "FAN-001",
      "status": "ON"
    }
  }
]
```

---

### `GET /api/zones/<zone_id>`

**Descripción**: Obtener detalles de una zona específica
**Requiere**: Token de usuario o admin
**Respuesta esperada**: Igual al JSON anterior (una sola zona)

---

### `POST /api/zones/`

**Descripción**: Crear una nueva zona
**Requiere**: Token de **admin**
**Body JSON de prueba**:

```json
{
  "name": "Zona 4",
  "x": "120px",
  "y": "180px",
  "sensor_id": 2,
  "fan_id": 2
}
```

---

### `PUT /api/zones/<zone_id>`

**Descripción**: Actualizar zona (nombre, ubicación, sensor o ventilador)
**Requiere**: Token de **admin**
**Body JSON de prueba**:

```json
{
  "name": "Zona Actualizada",
  "x": "200px",
  "y": "350px",
  "sensor_id": 3,
  "fan_id": 3
}
```

---

### `PUT /api/zones/<zone_id>/status`

**Descripción**: Actualizar el estado de la zona (`ENABLED` / `DISABLED`)
**Requiere**: Token de **admin**
**Body JSON de prueba**:

```json
{
  "status": "DISABLED"
}
```

---

### `DELETE /api/zones/<zone_id>`

**Descripción**: Eliminar una zona
**Requiere**: Token de **admin**
**Respuesta esperada**:

```json
{
  "message": "Zone deleted successfully"
}
```

---

## ✅ **USERS API** `/api/users`

### `GET /api/users/me`

**Descripción**: Obtener el perfil del usuario autenticado
**Requiere**: Token de usuario o admin
**Respuesta esperada**:

```json
{
  "username": "admin",
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "role": "ADMIN",
  "status": "ACTIVE",
  "registered_at": "2025-07-16T12:00:00"
}
```

---

### `PUT /api/users/me`

**Descripción**: Actualizar perfil propio (nombre y correo)
**Requiere**: Token de **usuario**
**Body JSON de prueba**:

```json
{
  "full_name": "Juan Actualizado",
  "email": "juan.actualizado@example.com"
}
```

---

### `GET /api/users`

**Descripción**: Listar todos los usuarios
**Requiere**: Token de **admin**
**Respuesta esperada**: Lista de usuarios como en el ejemplo de `me`

---

### `POST /api/users`

**Descripción**: Crear un nuevo usuario
**Requiere**: Token de **admin**
**Body JSON de prueba**:

```json
{
  "username": "usuario1",
  "password": "password123",
  "full_name": "Usuario Uno",
  "email": "usuario1@example.com",
  "role": "USER"
}
```

---

### `PUT /api/users/<username>`

**Descripción**: Actualizar usuario como admin
**Requiere**: Token de **admin**
**Body JSON de prueba**:

```json
{
  "full_name": "Nombre Modificado",
  "email": "nuevo@example.com",
  "role": "ADMIN"
}
```

---

### `DELETE /api/users/delete/<username>`

**Descripción**: Eliminar usuario
**Requiere**: Token de **admin**
**Respuesta esperada**:

```json
{
  "message": "User 'usuario1' deleted successfully"
}
```

---

