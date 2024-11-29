// script.js
document.getElementById("show-details").addEventListener("click", function() {
    const password = document.getElementById("password").value;
    
    // Aquí puedes implementar la lógica para verificar la contraseña
    if (password === "tuContraseñaSegura") {  // Cambia esto por la lógica de verificación real
        document.getElementById("additional-info").style.display = "block";
    } else {
        alert("Contraseña incorrecta. Inténtalo de nuevo.");
    }
});