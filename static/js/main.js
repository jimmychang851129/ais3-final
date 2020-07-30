// string format
String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k]);
    }
    return a;
};

// let str = "THIS_IS_SIMPLE_STRING";
// let key = CryptoJS.enc.Utf8.parse("cccccccccccccccc");
// let iv = "THIS_IS_IV";

function hex2a(hexx) {
    var hex = hexx.toString(); //force conversion
    var str = "";
    for (var i = 0; i < hex.length && hex.substr(i, 2) !== "00"; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}

// function AES_Decrypt(word, iv) {
//     console.log("word->" + word);
//     //如果加密返回的base64Str
//     var srcs = hex2a(word);
//     iv = hex2a(iv);
//     //若上面加密返回的hexStr,需打开下面两行注释，再次处理
//     //var encryptedHexStr = fun_aes.CryptoJS.enc.Hex.parse(word);
//     var srcs = CryptoJS.enc.Base64.stringify(hex2a(word));
//     var decrypt = CryptoJS.AES.decrypt(srcs, key, {
//         iv: iv,
//         mode: CryptoJS.mode.CBC,
//         padding: CryptoJS.pad.Pkcs7,
//     });
//     var decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
//     var value = decryptedStr.toString();
//     console.log("value->" + value);
//     return value;
// }

// AES_Decrypt(
//     "d34320620546b2c1789e378fe020fd36",
//     "0810cb80837ba5eabc78c6b52cc3f1df"
// );

$(function () {
    $("#submit_btn").on("click", function (event) {
        console.log("AJAX");
        $.ajax({
            type: "POST",
            url: "/HMIquery",
            async: false,
            data: {
                HMIquery: $("#input_bar").val(),
            },
            success: function (data) {
                console.log(data);
            },
        });
        return false;
    });
});
