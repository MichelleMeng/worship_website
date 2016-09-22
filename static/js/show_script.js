$(document).ready(function() {
	$("#btn1").click(function() {
		var host=document.location.hostname;
		var url = host+"/"+"static/js/worship_meaning.txt"
		$('#txt_script').load(url);

	})
})

