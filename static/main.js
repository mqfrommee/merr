AOS.init({
    duration: 1000,
    once: true
});

function updateCountdown() {
    const weddingDate = new Date('2024-08-15T13:00:00').getTime();
    const now = new Date().getTime();
    const distance = weddingDate - now;

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    document.getElementById('days').textContent = String(days).padStart(2, '0');
    document.getElementById('hours').textContent = String(hours).padStart(2, '0');
    document.getElementById('minutes').textContent = String(minutes).padStart(2, '0');
    document.getElementById('seconds').textContent = String(seconds).padStart(2, '0');
}

setInterval(updateCountdown, 1000);
updateCountdown();

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission


ymaps.ready(function () {
    const myMap = new ymaps.Map('map', {
        center: [55.76, 37.64], 
        zoom: 15
    });

    const myPlacemark = new ymaps.Placemark([55.76, 37.64], {
        hintContent: 'Ресторан "Панорама"',
        balloonContent: 'ул. Примерная, д. 123'
    });

    myMap.geoObjects.add(myPlacemark);
});