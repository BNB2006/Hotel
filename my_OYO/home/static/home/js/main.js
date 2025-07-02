// Smooth scrolling for anchor links
if (document.querySelectorAll('a[href^="#"]').length) {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });
}

// Add scroll animation
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

if (window.IntersectionObserver) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);

  document.querySelectorAll('.fade-in-up').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Set minimum date for check-in and check-out (hotel_detail.html)
if (document.getElementById('start_date') && document.getElementById('end_date')) {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('start_date').min = today;
  document.getElementById('end_date').min = today;

  document.getElementById('start_date').addEventListener('change', function() {
    document.getElementById('end_date').min = this.value;
  });
} 

