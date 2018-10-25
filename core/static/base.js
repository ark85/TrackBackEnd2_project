// $(document).ready(function () {
//     $('.likescount').each(function () {
//         $(this).load($(this).data('likes-url'))
//     })
// });

$(document).ready(
    function () {



        $("#category-new-a").click(function () {
            $("#category-new-content").load(this.href);
            $("#category-new-modal").popover('show');
            return false;
        });

        $(".submit-creation").on('click', function () {
            $("#category-new-modal").popover('hide');
            return false;
        });

        $(document).on("submit", ".ajaxform", function () {
            $.post(
                $(this).data('url'),
                $(this).serialize()
            );
            return false;
        })

    }
);