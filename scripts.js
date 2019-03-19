function filter_button_func() {

  // var scenario1 = $("input[name='scenario']:checked").val(); // Big Home
	// console.log(scenario);

  // var scenario2 = $("input[name='scenario2']:checked").val(); //
	// console.log(scenario2);
  // var scenario3 = $("input[name='scenario3']:checked").val();
	// console.log(scenario3);

  if (document.getElementById("big_home").checked == true) {
      console.log('Its scenario 1 bro!');
      document.getElementById("card1").style.display = "none";
      document.getElementById("card2").style.display = "block";
      document.getElementById("card3").style.display = "block";
      document.getElementById("card4").style.display = "block";
      document.getElementById("card5").style.display = "block";
      document.getElementById("card6").style.display = "block";
  }
  else if (document.getElementById("extra_cash").checked == true) {
    console.log('Its scenario 2 bro!');
    document.getElementById("card1").style.display = "none";
    document.getElementById("card2").style.display = "block";
    document.getElementById("card3").style.display = "block";
    document.getElementById("card4").style.display = "none";
    document.getElementById("card5").style.display = "block";
    document.getElementById("card6").style.display = "block";
  }
  else if (document.getElementById("pay_off_quickly").checked == true) {
      console.log('Its scenario 3 bro!');
      document.getElementById("card1").style.display = "none";
      document.getElementById("card2").style.display = "block";
      document.getElementById("card3").style.display = "block";
      document.getElementById("card4").style.display = "none";
      document.getElementById("card5").style.display = "none";
      document.getElementById("card6").style.display = "none";
  }

}
