const like_button_function = (event, sentence_id) => {
	const xhttp = new XMLHttpRequest();
	event.preventDefault();
	like_sentences_class = document.getElementsByClassName(
		`like_form_${sentence_id}`
	);
	unlike_sentences_class = document.getElementsByClassName(
		`unlike_form_${sentence_id}`
	);

	for (i = 0; i < unlike_sentences_class.length; i++) {
		//console.log(like_sentences_class[i][3]);
		//debugger;
		like_sentences_class[i].style.display = "none";
		like_sentences_class[i][4].firstChild.textContent =
			parseInt(like_sentences_class[i][4].firstChild.textContent) + 1;

		unlike_sentences_class[i].style.display = null;
		unlike_sentences_class[i][4].firstChild.textContent =
			parseInt(unlike_sentences_class[i][4].firstChild.textContent) + 1;
	}

	console.log("unlike class", unlike_sentences_class);

	form_data = document.getElementsByClassName(`like_form_${sentence_id}`)[0];
	//console.log(form_data);
	//console.log(form_data[0].defaultValue);
	submit_type = form_data[0].defaultValue;
	sentence_id = form_data[2].defaultValue;
	user_id = form_data[1].defaultValue;

	xhttp.open("POST", "/", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(
		`submit_type=${submit_type}&sentence_id=${sentence_id}&user_id=${user_id}`
	);
};
const unlike_button_function = (event, sentence_id) => {
	const xhttp = new XMLHttpRequest();
	//console.log(event);
	event.preventDefault();
	like_sentences_class = document.getElementsByClassName(
		`like_form_${sentence_id}`
	);
	console.log(like_sentences_class);
	unlike_sentences_class = document.getElementsByClassName(
		`unlike_form_${sentence_id}`
	);
	//console.log(unlike_sentences_class);
	//console.log(sentence_id);
	for (i = 0; i < unlike_sentences_class.length; i++) {
		//console.log(i, unlike_sentences_class[i][3]);
		like_sentences_class[i].style.display = null;
		like_sentences_class[i][4].firstChild.textContent =
			parseInt(like_sentences_class[i][4].firstChild.textContent) - 1;

		unlike_sentences_class[i].style.display = "none";
		unlike_sentences_class[i][4].firstChild.textContent =
			parseInt(unlike_sentences_class[i][4].firstChild.textContent) - 1;
	}

	form_data = document.getElementsByClassName(`unlike_form_${sentence_id}`)[0];
	//console.log("form data: ", form_data);
	//console.log(form_data[0].defaultValue);
	submit_type = form_data[0].defaultValue;
	sentence_id = form_data[2].defaultValue;
	user_id = form_data[1].defaultValue;

	xhttp.open("POST", "/", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(
		`submit_type=${submit_type}&sentence_id=${sentence_id}&user_id=${user_id}`
	);
};
