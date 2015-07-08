$(document).ready(function() {
	// DELETE
	$('.delete').on('click', function(e) {
		if ($(this).text() == 'delete') {
			e.preventDefault();
			$('.delete').text('delete');
			$(this).text('Are you sure?');
		}
	});

	var search_base = $('#search').attr('action')
						.substring(1, $('#search').attr('action').length - 1);
	var query;

	// SEARCH
	$('#search_input').on('keypress', function(e) {
		query = $('#search_input').val();
	});

	$('#search').on('submit', function(e) {
		e.preventDefault();
		window.location = window.location + 'search/' + query;
	});

	// MARK POST
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

	// DELETE ACCOUNT
	$('.delete_acc').on('click', function(e) {
		if ($(this).text() == 'Delete account') {
			e.preventDefault();
			$(this).text('Are you sure?');
		} else if ($(this).text() == 'Are you sure?') {
			if (prompt('Type DELETE to delete account. All posts that belong to the account will also be removed.') == 'DELETE') {
				console.log('Deleting account.');
			} else {
				e.preventDefault();
			}
		}
	});
});

// Remove panels
$(window).load(function() {
	// Fades away each panel after 1 second + 1 second for each panel
	$('.panel').each(function(index, element) {
		setTimeout(function() { $(element).fadeOut() }, 2000 + parseInt(index) * 1000)
	});
});
