$('#recipe-form').submit(function() {
	get_recipe($('#recipe-title').val());
	return false;
});

function get_recipe(title) {
	var url = '/recipe/search/' + title;
	$.get(url, 
	function(data) {
		$('#ingredients').empty();
		$('#method').empty();

		data = JSON.parse(data);
		$('#title').text("Recipe for " + data.title);
for (i = 0; i < data.ingredients.length; i++) {
	 	$('#ingredients').append('<li>' + data.ingredients[i][0] + data.ingredients[i][1] + " " + data.ingredients[i][2] + '</li>');
}
		for (i = 0; i < data.method.length; i++) {
			$('#method').append('<li>' + data.method[i] + '</li>');
		}
	});
}

