document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("btnSesion");
  const mensaje = document.getElementById("mensaje");

  btn.addEventListener("click", () => {
    mensaje.style.display = "block";
  });
});
