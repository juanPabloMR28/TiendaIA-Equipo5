#!/usr/bin/env bash
# Crea un usuario de RabbitMQ por servicio con permisos mínimos (Lab. 6, Parte F).
# Uso: ./scripts/usuarios_rabbitmq.sh   (con docker compose levantado)
# Las claves salen de .env (RMQ_CLAVE_VENTAS, RMQ_CLAVE_IA, ...).
#
# Mínimo privilegio: cada servicio solo puede tocar las colas/exchanges que usa.
# Si un servicio es comprometido, no puede leer ni publicar en lo de los demás.

# -e: detenerse ante un error; -u: error si falta una variable; -o pipefail:
# un fallo en cualquier parte de una tubería (|) cuenta como fallo
set -euo pipefail

source .env   # carga las claves RMQ_CLAVE_* como variables del shell

# rabbitmqctl es la herramienta de administración; se ejecuta DENTRO del
# contenedor rabbitmq. -T: sin terminal interactiva (necesario en scripts)
R="docker compose exec -T rabbitmq rabbitmqctl"

# crear <usuario> <clave> <configurar> <escribir> <leer>
# Cada permiso es una expresión regular sobre nombres de colas/exchanges:
# configurar = declarar o borrar; escribir = publicar; leer = consumir.
# '^$' no coincide con ningún nombre: equivale a "sin permiso".
crear() {
  # Si el usuario ya existe, add_user falla y solo se actualiza su contraseña
  $R add_user "$1" "$2" 2>/dev/null || $R change_password "$1" "$2"
  # -p / : los permisos aplican al virtual host raíz "/"
  $R set_permissions -p / "$1" "$3" "$4" "$5"
}

# ventas: publica eventos en el exchange tienda.eventos; no consume nada
crear ventas "$RMQ_CLAVE_VENTAS" \
  '^tienda\.eventos$' '^tienda\.eventos$' '^$'

# ia: declara la cola inferencias y publica en ella por el exchange por defecto
crear ia "$RMQ_CLAVE_IA" \
  '^inferencias$' '^amq\.default$' '^$'

# worker: solo consume (lee) de la cola inferencias
crear worker "$RMQ_CLAVE_WORKER" \
  '^inferencias$' '^$' '^inferencias$'

# notificaciones: enlaza su cola al exchange de eventos y consume de ambos
crear notificaciones "$RMQ_CLAVE_NOTIF" \
  '^(tienda\.eventos|notificaciones)$' \
  '^notificaciones$' \
  '^(tienda\.eventos|notificaciones)$'

# Muestra la tabla final de permisos para verificar
$R list_permissions -p /
