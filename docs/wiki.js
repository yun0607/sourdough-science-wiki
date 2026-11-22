const navigationLinks = document.querySelectorAll('nav a[href^="#"]');

function markCurrentLocation() {
  for (const link of navigationLinks) {
    if (link.hash === window.location.hash) {
      link.setAttribute('aria-current', 'location');
    } else {
      link.removeAttribute('aria-current');
    }
  }
}

window.addEventListener('hashchange', markCurrentLocation);
markCurrentLocation();
