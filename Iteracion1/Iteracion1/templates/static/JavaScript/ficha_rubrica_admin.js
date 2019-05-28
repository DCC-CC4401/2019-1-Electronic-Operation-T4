/**
 * Funcion que transforma el boton de cambiar nombre a un input
 * @returns Nada
 * @author Joaquin Cruz
 */
const cambiarNombre = function() {
  const div_edit_name = document.querySelector("#edit-name-div");
  let nombre = div_edit_name.querySelector("#titulo").innerHTML;
  div_edit_name.innerHTML = `<label for="nombre_rubrica"e><b>Nombre de la rubrica</b></label><br><input class='my-input'type='text' id='edit-name-input'  value='${nombre}'>`;
};
var nuevasFilas = 0;
/**
 Funcion que agrega una fila a la tabla
 @returns Nada, solo agrega una fila a la tabla
 @author Joaquin Cruz
 TODO: Generar que se añada al formulario de envio.
 */
const agregarFila = function() {
  const table_rubrica = document.querySelector("#rubrica_html");
  let th_puntaje = document.querySelectorAll(".puntaje");
  let tr_nuevaFila = document.createElement("tr");
  tr_nuevaFila.setAttribute("class","columnas");
  for (let i = 0; i < th_puntaje.length; i++) {
    let td_aspecto = document.createElement("td");
    if(i === 0){
      td_aspecto.className += ` aspecto`;
      td_aspecto.innerHTML += `<span onclick="editarFila('nuevoAspecto${nuevasFilas}');"><b><span class="info"></span></b><i class="fas fa-edit"></i></span>`;
    }
    td_aspecto.className += ` nuevoAspecto${nuevasFilas}`;
    tr_nuevaFila.appendChild(td_aspecto);
  }
  table_rubrica.appendChild(tr_nuevaFila);
};
/**
  Funcion que agrega una columna a la tabla
  @returns Nada, solo agrega una columna
   */
const agregarColumna = function() {
  const tr_columnas_all = document.querySelectorAll(".columnas");
  for (let i = 0; i < tr_columnas_all.length; i++) {
    let col;
    let col_actual = tr_columnas_all[i];
    let clase = col_actual.children[0].classList[1];
    if (i === 0) {
      col = document.createElement("th");
      col.setAttribute("class", "puntaje");
    } else {
      col = document.createElement("td");
    }
    col.className=` ${clase}`;
    col_actual.appendChild(col);
  }
};
/**
  Funcion que permite la edicion de los puntajes de la tabla
  @returns Nada
  @author Joaquin Cruz
   */
const cambiarPuntajes = function(boton) {
  let puntajes = document.querySelectorAll(".puntaje");
  for (let i = 1; i < puntajes.length; i++) {
    let elemento = puntajes[i];
    let texto = elemento.innerHTML;
    elemento.innerHTML = "";
    let input = document.createElement("input");
    input.setAttribute("type", "text");
    input.setAttribute("value", texto);
    elemento.appendChild(input);
    boton.disabled = true;
  }
};
/**
  Funcion que permite editar toda una fila de la tabla
  @param {string} className el nombre de la clase de la fila
  @returns Nada
  @author Joaquin Cruz
   */

const editarFila = function(className) {
  let clase_elemento = className.split(" ");
  let clase_buscar = "." + clase_elemento[0];
  let fila = document.querySelectorAll(clase_buscar);
  for (let i = 0; i < fila.length; i++) {
    let elemento = fila[i];
    let input_text;
    let info;
    if (i === 0) {
      input_text = document.createElement("input");
      input_text.setAttribute("type", "text");
      info = elemento.querySelector(".info").innerHTML;
      input_text.setAttribute("value", info);
    } else {
      input_text = document.createElement("textarea");
      input_text.setAttribute("rows", "4");
      input_text.setAttribute("cols", "20");
      input_text.addEventListener("keydown",()=>{ 
        console.log(input_text.value);
      });
      info = elemento.innerHTML;
      input_text.value = info;
      input_text.innerText = info;
    }
    elemento.innerHTML = "";
    elemento.appendChild(input_text);
  }
};
/**
  TODO:
  Funcion que permite guardar de manera asyncrona la tabla que se esta editando
  @param {DOM Element} boton el boton que permite hacer la accion
  @returns Nada, tal vez redireccione
  @author Joaquin Cruz
   */
const guardarRubrica = function(boton, rubrica_id) {
  let boton_original = boton.innerHTML;
  document.querySelector("#mensaje").innerHTML = "";
  boton.innerHTML +=
    '<br><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
  //obtener el nombre de la rubrica:
  const div_edit_name = document.querySelector("#edit-name-div");
  let nombre;
  if (div_edit_name.querySelector("#titulo") === null) {
    nombre = document.querySelector(".my-input").value;
  } else {
    nombre = div_edit_name.querySelector("#titulo").innerHTML;
  }
  
  let columnas = document.querySelectorAll(".columnas");
  let datos_tabla = [];
  for (let i = 0; i < columnas.length; i++) {
    let hijos = columnas[i].children;
    let datos = [];
    for (let j = 0; j < hijos.length; j++) {
      let recuadro_rubrica = hijos[j];
      if (recuadro_rubrica.children.length === 0) {
        // Si no es un aspecto, añadelo a su datos
        datos.push(recuadro_rubrica.innerHTML);
      } else if (recuadro_rubrica.classList[0] === "aspecto" || recuadro_rubrica.classList[0] === "puntaje") {
        // Si lo es, ve que onda su children
        if (recuadro_rubrica.firstChild.nodeName === "INPUT") {
          datos.push(recuadro_rubrica.firstChild.value);
        } else {
          datos.push(recuadro_rubrica.innerText);
        }
      } else if (recuadro_rubrica.children.length != 0) {
        if(recuadro_rubrica.firstElementChild.nodeName === "TEXTAREA" || recuadro_rubrica.firstElementChild.nodeName === "INPUT"){
          console.log(recuadro_rubrica.firstElementChild.value);
          datos.push(recuadro_rubrica.firstChild.value); 
        }
        else{
          console.log(recuadro_rubrica.firstChild.value);
          datos.push(recuadro_rubrica.firstChild.innerHTML);
        }
      }
    }
    datos_tabla.push(datos);
  }
  if (validar(datos_tabla)) {
    let mis_datos = {
      id: rubrica_id,
      nombre_tabla: nombre,
      rubrica: datos_tabla
    };
    console.log(mis_datos);
    fetch("/ajax/update_rubrica", {
      method: "POST",
      headers: {
        //headers of the submition
        Accept: "application/json, text/plain, */*",
        "Content-type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
      },
      credentials: "include",
      body: JSON.stringify(mis_datos)
    })
      .then(res => res.json())
      .then(
        data => {
          setTimeout(() => {
            boton.innerHTML = boton_original;
            document.querySelector(
              "#mensaje"
            ).innerHTML = `<hr style="width:50px;border:5px solid green" class="w3-round">
      <h3 class="w3-large w3-text-green"><i class="far fa-check-circle"></i> <b>Rubrica Actualizada </b></h3>
      <hr style="width:50px;border:5px solid green" class="w3-round">`;
          }, 1000);
          console.log(data);
        })
        .catch(
        reason => {
          setTimeout(() =>{
            document.querySelector(
            "#mensaje"
          ).innerHTML = `<hr style="width:50px;border:5px solid red" class="w3-round">
      <h3 class="w3-large w3-text-red"><i class="far fa-times-circle"></i> <b>Hubo un error al procesar los datos en el servidor.</b></h3>
      <hr style="width:50px;border:5px solid red" class="w3-round">`;
          boton.innerHTML = boton_original;
          },1000);
        }
      );
  }
  else{
    setTimeout(() =>{ 
      boton.innerHTML = boton_original;
      console.log("Datos no validos");
      console.log(datos_tabla);
    }, 1000);
  }
};
/**
    Funcion que valida los datos de la tabla en el update
    @param {Array} data un objeto de javascript con los datos de la tabla
    @return true si los datos estan ok, false en cualquier otro cas
    @author Joaquin Cruz
    // TODO: Mostrar mensaje de error si no pasa los puntajes
   */
const validar = function(data) {
  let blanco_puntajes = data[0];
  let puntajes = blanco_puntajes.slice(1, blanco_puntajes.length);
  const regex_puntajes = new RegExp("[0-9]+(.[0-9]+)?$");
  for (let i = 0; i < puntajes.length; i++) {
    if (!regex_puntajes.test(puntajes[i])) {
      console.log(puntajes[i]);
      return false;
    }
  }
  let sum = 0;
  const regex_info = new RegExp("[a-zA-Z]+|^$|\n");
  for (let i = 1; i < data.length; i++) {
    let fila = data[i];
    if (fila.length === 1) {
      return false;
    }
    for (let j = 0; j < fila.length; j++) {
      let info = fila[j];
      if (!regex_info.test(info)) {
        console.log("Dato no ok: " + info);
        return false;
      }
    }
    //TODO: ver que onda con la verificacion de puntajes
    sum += parseFloat(puntajes[fila.length - 2]); 
  }
  return sum === 6.0;
};
var borrarCol = false;
var borrarFila = false;
// TODO: Ver como eliminar aspectos!
const evntBtnBorrarCol = function() {
  if (!borrarCol) {
    const th_puntajes = document.querySelectorAll(".puntaje");
    for (let i = 1; i < th_puntajes.length; i++) {
      th_puntajes[i].innerHTML += `<br><button onclick='eliminarColumna()' class="btn btn-danger"><i class="fas fa-trash-alt"></i></button>`;
    }
    borrarCol = true;
  }
};
const evntBtnBorrarFila = function() {
  if(!borrarFila){
    const td_aspectos = document.querySelectorAll(".aspecto");
    for(let i = 0; i<td_aspectos.length; i++){
      let clase = td_aspectos[i].classList[1];
      td_aspectos[i].innerHTML+=`<br><button onclick='eliminarFila("${clase}")' class="btn btn-danger ${td_aspectos[i].className}"><i class="fas fa-trash-alt"></i></button>`;
    }
    borrarFila= true;
  }
};
const eliminarFila = function(clase) {
  let fila = document.querySelectorAll("." +clase);
  let parent = fila[0].parentNode;
  let table = parent.parentNode;
  table.removeChild(parent);
};
const eliminarColumna = function(pos) {
  console.log('Elimino la columna');
};