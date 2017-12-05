update_burner();

function update_burner(){
	$.ajax({
		url: "#",
		success: function(data){
			setTimeout(function(){
				$('#burner').html(data);
			}, 1000);
		}});
};

