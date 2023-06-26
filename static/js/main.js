const btnFlecha = document.querySelector('.flecha');
const flechaActivate = document.querySelector('.active');
let navbar = document.querySelector(".caja_buscar");
let searchBox = document.querySelector(".img_buscar");
let navbar2 = document.querySelector(".control_input");



flechaActivate.addEventListener('click', function(){
    document.getElementById('toggle').classList.toggle('active')
});

btnFlecha.addEventListener('click', function(){
    document.getElementById('bar_lado').classList.toggle('activate')
});

searchBox.addEventListener("click", ()=>{
    navbar2.classList.toggle("showInput2");
    if(navbar.classList.contains("showInput2")){
    } 
  });

searchBox.addEventListener("click", ()=>{
    navbar.classList.toggle("showInput");
    if(navbar.classList.contains("showInput")){
    }
});

function mostrar() {
    var tipo = document.getElementById("password");

    if(tipo.type == 'password') {
        tipo.type = 'text';
    } else {
        tipo.type = 'password';
    }
};

