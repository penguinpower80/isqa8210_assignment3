const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    showCloseButton: true,
    timer: 2000,
    timerProgressBar: true,
    didOpen: (toast) => {
        //toast.addEventListener('mouseenter', Swal.stopTimer)
        //toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

const buttonClass = {
                confirmButton: 'button is-primary',
                cancelButton: 'button is-danger'
            }

function msg(text, type) {
    if (typeof type == 'undefined') type = 'success'
    Toast.fire({
        icon: type,
        title: text,
    })
}

function closeVisibleQuickview() {
    $('[data-dismiss="quickview"]:visible').trigger('click')
}

jQuery(document).ready(function ($) {

    $(document).on('click', '.navbar-burger', function() {

          // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
          $(".navbar-burger").toggleClass("is-active");
          $(".navbar-menu").toggleClass("is-active");

      })

    $(document).on('click', '.notification.non_field_form_error .delete', function () {
        $(this).parent().slideUp(250, function () {
            $(this).remove();
        })
    })

    $(document).on('click', '[data-dismiss="quickview"]', function (e) {
        $(document).off('click', '#maincontent', closeVisibleQuickview)
        $(this).closest('.quickview').removeClass('is-active')
        $('body').css('overflow', 'auto')
    })

    $(document).on('click', '[data-show="quickview"]', function (e) {
        let $myButton = $(this)
        let myData = $myButton.data();

        let $myTarget = $('#' + myData.target);

        if ($myTarget.hasClass('is-active')) {
            $myTarget.find('.quickview-body .quickview-block').html('')
            $myTarget.removeClass('is-active')
            $('body').css('overflow', 'auto')
        } else {
            $('body').css('overflow', 'hidden')
            $myButton.prop('disabled', true)
            let $myIcon = $myButton.parent().find('.icon i');
            let iconClass = $myIcon.attr('class')
            $myIcon.attr('class', 'fas fa-spinner fa-spin')
            jQuery.get('ajax/job' + myData.type + '/' + myData.jobid, function (data) {
                $(document).on('click', '#maincontent', closeVisibleQuickview)
                $myTarget.find('.quickview-body .quickview-block').html(data)
                $myTarget.addClass('is-active')
            }).always(function () {
                $myIcon.attr('class', iconClass)
                $myButton.prop('disabled', false)
            }).fail(function (d) {
                if (d.status == 401) {
                    parent.location = '/accounts/login/'
                } else {
                    msg('There was an error retrieving ' + myData.type + ' data. Please try again later.', 'error')
                }
            })
        }
    })

    $(document).on('change', '.jobstatusfilter, .joblevelfilter', function(){
        $('#filterform').submit()
    })

    $(document).on('click', "#clearsearch", function(){
        $('input.jobsearch').val('')
        $('#filterform').submit()
    })

    $(document).on('click', "#resetsearch", function(){
        $('input.jobsearch').val('')
        $('select.jobstatusfilter').val('')
        $('select.joblevelfilter').val('')
        $('#filterform').submit()
    })

     flatpickr("#id_appointment", {
                    enableTime: true,
                    minuteIncrement: 15,
                    altInput: true,
                    altFormat: "F j, Y h:i K",
                    minDate: "today",
                    position: 'above center',
                });
})

