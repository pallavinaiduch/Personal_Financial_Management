document.querySelectorAll('.top-button').forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault();
    const target = document.querySelector(button.getAttribute('href'));
    if (target) {
      target.scrollIntoView({ behavior: 'smooth' });
    }
  });
});

// Predefined credentials (Demo purposes only)
const predefinedEmail = "Pallavi@gmail.com";
const predefinedPassword = "Pallavi21";

// Validate Login
function validateLogin(event) {
  event.preventDefault();
  
  const email = document.getElementById('loginEmail').value.trim();
  const password = document.getElementById('loginPassword').value.trim();
  const emailError = document.getElementById('emailError');
  const passwordError = document.getElementById('passwordError');

  emailError.textContent = "";
  passwordError.textContent = "";

  if (!email.includes('@') || !email.includes('.')) {
    emailError.textContent = "Enter a valid email address";
    return false;
  }

  if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";
    return false;
  }

  if (email === predefinedEmail && password === predefinedPassword) {
    alert("Login successful!");
    window.location.href = "dashboard.html";
  } else {
    alert("Incorrect email or password!");
  }

  return false;
}

// Validate Registration
function validateRegister(event) {
  event.preventDefault();
  
  const username = document.getElementById('regUsername').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const password = document.getElementById('regPassword').value.trim();
  const confirmPassword = document.getElementById('confirmPassword').value.trim();

  const usernameError = document.getElementById('usernameError');
  const emailError = document.getElementById('regEmailError');
  const passwordError = document.getElementById('regPasswordError');
  const confirmPasswordError = document.getElementById('confirmPasswordError');

  usernameError.textContent = "";
  emailError.textContent = "";
  passwordError.textContent = "";
  confirmPasswordError.textContent = "";

  if (username.length < 3) {
    usernameError.textContent = "Username must be at least 3 characters";
    return false;
  }

  if (!email.includes('@') || !email.includes('.')) {
    emailError.textContent = "Enter a valid email address";
    return false;
  }

  if (password.length < 6) {
    passwordError.textContent = "Password must be at least 6 characters";
    return false;
  }

  if (password !== confirmPassword) {
    confirmPasswordError.textContent = "Passwords do not match";
    return false;
  }

  alert("Registration successful!");
  window.location.href = "login.html";

  return false;
}