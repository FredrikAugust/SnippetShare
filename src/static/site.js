$(document).ready(function() {
	// SEARCH CONTENT
	$('form#search').on('submit', function(e) {
		e.preventDefault();
		
		window.location = $('#home_link').attr('href') + 'search/' + 
							$('#search_input').val();
	});

	// SEARCH CATEGORY
	$('a#language').on('click', function(e) {
		e.preventDefault();

		window.location = $('#home_link').attr('href') + 'search/@' + 
							$(this).text();
	});

	// DELETE
	$('.delete').on('click', function(e) {
		if ($(this).text() == 'delete') {
			$('.delete').text('delete');
			$(this).text('Are you sure?');
		} else {
			window.location = $('#home_link').attr('href') + 'delete/' + 
								$(this).closest('div').prev().find('time').attr('data-time');
		}
	});

	$('.post_a').on('click', function(event) {
		if (/post/i.test(window.location) == true) {
			event.preventDefault();

			target = this.childNodes[0].childNodes[0];

	        var selection = window.getSelection();            
	        var range = document.createRange();
	        range.selectNodeContents(target);
	        selection.removeAllRanges();
	        selection.addRange(range);
		}
	});
});