function init(){
	var premiertissue = document.getElementsByClassName("premiertissue");
	function dropdownmanager(){
		if(campaignselector.value == "Handphone Colour"){
			for (var i = 0; i<premiertissue.length; i++){
			premiertissue[i].style.display = 'none';
			console.log(premiertissue[i]);
		}
	}
		if(campaignselector.value == "Premier Face Tissue"){
		for (var i = 0; i<premiertissue.length; i++){
			premiertissue[i].style.display = 'block';
			console.log(premiertissue[i]);
		}
	} if(campaignselector.value == "Cutie Tissue Campaign"){
		for (var i = 0; i<premiertissue.length; i++){
			premiertissue[i].style.display = 'block';
			console.log(premiertissue[i]);
		}
	}
}
	var facetissue = document.getElementById("facetissue");
	if(facetissue == null){
		console.log("null");
	}
	var campaignselector = document.getElementById("campaignselector");
	campaignselector.onchange = dropdownmanager;
}


window.onload = init;