const d = document;

export default function eliminarMensajes(selecMensaje){
    if(!d.querySelector(selecMensaje)) return;

    const $mensaje = d.querySelector(selecMensaje),
        $padreMensaje = $mensaje.parentElement;

    $mensaje.classList.remove("mensaje--oculto");
    
    const refInterval = setInterval(() => {
        $padreMensaje.removeChild($mensaje);
        clearInterval(refInterval);
    }, 5000);
}