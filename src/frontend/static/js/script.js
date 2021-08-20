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

function draw_img_on_canvas(elem) {
	var canvas = elem.parentNode;
	var ctx = canvas.getContext("2d");
	ctx.drawImage(elem,0, 0, canvas.width, canvas.height);
}

function get_annotation(elem) {
	var img_id = elem.getAttribute("data-img-id");
	elem.disabled = true;
	fetch('pages/auto-annotate?id='+img_id, {
		method: 'GET'
	}).then(
		response => response.json()
	).then(
		res => {
			var bbox = res.bbox;
			var shape = res.shape;
			draw_boxes(bbox, shape, img_id)
		}
	).catch(
		e => {
			elem.disabled = false;
		}
	)
}

function draw_boxes(bbox, shape, node_id) {
	var c = document.getElementById(node_id).getElementsByTagName('canvas')[0];
	var ctx = c.getContext("2d");
	ctx.lineWidth = ".6";
	ctx.strokeStyle = "red";
	for (const box of bbox) {
		ctx.beginPath();
		ctx.moveTo(box[0][0]/shape[0]*c.width, box[0][1]/shape[1]*c.height);
		ctx.lineTo(box[1][0]/shape[0]*c.width, box[1][1]/shape[1]*c.height);
		ctx.lineTo(box[2][0]/shape[0]*c.width, box[2][1]/shape[1]*c.height);
		ctx.lineTo(box[3][0]/shape[0]*c.width, box[2][1]/shape[1]*c.height);
		ctx.closePath();
		ctx.stroke();
	}
}