function submit_login_form() {
	var username = document.getElementById('username-input').value;
	var pass = document.getElementById('password-input').value;
	console.log(username + pass)
	fetch('./users/login',{
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
}