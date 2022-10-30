// disables unused text box

var dropdown = document.getElementById('dropdown');
document.getElementById("volunteer_hours").disabled = true;

function disableOther(){
    if (dropdown.value === "payment") {
        document.getElementById("payment").disabled = false;
        document.getElementById("volunteer_hours").disabled = true;
    } else {
        document.getElementById("payment").disabled = true;
        document.getElementById("volunteer_hours").disabled = false;
    }
}
document.getElementById("dropdown").onchange = disableOther;
