// will read all the projects entries from the database and append it to the page.
for (let i = 0; i < parseInt("{{data_length}}"); i++) {
    var tag = document.createElement("p");
    var text = document.createTextNode("{{ data[0] | safe}}");
    tag.appendChild(text);
    var element = document.getElementById("elements");
    element.appendChild(tag);
}