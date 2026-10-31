// 1. Ask for confirmation before removing an item from the cart
const deleteLinks = document.querySelectorAll('.confirm-delete');
deleteLinks.forEach(function (link) {
  link.addEventListener('click', function (event) {
    if (!confirm('Remove this item from cart?')) {
      event.preventDefault();
    }
  });
});

// 2. Make sure the address is not empty before placing an order
const form = document.getElementById('checkout-form');
if (form) {
  form.addEventListener('submit', function (event) {
    const address = document.getElementById('address').value.trim();
    if (address === '') {
      alert('Please enter your delivery address');
      event.preventDefault();
    }
  });
}

// 3. Live search: hide product cards that don't match what the user types
const searchBox = document.getElementById('search-box');
if (searchBox) {                                                // only runs on the shop page
  const cards = document.querySelectorAll('.card');             // every product card
  const noResults = document.getElementById('no-results');      // the hidden "no match" message

  searchBox.addEventListener('input', function () {             // runs on every key the user types
    const text = searchBox.value.toLowerCase().trim();          // typed text, lowercase, no extra spaces
    let visible = 0;                                            // counts the cards still showing

    cards.forEach(function (card) {
      const matches = card.dataset.name.includes(text);         // does the card's name contain the text?
      card.style.display = matches ? '' : 'none';               // show it if yes, hide it if no
      if (matches) {
        visible++;                                              // count it
      }
    });

    noResults.style.display = visible === 0 ? 'block' : 'none'; // show the message only if nothing matched
  });
}

// 4. Zoom in / zoom out on the product details page
const zoomImage = document.getElementById('zoom-image');
if (zoomImage) {                                               // only runs on the details page
  const zoomFrame = document.getElementById('zoom-frame');
  const zoomLevel = document.getElementById('zoom-level');
  const MIN_ZOOM = 1;                                          // 1 = normal size (100%)
  const MAX_ZOOM = 3;                                          // 3 = three times bigger (300%)
  const STEP = 0.5;                                            // each click changes the size by 50%
  let zoom = 1;                                                // current zoom, starts at normal

  function applyZoom() {                                       // updates the screen to match 'zoom'
    zoomImage.style.transform = 'scale(' + zoom + ')';         // enlarge or shrink the picture
    zoomLevel.textContent = Math.round(zoom * 100) + '%';      // show 150% etc. as text
    zoomFrame.classList.toggle('zoomed', zoom > 1);            // add the class when zoomed, remove it when not
    if (zoom === 1) {
      zoomImage.style.transformOrigin = 'center center';       // back to the middle when reset
    }
  }

  document.getElementById('zoom-in').addEventListener('click', function () {
    zoom = Math.min(MAX_ZOOM, zoom + STEP);                    // +0.5 but never above the maximum
    applyZoom();
  });

  document.getElementById('zoom-out').addEventListener('click', function () {
    zoom = Math.max(MIN_ZOOM, zoom - STEP);                    // -0.5 but never below the minimum
    applyZoom();
  });

  document.getElementById('zoom-reset').addEventListener('click', function () {
    zoom = 1;
    applyZoom();
  });

  zoomFrame.addEventListener('click', function () {            // clicking the picture itself
    zoom = zoom >= MAX_ZOOM ? 1 : zoom + STEP;                 // zoom in a step; after the maximum, go back to normal
    applyZoom();
  });

  zoomFrame.addEventListener('mousemove', function (event) {   // runs while the mouse moves over the frame
    if (zoom === 1) {
      return;                                                  // nothing to move when not zoomed
    }
    const box = zoomFrame.getBoundingClientRect();             // position and size of the frame on screen
    const x = (event.clientX - box.left) / box.width * 100;    // mouse position inside the frame, as a percentage
    const y = (event.clientY - box.top) / box.height * 100;
    zoomImage.style.transformOrigin = x + '% ' + y + '%';      // grow from the point under the mouse
  });
}