/**
 * Funcion que transforma el boton de cambiar nombre a un input
 * @returns Nada
 * @author Joaquin Cruz
 */
const cambiarNombre = function(){
    const div_edit_name = document.querySelector('#edit-name-div');
    let nombre = div_edit_name.querySelector('#titulo').innerHTML;
    div_edit_name.innerHTML = `<label for="nombre_rubrica"e><b>Nombre de la rubrica</b></label><br><input class='my-input'type='text' id='edit-name-input'  value='${nombre}'>`;
};
/**
 Funcion que agrega una fila a la tabla
 @returns Nada, solo agrega una fila a la tabla
 @author Joaquin Cruz
 */
  const agregarFila = function(){
    const table_rubrica = document.querySelector("#rubrica_html");
    let th_puntaje = document.querySelectorAll(".puntaje");
    let tr_nuevaFila = document.createElement("tr");
    for(let i = 0; i < th_puntaje.length; i++){
      let td_aspecto = document.createElement("td");
      tr_nuevaFila.appendChild(td_aspecto);
    }
    table_rubrica.appendChild(tr_nuevaFila);
  };
  /**
  Funcion que agrega una columna a la tabla
  @returns Nada, solo agrega una columna
   */
  const agregarColumna = function(){
    const tr_columnas_all = document.querySelectorAll(".columnas");
    for(let i = 0; i< tr_columnas_all.length; i++){
      let col;
      if(i === 0){
        col = document.createElement("th");
        col.setAttribute("class","puntaje");
      }
      else{
        col = document.createElement("td");
      }
      tr_columnas_all[i].appendChild(col);
    }
  };
  /**
  Funcion que permite la edicion de los puntajes de la tabla
  @returns Nada
  @author Joaquin Cruz
   */
  const cambiarPuntajes = function(){
    let puntajes = document.querySelectorAll(".puntaje");
    for(let i = 1; i< puntajes.length; i++){
      let elemento = puntajes[i];
      let texto = elemento.innerHTML;
      elemento.innerHTML = "";
      let input = document.createElement("input");
      input.setAttribute("type","text");
      input.setAttribute("value",texto);
      elemento.appendChild(input);
    }
  }
  /**
  Funcion que permite editar toda una fila de la tabla
  @param {string} className el nombre de la clase de la fila
  @returns Nada
  @author Joaquin Cruz
   */
   
  const editarFila = function(className){
    let clase_elemento = className.split(" ");
    let clase_buscar = '.'+clase_elemento[0];
    let fila = document.querySelectorAll(clase_buscar);
    for(let i = 0; i < fila.length; i++){
      let elemento = fila[i];
      let input_text;
      let info;
      if(i === 0){
        input_text = document.createElement("input");
        input_text.setAttribute("type","text");
        info = elemento.querySelector(".info").innerHTML;
        input_text.setAttribute("value",info);
      }
      else{
        input_text = document.createElement("textarea");
        input_text.setAttribute("rows","4");
        input_text.setAttribute("cols","20");
        info = elemento.innerHTML;
        input_text.innerHTML=info;
      }
      elemento.innerHTML = "";
      elemento.appendChild(input_text);
    }
  }
  /**
  TODO:
  Funcion que permite guardar de manera asyncrona la tabla que se esta editando
  @param {DOM Element} boton el boton que permite hacer la accion
  @returns Nada, tal vez redireccione
  @author Joaquin Cruz
   */
  const guardarRubrica = function(boton,rubrica_id){
    let boton_original = boton.innerHTML;
    boton.innerHTML += '<br><span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    //obtener el nombre de la rubrica:
    const div_edit_name = document.querySelector('#edit-name-div');
    let nombre;
    if(div_edit_name.querySelector("#titulo") === null){
      nombre = document.querySelector(".my-input").value;
    }
    else{
      nombre = div_edit_name.querySelector("#titulo").innerHTML;
    }
    // TODO: Ahora con los puntajes y los aspectos
    let columnas = document.querySelectorAll(".columnas");
    let datos_tabla = [];
    for(let i = 0; i < columnas.length; i++){
      let hijos = columnas[i].children;
      let datos = [];
      for(let j = 0; j<hijos.length;j++){
        let recuadro_rubrica = hijos[j];
        if(recuadro_rubrica.children.length === 0){ // Si no es un aspecto, añadelo a su datos
          datos.push(recuadro_rubrica.innerHTML);
        }
        else if(recuadro_rubrica.classList[0] === "aspecto"){ // Si lo es, ve que onda su children
          if(recuadro_rubrica.firstChild.nodeName === "INPUT"){
               datos.push(recuadro_rubrica.firstChild.value);
          }
          else{
               datos.push(recuadro_rubrica.innerText);
          }
        }
        else if(recuadro_rubrica.children.length != 0){
             datos.push(recuadro_rubrica.firstChild.innerHTML);
        }
      }
      datos_tabla.push(datos);
    }
    if(validar(datos_tabla)){
      let mis_datos = {id: rubrica_id,nombre_tabla: nombre, datos: datos_tabla};
      console.log(JSON.stringify(mis_datos));
      fetch('/ajax/update_rubrica',{
        method: 'POST',
        headers: { //headers of the submition
        'Accept': 'application/json, text/plain, */*',
        'Content-type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'include',
        body: JSON.stringify(mis_datos)
      })
      .then(res => res.json())
      .then(data => console.log(data));
    }
    boton.innerHTML = boton_original;
  }
  /**
    Funcion que valida los datos de la tabla en el update
    @param {Array} data un objeto de javascript con los datos de la tabla
    @return true si los datos estan ok, false en cualquier otro cas
    @author Joaquin Cruz 
   */
  const validar = function(data){
       let blanco_puntajes = data[0];
       let puntajes = blanco_puntajes.slice(1,blanco_puntajes.length);
       const regex_puntajes = new RegExp("[0-9]+(\.[0-9]+)?$");
       for(let i = 0; i<puntajes.length;i++){
         if(!regex_puntajes.test(puntajes[i])){
           return false;
         }
       }
       let sum = 0;
       const regex_info = new RegExp("[a-zA-Z]+");
       for(let i = 1; i < data.length; i++){
         let fila = data[i];
         if(fila.length === 1){
           return false;
         }
         for(let j = 0; j<fila.length; j++){
           let info = fila[j];
           if(!regex_info.test(info)){
             console.log("Dato no ok: "+info);
             return false; 
           }
         }
         sum+=parseFloat(puntajes[fila.length-2]);
       }
       return sum === 6.0; 
      
  }

// TODO: una exportacion de los puntajes por si queremos reutilizar el codigo :)
