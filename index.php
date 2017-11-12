<?php
//index.php

$error = '';
$name = '';
$email = '';
$gender = '';
$age ='';
$height ='';
$weight = '';
$dietary ='';
$activity = '';

function clean_text($string)
{
	$string = trim($string);
	$string = stripslashes($string);
	$string = htmlspecialchars($string);
	return $string;
}

if(isset($_POST["submit"]))
{
	if(empty($_POST["name"]))
	{
		$error .= '<p><label class="text-danger">Please Enter your Name</label></p>';
	}
	else
	{
		$name = clean_text($_POST["name"]);
		if(!preg_match("/^[a-zA-Z ]*$/",$name))
		{
			$error .= '<p><label class="text-danger">Only letters and white space allowed</label></p>';
		}
	}
	
	if(empty($_POST["email"]))
	{
		$error .= '<p><label class="text-danger">Please Enter your Email</label></p>';
	}
	else
	{
		$email = clean_text($_POST["email"]);
		if(!filter_var($email, FILTER_VALIDATE_EMAIL))
		{
			$error .= '<p><label class="text-danger">Invalid email format</label></p>';
		}
	}
	$gender = $_POST["gender"];
	
	if(empty($_POST["age"]))
	{
		$error .= '<p><label class="text-danger">Age is required</label></p>';
	}
	else
	{
		$age = clean_text($_POST["age"]);
	}
	
	if(empty($_POST["height"]))
	{
		$error .= '<p><label class="text-danger">Height is required</label></p>';
	}
	else
	{
		$height = ((int)clean_text($_POST["height"])) * 2.54;
	}
	
	if(empty($_POST["weight"]))
	{
		$error .= '<p><label class="text-danger">Weight is required</label></p>';
	}
	else
	{
		$weight = ((int)clean_text($_POST["weight"])) * .45;
	}
	
	$dietary = $_POST["dietary"];
	$activity = ((int)$_POST["activity"]);
	
	if (empty(


	if($error == '')
	{
		$file_open = fopen("contact_data.csv", "a");
		$no_rows = count(file("contact_data.csv"));
		if($no_rows > 1)
		{
			$no_rows = ($no_rows - 1) + 1;
		}
		$form_data = array(
			'sr_no'		=>	$no_rows,
			'Name'		=>	$name,
			'Email'		=>	$email,
			'Gender'	=>	$gender,
			'Age' 		=>  $age,
			'Height'	=>	$height,
			'Weight'	=>	$weight,
			'Dietary'	=>	$dietary,
			'Activity'	=>	$activity
		);
		fputcsv($file_open, $form_data);
		$error = '<label class="text-success">Thank you for signing up.</label>';
		$name = '';
		$email = '';
		$gender = '';
		$age ='';
		$height ='';
		$weight = '';
		$dietary ='';
		$activity = '';
	}
}

?>
<!DOCTYPE html>
<html lang="en"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="data:image/webp;base64,UklGRloEAABXRUJQVlA4TE0EAAAvh8AfEIcgEEjy1xh2hcGbVoFACje4RA0GA5Yku3EbcBHFne/+17UIECST74j+TwApm1gs/QddB+J/wA0AYSufak3+PqYBgGHEmrQyPsN1KgBkmkcAXidiGi4T8etnZgCIKhZMexWP307zFwC8SubUm5j+ERj9x80eNNngwF8k4XeYWcAvzTvwSDzY9R4en5nm9afOHIAkiTzYa/QvN7P4zbMEoEqKIN0i4rPRPH+8s7qiCsYl7Ph6Z2Z8+BkAdMkQ4LlDxredBXzS9PmBBNJyBYvvTvP60WZpB9gb5EmaWXymWf/pAiOLF7CYhtn7FSYWv1XgZf0CaeZn7ctNwh7w540ZTR0+B03zJvm4AFn6KrPxUdSGOa3IzPiKE4fPqIZwmIEs4NtP0jb1sMAxH2ZM7KR/PXqwZ2VO/EiY0rfHt98gntU5CEQUICoTK7BL+lEW/F47RA5Tki6BO8kLhOajTvoW+aSoEX9eTOsW41LI3kfMk2gsQTioqghfUV1T/gK/B8wfYDZ57zdIHBe1+5Vd4K73yt5V6Zi4jZX5Vf2Yd5dG2+A5xe3yLrDL8inUNzELaBnMKWmPTDuFU+wedklb1k6htEOmpXUZ7Cmm6w27WTqFnF6ktWldP4aCVqPFcR2eYygMlWH3K+eQawrD0eqgAHMO0TtWDUfLvcZ7Epk4lhRDR/SjiPqC6knTacAfZSHs5bWkrJKPemcPWUdbqsCc1Ga0bVd5D7KY1n2qSj8ozOId8JxTZn6fqFOOMZjTJWBPCbO6kVdKp5RZ3MgpjVMw9xuREsIZD4N27krtjDyrWxUluCPGLG0VtfIJD+bPVl5rmAMyw2xFWggH9FmjvatW289hnjeLWnDbJUbYzKnl7TrDbkZda5jNHOaDdk9aCJslRtnOqrXNOiNuR1ULbisLpt8vqKWtXg4d2LXGVo3RTvBaCBtZMPMJVLTqRi8nHGGGEuw+jeOOIK+VtrHg0qFBqW/zcuopFHTw7NI46RhylVOCJV9ZZRMLbjiHyOcOYJRg6PPlwO7xsuxJCzvn3aNxBl01cPoWFtx6F8uB3+FlxbtQ4+QdGuu5TOLA6Fmw7WUC69V7WYMu61hdr7PKbWhw4LUc2PE6hZW1Es9f52XBKHWeuY7jvToe7E735XWdzCsXqix4lcGLF4q8rPGA7y/keTAKWWAuRIK4zoDf6caV19cFQb5S5OFZVgTvlbygrjIQ+iuRAHZRkNCdiyAvKoJ2qVcwzJohyJdyAoQlD4TxUjQEfUmW+FtlAfyKLjG3CpKywEHY6dZGAit7JeVa1CRJViTxXlEyZEPi7+UkCBIHKV28S5rklbSbZQm8oEjSzR5RFnRJuBkNCQwPUnu1JAosL2l0dScqGuluVCXQcJfzIreu0e2rxK8L13MKxOt0/6jQWOEPoMIaxH45lf5CUziRR23WzJ9AFMckk9DUr2Lor7SxAeiR5E+sJVr6uwEA">

    <title>Signup</title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" />
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    <!-- Bootstrap core CSS -->
    <link href="./bootstrap/bootstrap.min.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="./bootstrap/starter-template.css" rel="stylesheet">
	<style>
	.knowfood{
		text-align:center;
	}
	</style>
  </head>

  <body>
    <main role="main" class="container">
		<nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
		  <a class="navbar-brand" href="signup.html">KnowFood</a>
		  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
			<span class="navbar-toggler-icon"></span>
		  </button>

		  <div class="collapse navbar-collapse" id="navbarsExampleDefault">
			<ul class="navbar-nav mr-auto">
			</ul>
			<a class="btn btn-outline-success" href="login.html" role="button">Login</a>
		  </div>
		</nav>
      <div class="knowfood">
        <h1>KNOWFOOD</h1>
        <p class="lead">Know the food you will eat.<br> No food wasted.</p>
		<div class="row">
		<div class="col-lg-2"></div>
		<div class="col-lg-8">
			<form onsubmit="readAttr">
			  <p class="lead" style="text-align:left">Sign Up<br><small id="emailHelp" class="form-text text-muted"><br>Already have an account? <a href="login.html">Login</a>.</small></p>
			  
			  
			  <div class="form-group" style="text-align:left">
				<label for="inputEmail">Email address</label>
				<input type="email" class="form-control" id="inputEmail" aria-describedby="emailHelp" placeholder="Enter email" value="<?php echo $name; ?>" />
				<small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputPassword">Password</label>
				<input type="password" class="form-control" id="inputPassword" placeholder="Password" value="<?php echo $password; ?>" />
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputName">Name</label>
				<input type="text" class="form-control" id="inputName" placeholder="Ex: Jerry Smith" value="<?php echo $name; ?>" />
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputGender">Sex assigned at birth</label>
				<select type="text" class="form-control" id="inputGender" name="gender">
					<option>Female</option>
					<option>Male</option>
				</select>
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputAge">Age</label>
				<input type="text" class="form-control" id="inputAge" placeholder="Ex: 19" value="<?php echo $age; ?>" />
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputHeight">Height (inches)</label>
				<input type="text" class="form-control" id="inputHeight" placeholder="Ex: 72" value="<?php echo $height; ?>" />
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputWeight">Weight (pounds)</label>
				<input type="text" class="form-control" id="inputWeight" placeholder="Ex: 150" value="<?php echo $weight; ?>" />
			  </div>
			  <div class="form-group" style="text-align:left">
				<label for="inputDiet">Dietary Restriction</label>
				<select type="text" class="form-control" id="inputDiet" name="dietary" multiple>
					<option>Vegetarian</option>
					<option>Vegan</option>
					<option>Pork</option>
				</select>
			  </div>
			  
			  <div class="form-group" style="text-align:left">
				<label for="inputActLev">How active are you?</label>
				<small>(1 = Sedentary, Potato Chip Lifestyle, 5 = Very Active)</small>
				<select type="text" class="form-control" id="inputActLev" name="activity">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="5">5</option>
				</select>
			  </div>
			  
			  <div class="row" style="text-align:right"><div class="col-lg-12">
			  <button type="submit" class="btn btn-primary">Submit</button></div></div>
			</form>
			<p></p>
		</div>
		</div>
	  </div>
		
    </main><!-- /.container -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="./Starter Template for Bootstrap_files/jquery-3.2.1.slim.min.js.download" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="../../../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="./Starter Template for Bootstrap_files/popper.min.js.download"></script>
    <script src="./Starter Template for Bootstrap_files/bootstrap.min.js.download"></script>
  

<div id="naptha_container0932014_0707"></div></body></html>