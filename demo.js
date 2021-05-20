function f_color(){
    if (document.getElementById('my-output').value = ["you have parkinson's disease"]) {
    document.getElementById('my-output').style.color = "red";
    }
    else if (document.getElementById('my-output').value = ["you dont have"]){
    document.getElementById('my-output').style.color = "green";
    }
    else{
        document.getElementById('my-output').style.color = "black";    
    }
    }
    document.getElementById('my-output').onchange= f_color;
    