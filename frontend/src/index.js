const checkbox = document.querySelector('.my-form input[type="checkbox"]');
const btns = document.querySelectorAll(".my-form button");
const formData = new FormData();


checkbox.addEventListener("change", function() {
    const checked = this.checked;
    for (const btn of btns) {
        checked ? (btn.disabled = false) : (btn.disabled = true);
    }
});


function displayRes(val) {
    // console.log(val);
    var textBox = document.getElementById('textBox');
    var submitButtons = document.getElementById('buttonsBottom');
    var tickBox = document.getElementById('searchTickBox');
    var imageSelector = document.getElementById('file ');
    var image = document.getElementById('output')
    if (val == "Search Via Image") {
        textBox.style.display = 'none';
        image.style.display = 'block';
        imageSelector.style.display = 'block';
        tickBox.style.display = 'block';
        submitButtons.style.display = 'block';
    }
    else{
        image.style.display = 'none';
        textBox.style.display = 'block';
        imageSelector.style.display = 'none';
        tickBox.style.display = 'block';
        submitButtons.style.display = 'block';
    }

}
function test(event) {
    event.preventDefault();

    const fileInput = document.querySelector('.test');
    // console.log(event.target.files)
    // console.log()
    formData.append('picture', fileInput.files[0]);
    const options = {
        method: "POST",
        body: formData,


    }
    var respons;
    var url = "http://192.168.29.106:12345/test";
    console.log(formData)
    fetch(url, options).then((response) => response.json()).then((data) => {
        addImage(data.image[0])

    });

}

function sendImage(event){
    event.preventDefault();

    const fileInput = document.querySelector('.test');
    // console.log(event.target.files)
    console.log(fileInput.files)
    formData.append('picture', fileInput.files[0]);
    const options = {
        method: "POST",
        body: formData,
    }
    var url = "http://192.168.29.106:12345/image";
    console.log(formData['picture'])
    fetch(url, options).then((response) => response.json()).then((data) => {
        addText(data['ans'])

    });

}


function sendText(event){
    event.preventDefault();
    const textInput = document.getElementById('textBox');
    // console.log(event.target.files)
    // console.log(textInput.value)
    formData.append('search', textInput.value);
    // console.log(formData)
    const options = {
        method: "POST",
        body:JSON.stringify({'search':textInput.value}),


    }
    var url = "http://192.168.29.106:12345/search";
    fetch(url, options).then((response)=> response.json()).then((data)=>{
        data['image'].forEach(addImage);
        // console.log(data)
    });

    

}

var loadFile = function(event) {
    var image = document.getElementById('output');
    image.src = URL.createObjectURL(event.target.files[0]);
};

function addText(text){
    const container = document.querySelector('.container');

    div = document.createElement('div');
    console.log(text)
    div.innerHTML = "<p>"+"\""+ text + "\"" + "</p>";
    container.appendChild(div);
}

function addCard(item) {
    var card = getNewCard();
    card.querySelector(".id").innerHTML = item.id;
    card.querySelector(".name").innerHTML = item.name;
    card.querySelector(".caption").innerHTML = item.caption;
    card.querySelector(".image").src = item.url;
    container.appendChild(card);
}

function addImage(image) {
    const container = document.querySelector('.container');

    div = document.createElement('div');
    const img = image.slice(2, image.length - 1)
    console.log(img)
    div.innerHTML = "<img src="+"\"data:image/png;base64,"+img +"\"" + " alt=\"alt text\" width=\"500\" height= \"500\">";
    container.appendChild(div);
}

function getNewCard() {
    var card = document.createElement('div');
    card.className = "card";
    card.innerHTML =
        "<div class\"card-body\">" +
        "<div class =\"id\" hidden></div>" +
        "<h3 class=\"name card-title ml-3 mt-2\"></h3>" +
        "<p class=\"caption card-text ml-3\"></p>" +
        "<img class=\"image card-img\">" +
        "</div>";
    return card;
}