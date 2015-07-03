$(document).ready(function() {
	$('form#search').on('submit', function(e) {
		e.preventDefault();
		
		window.location = ($('#home_link').attr('href') || '/') + 'search/' + $('#search_input').val();
	});

	$('a#language').on('click', function(e) {
		e.preventDefault();

		window.location = ($('#home_link').attr('href') || '/') + 'search/@' + $(this).text();
	});
});