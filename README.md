# Miniproyecto_Admn_sistemas
Ejercicio del módulo de Administración de Sistemas del curso Python en Entornos Industriales, impartido por la Escuela de Organización Industrial.


Más concretamente:

# Miniproyecto - Administración de sistemas

## Descripción

La tarea se divide en dos partes principales:
1. Implementar una pequeña API HTTP para el projecto taskmaster
2. Crear un Dockerfile que automatice la generación de una imagen pública en Docker
Hub

## Implementación de la API

El objetivo de esta primera sección es habilitar una serie de endpoints que amplíen la
funcionalidad por defecto de la aplicación web Taskmaster. Dicha funcionalidad consiste en
dotar a la aplicación de una API HTTP que permita manipular tareas de manera
programática.

Para ello, necesitaremos cumplir los siguientes requisitos:

- Si la URL raíz de nuestra aplicación es http://127.0.0.1:8000/ , añadiremos un
nuevo endpoint en http://127.0.0.1:8000/api/tasks.

- Dicho endpoint tiene que ceñirse a los preceptos REST: utilizar métodos HTTP con la
semántica adecuada, códigos de respuesta HTTP estándares y utilizar JSON como
formato universal de intercambio de datos.

- Este endpoint debe ser capaz de aceptar peticiones GET y POST.

## Método GET

Una petición GET sobre /api/tasks debe devolver una lista JSON con las tareas
existentes actualmente en la base de datos (o una lista vacía en su defecto). Los campos
concretos dentro de cada objeto de la lista son de libre elección y formato, pero se
recomienda seguir las mismas convenciones que su representación en la base de datos. A
continuación se muestra un ejemplo de posible representación:

```json
[
 {
 "id": 12,
 "name": "sacar a pasear al perro",
 "orden": 100,
 "due_date": null,
 "priority": "H",
 "color": "red",
 "finished": false,
 "project_id": null
 },
 {
 "id": 29,
 "name": "ir a correos a recoger el paquete",
 "orden": 100,
 "due_date": "2023-06-11",
 "priority": "N",
 "color": "orange",
 "finished": true,
 "project_id": 1
 }
]
```

Para devolver un único objeto, la API debe atender también peticiones GET a
/api/tasks/<id> , donde <id> es un identificador numérico correspondiente a una
tarea ya creada. Si en la base de datos existe una tarea con el <id> solicitado, la API
debe retornar un código de respuesta 200 OK junto con un único objeto JSON
conteniendo sus datos; por ejemplo, esto podría ser una respuesta realista a la petición
GET /api/tasks/12 :

```json
{
 "id": 12,
 "name": "sacar a pasear al perro",
 "orden": 100,
 "due_date": null,
 "priority": "H",
 "color": "red",
 "finished": false,
 "project_id": null
}
```

En caso de que la tarea solicitada no exista, la API debe retornar un código de respuesta
404 Not Found y un objeto JSON indicando la naturaleza del error; por ejemplo:

```json
{
 "status": {
 "type": "error",
 "code": 404,
 "message": "The requested task could not be found"
 }
}
Método POST
Una petición POST debe aceptar un cuerpo JSON que incluya la información de la nueva
tarea a insertar en la base de datos (de manera análoga a como lo hace la interfaz web
habitual). Siguiendo con el ejemplo anterior, la API aceptaría una entrada similar a la
siguiente:
{
 "name": "comprar fruta",
 "due_date": "2023-06-08",
 "orden": 100,
 "priority": "L",
 "color": "green",
 "finished": false,
 "project_id": null
}
```

Nótese como el cliente que realiza la petición no especifica un campo id . Esto es así
porque el cliente no tiene manera de conocerlo de antemano, y el servidor es quien se
encarga de generar un id adecuado para la nueva tarea.
Ante una petición correcta, el endpoint debe retornar un código de estado 200 OK indicando
en el cuerpo una pequeña descripción del resultado y el id generado para la nueva
entrada. Por ejemplo:

```json
{
 "status": {
 "type": "ok",
 "code": 200,
 "message": "Task created successfully"
 },
 "id": 33
}
```

Del mismo modo, ante una petición errónea, el servidor debe informar de ello al cliente.
Existen muchas maneras en las que una petición podría ser considerada inválida, pero
vamos a considerar al menos dos casos: cuerpo inexistente o en formato incorrecto (es
decir, cualquier cosa que no sea JSON válido) y tratar de crear una entrada ya existente:
Cuerpo inexistente o inválido: La API debe retornar un código de estado 400 Bad
Request en cualquiera de los siguientes casos:
La petición POST no incluye datos en el cuerpo. Una pista para saber esto es
comprobar si el header Content-Length es igual a 0
La petición POST incluye un header Content-Type cuyo valor es distinto de
application/json . Nuestra API únicamente procesa datos en formato JSON,
por lo que una petición que incluya datos en cualquier otro formato será denegada
En cuanto al cuerpo de la respuesta, este puede ser un ejemplo representativo:

```json
{
 "status": {
 "type": "error",
 "code": 400,
 "message": "Malformed body: only valid JSON is accepted"
 }
}
```

Tarea ya existente: Si el cliente trata de insertar una tarea que ya existe en la base de
datos, la API debe retornar un código de estado 409 Conflict. Debido a que el cliente
no sabe qué id s están ya insertados, el criterio para determinar si una tarea ya existe
consistirá en buscar en la base de datos tareas con exactamente el mismo nombre y la
misma fecha límite (due date). Ejemplo de cuerpo de la respuesta:

```json
{
 "status": {
 "type": "error",
 "code": 409,
 "message": "A task with the same name and due date already
exists"
 }
}
```

## Dockerfile

Una vez esté lista la funcionalidad de la API encima de Taskmaster, se deberá preparar un
fichero Dockerfile con los pasos necesarios para empaquetar la aplicación completa en
una imagen Docker. Una vez construida la imagen, se deberá subir a la cuenta personal en
Docker Hub de cada alumno y el objetivo será poder testear la aplicación localmente
ejecutando docker run -p 8000:8000 <usuario_docker_hub>/taskmasterapi .

Algunos recordatorios y pistas:

- Se recomienda crear el fichero Dockerfile en la raíz del proyecto taskmaster ,
es decir, junto a otros ficheros que controlan cuestiones a nivel de proyecto tales como
manage.py y requirements.txt

- Algunas directivas comunes y útiles son FROM, COPY, RUN, EXPOSE y CMD.

- Para construir la imagen se usa el comando docker build . -t
<usuario_docker_hub>/taskmaster-api , habiéndonos asegurado primero de
estar posicionados en el directorio donde está el Dockerfile (el punto . hace
referencia a esto)

- Para subir la imagen una vez construida se utiliza docker push
<usuario_docker_hub>/taskmaster-api . Puede que tengamos sea necesario
ejecutar docker login primero
