$(document).ready(function () {
  	$('#newacct').on('click', function(event) {
  		window.location.href = "/register/";

	});
	$('#logout').on('click', function(event) {
  		window.location.href = "/accounts/logout?next=/";

	});
    $(".pop").popover();


});