// функция срабатывает по пользовательскому клику
$(".like").click(function () {
    const elem = this.id;  // id элемента
    $.ajax({
        url:'/',
        type:'POST',
        data:{'like': elem, 'dislike': ''},  // эти данные передаются в index.index
    });
    
    this.disabled=true;  // кнопка становится неактивной
})