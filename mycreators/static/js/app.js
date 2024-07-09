document.addEventListener('DOMContentLoaded', function () {
    let items = document.querySelectorAll('.slider .item');
    let next = document.getElementById('next');
    let prev = document.getElementById('prev');

    let active = 0; // Set the initial active item to 1

    function loadShow() {
        let stt = 0;
        console.log("Active item index:", active);
        // Ensure all items are reset
        items.forEach(item => {
            item.style.transform = '';
            item.style.zIndex = '';
            item.style.filter = '';
            item.style.opacity = '';

        });
        console.log(`Item ${active} set as active`);
        // Set the active item
        items[active].style.transform = `none`;
        items[active].style.zIndex = 1;
        items[active].style.filter = 'none';
        items[active].style.opacity = 1;
        console.log(`Item ${active} set as active`);

        // Set the items after the active item
        for (var i = active + 1; i < items.length; i++) {
            stt++;
            items[i].style.transform = `translateX(${120 * stt}px) scale(${1 - 0.2 * stt}) perspective(16px) rotateY(-1deg)`;
            items[i].style.zIndex = -stt;
            items[i].style.filter = 'blur(5px)';
            items[i].style.opacity = stt > 2 ? 0 : 0.6;
            console.log(`Item ${i} positioned to the right: translateX(${120 * stt}px)`);
        }

        // Reset stt for items before the active item
        stt = 0;
        for (var i = active - 1; i >= 0; i--) {
            stt++;
            items[i].style.transform = `translateX(${-120 * stt}px) scale(${1 - 0.2 * stt}) perspective(16px) rotateY(1deg)`;
            items[i].style.zIndex = -stt;
            items[i].style.filter = 'blur(5px)';
            items[i].style.opacity = stt > 2 ? 0 : 0.6;
            console.log(`Item ${i} positioned to the left: translateX(${-120 * stt}px)`);
        }
    }

    loadShow();

    next.onclick = function () {
        active = active + 1 < items.length ? active + 1 : active;
        console.log("Next button clicked. New active item index:", active);
        loadShow();
    }

    prev.onclick = function () {
        active = active - 1 >= 0 ? active - 1 : active;
        console.log("Previous button clicked. New active item index:", active);
        loadShow();
    }
});
