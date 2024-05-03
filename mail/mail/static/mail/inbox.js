document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('#compose_button').addEventListener('click', sent_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      const emails_amount = emails.length;

      var back_color = "#ffffff";

      for (let i = 0; i < emails_amount; i++){
        if (emails[i].read==false)back_color="#ffffff";
        else back_color="#E8E8E8";
        document.querySelector('#emails-view').insertAdjacentHTML("beforeend",`<div style="display: flex; border: 1px solid #000;background-color: ${back_color};" id="A${emails[i].id}"> <p style="font-weight: bold; margin-left: 5px"> ${emails[i].sender}</p> <p style="margin-right: 20px; margin-left: 20px"> ${emails[i].subject} </p> <p>${emails[i].timestamp}</p> </div>`);
        document.querySelector(`#A${emails[i].id}`).addEventListener('click', () => open_mail(emails[i].id));
      }
  });

}

function sent_email() {
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })

  .then(result => {
    if (result.status == 201) alert("Mail sent correctly");
    else alert("Mail not sent, something went wrong");
  })

  load_mailbox('sent')

}

function open_mail(email_id) {
    document.querySelector('#emails-view').innerHTML = ``;
    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {
        document.querySelector('#emails-view').insertAdjacentHTML("beforeend",`
        <div>
        <div style="display: flex;">
            <p style="font-weight: bold; margin-right: 5px;">From:</p>
            <p>${email.sender}</p> 
        </div>
        <div style="display: flex;">
            <p style="font-weight: bold; margin-right: 5px;">To:</p>
            <p>${email.recipients}</p> 
        </div>
        <div style="display: flex;">
            <p style="font-weight: bold; margin-right: 5px;">Subject:</p>
            <p>${email.subject}</p> 
        </div>
        <div style="display: flex;">
            <p style="font-weight: bold; margin-right: 5px;">Timestamp:</p>
            <p>${email.timestamp}</p>  
        </div>
          
        <div style="display: flex;">
            <p style="font-weight: bold; margin-right: 5px;">Body:</p>
            <p>${email.body}</p>  
        </div> 
        </div>`);
    
        console.log(document.querySelector("#user_mail").textContent)
        console.log(email.recipients)
        console.log(document.querySelector("#user_mail").textContent == email.recipients)

    if (document.querySelector("#user_mail").textContent == email.recipients){
        document.querySelector('#emails-view').insertAdjacentHTML("beforeend",`
        <form action="/">
            <button class="btn btn-sm btn-outline-primary" id="archived_button">${email.archived ? "Unarchive" : "Archive"}</button>
        </form>
        `);
        document.querySelector(`#archived_button`).addEventListener('click', () => archive(email_id));

        document.querySelector('#emails-view').insertAdjacentHTML("beforeend",`
        <button class="btn btn-sm btn-outline-primary" id="reply_button" style="margin-top: 5px">Reply</button>
        `);
        document.querySelector(`#reply_button`).addEventListener('click', () => reply(email_id));
    }
    
    });


    fetch(`/emails/${email_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
}


function archive (email_id) {

    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(mail => {
        fetch(`/emails/${email_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                archived:  mail.archived ? false : true
            })
          })
    })

}

function reply(email_id) {
	compose_email()
	fetch(`/emails/${email_id}`)
    .then(response => response.json())
	.then(mail => {
		document.querySelector('#compose-recipients').value = mail.sender;
		document.querySelector('#compose-subject').value = `re: ${mail.subject} `;
		document.querySelector('#compose-body').value = `${mail.timestamp} ${mail.sender} wrote: ${mail.body}\n`;
	})

}