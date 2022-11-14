/**
 * Cookie handling functions
 */


/**
 * Set a cookie.
 * @param {String} name 
 * @param {String} value 
 * @param {Number} days 
 */
var createCookie = function(name, value, days=365) {
    var expires;
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toGMTString();
    }
    else {
        expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

/**
 * Read a cookie.
 * @param {String} c_name 
 * @returns the contents of the cookie, or ""
 */
function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}



/**
 * Event Handlers
 */



/**
 * Handle the click of a filter button.
 * @param {Event} e 
 */
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
        // show all resorts
        allResorts = document.querySelectorAll('.fcst-sum');
        allResorts.forEach(resort => {
            resort.classList.add('showing');
            resort.classList.remove('hidden');
        });
    } else if(e.target.textContent == 'Favorites') {
        // show the favorite resorts
        const favResorts = document.querySelectorAll('div[data-favorite="1"');
        favResorts.forEach(resort => {
           resort.classList.add('showing');
           resort.classList.remove('hidden'); 
        });
        const nonFavResorts = document.querySelectorAll('div[data-favorite="0');
        nonFavResorts.forEach(nonFav => {
            nonFav.classList.add('hidden');
            nonFav.classList.remove('showing');
        });
    }
    inactivateButtons();
    e.target.classList.add('con-fltr-btn-active');
    e.target.classList.remove('con-fltr-btn-inactive');
};


/**
 * Inactivate all of the filter buttons.
 * @returns nothing
 */
function inactivateButtons() {
    buttons = Array.from(document.querySelectorAll('button'));
    buttons.forEach(button => {
        button.classList.remove('con-fltr-btn-active');
        button.classList.add('con-fltr-btn-inactive');
    });
    return;
};


/**
 * Handle the favorite click event.
 * @param {Event} e 
 */
function favoriteClick(e) {
    // get the selected resort
    selected_resort = e.target.dataset.resort;

    // update the cookie
    toggleFavoriteCookie(selected_resort);

    // update the favorite icon
    toggleFavoriteIcon(e.target);

    // update the forecast summary div
    toggleForecastSummary(selected_resort);
    

};


/**
 * Update the favorite status of the Forecast Summary div.
 * @param {String} selected_resort 
 */
function toggleForecastSummary(selected_resort) {
    const fcstSum = document.querySelector('div[data-resort="'+selected_resort+'"');
    favoriteValue = fcstSum.dataset.favorite;
    if(favoriteValue == "0") {
        fcstSum.dataset.favorite = "1";
    } else {
        fcstSum.dataset.favorite = "0";
    }
};

/**
 * Add or remove the resort from the favorites cookie.
 * @param {String} selected_resort 
 */
function toggleFavoriteCookie(selected_resort) {
    let json_str = getCookie('favorites');
    let favorites = [];
    if(json_str == "") { // there is no cookie
        favorites.push(selected_resort);
        json_str = JSON.stringify(favorites);
        createCookie('favorites', json_str);
    } else { // there is a cookie
        json_str = getCookie('favorites');
        favorites = JSON.parse(json_str);
        if(favorites.includes(selected_resort)) { // this is already a favorite
            // remove the favorite
            const index = favorites.indexOf(selected_resort);
            if(index > -1) {
                favorites.splice(index, 1);
            }
        } else { // this is not already a favorite
            favorites.push(selected_resort);
        }
        // re-write the cookie
        json_str = JSON.stringify(favorites);
        createCookie('favorites', json_str);
    }
};

/**
 * Fill or Un-Fill the favorite icon.
 * @param {Element} button 
 */
function toggleFavoriteIcon(button) {
    star = button.querySelector('#star');
    starFill = button.querySelector('#star-fill');

    if(star.classList.contains('showing')) {
        star.classList.remove('showing');
        star.classList.add('hidden');
    
        starFill.classList.remove('hidden');
        starFill.classList.add('showing');
    } else {
        star.classList.remove('hidden');
        star.classList.add('showing');
    
        starFill.classList.remove('showing');
        starFill.classList.add('hidden');
    }
};

/**
 * Initialize the favorites based on the cookie.
 * @returns nothing
 */
function initFavorites() {
    const json_str = getCookie('favorites');
    if(json_str == "") {
        return;
    } else {
        const favorites = JSON.parse(json_str);
        favorites.forEach(fav => {
            favBtn = document.querySelector('button[data-resort="'+fav+'"');
            toggleFavoriteIcon(favBtn);
            fcstSum = document.querySelector('div[data-resort="'+fav+'"');
            fcstSum.dataset.favorite = "1";
        });
    }
}

/**
 * Register the filter button event listeners
 */

allBtn = document.querySelector('#all-fltr-btn');
allBtn.addEventListener('click', filterClick);

openBtn = document.querySelector('#open-fltr-btn');
openBtn.addEventListener('click', filterClick);

favBtn = document.querySelector('#fav-fltr-btn');
favBtn.addEventListener('click', filterClick);


/**
 * register the favorite star event listeners
 */

stars = Array.from(document.querySelectorAll('.fav-btn'));
stars.forEach(star => {
    star.addEventListener('click', favoriteClick);
});


/**
 * Initialize the favorites in the UI from the cookie.
 */
initFavorites();