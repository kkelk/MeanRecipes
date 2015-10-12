$('#suggestions').typed({
    strings: ["chocolate chip cookies", "brownies", "pancakes", "pizza", "cheesecake", "lasagne", "korma", "ice cream", "sandwiches", "spaghetti"],
    typeSpeed: 50,
    backSpeed: 15,
    backDelay: 1500,
    loop: true
});

$('#recipe-form').submit(function() {
    get_recipe($('#recipe-title').val());

    return false;
});

function format_ingredient(ingredient) {
	var quantity = ingredient[0];
	var unit = ingredient[1];
	var description = ingredient[2];

	if (quantity) {
		quantity = quantity.toFixed(2);
	}
	else {
		quantity = "";
	}

	if (!unit) {
		unit = "";
	}
	return [quantity, unit, description].join(' ');
}

function get_recipe(title) {
    var url = '/recipe/search/' + title;
    $.ajax({
	url: url,
	type: "GET",
	data: {'silliness': value},
	success: function(data) {
                $('#ingredients').empty();
                $('#method').empty();

                $('html,body').css('overflow-y', 'visible');

                $('#info-row').show();

                $('#title').text("Recipe for " + data.title);
                for (i = 0; i < data.ingredients.length; i++) {
		    var string = format_ingredient(data.ingredients[i]);
                    $('#ingredients').append('<li>' + string + '</li>');
                }
                for (i = 0; i < data.method.length; i++) {
                    $('#method').append('<li>' + data.method[i] + '</li>');
                }

                target = $('#result');
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                document.getElementById('image').style.display = "none";
            }
    });
}
