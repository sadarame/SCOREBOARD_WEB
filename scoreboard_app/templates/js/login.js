let currentIndex = 0;

//スライダーが機能しないので、コメントアウト
//ajexでやりたい

// function showSlide(index) {
//     const slides = document.querySelectorAll('.slide');
//     const totalSlides = slides.length;

//     if (index >= totalSlides) {
//         currentIndex = 0;
//     } else if (index < 0) {
//         currentIndex = totalSlides - 1;
//     } else {
//         currentIndex = index;
//     }

//     const offset = -currentIndex * 100;
//     document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
// }

// document.addEventListener('DOMContentLoaded', () => {
//     showSlide(currentIndex);
//     setInterval(() => {
//         showSlide(currentIndex + 1);
//     }, 3000);
// });
