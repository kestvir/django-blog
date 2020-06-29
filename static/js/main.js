$(document).ready(function () {

    // reply to comments
    $(".reply-form-toggle").click(function () {
        $($(this).closest(".row").find("~form")[0]).toggle();
    });

    // rich text editor size
    $(".django-ckeditor-widget").css({ "display": "block" });

});
