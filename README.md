# 2019-1-Electronic-Operations-T4
# Requisitos a hacer:

## (Requisitos generales)

### Del 1 al 9:
 - [x] El sistema debe permitir que el administrador del sistema cree cuentas de
evaluador en el sistema, solicitando el nombre, apellido, correo electrónico y
generando al azar la contraseña del usuario.
 - [x] Todo usuario debe autentificarse para acceder al sistema, usando su correo
electrónico y su contraseña.
 - [x] No se puede crear más de una cuenta en el sistema con el mismo correo
electrónico.
 - [x] El sistema debe considerar 2 tipos de usuarios: administrador, y evaluador.
 - [x] El administrador también puede evaluar presentaciones.
 - [x] Cada curso debe tener un nombre, código, número de sección, y año y semestre
de realización.
 - [x] Cada combinación de código, número de sección, y año y semestre de
realización de curso debe ser única en el sistema.
 - [x] Un curso puede tener más de un evaluador.
 - [x] Dentro de un curso, cada estudiante debe pertenecer a un equipo de trabajo.

### Requisito 11:

 - [x] Cada curso puede tener cero o más evaluaciones.

### Requisito 15 y 16:
 - [ ]  El sistema debe mostrar un listado de las últimas 10 evaluaciones asociadas al
usuario, ordenados por fecha (más nuevos al inicio de la lista), indicando el
curso asociado, cuales están pendientes y cuales ya fueron contestadas.
 - [ ]  El usuario puede acceder a la ficha de una evaluación desde el resumen de las
evaluaciones.

## Requisitos 28 al 45 (Ficha de una evaluación):

- [ ] El sistema debe indicar el curso asociado a la evaluación, el estado de la
evaluación (abierta, cerrada), las fechas de inicio y fin, duración esperada de las
presentaciones y la rúbrica asociada.
- [ ] En el caso del administrador, el sistema debe permitir actualizar los plazos de
una evaluación, sin perder las evaluaciones que ya fueron realizadas por los
evaluadores.
- [ ] En el caso del administrador, el sistema debe mostrar una lista de los
evaluadores asociados a la evaluación.
- [ ] El administrador puede agregar o quitar evaluadores antes de abrir la evaluación
a los evaluadores.
- [ ] Una vez iniciada una evaluación, el administrador solo puede quitar evaluadores
asociado que no han ingresado notas.
- [ ] Una vez iniciada una evaluación, el administrador puede agregar nuevos
evaluadores.
- [ ] El sistema debe mostrar la rúbrica asociada a la evaluación.
- [ ] El administrador puede editar la rúbrica asociada a una evaluación antes de abrir
la evaluación a los evaluadores.
- [ ] No se podrá modificar la rúbrica de una evaluación después de que se haya
registrado la evaluación de un equipo.
- [ ] Si la evaluación aún está abierta, en el caso del administrador se debe mostrar
un listado de los equipos cuya evaluación aún está pendiente.
- [ ] Si la evaluación aún está abierta, el administrador puede elegir uno de los
equipos cuya evaluación está pendiente, para comenzar su evaluación.
- [ ] Al comenzar la evaluación de un equipo, en el caso del administrador, el sistema
debe mostrar quiénes del equipo han presentado y quienes no. El administrador
debe indicar los nombres de los estudiantes que presentaran.
- [ ] Una vez iniciada una evaluación, los evaluadores asociados solo podrán
ingresar puntajes al equipo seleccionado por el administrador.
- [ ] En cada evaluación de equipo, los evaluadores deben indicar puntajes para
todos los aspectos de la rúbrica.
- [ ] Para finalizar una evaluación, el usuario debe confirmar los puntajes ingresados.
- [ ] Si un usuario no está de acuerdo con los puntajes ingresados, debe poder
actualizar los puntajes ingresados.
- [ ] Solo el administrador puede indicar el tiempo que demoró una presentación.
- [ ] El sistema debe indicar si corresponde aplicar un descuento a un equipo, en
base a la duración mínima y máxima asociada a la rúbrica aplicada.

## Requisitos 47 al 51 (Ficha de una rubrica):
- [x] El sistema debe mostrar los aspectos a evaluar, como también los niveles de
cumplimiento y los puntajes asociados.
- [ ] En el caso del administrador, el sistema debe permitir agregar, quitar o modificar
aspectos a evaluar.
- [ ] En el caso del administrador, el sistema debe permitir agregar, quitar o modificar
niveles de cumplimiento para un aspecto a evaluar.
- [ ] En el caso del administrador, el sistema debe permitir indicar las duraciones
mínimas y máximas de las presentaciones que serán evaluadas.
- [ ] El sistema debe validar que la suma de los niveles máximos de los todos los
aspectos de cualquier rúbrica siempre sea 6.

## Requisitos landing page admin 61, 64 y 65:
- [ ] El sistema debe permitir la gestión (creación, modificación y eliminación) de evaluadores.
- [ ] El sistema debe permitir la gestión (creación, modificación y eliminación) de
evaluaciones.
- [ ] El sistema debe permitir la gestión (creación, modificación y eliminación) de
rubricas.
