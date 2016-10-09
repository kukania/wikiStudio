var isAdvancedUpload = function() {
		var div = document.createElement('div');
		return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window;
}();

if(isAdvancedUpload){
	console.log("is possible");

	$form = $(".box");
	$form.addClass('has-advanced-upload');

  var fileBuffer =[];

  var onDropFuc = function(e) {
    droppedFiles = ( e.type == 'drop' ? e.originalEvent.dataTransfer.files : document.getElementById("file").files);
    console.log(droppedFiles);
    Array.prototype.push.apply( fileBuffer, droppedFiles);        

    $('.box__input').hide();
    $('.box__success').show();

    var count = 0;
    for( i = 0; i < droppedFiles.length; i++){
      var reader = new FileReader();
      reader.onload = function (e){
        var imgTag = $(document.createElement('img'));

        imgTag.attr('src', e.target.result);
        imgTag.addClass('added-img');
      
        $('.box__success').append(imgTag);       
      }

      if(droppedFiles[i].type.substring(0, 5) != 'image'){
        count++;
        console.log("aa");
        continue;
      }
      reader.readAsDataURL(droppedFiles[i]);
    }
    if(count == droppedFiles.length){
      alert("선택한 파일 혹은 폴더에는 이미지 파일이 없습니다.");
      $('.box__input').show();
    }
  };

	$form.on('drag dragstart dragend dragover dragenter dragleave drop', function(e) {
  		e.preventDefault();
  		e.stopPropagation();
		})
		.on('dragover dragenter', function() {
  		$form.addClass('is-dragover');
		})
		.on('dragleave dragend drop', function() {
  		$form.removeClass('is-dragover');
		})
		.on('drop', onDropFuc)
    .on('change', onDropFuc);
}else {

}