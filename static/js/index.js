function countChar(obj) {
    var characterCount = obj.value.length,
        current = document.getElementById("counter");
    current.innerHTML = characterCount + "/300";
    // Change counter color if = 300
    if (characterCount == 300) {
        current.style.color = "red";
    }
    else {
        current.style.color = "#7C7A7D";
    }
}

function create() {
    // Text of textarea
    // New div created
    // main element
    // Loading (<p>)
    /* 
        <div id="imgCreated">
            <!--Here is: Button clicked -> Animation -> image -> Download icon-->
        </div>
    */
    // Dete graph.png before execution
    fetch('/delete-file', {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify("static/images/graphs/graph.png")
    })
    var text = document.getElementsByTagName("textarea")[0].value,
        newDiv = document.createElement("div"),
        main = document.getElementsByTagName("main")[0]
    // If there is no text
    if (text == '') {
        return
    }
    fetch('/graph', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(text),
    });
    // Check if div imgCreated is in the document, if there is one then delete it and create another one
    var imgCreatedDiv = document.getElementById("imgCreated");
    if (imgCreatedDiv) {
        imgCreatedDiv.remove();
        location.reload(true);
    }
    // Add id
    newDiv.setAttribute("id", "imgCreated");
    const animationParagraph = ['Loading', 'Loading.', 'Loading..', 'Loading...'];
    let animationParagraphIndex = 0
    function updateAnimation() {
        paragraph.innerHTML = animationParagraph[animationParagraphIndex];
        animationParagraphIndex = (animationParagraphIndex + 1) % animationParagraph.length;
    }
    // Call the interval
    const intervalAnimation = setInterval(updateAnimation, 1000);
    // Animation for loading
    paragraph = document.createElement("p");
    // Add paragraph to newDiv
    newDiv.appendChild(paragraph);
    // Add newdiv to main
    main.appendChild(newDiv);
    // If the image was finally added
    fetch("/static/images/graphs/graph.png").then((response) => {
        if (response.status === 200) {
            // Clear interval animation, eliminate paragraph and clear intervalImage
            clearInterval(intervalAnimation);
            paragraph.remove();
            // Create img and add it to newDiv
            // Creation of the image
            const graph = new Image();
            // Src image
            graph.id = "graphImage";
            graph.src = "/static/images/graphs/graph.png";
            newDiv.appendChild(graph);
            // Add download icon
            const download = new Image();
            download.src = "static/images/download.png";
            download.id = "download";
            download.addEventListener('click', function () {
                var anchor = document.createElement('a');
                anchor.setAttribute('href', 'static/images/graphs/graph.png');
                anchor.setAttribute('download', '');
                document.body.appendChild(anchor);
                anchor.click();
                anchor.parentNode.removeChild(anchor);
            });
            newDiv.appendChild(download);
        }
    });
} 