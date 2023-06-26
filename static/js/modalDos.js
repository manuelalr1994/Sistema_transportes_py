let cerrarDos = document.querySelectorAll ("#closeModalDos")[0];
let lista_abrirDos = document.getElementById ("contenido_tabla_capturas_dos");
let modalDos = document.querySelectorAll (".modalDos")[0];
let modalContainerDos = document.querySelectorAll (".modalContainerDos")[0];
let semana_selectDos = document.querySelectorAll("#semanaDos")[0];

cerrarDos.addEventListener ("click" , function(){
    modalDos.classList.toggle("modalCloseDos");
    setTimeout(function(){
        modalContainerDos.style.opacity = "0";
        modalContainerDos.style.visibility = "hidden";
    });
});

window.addEventListener("click" , function(e){
    if(e.target == modalContainerDos){
        modalDos.classList.toggle("modalCloseDos");
        setTimeout(function(){
            modalContainerDos.style.opacity = "0";
            modalContainerDos.style.visibility = "hidden";
        });
    }
});

// Cada que se generan nuevas capturas en la lista, se les aplica el evento
// para ventana modal
lista_abrirDos.addEventListener("click", function(e){
    const elemento_accionado = e.target;
    if (elemento_accionado.matches(".btnDesgloce, #abrirModalDos")){
        e.preventDefault();
        modalContainerDos.style.opacity = "1";
        modalContainerDos.style.visibility = "visible";
        modalDos.classList.toggle("modalCloseDos");
    }
});

function checkUncheck(main) {
    all = document.getElementsByName('lang');
    for (var a=0;a<all.length;a++) {
        all[a].checked = main.checked;
    }
};

