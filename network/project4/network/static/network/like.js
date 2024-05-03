document.addEventListener('DOMContentLoaded', function() {

    var likeButtons = document.querySelectorAll("#give-like");
    likeButtons.forEach(function(button) {
        update_button(button);
        button.addEventListener('click', function(event) {
            like_twit(this);
        });
    });


});

function like_twit (clicked_button){
    var id = clicked_button.getAttribute('data-twit-id');

    fetch("/like/", {
        method : "PUT",
        body: JSON.stringify ({
            id : id
        })
    })
    .then(response => {
        fetch(`/like/?id=${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.state){
                clicked_button.value = "💗";
            }
            else {
                clicked_button.value = "🤍";
            }
            var likeCount = document.querySelector(`#like-count-${id}`);
            likeCount.textContent = data.amount;
        })
    })
}

function update_button (button){
    console.log("1")
    var id = button.getAttribute('data-twit-id');
    fetch(`/like-button/?id=${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.state){
                button.value = "💗";
            }
            else {
                button.value = "🤍";
            }
        })
}
