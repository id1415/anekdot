  // функция срабатывает по пользовательскому клику
  $(".dislike").click(function () {
    const elem = this.id;
    $.ajax({
        url:'/',
        type:'POST',
        data:{'like': '', 'dislike': elem},
    });

    this.disabled=true;
})