const chapterLinks = [...document.querySelectorAll('.reading-rail a[href^="#"]')];
const chapters = chapterLinks.map((link) => ({
  link,
  section: document.querySelector(link.getAttribute('href')),
})).filter(({ section }) => section);

let activeChapter = null;
let framePending = false;

function updateChapter() {
  const readingLine = Math.min(window.innerHeight * 0.25, 180);
  let currentChapter = null;

  for (const chapter of chapters) {
    if (chapter.section.getBoundingClientRect().top <= readingLine) {
      currentChapter = chapter;
    }
  }

  if (currentChapter !== activeChapter) {
    activeChapter?.link.removeAttribute('aria-current');
    currentChapter?.link.setAttribute('aria-current', 'location');
    activeChapter = currentChapter;
  }

  framePending = false;
}

function scheduleUpdate() {
  if (!framePending) {
    framePending = true;
    window.requestAnimationFrame(updateChapter);
  }
}

window.addEventListener('scroll', scheduleUpdate, { passive: true });
window.addEventListener('resize', scheduleUpdate);
window.addEventListener('load', scheduleUpdate);
updateChapter();
