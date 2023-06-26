let escoger = document.querySelector (".escoger");
let contenedorOpciones = document.querySelector (".contenedor_opciones");

let listaOpciones = document.querySelectorAll (".option");

let cajaBuscar = document.querySelector (".buscar_select input")

escoger.addEventListener("click", () => {
        contenedorOpciones.classList.toggle("opciones_activate");
        if (contenedorOpciones.classList.contains("opciones_activate"));

    });

    listaOpciones.forEach(o => {
            o.addEventListener ("click", () => {
                escoger.innerHTML = o.querySelector("label").innerHTML;
                contenedorOpciones.classList.remove("opciones_activate");
            });
    });

cajaBuscar.addEventListener ("keyup", function(e) {
        filterList(e.target.value);
});

let filterList = searchTerm => {
        searchTerm = searchTerm.toLowerCase();
        listaOpciones.forEach ( option => {
                let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
                if (label.indexOf(searchTerm) != -1) {
                        option.style.display = "block";
                } else {
                        option.style.display = "none";
                }
        });

}


let tope = document.querySelector(".tope");

tope.addEventListener("change", function calcular() {
    let numero = parseInt(this.value);
    if (numero <= 0.1) this.value = 0.5;
    if (numero >= 24.99) this.value = 24.5;
  });


