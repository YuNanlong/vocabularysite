$(document).ready(function () {
    /*** Retina Image Loader ***/
    if ($.fn.unveil) {
        $("img").unveil();
    }

    /**** Scroller ****/
    if ($.fn.niceScroll) {
        var mainScroller = $("html").niceScroll({
            zindex: 999999,
            boxzoom: true,
            cursoropacitymin: 0.5,
            cursoropacitymax: 0.8,
            cursorwidth: "10px",
            cursorborder: "0px solid",
            autohidemode: false
        });
    }

    /**** Carousel for Testominals ****/
    if ($.fn.owlCarousel) {
        $("#testomonials").owlCarousel({
            singleItem: true
        });
    }

    /**** Mobile Side Menu ****/
    if ($.fn.waypoint) {
        var $head = $('#ha-header');
        $('.ha-waypoint').each(function (i) {
            var $el = $(this),
                animClassDown = $el.data('animateDown'),
                animClassUp = $el.data('animateUp');

            $el.waypoint(function (direction) {
                if (direction === 'down' && animClassDown) {
                    $head.attr('class', 'ha-header ' + animClassDown);
                }
                else if (direction === 'up' && animClassUp) {
                    $head.attr('class', 'ha-header ' + animClassUp);
                }
            }, { offset: '100%' });
        });
    }
    /**** Revolution Slider ****/
    if ($.fn.revolution) {
        revapi = $('#home').revolution(
            {
                delay: 15000,
                startwidth: 1170,
                startheight: 500,
                hideThumbs: 10,
                fullWidth: "off",
                fullScreen: "on",
                navigationType: "none",
                fullScreenOffsetContainer: "",
                touchenabled: "on",
                videoJsPath: "assets/plugins/rs-plugin/videojs/"
            });

    }


    /**** Appear JS ****/
    if ($.fn.appear) {
        $('[data-ride="animated"]').appear();
        if (!$('html').hasClass('ie no-ie10')) {
            $('[data-ride="animated"]').addClass('appear');
            $('[data-ride="animated"]').on('appear', function () {
                var $el = $(this), $ani = ($el.data('animation') || 'fadeIn'), $delay;
                if (!$el.hasClass('animated')) {
                    $delay = $el.data('delay') || 0;
                    setTimeout(function () {
                        $el.removeClass('appear').addClass($ani + " animated");
                    }, $delay);
                }
            });
        };
        $('.number-animator').appear();
        $('.number-animator').on('appear', function () {
            $(this).animateNumbers($(this).attr("data-value"), true, parseInt($(this).attr("data-animation-duration")));
        });

        $('.animated-progress-bar').appear();
        $('.animated-progress-bar').on('appear', function () {
            $(this).css('width', $(this).attr("data-percentage"));
        });
    }

    /**** Animate Numbers ****/
    if ($.fn.animateNumbers) {
        $('.animate-number').each(function () {
            $(this).animateNumbers($(this).attr("data-value"), true, parseInt($(this).attr("data-animation-duration")));
        })
    }

    $('.animate-progress-bar').each(function () {
        $(this).css('width', $(this).attr("data-percentage"));

    })

    if ($("#thumbs").length > 0) {
        var $container = $('#thumbs');
        $container.isotope({
            filter: '*',
            animationOptions: {
                duration: 750,
                easing: 'linear',
                queue: false
            }
        });

        $(window).resize(function () {
            var $container = $('#thumbs');
            $container.isotope({
                itemSelector: '.item',
                animationOptions: {
                    duration: 250,
                    easing: 'linear',
                    queue: false
                }
            });
        });


        // filter items when filter link is clicked
        $('#portfolio-nav a, #gallery-nav a').click(function () {
            var selector = $(this).attr('data-filter');
            $container.isotope({ filter: selector });

            $("#portfolio-nav li, #gallery-nav li").removeClass("current");
            $(this).closest("li").addClass("current");

            return false;
        });
    }



    $(".portfolio-grid ul li").hover(function () {
        var imgHeight = $(this).find("img").height();
        $(this).find(".portfolio-image-wrapper").height(imgHeight);

    });

    $('#button-send').click(function (event) {
        $('#button-send').html('Sending E-Mail...');
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: 'send_form_email.php',
            data: $('#contact_form').serialize(),
            success: function (html) {
                if (html.success == '1') {
                    $('#button-send').html('Send');
                    $('#success').show();
                }
                else {
                    $('#button-send').html('Send');
                    $('#error').show();
                }
            },
            error: function () {
                $('#button-send').html('Send');
                $('#error').show();
            }
        });

    });

});

/* 获取cookie */

function getCookie(name) {
    var cookie_value = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_value;
}

/* 模态框 */

$("#logout-btn").click(function () {
    $.ajax({
        url: "/accounts/logout",
        type: "GET",

        success: function (e) {
            window.location.href = "/recite/home";
        }
    });
});

$("#login-btn").click(function () {
    var username = $("#loginform-username-input").val();
    var password = $("#loginform-password-input").val();
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: "/accounts/login",
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrftoken,
            "username": username,
            "password": password,
        },

        success: function (json) {
            if (json['status'] == 'success') {
                $('#modal-container-login').modal('hide');
                window.location.reload();
            }
            else if (json['status'] == 'fail') {
                $('#loginform-password-feedback').html(json['error_message']);
                $('#loginform-password-feedback').show();
                $('#loginform-password-input').addClass('is-invalid');
            }
        }
    });
});

$("#signup-btn").click(function () {
    var username = $("#signupform-username-input").val();
    var password1 = $("#signupform-password1-input").val();
    var password2 = $("#signupform-password2-input").val();
    var email = $("#signupform-email-input").val();
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: "/accounts/signup",
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrftoken,
            "username": username,
            "password1": password1,
            "password2": password2,
            "email": email,
        },

        success: function (json) {
            if (json['status'] == 'success') {
                $('#modal-container-signup').modal('hide');
                window.location.reload();
            }
            switch (json['field']) {
                case 'username':
                    $('#signupform-username-feedback').html(json['error_message']);
                    $('#signupform-username-feedback').show();
                    $('#signupform-username-input').addClass('is-invalid');
                    break;
                case 'password1':
                    $('#signupform-password1-feedback').html(json['error_message']);
                    $('#signupform-password1-feedback').show();
                    $('#signupform-password1-input').addClass('is-invalid');
                    break;
                case 'password2':
                    $('#signupform-password2-feedback').html(json['error_message']);
                    $('#signupform-password2-feedback').show();
                    $('#signupform-password2-input').addClass('is-invalid');
                    break;
                case 'email':
                    $('#signupform-email-feedback').html(json['error_message']);
                    $('#signupform-email-feedback').show();
                    $('#signupform-email-input').addClass('is-invalid');
                    break;
            }
        }
    });
});

$("#learnset-btn").click(function () {
    var daily_task_amount = $("#learnsetform-dailytaskamount-input").val();
    var exam_amount = $("#learnsetform-examamount-input").val();
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: "/accounts/setting",
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrftoken,
            "daily-task-amount": daily_task_amount,
            "exam-amount": exam_amount,
            "learn-set": "",
        },

        success: function (json) {
            if (json['status'] == 'success') {
                $('#modal-container-learn-set').modal('hide');
                window.location.reload();
            }
            switch (json['field']) {
                case 'dailytaskamount':
                    $('#learnsetform-dailytaskamount-feedback').html(json['error_message']);
                    $('#learnsetform-dailytaskamount-feedback').show();
                    $('#learnsetform-dailytaskamount-input').addClass('is-invalid');
                    break;
                case 'examamount':
                    $('#learnsetform-examamount-feedback').html(json['error_message']);
                    $('#learnsetform-examamount-feedback').show();
                    $('#learnsetform-examamount-input').addClass('is-invalid');
                    break;
            }
        }
    });
});

$("#profileset-btn").click(function () {
    var username = $("#profilesetform-username-input").val();
    var password1 = $("#profilesetform-password1-input").val();
    var password2 = $("#profilesetform-password2-input").val();
    var email = $("#profilesetform-email-input").val();
    var csrftoken = getCookie("csrftoken");
    $.ajax({
        url: "/accounts/setting",
        type: "POST",
        data: {
            "csrfmiddlewaretoken": csrftoken,
            "username": username,
            "password1": password1,
            "password2": password2,
            "email": email,
            "personal-set": "",
        },

        success: function (json) {
            if (json['status'] == 'success') {
                $('#modal-container-profile-set').modal('hide');
                window.location.reload();
            }
            switch (json['field']) {
                case 'username':
                    $('#profilesetform-username-feedback').html(json['error_message']);
                    $('#profilesetform-username-feedback').show();
                    $('#profilesetform-username-input').addClass('is-invalid');
                    break;
                case 'password1':
                    $('#profilesetform-password1-feedback').html(json['error_message']);
                    $('#profilesetform-password1-feedback').show();
                    $('#profilesetform-password1-input').addClass('is-invalid');
                    break;
                case 'password2':
                    $('#profilesetform-password2-feedback').html(json['error_message']);
                    $('#profilesetform-password2-feedback').show();
                    $('#profilesetform-password2-input').addClass('is-invalid');
                    break;
                case 'email':
                    $('#profilesetform-email-feedback').html(json['error_message']);
                    $('#profilesetform-email-feedback').show();
                    $('#profilesetform-email-input').addClass('is-invalid');
                    break;
            }
        }
    });
});
