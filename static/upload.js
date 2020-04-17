	var MAX_SIZE = 512 * 1024 * 1024
	
	// getElementById
	function $id(id) {
		return document.getElementById(id);
	}

	function $name(name) {
		return document.getElementsByName(name);
	}

	//copy to clipboadr button
	function CopyToClipboard() {
		text = $id("download-url").innerHTML;
		if (text != ""){
			const el = document.createElement('textarea');
			el.value = text;
			document.body.appendChild(el);
			el.select();
			document.execCommand('copy');
			document.body.removeChild(el);
		}
	  };


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

      	var progress = $id("progress");
		var cancel_btn = $id("cancel-btn");
		var copy_btn = $id("copy-btn");
		var drag_box_text = $id("filedrag-text")
		
		var expiration_buttons = $name("expire");
		var expiration_id = "0";

		cancel_btn.style = ""
		progress.style = "display: flex;"

		// progress bar
		xhr.upload.addEventListener("progress", function(e) {
				var pc = e.loaded / e.total;
				console.log(e.loaded, e.total);
				progress.value = pc;
				text = Math.round(pc * 100) + "% uploaded"
				drag_box_text.innerHTML = text

				if (pc == 1) { 
					cancel_btn.style = "display: none;";
					drag_box_text.innerHTML = "Processing your files"
				 }

			}, false);

		cancel_btn.addEventListener("click", function(e){
			drag_box_text.innerHTML = "Upload canceled"
			xhr.abort();
		}, false)

		// putting all files in one Form
		for (var i = 0, f; f = file[i]; i++) {
			formData.append("file" + i, f)
		}
		
		// files expiration time
		for (var i = 0, l = expiration_buttons.length; i < l; i++) {
		if (expiration_buttons[i].checked) {
			expiration_id = expiration_buttons[i].value;
		}}
		formData.append("expire", expiration_id);
	  
		// error handling
      	xhr.onreadystatechange = state => { 
        if (xhr.status != 200 && xhr.status != 0) {
			// alright then
		}} 
		
		xhr.onload = function () {
			if (xhr.status == 200) {
				drag_box_text.innerHTML = "Download link is below";
				filedrag.removeEventListener("dragover", FileDragHover, false);
				filedrag.removeEventListener("dragleave", FileDragHover, false);
				filedrag.removeEventListener("drop", FileSelectHandler, false);
				fileselect.removeEventListener("change", FileSelectHandler, false);
				$id("hidden-input").innerHTML = '<span class="file-custom"></span>'
			} 

			const link = $id("download-url");
			copy_btn.style = ""
			progress.style = "display: none;"
			link.innerHTML = this.response;
			link.href = this.response;
			console.log(xhr.status)
		};

		var size = 0;
		for(var pair of formData.entries()) {
			if (pair[1] instanceof Blob) 
			size += pair[1].size;
			else
			size += pair[1].length;
		}
		
		if (size <= MAX_SIZE){
			xhr.open("POST", '', true);
			xhr.send(formData);
		}
		else {
			progress.style = "display: none;"
			cancel_btn.style = "display: none;";
			drag_box_text.innerHTML = "Files are too large. Choose something smaller";
		}
		


	}

var fileselect = $id("select-btn"),
  filedrag = $id("filedrag");

// file select
fileselect.addEventListener("change", FileSelectHandler, false);


// file drop
filedrag.addEventListener("dragover", FileDragHover, false);
filedrag.addEventListener("dragleave", FileDragHover, false);
filedrag.addEventListener("drop", FileSelectHandler, false);


