// Initialize Firebase
var firebaseConfig = {
    apiKey: "AIzaSyC1Tl-n-djqcggh-sl6ovoJa53f8c6wo-I",
    authDomain: "landingpage-29c21.firebaseapp.com",
    databaseURL: "https://landingpage-29c21.firebaseio.com",
    projectId: "landingpage-29c21",
    storageBucket: "landingpage-29c21.appspot.com",
    messagingSenderId: "870824592398",
    appId: "1:870824592398:web:0d750d330b759078b5285f"
  };
  // Initialize Firebase
firebase.initializeApp(firebaseConfig);

//Reference messages collection
var emailsRef = firebase.database().ref('emails'); 


// Listen for form submit
document.getElementById('contactForm').addEventListener('submit', submitForm);
//Submit form 
function submitForm(e){
	e.preventDefault(); 


//Get Values
var email = getInputVal('email'); 
	
	const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	
	var res = re.test(String(email).toLowerCase());

	if(email != '' && res == true)
	{
		document.getElementById('submit').innerHTML = '<i class="fa fa-check"></i> Success';
		document.getElementById('submit').style.backgroundColor = 'green';
		document.getElementById('email').value = '';
		
		saveEmail(email); 
	} else {
		document.getElementById('email').focus();
		
		document.getElementById('submit').style.backgroundColor = '#0B3360';
		document.getElementById('submit').innerHTML = 'Submit';
	}
	//Save Emails
	
} 

// Function to get from values 
function getInputVal(id){
	return document.getElementById(id).value; 
}

//Save emails to firebase
function saveEmail(email){
	var newEmailRef = emailsRef.push();
	newEmailRef.set({
		email:email
	}); 

}