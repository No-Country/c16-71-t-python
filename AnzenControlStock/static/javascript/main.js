const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
  document.querySelector("#sidebar").classList.toggle("expand");
});

document.addEventListener("DOMContentLoaded", function() {
  const eliminarBtn = document.querySelector('.btn-eliminar');
  const mensajeDiv = document.querySelector('.mensaje');

  eliminarBtn.addEventListener('click', function() {
    mensajeDiv.style.display = 'block';
    mensajeDiv.style.width = '454px';
    mensajeDiv.style.height = '260px';
    mensajeDiv.style.backgroundColor = '#FFFFFF';
    mensajeDiv.style.border = "1px solid #000000";
    mensajeDiv.style.borderRadius = '8px';
    mensajeDiv.style.position = 'absolute';
    mensajeDiv.style.left = '214px';
    mensajeDiv.style.top = '61px';
    mensajeDiv.style.display = 'flex';
    mensajeDiv.style.justifyContent = 'center';
    mensajeDiv.style.flexDirection = 'column';
    mensajeDiv.style.alignItems = 'center';
});


  // Optional: Hide the mensajeDiv when cancel button is clicked
  const cancelarBtn = document.querySelector('.btn-mensajeCancelar');
  cancelarBtn.addEventListener('click', function() {
      mensajeDiv.style.display = 'none';
  });
});
