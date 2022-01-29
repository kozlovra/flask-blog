function dosearch(){
	window.location = '/blog/search/'+$('#search-input').val();
}

$('#search-button').click(function(){
	dosearch();
})
$('#search-input').on('keypress',function(e) {
    if(e.which == 13) {
    	dosearch();
    }
});