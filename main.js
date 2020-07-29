// string format
String.prototype.format = function () {
    a = this;
    for (k in arguments) {
        a = a.replace("{" + k + "}", arguments[k]);
    }
    return a;
};

$(document).ready(function () {
    console.log("AIS3{HI}");
});
