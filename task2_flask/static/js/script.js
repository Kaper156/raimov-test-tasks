function eval_expression() {
    $.ajax({
        url: "/eval_data",
        data: $('#enter-form').serialize(),
        type: 'POST',
        success: function (response) {
            // Success mean got response from server
            var json = jQuery.parseJSON(response);
            $('#errors').text(json.error); // Show error which can be raised in view
            $('#result').text(json.result); // Show result of expression
            console.log(json);
        },
        error: function (error) {
            // Error mean: cannot get response from server
            console.log("ERROR:" + error);
        }
    });
}