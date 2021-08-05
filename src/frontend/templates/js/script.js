function submit_login_form() {
	var username = document.getElementById('username-input').value;
	var pass = document.getElementById('password-input').value;
	
	fetch('./users/login',{
		header: {
			'Accept': 'application/json',
      'Content-Type': 'application/json'
		}, 
		method: 'POST',
		body: JSON.stringify({
			'username': username, 
			'password': pass
		})
	})
}