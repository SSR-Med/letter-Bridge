function check() {
    searchingParagraph = document.getElementById("check");
    if (searchingParagraph) {
        searchingParagraph.remove();
    }
    inputText = document.getElementsByTagName("input");
    var texts = [];
    for (var i = 0; i < inputText.length; i++) {
        // Apend texts
        var inside = inputText[i].value;
        if (inside === "") {
            inside = " "
        }
        texts.push(inside.toLowerCase());
    }
    // Post matrix
    fetch('/list', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(texts)
    }).then(response => response.json())
        .then(data => {
            var checked = data.Value;
            // Create paragraph
            var paragraph = document.createElement("p"),
                main = document.getElementsByTagName("main")[0];
            paragraph.id = "check";
            if (checked == true) {
                paragraph.innerHTML = "Matrix is fine."
            }
            else {
                paragraph.innerHTML = "Matrix is incorrect."
            }
            main.appendChild(paragraph);
        })
        .catch(error => console.error(error));;
    /*
    fetch('/list')
        .then(response => response.json())
        .then(data => {
            var checked = data.Value;
            // Create paragraph
            var paragraph = document.createElement("p"),
                main = document.getElementsByTagName("main")[0];
            paragraph.id = "check";
            if (checked == true) {
                paragraph.innerHTML = "Matrix is fine."
            }
            else {
                paragraph.innerHTML = "Matrix is incorrect."
            }
            main.appendChild(paragraph);
        })
        .catch(error => console.error(error));
    */

}