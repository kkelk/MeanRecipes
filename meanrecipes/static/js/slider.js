var tooltipSlider = document.getElementById('slider-tooltip');

noUiSlider.create(tooltipSlider, {
	start: [60],
	range: {
		'min': 0,
		'max': 100
	}
});

var tipHandle = tooltipSlider.getElementsByClassName('noUi-handle')[0]
var tooltip = [];

tooltip = document.createElement('div');
tipHandle.appendChild(tooltip);

// Add a class for styling
tooltip.className += 'tooltip-slider';
// Add additional markup
tooltip.innerHTML = '<strong>Silliness: </strong><span></span>';
// Replace the tooltip reference with the span we just added
tooltip = tooltip.getElementsByTagName('span')[0];

// When the slider changes, write the value to the tooltips.
tooltipSlider.noUiSlider.on('update', function( values, handle ){
	tooltip.innerHTML = Math.round(values[handle]);
});
