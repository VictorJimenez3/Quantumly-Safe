function signUp() {
    const username = document.getElementById("signup-username").value;
    const password = document.getElementById("signup-password").value;

    if (username && password) {
        alert(`User ${username} registered successfully! (Simulated)`);
        document.getElementById("signup-form").reset();
    } else {
        alert("Please fill in all fields for sign-up.");
    }
}
