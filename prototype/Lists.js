function setupLists() {
    /* Original code - https://www.w3schools.com/howto/howto_js_collapsible.asp */
    var lists = document.getElementsByClassName('opening-btn');
    
    for (var i = 0; i < lists.length; i++) {
        lists[i].addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        })
    }
}
