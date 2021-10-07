document.addEventListener("DOMContentLoaded", function (event) {
var buttons = document.querySelectorAll('.estiloModificar');
buttons.forEach(button => {
    button.addEventListener("click", function (event) {

        var selectform = button.closest('tr')
        console.log(selectform)
        var nuevo = selectform.querySelector('.select')
        console.log(nuevo)
        nuevo.disabled = !nuevo.disabled
        selectform.disabled=false
        var nuevo = selectform.querySelector('.estiloGuardar')
        console.log(nuevo)
        nuevo.disabled = !nuevo.disabled
        selectform.disabled=false

        });
    })
});

console.log("hola")






