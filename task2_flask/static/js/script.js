$.ready(
    function () {
        var formulas_max = 6;
        var formulas_counter = 1;
        var tr_for_formulas = $('#add-formula');
        var add_button = tr_for_formulas.select("a").first();


        $(add_button).onclick(
            function (e) {
                console.log("ds"+add_button);
                if (formulas_counter < formulas_max) {
                    $("<tr><td>Formula</td><td><input type=\"text\" name=\"expressions[]\"></td>" +
                        "<td><a href=\"#\" class=\"formula-delete\">Delete</a></td></tr>").insertBefore(tr_for_formulas);
                    formulas_counter++;
                //    TODO set on new formula formula-delete.onclick trigger
                }
            }
        );
        // TODO set on formulas formula-delete.onclick trigger

    }
);


function eval_expression() {
    var $form = $('#main-form'),
        $error_p = $('#errors'),
        $result_p = $('#result');
    $.ajax({
        url: $form.attr('action'),
        data: $form.serialize(),
        type: 'POST',
        success: function (response) {
            // Success mean got response from server
            var json = jQuery.parseJSON(response);
            $error_p.text('');
            $result_p.text('');
            for (var expression in json.expressions_ctx) {
                var ctx = json.expressions_ctx[expression];
                if (ctx.error) {
                    $error_p.append(ctx.error);
                } else {
                    $result_p.append(expression + "=" + ctx.result);
                }

            }
            console.log(json);
            return json;
        },
        error: function (error) {
            // Error mean: cannot get response from server
            console.log("ERROR:" + error);
        }
    });
}
