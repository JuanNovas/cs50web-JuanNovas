document.addEventListener('DOMContentLoaded', function() {

    var editButtons = document.querySelectorAll(".edit-button");
    editButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            edit_twit(this);
        });
    });

});

function edit_twit(clicked_button) {

   var div = clicked_button.closest('.post');
   var twit_body = div.querySelector('#body');
   var edit_button = div.querySelector(".edit-button");
   twit_body.style.display = "none";
   edit_button.style.display = "none";

    var twit_ta = div.querySelector('#texare-edit');
    var twit_confirm = div.querySelector('#confirm-edit');
    twit_ta.style.display = "block";
    twit_confirm.style.display = "block";

    twit_ta.value = twit_body.textContent;

    var id = edit_button.getAttribute('data-twit-id');

    twit_confirm.addEventListener('click', () => confirm_edit(div,id));
}

function confirm_edit(div,id) {
    var content = div.querySelector('#texare-edit').value;
    if (content.trim() !== ""){
        fetch("/compose", {
            method : "PUT",
            body : JSON.stringify ({
                twit : content,
                id : id
            })
        })
        .then (response => {
            var twit_body = div.querySelector('#body');
            var edit_button = div.querySelector(".edit-button");
            twit_body.style.display = "block";
            twit_body.textContent = content;
            edit_button.style.display = "block";

            var twit_ta = div.querySelector('#texare-edit');
            var twit_confirm = div.querySelector('#confirm-edit');
            twit_ta.style.display = "none";
            twit_confirm.style.display = "none";
        })
    }
}