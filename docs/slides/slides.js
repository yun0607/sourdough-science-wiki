const deck = document.querySelector('#deck');
const slides = Array.from(deck.querySelectorAll('.slide'));
const chapters = Array.from(document.querySelectorAll('.chapters a'));
const pager = document.querySelector('.pager');
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const pageNumber = document.querySelector('#page-number');
const progress = document.querySelector('#reading-progress');
const references = document.querySelector('#references');
let current = 0;

function showSlide(moveFocus = false) {
  const requested = slides.findIndex((slide) => '#' + slide.id === location.hash);
  current = Math.max(0, requested);

  slides.forEach((slide, index) => {
    slide.hidden = current !== index;
  });
  chapters.forEach((link, index) => {
    const start = slides.findIndex((slide) => '#' + slide.id === link.hash);
    const nextChapter = chapters[index + 1];
    const end = nextChapter
      ? slides.findIndex((slide) => '#' + slide.id === nextChapter.hash)
      : slides.length;
    link.toggleAttribute('data-complete', current >= end);
    if (current >= start && current < end) {
      link.setAttribute('aria-current', 'step');
    } else {
      link.removeAttribute('aria-current');
    }
  });
  previous.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  pageNumber.textContent = (current + 1) + ' / ' + slides.length;
  progress.value = current + 1;

  if (moveFocus) slides[current].focus({ preventScroll: true });
  window.scrollTo(0, 0);
}

function step(direction) {
  const target = slides[current + direction];
  if (target) location.hash = target.id;
}

previous.addEventListener('click', () => step(-1));
next.addEventListener('click', () => step(1));
window.addEventListener('hashchange', () => showSlide(true));
document.addEventListener('keydown', (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || references.open) return;
  if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
  event.preventDefault();
  step(event.key === 'ArrowLeft' ? -1 : 1);
});

document.querySelector('#reference-link').addEventListener('click', (event) => {
  if (typeof references.showModal !== 'function' || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
  event.preventDefault();
  references.showModal();
});

deck.setAttribute('data-ready', '');
pager.hidden = false;
showSlide();
