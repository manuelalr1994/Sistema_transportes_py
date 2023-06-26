let cerrar = document.querySelectorAll ("#closeModal")[0];
let cerrarDos = document.querySelectorAll ("#closeModalDos")[0];
let lista_abrir = document.getElementById ("contenido_tabla_capturas");
let modal = document.querySelectorAll (".modal")[0];
let modalContainer = document.querySelectorAll (".modalContainer")[0];
let semana_select = document.querySelectorAll("#semana")[0];

console.log(semana_select)

cerrar.addEventListener ("click" , function(){
    modal.classList.toggle("modalClose");
    setTimeout(function(){
        modalContainer.style.opacity = "0";
        modalContainer.style.visibility = "hidden";
    });
});

window.addEventListener("click" , function(e){
    if(e.target == modalContainer){
        modal.classList.toggle("modalClose");
        setTimeout(function(){
            modalContainer.style.opacity = "0";
            modalContainer.style.visibility = "hidden";
        });
    }
});

// Cada que se generan nuevas capturas en la lista, se les aplica el evento
// para ventana modal
lista_abrir.addEventListener("click", function(e){
    const elemento_accionado = e.target;
    if (elemento_accionado.matches(".imgEditar, #abrirModal")){
        e.preventDefault();
        modalContainer.style.opacity = "1";
        modalContainer.style.visibility = "visible";
        modal.classList.toggle("modalClose");
    }
});

function checkUncheck(main) {
    all = document.getElementsByName('lang');
    for (var a=0;a<all.length;a++) {
        all[a].checked = main.checked;
    }
};



