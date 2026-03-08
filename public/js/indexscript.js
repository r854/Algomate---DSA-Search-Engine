function toggleMenu() {
    var menu = document.getElementById("menu");
    menu.classList.toggle("active");
  }
    var typed = new Typed('#typing-text', {
      strings: ['Leetcode','Codeforces','Codechef','Hackerrank','Hackerearth'],
      typeSpeed: 200,
      loop: true
    });
    // JavaScript code for triggering the login modal
    var loginModal = new bootstrap.Modal(document.getElementById('loginModal'), {
      keyboard: false
    });

    // Add an event listener to the login button
    var loginButton = document.getElementById('loginButton');
    loginButton.addEventListener('click', function() {
      loginModal.show();
    });
     // JavaScript code for triggering the sign up modal
  var signupModal = new bootstrap.Modal(document.getElementById('signupModal'), {
    keyboard: false
  });

  // Add an event listener to the sign up button
  var signupButton = document.getElementById('signupButton');
  signupButton.addEventListener('click', function() {
    signupModal.show();
  });