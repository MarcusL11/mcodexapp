// Get the user menu and the button
// Check to see if this is in the proejct:
const userMenuButton = document.getElementById('user-menu-button');
const userMenu = document.getElementById('user-menu');

// Get the current URL or any other logic to determine the active page
const currentUrl = window.location.href;

// Get all the navigation links
const navigationLinks = document.querySelectorAll('nav a');

// Toggle the menu when the mobile menu button is clicked
// Check to see if this is in the proejct:
function toggleMobileMenu() {
  const mobileMenuItems = document.querySelector('#mobile-menu');
  const expanded = this.getAttribute('aria-expanded') === 'true';
  this.setAttribute('aria-expanded', !expanded);
  mobileMenuItems.style.display = expanded ? 'none' : 'block';
}

// Toggle the user menu when the user menu button is clicked
function toggleUserMenu() {
  userMenu.classList.toggle('hidden');
}

// Hide the user menu if user clicks outside of it
function hideUserMenu(event) {
  if (!userMenuButton.contains(event.target)) {
    userMenu.classList.add('hidden');
  }
}

// Loop through each navigation link
function handleNavigationLinks() {
  navigationLinks.forEach(link => {
    if (link.id === 'user-menu-item-0') {
      return;
    }

    if (link.href === currentUrl) {
      link.setAttribute('aria-current', 'page');
      link.classList.add('bg-secondary');
    } else {
      link.removeAttribute('aria-current');
      link.removeAttribute('bg-secondary');
    }
  });
}

// Add event listeners
document.addEventListener('DOMContentLoaded', function() {
  const toggleMobileMenuButton = document.querySelector('#mobile-menu-button');
  toggleMobileMenuButton.addEventListener('click', toggleMobileMenu);
  userMenuButton.addEventListener('click', toggleUserMenu);
  document.addEventListener('click', hideUserMenu);
  handleNavigationLinks();
});

