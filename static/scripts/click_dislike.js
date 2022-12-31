// По нажатию дизлайка уменьшается цифра рейтинга
document.addEventListener('click', ({ target: t }) => {
    if (t.classList.contains('dislike')) {
        const index = [...document.querySelectorAll('.dislike')].indexOf(t);
        const count = document.querySelectorAll('.rate')[index];
        count.innerText -= 1;
    }
});
