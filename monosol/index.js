var app = new Vue({
    el: '#app',
    data: {
        stage: 'stage1',
        character_presets: {
            "English": "etaoinshrdluwmfcgypbkvjxqz",
            "Romaji": "aiounetksryhmwdgzbpfvq"
        },
        charset_cipher: "",
        charset_plain: "",
        ciphertext: "",
        decryption_table: [],
        rearrange: false,
        rearrange_old_id: undefined,
        rearrange_new_id: undefined,
        mousepos: undefined,
        decryption_table_x_pos: 0,
        decryption_table_item_width: 30
    },
    computed: {
        table_hash: function () {
            let hash = {}
            for (let i = 0; i < this.decryption_table.length; i++) {
                hash[this.decryption_table[i][0]] = this.decryption_table[i][1]
            }
            return hash
        },
        plaintext: function () {
            let text = ""
            for (let i = 0; i < this.ciphertext.length; i++) {
                if (this.ciphertext[i] === '\n') {
                    text += '\n'
                } else {
                    let decrypted = this.table_hash[this.ciphertext[i]]

                    if (decrypted === undefined) {
                        text += ' '
                    } else {
                        text += this.table_hash[this.ciphertext[i]]
                    }
                }
            }
            return text
        }
    },
    watch: {
        mousepos: function (val) {
            this.rearrange_new_id = Math.floor((val[0] - this.decryption_table_x_pos) / this.decryption_table_item_width)
        }
    },
    methods: {
        enable_rearrange_mode: function (id) {
            this.rearrange = true
            this.rearrange_old_id = id
            this.rearrange_new_id = id
        },
        disable_rearrange_mode: function () {
            this.rearrange = false
            let oldi = this.rearrange_old_id;
            let newi = this.rearrange_new_id;
            let table = this.decryption_table;
            if (newi < oldi) {
                let tmp = table[oldi][1]
                for (let i = 0; i < oldi - newi; i++) {
                    table[oldi - i][1] = table[oldi - i - 1][1]
                }
                Vue.set(table[newi], 1, tmp)
            }
            if (oldi < newi) {
                let tmp = table[oldi][1]
                for (let i = 0; i < newi - oldi; i++) {
                    table[oldi + i][1] = table[oldi + i + 1][1]
                }
                Vue.set(table[newi], 1, tmp)
            }
        },
        change_mouse_pos: function (ev) {
            this.mousepos = [ev.clientX, ev.clientY]
        },
        next_stage: function () {
            switch (this.stage) {
                case 'stage1':
                    this.stage = 'stage2'
                    break;
                case 'stage2':
                    this.stage = 'stage3'
                    this.make_decryption_table()
                    break;
            }
        },
        make_decryption_table: function () {
            this.decryption_table = []
            for (let i = 0; i < this.charset_cipher.length; i++) {
                this.decryption_table.push([this.charset_cipher[i], this.charset_plain[i] || ' '])
            }
        },
    }
})

document.getElementById("app").style.display = "block"