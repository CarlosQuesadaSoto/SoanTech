function activa_boton(campo,boton){
	if (campo.value != "0"){
		boton.disabled=false;
	} else {
		boton.disabled=true;
	}
}