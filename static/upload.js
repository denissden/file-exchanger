	// getElementById
	function $id(id) {
		return document.getElementById(id);
	}


	// file drag hover
	function FileDragHover(e) {
		e.stopPropagation();
		e.preventDefault();
		e.target.className = (e.type == "dragover" ? "hover" : "");
	}


	// file selection
	function FileSelectHandler(e) {
		FileDragHover(e);
		var files = e.target.files || e.dataTransfer.files;
		UploadFiles(files);
		
  }

	// upload files
	function UploadFiles(file) {

		let xhr = new XMLHttpRequest();
		let formData = new FormData();
			// create progress bar
      	var progress = $id("progress");
      	var cancel_btn = $id("cancel-btn")

			// progress bar
			xhr.upload.addEventListener("progress", function(e) {
        var pc = e.loaded / e.total;
        console.log(e.loaded, e.total);
				progress.value = pc;
			}, false);

		cancel_btn.addEventListener("click", function(e){
			xhr.abort();
		}, false)

			for (var i = 0, f; f = file[i]; i++) {
				formData.append("file" + i, f)
			}
	  
		// error handling
      	xhr.onreadystatechange = state => { 
        if (xhr.status != 200 && xhr.status != 0) {
		}} 
		
		xhr.onload = function () {
			const serverResponse = $id("download-url");
			serverResponse.innerHTML = this.response;
		};

		xhr.open("POST", '', true);
		xhr.send(formData);



	}

var fileselect = $id("select-btn"),
  filedrag = $id("filedrag");

// file select
fileselect.addEventListener("change", FileSelectHandler, false);


// file drop
filedrag.addEventListener("dragover", FileDragHover, false);
filedrag.addEventListener("dragleave", FileDragHover, false);
filedrag.addEventListener("drop", FileSelectHandler, false);


