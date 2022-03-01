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

function msg(text, type) {
    if (typeof type == 'undefined') type = 'success'
    Toast.fire({
        icon: type,
        title: text,
    })
}

async function timeMessage(jobid, timeid) {
    const {value: text} = await Swal.fire({
        customClass: {
            confirmButton: 'button is-primary',
            cancelButton: 'button is-danger'
        },
        input: 'textarea',
        inputLabel: 'Message',
        inputPlaceholder: 'Type your message here...',
        inputAttributes: {
            'aria-label': 'Type your message here'
        },
        showCancelButton: true
    })

    if (text) {
        jQuery.post('ajax/addtimecomment/' + jobid + '/' + timeid, {
            text: text,
            csrfmiddlewaretoken: csrftoken
        }, function (data) {
            msg('Time comment added!')
            if ($('#time_' + timeid).find('.card-content').length) {
                $('#time_' + timeid).find('.card-content .content').text(text)
            } else {
                $('#time_' + timeid).find('.card-header').after('<div class="card-content"><div class="content">' + text + '</div></div>');
            }

        }).always(function () {
        }).fail(function (d) {
            if (d.status == 401) {
                parent.location = '/accounts/login/'
            } else {
                msg('There was an error adding this comment. Please try again later.', 'error')
            }
        })
    }
}

async function selectorPopup(title, choices, value, callback) {
    const {value: choice} = await Swal.fire({
        customClass: {
            confirmButton: 'button is-primary',
            cancelButton: 'button is-danger'
        },
        title: 'Select Job Status',
        input: 'select',
        inputValue: value,
        inputOptions: choices,
        inputPlaceholder: 'Select a ' + title.toLowerCase(),
        showCancelButton: true,

    })

    if (choice) {
        callback(choice)
    }
}

function updatejob(jobid, element, value) {
    jQuery.post('ajax/updatejob/' + jobid, {
        element: element,
        value: value,
        csrfmiddlewaretoken: csrftoken
    }, function (data) {
        if (element != '') {
            msg('Job Updated!')
        }
        $('#job_' + jobid).replaceWith(data);
    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            parent.location = '/accounts/login/'
        } else {
            msg('There was an error updating this job. Please try again later.', 'error')
        }
    })
}

function updatepart(jobid, partid, element, value) {
    jQuery.post('ajax/updatepart/' + jobid + '/' + partid, {
        element: element,
        value: value,
        csrfmiddlewaretoken: csrftoken
    }, function (data) {
        msg('Part Updated!')
        $('#jobpart_' + partid).replaceWith(data);

        updatejob(jobid, '', '')

    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            parent.location = '/accounts/login/'
        } else {
            msg('There was an error updating this part. Please try again later.', 'error')
        }
    })
}

function closeVisibleQuickview() {
    $('[data-dismiss="quickview"]:visible').trigger('click')
}

jQuery(document).ready(function ($) {

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

    $(document).on('click', '#togglepartslist', function (e) {
        var $button = $(this);
        let v = $('#parts_list').is(':visible');
        if (v) {
            $button.find('.list_visiblity_label').text('Show Available Parts')

        } else {
            $button.find('.list_visiblity_label').text('Hide Available Parts')
        }
        $('#parts_list').slideToggle(250)
        $(this).find('.fas').toggleClass('fa-caret-right fa-caret-down')

    })

    $(document).on('click', '.partadd', function (e) {
        let $myButton = $(this)
        let myData = $myButton.data();
        $myButton.prop('disabled', true)
        jQuery.get('ajax/addpart/' + myData.jobid + '/' + myData.partid, function (data) {
            msg('Part Added!')
            $('.nopartsmessage').remove();
            $('#jobparts').append(data)
        }).always(function () {
            $myButton.prop('disabled', false)
        }).fail(function (d) {
            if (d.status == 401) {
                parent.location = '/accounts/login/'
            } else {
                msg('There was an error adding the part. Please try again later.', 'error')
            }
        })
    })

    $(document).on('click', '.partremove', function (e) {
        let $myButton = $(this)
        let myData = $myButton.data();
        Swal.fire({
            customClass: {
                confirmButton: 'button is-primary',
                cancelButton: 'button is-danger'
            },
            title: 'Are you sure?',
            text: 'This will permanently delete this part from the job.',
            icon: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Keep It',
            confirmButtonText: 'Remove It'
        }).then((result) => {
            if (result.isConfirmed) {
                $myButton.prop('disabled', true)
                jQuery.get('ajax/removepart/' + myData.jobid + '/' + myData.jobpartid, function (data) {
                    msg('Part Removed!')
                    $('#jobpart_' + myData.jobpartid).remove()
                }).always(function () {
                    $myButton.prop('disabled', false)
                }).fail(function (d) {
                    if (d.status == 401) {
                        parent.location = '/accounts/login/'
                    } else {
                        msg('There was an error removing the part. Please try again later.', 'error')
                    }
                })
            }
        })
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

    $(document).on('click', '.togglejobtimer', function (e) {
        e.preventDefault()
        let $myButton = $(this)
        $myButton.prop('disabled', true)
        let myData = $myButton.data();
        var action = "start"
        if (myData.active == 1) {
            action = "stop"
        }
        jQuery.get('ajax/' + action + 'time/' + myData.job, function (data) {
            if (myData.active == 0) {
                msg('Timer started.')
                $myButton.removeClass('is-success').addClass('is-danger')
                $myButton.find('.fas').attr('class', 'fas fa-stop')
                $myButton.data('active', 1)
                $myButton.find('.timertext').text('Stop Time')
            } else {
                $myButton.find('.fas').attr('class', 'fas fa-play')
                $myButton.removeClass('is-danger').addClass('is-success')
                $myButton.find('.timertext').text('Start Time')
                msg('Timer stopped.')
                $myButton.data('active', 0)
                updatejob(myData.job, '', '')
            }
        }).always(function () {
            $myButton.prop('disabled', false)
        }).fail(function (d) {
            if (d.status == 401) {
                parent.location = '/accounts/login/'
            } else {
                if (myData.active === "1") {
                    msg('There was an error stopping the timer for this job. Please try again later.', 'error')
                } else {
                    msg('There was an error starting the timer for this job. Please try again later.', 'error')
                }
            }
        })
    })

    $(document).on('click', '.timeremove', function (e) {
        let $myButton = $(this)
        let myData = $myButton.data();
        Swal.fire({
            customClass: {
                confirmButton: 'button is-primary',
                cancelButton: 'button is-danger'
            },
            title: 'Are you sure?',
            text: 'This will permanently delete this time from the job.',
            icon: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Keep It',
            confirmButtonText: 'Remove It'
        }).then((result) => {
            if (result.isConfirmed) {
                $myButton.prop('disabled', true)
                jQuery.get('ajax/removetime/' + myData.jobid + '/' + myData.timeid, function (data) {
                    msg('Time Removed!')
                    $('#time_' + myData.timeid).remove()
                    updatejob(myData.jobid, '', '')
                }).always(function () {
                    $myButton.prop('disabled', false)
                }).fail(function (d) {
                    if (d.status == 401) {
                        parent.location = '/accounts/login/'
                    } else {
                        msg('There was an error removing the time. Please try again later.', 'error')
                    }
                })
            }
        })
    })

    $(document).on('click', '.addtimecomment', function (e) {
        let $myButton = $(this)
        let myData = $myButton.data();
        timeMessage(myData.jobid, myData.timeid)
    })

    $(document).on('change', '.joblevelselector', function (e) {
        let $mySelector = $(this)
        let myData = $mySelector.data();
        updatejob(myData.id, 'level', $mySelector.val())
    })

    $(document).on('change', '.jobstatusselector', function (e) {
        let $mySelector = $(this)
        let myData = $mySelector.data();
        updatejob(myData.id, 'status', $mySelector.val())
    })

    $(document).on('click', '.statusflag', function (e) {
        let $mySelector = $(this)
        let myData = $mySelector.data();
        selectorPopup("Job Status", job_statii, myData.value, function (newvalue) {
            updatejob(myData.jobid, 'status', newvalue)
        })
    })

    $(document).on('click', '.levelflag', function (e) {
        let $mySelector = $(this)
        let myData = $mySelector.data();
        selectorPopup("Job Level", job_levels, myData.value, function (newvalue) {
            updatejob(myData.jobid, 'level', newvalue)
        })
    })

    $(document).on('click', '.partstatusflag', function (e) {
        let $mySelector = $(this)
        let myData = $mySelector.data();
        selectorPopup("Part Status", part_statii, myData.value, function (newvalue) {
            updatepart(myData.jobid, myData.jobpartid, 'status', newvalue)
        })
    })

    $(document).on('click', '.iscustomerappt', function (e) {

        Swal.fire({
            title: '<strong>HTML <u>example</u></strong>',
            icon: 'info',
            html: '<input id="datepicker">',
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            willOpen: function () {
                $('#datepicker').datetimepicker({});
            },
            confirmButtonText:
                '<i class="fa fa-thumbs-up"></i> Great!',
            confirmButtonAriaLabel: 'Thumbs up, great!',
            cancelButtonText:
                '<i class="fa fa-thumbs-down"></i>',
            cancelButtonAriaLabel: 'Thumbs down'
        })
    })
})

