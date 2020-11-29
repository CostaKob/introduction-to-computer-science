const presentation = (name) => {

    switch(name) {
        case "Costa":
            document.getElementById("costaDescription").innerHTML = "Costa is 32 years old !";
            break;
        case "Darya":
            document.getElementById("daryaDescription").innerHTML = "Darya is 32 years old and she is a Dental hygienist";
            break;
        case "Diana":
            document.getElementById("dianaDescription").innerHTML = "Diana is 6 years old and she is a 1st grade pupil";
            break;
        case "Yuli":
            document.getElementById("yuliDescription").innerHTML = "Yuli is 4 years old and she is cute";
            break;
        default:
            alert("Dont Worry, be happy!")
    }
}