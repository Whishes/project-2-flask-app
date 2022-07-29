const like_button_function = (event, sentence_id) => {
	const xhttp = new XMLHttpRequest();
	event.preventDefault();
	// get all sentences with the specific id
	like_sentences_class = document.getElementsByClassName(
		`like_form_${sentence_id}`
	);
	unlike_sentences_class = document.getElementsByClassName(
		`unlike_form_${sentence_id}`
	);

	// loops through the arrays and minuses the text value to match the +1 in the backend
	for (i = 0; i < unlike_sentences_class.length; i++) {
		like_sentences_class[i].style.display = "none";
		like_sentences_class[i][4].firstChild.textContent =
			parseInt(like_sentences_class[i][4].firstChild.textContent) + 1;

		unlike_sentences_class[i].style.display = null;
		unlike_sentences_class[i][4].firstChild.textContent =
			parseInt(unlike_sentences_class[i][4].firstChild.textContent) + 1;
	}

	// grabs form data
	form_data = document.getElementsByClassName(`like_form_${sentence_id}`)[0];
	submit_type = form_data[0].defaultValue;
	sentence_id = form_data[2].defaultValue;
	user_id = form_data[1].defaultValue;

	// request to the backend
	xhttp.open("POST", "/", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(
		`submit_type=${submit_type}&sentence_id=${sentence_id}&user_id=${user_id}`
	);
};
const unlike_button_function = (event, sentence_id) => {
	const xhttp = new XMLHttpRequest();
	event.preventDefault();
	// get all sentences with the specific id
	like_sentences_class = document.getElementsByClassName(
		`like_form_${sentence_id}`
	);
	unlike_sentences_class = document.getElementsByClassName(
		`unlike_form_${sentence_id}`
	);

	// loops through the arrays and minuses the text value to match the -1 in the backend
	for (i = 0; i < unlike_sentences_class.length; i++) {
		like_sentences_class[i].style.display = null;
		like_sentences_class[i][4].firstChild.textContent =
			parseInt(like_sentences_class[i][4].firstChild.textContent) - 1;

		unlike_sentences_class[i].style.display = "none";
		unlike_sentences_class[i][4].firstChild.textContent =
			parseInt(unlike_sentences_class[i][4].firstChild.textContent) - 1;
	}

	// grabs form data to send to the backend
	form_data = document.getElementsByClassName(`unlike_form_${sentence_id}`)[0];
	submit_type = form_data[0].defaultValue;
	sentence_id = form_data[2].defaultValue;
	user_id = form_data[1].defaultValue;

	// post request for the backend
	xhttp.open("POST", "/", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(
		`submit_type=${submit_type}&sentence_id=${sentence_id}&user_id=${user_id}`
	);
};

const shareButton = (event, sentence_id) => {
	event.preventDefault();
	// share's the sentence link to the user or if on pc etc it just copies to clipboard
	if (navigator.share) {
		navigator
			.share({
				title: `https://immense-chamber-64350.herokuapp.com/share/${sentence_id}`,
				url: "https://immense-chamber-64350.herokuapp.com/share/${sentence_id}",
			})
			.then(() => {
				console.log("sentence has been shared");
			})
			.catch((error) => {
				console.log("error sharing the sentence: ", error);
			});
	} else {
		navigator.clipboard.writeText(
			`https://immense-chamber-64350.herokuapp.com/share/${sentence_id}`
		);
		alert("The sentence has been copied to your clipboard!");
	}
};

const deleteButton = (event, sentence_id) => {
	event.preventDefault();
	confirmDelete = confirm("Are you sure you want to delete this sentence?");

	// if user has confirmed the deletion send delete request to the backend
	if (confirmDelete) {
		const xhttp = new XMLHttpRequest();
		xhttp.open("DELETE", "/delete_sentence_action", true);
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		xhttp.onload = function () {
			// if delete request is successful, remove the specific element from the screen
			if (xhttp.status === 200) {
				const dataSet = document.getElementsByClassName("profile_content");
				for (i = 0; i < dataSet.length; i++) {
					//console.log(dataSet[i].dataset);
					if (parseInt(dataSet[i].dataset.id) === sentence_id) {
						//console.log("removed: ", dataSet[i]);
						dataSet[i].remove();
					}
				}
			}
		};
		xhttp.send(`sentence_id=${sentence_id}`);
	}
};
