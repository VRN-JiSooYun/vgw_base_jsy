$(".fieldset-form-group-login-btn").click((e) => {
    e.preventDefault();
    $.ajax({
        url: '/security/login/',
        type: 'POST',
        data: $('#login-form-1').serialize(),
        success:function(response) {
            console.log(response);

            if (response.result == 'failed') {
                $('#login-form-1').append('<div class="alert alert-warning alert-login-invalid" role="alert">Invalid login info</div>');
                return;
            }

            if (response.form == 'default') {
                window.location.href = response.next == null ? '/member' : response.next;
                return;
            }

            var html = `
                <div class="before">
                    <div class="" style="margin-top: 50px; display: flex; flex-wrap: wrap; justify-content: center; overflow: auto;">
                        <input class="sms-request-btn" type="button" style="margin: 10px; width: 320px; min-width: 320px; height: 50px; text-align: center;" value="인증번호 요청">
                    </div>
                    <div class="time-left" style="margin-top: 50px; display: flex; flex-wrap: wrap; justify-content: center; overflow: auto; color: rgb(105, 0, 0);">&nbsp;</div>
                
                    <div class="" style="margin-top: 50px; display: flex; flex-wrap: wrap; justify-content: center; overflow: auto;">
                        Please Enter Mobile SMS Code
                    </div>
                    <div class="" style="display: flex; flex-wrap: wrap; justify-content: center; overflow: auto;">
                        <input type="text" style="margin: 10px; width: 320px; min-width: 320px; height: 50px; text-align: center;" name="code" placeholder="SMS Code">
                    </div>
                    <div class="" style="display: flex; flex-wrap: wrap; justify-content: center; overflow: auto;">
                        <input class="sms-verification-btn" type="submit" style="margin: 10px; width: 320px; min-width: 320px; height: 50px; text-align: center;" value="인증하기">
                    </div>
                    <input class="registration" type="text" name="registration" value="" style="display:none">
                </div>
            `;
            $('.fieldset-form-group-login,.fieldset-form-group-login-btn,.alert-login-invalid').hide();
            $('.fieldset-form-group-sns').append(html);
            
            $(".sms-request-btn").click((e) => {
                e.preventDefault();
                $(".sms-request-btn").val("인증번호 발송 중").prop("disabled", true);
                
                $.ajax({
                    url: '/kpviewer/sendNumbers/',
                    type: 'POST',
                    data: $('#login-form-1').serialize(),
                    success: function (response) {
                        console.log(response);
                        $(".sms-request-btn").val("인증번호 발송 완료");

                        var interval = 1000; // ms
                        var expected = Date.now() + interval;
                        setTimeout(step, interval);
                        var total = 60;
                        var second = 0;
                        function step() {
                            var dt = Date.now() - expected; // the drift (positive for overshooting)
                            if (dt > interval) {
                                return;
                            }
                            
                            // console.log(second++);
                            var timeElapse = total - (second++);
                            var minutes = Math.floor(timeElapse / 60);
                            var seconds = timeElapse - minutes * 60;

                            $(".time-left").html(minutes + ":" + (seconds != 0 ? seconds : "00"));
                            if (timeElapse <= 0) {
                                window.location.href = $('.class-next').val() == null ? '/member' : $('.class-next').val();
                                return;
                            }

                            expected += interval;
                            setTimeout(step, Math.max(0, interval - dt)); // take into account drift
                        }

                        if (response.result == 'registered') {
                            $('.registration').val('registered');
                        }
                        else {
                            $('.registration').val('new');
                        }
                        
                    }
                });
            });

            $(".sms-verification-btn").click((e) => {
                e.preventDefault();

                var cookie = getCookie("csrftoken");
                console.log('cookie:', cookie);

                // var csrftoken = Cookies.get('csrftoken');

                $.ajaxSetup({
                    beforeSend: function (xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                            // xhr.setRequestHeader("X-CSRFToken", csrftoken);
                            xhr.setRequestHeader("X-CSRFToken", cookie);
                        }
                    }
                });

                $.ajax({
                    url: '/kpviewer/sns/',
                    type: 'POST',
                    data: $('#login-form-1').serialize(),
                    success: (response) => {
                        console.log(response);
                        if (response.result == 'failed') {
                            $('#login-form-1').append('<div class="alert alert-warning alert-login-invalid" role="alert">Invalid SMS Code</div>');
                            return;
                        }

                        window.location.href = $('.class-next').val() == null ? '/member' : $('.class-next').val();
                    }
                });
            });
        }
    });
});

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
