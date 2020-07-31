// string format
String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k]);
    }
    return a;
};

function get_cookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(";");
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function change_water(per) {
    $("#water").css("height", "{0}%".format(per.toString()));
    $("#water_percentage").text(per);
}

function aes_encrypt(plaintext, key, iv) {
    key = CryptoJS.enc.Utf8.parse(key);
    iv = CryptoJS.enc.Utf8.parse(iv);
    let srcs = CryptoJS.enc.Utf8.parse(plaintext);
    let encrypted = CryptoJS.AES.encrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
    });
    return encrypted.ciphertext.toString();
}

function aes_decrypt(ciphertext, key, iv) {
    key = CryptoJS.enc.Utf8.parse(key);
    iv = CryptoJS.enc.Utf8.parse(iv);
    let hex_string = CryptoJS.enc.Hex.parse(ciphertext);
    let srcs = CryptoJS.enc.Base64.stringify(hex_string);
    let decrypt = CryptoJS.AES.decrypt(srcs, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7,
    });
    decrypt = decrypt.toString(CryptoJS.enc.Utf8);
    return decrypt.toString();
}

$(function () {
    $("#submit_btn").on("click", function (event) {
        $.ajax({
            type: "POST",
            url: "/HMIquery",
            async: false,
            data: {
                HMIquery: $("#input_bar").val(),
                jwttoken: get_cookie("supersecretKey"),
            },
            success: function (data) {
                console.log("IV", data.IV);
                console.log("Cipher", data.cipher);
                console.log(
                    aes_decrypt(data.cipher, "cccccccccccccccc", data.IV)
                );
            },
        });
    });
    $("#username_btn").on("click", function (event) {
        $.ajax({
            type: "POST",
            url: "/genhashchain",
            async: false,
            data: {
                username: $("#input_username").val(),
            },
            success: function (data) {
                $("#username").text(
                    ": {0}, Token : {1}".format(
                        data.username,
                        data.supersecretKey
                    )
                );
                document.cookie = "cntDay={0}".format(data.cntDay);
                document.cookie = "supersecretKey={0}".format(
                    data.supersecretKey
                );
                document.cookie = "username={0}".format(data.username);
            },
        });
    });

    var odometer = new Odometer({
        el: $("#water_percentage")[0],
        value: 10,
        theme: "minimal",
        duration: 200,
    });
    odometer.render();

    change_water(50);
});

// let plaintext = "SOMETHING_SUPER_SECRET";
// let key = "cccccccccccccccc";
// let iv = "THIS_IS_COOL_IV!!";

// let ciphertext = aes_encrypt(plaintext, key, iv);
// console.log("ciphertext", ciphertext);

// plaintext = aes_decrypt(ciphertext, key, iv);
// console.log("plaintext", plaintext);
