const logo = {
    view: "button", type: "image",
    image: "../static/cEdu_logo.png",
    width: 200,
    css: "webix_transparent",
    click: () => { location.href="/"; }
}

const before_login_top_toolbar = {
    view: "toolbar",
    borderless: true,
    elements: [
        {
            align: "right", body: {
                cols: [
                    {
                        view: "button", value: "로그인",
                        css: "webix_transparent",
                        width: 100,
                        click: () => {
                            $$("login_popup").show();
                        }
                    },
                    {
                        view: "button", value: "회원가입",
                        css: "webix_transparent",
                        width: 100,
                        click: () => {
                            $$("signup_popup").show();
                        }
                    },
                    {
                        view: "button", value: "고객선거",
                        css: "webix_transparent",
                        width: 100,
                        click: () => {
                            webix.message("고객선거");
                        }
                    }
                ]
            }
        }
    ]
}

const after_login_top_toolbar = {
    view: "toolbar",
    borderless: true,
    elements: [
        {
            align: "right", body: {
                cols: [
                    {
                        view: "button", value: "로그아웃",
                        css: "webix_transparent",
                        width: 100,
                        click: () => {
                            webix.ajax().del("/loginout")
                            .then((res) => {
                                var response = res.text();
                                if (response == "logout successful") {
                                    location.href="/";
                                } else {
                                    webix.message({
                                        type: "error",
                                        text: "문제가 발생했습니다."
                                    });
                                }
                            });
                        }
                    },
                    {
                        view: "button", value: "고객선거",
                        css: "webix_transparent",
                        width: 100,
                        click: () => {
                            webix.message("고객선거");
                        }
                    }
                ]
            }
        }
    ]
}

const main_menu = {
    view: "menu", id: "my_menu",
    type: {
        width: 147,
        height: 50,
    },
    submenuConfig: {
        width: 147
    },
    data: [
        {
            id: "hello", value: "지식 거래 장터 소개"
        },
        {
            id: "peer-feedback", value: "동료평가", submenu: [
                {
                    id: "register/specialists", value: "전문가 등록"
                },
                {
                    id: "intellectual-asset/apply", value: "지식자산 평가 신청"
                },
                {
                    id: "evaluation-results", value: "평가결과 공개"
                },
                {
                    id: "intellectual-asset/select", value: "지식자산 선별"
                }
            ]
        },
        {
            id: "auction", value: "옥션",
        },
        {
            id: "market", value: "마켓"
        },
        {
            id: "odi", value: "ODI"
        },
        {
            id: "idea/market", value: "아이디어 장터", submenu: [
                {
                    id: "idea/challenge", value: "아이디어 도전"
                },
                {
                    id: "idea/basket", value: "아이디어 바구니"
                },
                {
                    id: "idea/community", value: "커뮤니티"
                }
            ]
        },
        {
            id: "nft", value: "NFT 생성"
        }
    ],
    on: {
        onMenuItemClick: (id) => {
            location.href="/" + id;
        }
    }
}

const before_login_header = {
    cols: [
        logo,
        {
            rows: [
                before_login_top_toolbar,
                {
                    view: "spacer", height: 30
                },
                main_menu
            ]
        }
    ]
}

const after_login_header = {
    cols: [
        logo,
        {
            rows: [
                after_login_top_toolbar,
                {
                    view: "spacer", height: 30
                },
                main_menu
            ]
        }
    ]
}