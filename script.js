/* ==========================================================================
   HARVARD MINIMALIST SLIDESHOW ENGINE & MOBILE GESTURES
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  const slides = Array.from(document.querySelectorAll('.slide-card'));
  const totalSlides = slides.length;
  let currentSlideIndex = 0;
  let isScrollMode = false;

  // UI Elements
  const prevBtn = document.getElementById('btn-prev');
  const nextBtn = document.getElementById('btn-next');
  const counterEl = document.getElementById('slide-counter');
  const progressBar = document.getElementById('progress-bar');
  const tocBtn = document.getElementById('btn-toc');
  const tocDrawer = document.getElementById('toc-drawer');
  const drawerBackdrop = document.getElementById('drawer-backdrop');
  const closeDrawerBtn = document.getElementById('btn-close-drawer');
  const tocList = document.getElementById('toc-list');
  const modeToggleBtn = document.getElementById('btn-mode-toggle');
  const fullscreenBtn = document.getElementById('btn-fullscreen');

  // Lightbox Elements
  const lightbox = document.getElementById('lightbox-modal');
  const lightboxImg = document.getElementById('lightbox-img');
  const lightboxCaption = document.getElementById('lightbox-caption');
  const closeLightboxBtn = document.getElementById('btn-close-lightbox');

  // Populate Table of Contents
  slides.forEach((slide, idx) => {
    const titleEl = slide.querySelector('.slide-title');
    const titleText = titleEl ? titleEl.textContent.trim() : `Diapositiva ${idx + 1}`;
    const tocItem = document.createElement('div');
    tocItem.className = `toc-item ${idx === 0 ? 'active' : ''}`;
    tocItem.dataset.index = idx;
    
    const numSpan = document.createElement('span');
    numSpan.className = 'toc-num';
    numSpan.textContent = String(idx + 1).padStart(2, '0');

    const textSpan = document.createElement('span');
    textSpan.textContent = titleText;

    tocItem.appendChild(numSpan);
    tocItem.appendChild(textSpan);

    tocItem.addEventListener('click', () => {
      goToSlide(idx);
      closeDrawer();
      if (isScrollMode) {
        slide.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });

    tocList.appendChild(tocItem);
  });

  // Update Slide View
  function updateSlide(index) {
    if (index < 0 || index >= totalSlides) return;
    currentSlideIndex = index;

    // Toggle active slide class
    slides.forEach((slide, idx) => {
      slide.classList.toggle('active', idx === currentSlideIndex);
      if (idx === currentSlideIndex) {
        slide.scrollTop = 0;
      }
    });

    // Update Counter & Progress
    const displayNum = String(currentSlideIndex + 1).padStart(2, '0');
    const displayTotal = String(totalSlides).padStart(2, '0');
    counterEl.textContent = `${displayNum} / ${displayTotal}`;

    const progressPct = ((currentSlideIndex + 1) / totalSlides) * 100;
    progressBar.style.width = `${progressPct}%`;

    // Update Nav Buttons State
    prevBtn.disabled = currentSlideIndex === 0;
    nextBtn.disabled = currentSlideIndex === totalSlides - 1;

    // Update Drawer Active Item
    const tocItems = tocList.querySelectorAll('.toc-item');
    tocItems.forEach((item, idx) => {
      item.classList.toggle('active', idx === currentSlideIndex);
    });

    // Render KaTeX in active slide if not already rendered
    renderMath();
  }

  function goToSlide(index) {
    updateSlide(index);
  }

  function nextSlide() {
    if (currentSlideIndex < totalSlides - 1) {
      updateSlide(currentSlideIndex + 1);
    }
  }

  function prevSlide() {
    if (currentSlideIndex > 0) {
      updateSlide(currentSlideIndex - 1);
    }
  }

  // Event Listeners for Nav Buttons
  prevBtn.addEventListener('click', prevSlide);
  nextBtn.addEventListener('click', nextSlide);

  // Keyboard Navigation
  document.addEventListener('keydown', (e) => {
    // Ignore keydown if lightbox or drawer is open
    if (lightbox.classList.contains('active')) {
      if (e.key === 'Escape') closeLightbox();
      return;
    }

    if (tocDrawer.classList.contains('open')) {
      if (e.key === 'Escape') closeDrawer();
      return;
    }

    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      if (!isScrollMode) {
        e.preventDefault();
        nextSlide();
      }
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      if (!isScrollMode) {
        e.preventDefault();
        prevSlide();
      }
    } else if (e.key === 'Home') {
      if (!isScrollMode) {
        e.preventDefault();
        goToSlide(0);
      }
    } else if (e.key === 'End') {
      if (!isScrollMode) {
        e.preventDefault();
        goToSlide(totalSlides - 1);
      }
    } else if (e.key.toLowerCase() === 'f') {
      toggleFullscreen();
    }
  });

  // Touch & Swipe Support for Mobile
  let touchStartX = 0;
  let touchStartY = 0;
  let touchEndX = 0;
  let touchEndY = 0;

  const deck = document.getElementById('slide-deck');

  deck.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
    touchStartY = e.changedTouches[0].screenY;
  }, { passive: true });

  deck.addEventListener('touchend', (e) => {
    if (isScrollMode) return; // In scroll mode, allow native scrolling
    touchEndX = e.changedTouches[0].screenX;
    touchEndY = e.changedTouches[0].screenY;
    handleSwipe();
  }, { passive: true });

  function handleSwipe() {
    const deltaX = touchEndX - touchStartX;
    const deltaY = touchEndY - touchStartY;

    // Must be predominantly horizontal and sufficiently long (min 50px)
    if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 45) {
      if (deltaX < 0) {
        // Swiped Left -> Next
        nextSlide();
      } else {
        // Swiped Right -> Previous
        prevSlide();
      }
    }
  }

  // Drawer Actions
  function openDrawer() {
    tocDrawer.classList.add('open');
    drawerBackdrop.classList.add('active');
  }

  function closeDrawer() {
    tocDrawer.classList.remove('open');
    drawerBackdrop.classList.remove('active');
  }

  tocBtn.addEventListener('click', openDrawer);
  closeDrawerBtn.addEventListener('click', closeDrawer);
  drawerBackdrop.addEventListener('click', closeDrawer);

  // Lightbox Actions
  function openLightbox(src, caption) {
    lightboxImg.src = src;
    lightboxCaption.textContent = caption || '';
    lightbox.classList.add('active');
  }

  function closeLightbox() {
    lightbox.classList.remove('active');
  }

  document.querySelectorAll('.figure-wrapper').forEach((wrapper) => {
    wrapper.addEventListener('click', () => {
      const img = wrapper.querySelector('img');
      const cap = wrapper.querySelector('.figure-caption');
      if (img) {
        openLightbox(img.src, cap ? cap.textContent : '');
      }
    });
  });

  closeLightboxBtn.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });

  // Toggle Mode (Slide vs Continuous Scroll)
  modeToggleBtn.addEventListener('click', () => {
    isScrollMode = !isScrollMode;
    document.body.classList.toggle('scroll-mode', isScrollMode);
    
    if (isScrollMode) {
      modeToggleBtn.classList.add('active');
      modeToggleBtn.querySelector('.mode-label').textContent = 'Modo Diapositivas';
      // Scroll to current active slide in view
      slides[currentSlideIndex].scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      modeToggleBtn.classList.remove('active');
      modeToggleBtn.querySelector('.mode-label').textContent = 'Modo Lectura';
      updateSlide(currentSlideIndex);
    }
  });

  // Fullscreen Toggle
  function toggleFullscreen() {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(() => {});
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  }

  fullscreenBtn.addEventListener('click', toggleFullscreen);

  // KaTeX Math Rendering
  function renderMath() {
    if (window.renderMathInElement) {
      renderMathInElement(document.body, {
        delimiters: [
          { left: '$$', right: '$$', display: true },
          { left: '$', right: '$', display: false },
          { left: '\\[', right: '\\]', display: true },
          { left: '\\(', right: '\\)', display: false }
        ],
        throwOnError: false
      });
    }
  }

  // Initial Run
  updateSlide(0);
  setTimeout(renderMath, 200);
});
