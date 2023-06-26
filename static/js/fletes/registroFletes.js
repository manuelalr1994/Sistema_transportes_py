const formulario = document.querySelector("#formulario");
const inputs = document.querySelectorAll('.colum_input input');
const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{3,35}$/, // Letras y espacios, pueden llevar acentos.
	password: /^.{4,12}$/, // 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/, // 7 a 14 numeros.
    dinero: /^\d{1,4}[.]\d{2}$/, // 1 a 6 numeros.
	direccion: /^[a-zA-Z0-9\s]{3,70}$/, // Letras, numeros, guion y guion_bajo
	rfc: /^[A-Za-zñÑ&]{3,4}\d{6}\w{3}$/, // Letras y espacios, pueden llevar acentos.
	cnta_banco: /^\d{10}/, // 10 numeros.
    tar_banco: /^\d{16}$/, // 16 numeros.
    cod_postal:/^\d{5}$/, // 5 numeros.
	codigo: /^\d{4}$/, // 4 numeros.
	codigoEmpleado: /^\d{8}$/ // 8 numeros.
}
const validarFormulario = (e) => {
	switch (e.target.name) {
		case "alias":
			validarCampo(expresiones.nombre, e.target, 'Alias');
		break;
		case "nombre":
			validarCampo(expresiones.nombre, e.target, 'Nombre');
		break;
		case "puesto":
			validarCampo(expresiones.nombre, e.target, 'Puesto');
		break;
		case "costo_hra":
			validarCampo(expresiones.dinero, e.target, 'Hora');
		break;
		case "cuenta":
			validarCampo(expresiones.cnta_banco, e.target, 'Cuenta');
		break;
		case "tarjeta":
			validarCampo(expresiones.tar_banco, e.target, 'Tar');
		break;
		case "rfc":
			validarCampo(expresiones.rfc, e.target, 'RFC');
		break;
		case "direccion":
			validarCampo(expresiones.direccion, e.target, 'Dir');
		break;
		case "ciudad":
			validarCampo(expresiones.nombre, e.target, 'Ciudad');
		break;
		case "colonia":
			validarCampo(expresiones.nombre, e.target, 'Col');
		break;
		case "codigo_postal":
			validarCampo(expresiones.cod_postal, e.target, 'CodPostal');
		break;
		case "estado":
			validarCampo(expresiones.nombre, e.target, 'EstadEmp');
		break;
		case "cp":
			validarCampo(expresiones.cod_postal, e.target, 'CpEmp');
		break;
		case "estado":
			validarCampo(expresiones.nombre, e.target, 'EstadEmp');
		break;
		case "codigo":
			validarCampo(expresiones.codigo, e.target, 'CodEmp');
		break;
		case "apellido_m":
			validarCampo(expresiones.nombre, e.target, 'Apellido_m');
		break;
		case "apellido_p":
			validarCampo(expresiones.nombre, e.target, 'Apellido_p');
		break;
		case "codigo_empleado":
			validarCampo(expresiones.codigoEmpleado, e.target, 'CodEmpleado');
		break;
	}
};
const validarCampo = (expresion, input, campo) => {
	if(expresion.test(input.value)){
		document.querySelector(`#grupo${campo} span`).classList.remove('quitarRojo');
		document.querySelector(`#grupo${campo} span`).classList.add('ponerRojo');
		document.querySelector(`#grupo${campo} label`).classList.remove('quitarRojo')
	} else {
		document.querySelector(`#grupo${campo} label`).classList.add('quitarRojo')
		document.querySelector(`#grupo${campo} span`).classList.add('quitarRojo');
		document.querySelector(`#grupo${campo} span`).classList.remove('ponerRojo');
	}
};
inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});