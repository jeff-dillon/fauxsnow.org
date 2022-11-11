function filterClick(e) {
    if(e.target.textContent == 'Open') {
        // hide the closed results
        openResorts = document.querySelectorAll('div[data-open="0"');
        openResorts.forEach(resort => {
            resort.classList.add('hidden');
            resort.classList.remove('showing');
        });
        // show the open results
         openResorts = document.querySelectorAll('div[data-open="1"');
        openResorts.forEach(resort => {
            resort.classList.add('showing');
            resort.classList.remove('hidden');
        });
    } else if(e.target.textContent == 'All') {
        allResorts = document.querySelectorAll('.resort-box');
        allResorts.forEach(resort => {
            resort.classList.add('showing');
            resort.classList.remove('hidden');
        });
    }
    inactivateButtons();
    e.target.classList.add('content-header-button-active');
    e.target.classList.remove('content-header-button-inactive');
};

function inactivateButtons() {
    buttons = Array.from(document.querySelectorAll('button'));
    buttons.forEach(button => {
        button.classList.remove('content-header-button-active');
        button.classList.add('content-header-button-inactive');
    });
};


allBtn = document.querySelector('#all-btn');
allBtn.addEventListener('click', filterClick);

openBtn = document.querySelector('#open-btn');
openBtn.addEventListener('click', filterClick);

favBtn = document.querySelector('#fav-btn');
favBtn.addEventListener('click', filterClick);
