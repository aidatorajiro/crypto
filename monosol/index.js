var app = new Vue({
    el: '#app',
    data: {
        stage: 'stage3',
        character_presets: {
            "English": "etaoinshrdluwmfcgypbkvjxqz",
            "Romaji": "aiounetksryhmwdgzbpfvq"
        },
        charset_cipher: "",
        charset_plain: "",
        decryption_table: [],
        ciphertext: "",
        plaintext: "",
        rearrange: false,
        rearrange_old_id: undefined,
        rearrange_new_id: undefined,
        mousepos: undefined,
        decryption_table_x_pos: 0,
        decryption_table_item_width: 30
    },
    compute: {
        table_hash: function () {
            let hash = {}
            for (let i = 0; i < app.decryption_table.length; i++) {
                hash[app.decryption_table[i][0]] = app.decryption_table[i][1]
            }
            return hash
        }
    },
    watch: {
        mousepos: function (val) {
            app.rearrange_new_id = Math.floor((val[0] - app.decryption_table_x_pos) / app.decryption_table_item_width)
        },
        decryption_table: function () {
            app.plaintext = ""
        }
    },
    methods: {
        enable_rearrange_mode: function (id) {
            app.rearrange = true
            app.rearrange_old_id = id
            app.rearrange_new_id = id
        },
        disable_rearrange_mode: function () {
            app.rearrange = false
            let oldi = app.rearrange_old_id;
            let newi = app.rearrange_new_id;
            let table = app.decryption_table;
            if (newi < oldi) {
                let tmp = table[oldi][1]
                for (let i = 0; i < oldi - newi; i++) {
                    table[oldi - i][1] = table[oldi - i - 1][1]
                }
                table[newi][1] = tmp
            }
            if (oldi < newi) {
                let tmp = table[oldi][1]
                for (let i = 0; i < newi - oldi; i++) {
                    table[oldi + i][1] = table[oldi + i + 1][1]
                }
                table[newi][1] = tmp
            }
        },
        change_mouse_pos: function (ev) {
            app.mousepos = [ev.clientX, ev.clientY]
        },
        next_stage: function () {
            switch (app.stage) {
                case 'stage1':
                    app.stage = 'stage2'
                    break;
                case 'stage2':
                    app.stage = 'stage3'
                    app.make_decryption_table()
                    break;
            }
        },
        make_decryption_table: function () {
            for (let i = 0; i < app.charset_cipher.length; i++) {
                app.decryption_table.push([app.charset_cipher[i], app.charset_plain[i] || ' '])
            }
        }
    }
})

app.charset_cipher="e0!9f61>asy/wm;,p&?.hqz[]=*d()-ujt"
app.charset_plain="aiounetksryhmwdgzbpfvq"
app.cyphertext="6/e96>1e9!0weq!/efe>1,ef!ys0s,\n0w6sf6q9!?60?60f,0w!/efe&090w;\n6/6>1e&!>10f6/em009!e>1as;\nep090w!efe&aef0w!90f!y6/6>16sf0ma/0s,\n0w!9!/efe&090w,ey0f0>16>1!afa!>1,\n6>1e90w0f0>16/0?109!9e>1e909e>1a/ep;\n6w0f0w0me>1!e>109[!/!e>1!as9a];\n6w0s090m!yese09[6?60?60s66>1];\n60/6p6f!/efe>1!99a!aaf!ysez0f!99a!a,\n0me/!q0f09em!90>1eyeffem0f09!>10f;\n60h>160s!/ef!ys9e>10m!ep6w;\n60f096>10p0>1090?09e>1!>1e90we9;\n!/efe&090w!>1e90we9!e909!aw!epepew;\n...ey!>10f090s6sfa>1em0m0f0wef,\neqe/e96/eapew6>1e0f!ys9af,\neqe/e96/a0fefe&!ysefem0fefe6e;\n!9!>10f090s6eap!qef!w;\nef!afawam!>10m9af90p,\ney0/0>10>09(!ysefem)0?09e>1;\n!s!a/!d9ey0f66h>190s09!/!&e>16sefem!m...\n!e960h6f!yaf9e9ef!yse;\n!e9eyap60?!ef,\ne960h09e/0?09e>1e/a/e>1,\ney!ys09!ysefem;\neffe>1em0>16>1e90w6sfaf0fe&6f!?!?090s;\nafa/es!ay66h!960f0999e6y,\neffe&e!w6sf6>1e>1f6s6...\neffe>1ef!ef!ysae>1!/6>1,\n0m9e>1!?!?e90!99a!a;\nef!ys!90f0>16/6s60z60s0m!e>1as,\n!/0f!9ef0m[0f-09]0f[9ad]!qefef6ye/e>1ep;\ne/e>1ep!e>1as09!ysefem,\ne&a>1epap!0w00f60s66>1;\ne/e>1!e9e&0hseq!0996q!?e>1!ys!90>10>1;\neqa/a>1e9aw0f!>1asap60s!e>190h!ep,\ney60s60q09!ysefem090>1e>1;\n!eua/e/aefeyew!\ney096>10&60e9!yse>1!ys,\ne&60h&9!9!/6sfeheeha/!>1090f!\nj...e960h!!ysa/6a>1ep!ys0?16s,0wap;\ne9e>1096/!af!ys60ffe>1,\nap90h0!90&090>1ey!ysefem...\nepe/e>1!e9yap[/af=e/ey=***];\ney!yaefem,eya/0s;e>1aze9,\n!e9e&aewe9ey!9!ysefem;\nepe/e>16/!af!ss0ye&0?09e>1,\n0m!ez90s09!ysetem,eya/0s;e>1aze9;\n6/!ap!ys!ez90s,ey!ysefem,e&ep;\nafa/6>1af!>1aff0p0w,efew.60fe&!/e;\n60yaw!?ey0p!y=!60w,0m!/efe&090w!!yse/efe;\n9m09>196"
app.make_decryption_table()

document.getElementById("app").style.display = "block"