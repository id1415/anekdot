// По нажатию лайка увеличивается цифра рейтинга
document.addEventListener('click', ({ target: t }) => {
    if (t.classList.contains('like')) {
        const index = [...document.querySelectorAll('.like')].indexOf(t);
        const count = document.querySelectorAll('.rate')[index];
        count.innerText -= -1;
    }
});