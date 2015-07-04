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

	// EDIT
	$('.edit').on('click', function(e){
		if ($(this).text() == 'edit') {
			$('.edit').text('edit');
			$(this).text('Proceed?');
		} else {
			window.location = $('#home_link').attr('href') + 'edit/' + 
								$(this).closest('div').prev().find('time').attr('data-time');
		}
	});
});