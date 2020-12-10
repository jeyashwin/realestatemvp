var timerID = setInterval(function() {
    recaptchaReset();
}, 2.1 * 60000);

function recaptchaReset(){
    var recaptchaV3Id = JSON.parse(document.getElementById('recaptchaV3Id').textContent);
    console.log('recaptcha reset')
    var widgetId = document.getElementById(recaptchaV3Id).getAttribute('data-sitekey');
    grecaptcha.execute(widgetId, {action: 'form'})
    .then(function(token) {
        var element = document.getElementById(recaptchaV3Id);
        element.value = token;
    });
}