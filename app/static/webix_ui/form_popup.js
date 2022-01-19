// without webix.ready(() => {}), index.html fails to load this webix ui
webix.ready(() => {
    webix.ui({
        id: "login_popup",
        view: "window",
        modal: true,
        move: true,
        position: "center",
        head: "로그인",
        body: {
            view: "form", id: "login_form",
            width: 400,
            elements: [
                {
                    view: "text",
                    label: "이메일",
                    name: "email",
                    invalidMessage: "이메일을 입력하세요."
                },
                {
                    view: "text",
                    type: "password",
                    label: "비밀번호",
                    name: "password",
                    invalidMessage: "비밀번호를 입력하세요."
                },
                {
                    cols: [
                        {
                            view: "button", value: "확인",
                            hotkey: "enter",
                            css: "webix_primary",
                            click: () => {
                                var form = $$("login_form");
                                if (form.validate()) {
                                    var values = form.getValues();
                                    webix.ajax().post("/loginout", JSON.stringify(values))
                                        .then((res) => {
                                            var response = res.text();
                                            if (response == "login successful") {
                                                $$("login_popup").hide();
                                                location.href = "/";
                                            } else {
                                                webix.message({ type: "error", text: "일치하는 회원 정보가 없습니다." });
                                            }
                                        })
                                }
                            }
                        },
                        {
                            view: "button", value: "취소", click: () => {
                                $$("login_popup").hide();
                            }
                        }
                    ]
                }
            ],
            rules: {
                "email": webix.rules.isEmail,
                "password": webix.rules.isNotEmpty
            }
        }
    });

    webix.ui({
        id: "signup_popup",
        view: "window",
        modal: true,
        move: true,
        position: "center",
        head: "회원가입",
        body: {
            view: "form", id: "signup_form",
            width: 400,
            elements: [
                {
                    view: "text",
                    label: "이메일",
                    name: "email",
                    invalidMessage: "이메일을 입력하세요."
                },
                {
                    view: "text",
                    type: "password",
                    label: "비밀번호",
                    name: "password",
                    invalidMessage: "비밀번호를 입력하세요."
                },
                {
                    cols: [
                        {
                            view: "button", value: "확인",
                            hotkey: "enter",
                            css: "webix_primary",
                            click: () => {
                                var form = $$("signup_form");
                                if (form.validate()) {
                                    var values = form.getValues();
                                    webix.ajax().post("/users", JSON.stringify(values))
                                        .then((res) => {
                                            var response = res.text();
                                            if (response == 'duplicated') {
                                                webix.message({ type: "debug", text: "사용할 수 없는 이메일입니다." });
                                            } else if (response == 'signup successful') {
                                                $$("signup_popup").hide();
                                                location.href="/";
                                            } else {
                                                webix.message({ type: "error", text: "회원가입에 문제가 발생했습니다." });
                                            }
                                        })
                                }
                            }
                        },
                        {
                            view: "button", value: "취소", click: () => {
                                $$("signup_popup").hide();
                            }
                        }
                    ]
                }
            ],
            rules: {
                "email": webix.rules.isEmail,
                "password": webix.rules.isNotEmpty
            }
        }
    });
});