function submit_login_form(event) {
	event.preventDefault()
	var username = document.getElementById('username-input').value;
	var pass = document.getElementById('password-input').value;
	fetch('users/login',{
		header: {
			'Accept': 'application/json',
      'Content-Type': 'application/json'
		}, 
		method: 'POST',
		mode: 'no-cors',
		body: JSON.stringify({
			'username': String(username), 
			'password': String(pass)
		})
	})
	.then(response => response.json())
	.then(response => {
		if (response.redirect) {
			location.replace(response.data);
		}
		else {
			document.getElementById('warning').innerHTML = response.data;
		}
	})
}

function reset_warning() {
	document.getElementById('warning').innerHTML = '';
}

function check_password_on_register() {
	var psw = document.getElementById('password-content').value;
	var psw_rpt = document.getElementById('password-repeat-content').value;
	if (psw == psw_rpt) {
		document.getElementById('submit-signup-button').disabled =false;
	} else {
		document.getElementById('submit-signup-button').disabled =true;
	}
}

function submit_register_form(event) {
	event.preventDefault()
	var username = document.getElementById('username-content').value;
	var pass = document.getElementById('password-content').value;
	fetch('users/register',{
		header: {
			'Accept': 'application/json',
      'Content-Type': 'application/json'
		}, 
		method: 'POST',
		mode: 'no-cors',
		body: JSON.stringify({
			'username': String(username), 
			'password': String(pass)
		})
	})
	.then(response => response.json())
	.then(response => {
		if (response.redirect) {
			location.replace(response.data);
		}
		else {
			document.getElementById('warning').innerHTML = response.data;
		}
	})
}

function upload_zip_book(event) {
	// event.preventDefault()
	const input = document.getElementById('file-input');
	
	// This will upload the file after having read it
	const upload = (file) => {
		fetch('books/upload', {
			method: 'POST',
			headers: {
				"Content-Type": "application/zip"
			},
			body: file
		}).then(
			response => response.json() // if the response is a JSON object
		).then(
			success => console.log(success) // Handle the success response object
		).catch(
			error => console.log(error) // Handle the error response object
		);
	};

	// Event handler executed when a file is selected
	const onSelectFile = () => upload(input.files[0]);

	onSelectFile()
	
}

function draw_ing_on_canvas(elem) {
	var canvas = elem.parentNode;
	var ctx = canvas.getContext("2d");
	ctx.drawImage(elem,0, 0,500, 500);
}