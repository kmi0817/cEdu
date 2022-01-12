const logo = {
    view: "button", type: "image",
    image: "../static/cEdu_logo.png",
    width: 200,
    css: "webix_transparent"
}

const top_toolbar = {
    view: "toolbar",
    borderless: true,
    elements: [
        {
            align: "right", body: {
                cols: [
                    {
                        view: "button", value: "로그인",
                        width: 100,
                        click: () => {
                            webix.message("로그인");
                        }
                    },
                    {
                        view: "button", value: "회원가입",
                        width: 100,
                        click: () => {
                            webix.message("회원가입");
                        }
                    },
                    {
                        view: "button", value: "고객선거",
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
    align: "center",
    body: {
        view: "toolbar",
        borderless: true,
        elementsConfig: {
            autowidth: true,
            minWidth: 120,
        },
        elements: [
            {
                id: "hello", view: "button", label: "지식 거래 장터 소개"
            },
            {
                id: "peer-feedback", view: "button", label: "동료평가", popup: "peer_feedback_popup"
            },
            {
                id: "auction", view: "button", value: "옥션",
            },
            {
                id: "market", view: "button", value: "마켓"
            },
            {
                id: "odi", view: "button", value: "ODI"
            },
            {
                id: "idea", view: "button", value: "아이디어 장터"
            },
            {
                id: "NFT", view: "button", value: "NFT 생성"
            }
        ]
    }
}

// webix.ui({
//     view: "popup", id: "peer_feedback_popup",
//     scroll: "disable",
//     body: {
//         view: "list",
//         data: [
//             {
//                 id: "register/specialists", value: "전문가 등록"
//             },
//             {
//                 id: "apply/intellectual-asset", value: "지식자산 평가 신청"
//             },
//             {
//                 id: "evaluation-results", value: "평가결과 공개"
//             },
//             {
//                 id: "select/intellctual-asset", value: "지식자산 선별"
//             }
//         ]
//     }
// });

const main_menu2 = {
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
                    id: "apply/intellectual-asset", value: "지식자산 평가 신청"
                },
                {
                    id: "evaluation-results", value: "평가결과 공개"
                },
                {
                    id: "select/intellctual-asset", value: "지식자산 선별"
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
            id: "idea", value: "아이디어 장터", submenu: [
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
            id: "NFT", value: "NFT 생성"
        }
    ],
    on: {
        onMenuItemClick: (id) => {
            webix.message(id);
        }
    }
}

const before_login_header = {
    cols: [
        logo,
        {
            rows: [
                top_toolbar,
                {
                    view: "spacer", height: 30
                },
                main_menu2
            ]
        }
    ]
}