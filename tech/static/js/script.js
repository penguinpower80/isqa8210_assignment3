jQuery(document).ready(function($){
    $(document).on('click', '.notification.non_field_form_error .delete', function(){
        $(this).parent().slideUp(250, function(){
            $(this).remove();
        })
    })
})