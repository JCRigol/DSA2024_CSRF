# Entrega Trabajo Final de opiuqe led erbmoN

Autor: Juan Cruz Rigol

El ejercicio corresponde a la vulnerabilidad [Cross Site Request Forgery](https://owasp.org/www-community/attacks/csrf). Esta diseñado como un ejercicio facil e introductorio al tema.

La vulnerabilidad es explotada aprovechando el sitio inseguro al cual entra el agente automatico, cargano al mismo un HTML malicioso con el que el agente interactua y aprovecha el servicio de cambio de contraseña del sitio vulnerable para apropiarse de la cuenta.

Con fines demostrativos, el HTML malicioso se encuentra hecho en esta entrega, siendo la variable 'default_attack_html' del sitio2. La misma deberia ser setteada a None para que el ejercicio quede a 0.

El ejercicio esta hecho para que ciertos valores se resetteen automaticamente luego de ciertas operaciones (un ejemplo es la contraseña apropiada del usuario admin, la cual se resetea luego del proximo login). Esto esta hecho asi asumiendo que la baja dificultad del ejercicio garantiza que esto no genere errores en la funcionalidad del ejercicio. En caso de surgir problemas reiniciar el contenedor.

Para modificar los parametros y la flag, cambiar los valores en .env antes de levantar el contenedor.

DISCLAIMER: Docker deberia andar mejor esta vez, pero sin embargo Redis me da un poco de miedo asi que recomendaria que le den un vistazo.

Ejecutar con:
```
docker-compose up
```