// в цикле классам like и dislike присваиваются id из списка lst
// знаю что на странице не должно быть элементов с одинаковым id, но пока так
for (var i = 0; i < 11; i++) {
    document.getElementsByClassName("like")[i].id = lst[i];
    document.getElementsByClassName("dislike")[i].id = lst[i];
    };
