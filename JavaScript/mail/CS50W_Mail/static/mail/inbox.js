document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views
  document
    .querySelector("#inbox")
    .addEventListener("click", () => load_mailbox("inbox"));
  document
    .querySelector("#sent")
    .addEventListener("click", () => load_mailbox("sent"));
  document
    .querySelector("#archived")
    .addEventListener("click", () => load_mailbox("archive"));
  document.querySelector("#compose").addEventListener("click", compose_email);

  // By default, load the inbox
  load_mailbox("inbox");
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";
  document.querySelector("#email-view").style.display = "none";

  // Send email
  document
    .querySelector("#compose-form")
    .addEventListener("submit", (event) => {
      event.preventDefault();
      const recipients = document.querySelector("#compose-recipients").value;
      const subject = document.querySelector("#compose-subject").value;
      const body = document.querySelector("#compose-body").value;

      fetch("/emails", {
        method: "POST",
        body: JSON.stringify({
          recipients: recipients,
          subject: subject,
          body: body,
        }),
      })
        .then((response) => response.json())
        .then((result) => {
          console.log(result);
        });
      load_mailbox("sent");
    });
  // Clear out composition fields
  document.querySelector("#compose-recipients").value = "";
  document.querySelector("#compose-subject").value = "";
  document.querySelector("#compose-body").value = "";
}
function load_mailbox(mailbox) {
  fetch(`/emails/${mailbox}`)
    .then((response) => response.json())
    .then((emails) => {
      const emailsView = document.querySelector("#emails-view");
      emailsView.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
      
      emails.forEach((email) => {
        const element = document.createElement("div");
        element.id = "email-" + email.id;
        element.classList = "list-group-item list-group-item-action";
        const button = document.createElement("button");
        button.classList = "btn btn-outline-primary fa fa-archive align-self-baseline";
        button.id = "archive";
        
        const unarchiveButton = document.createElement("button");
        unarchiveButton.classList = "btn btn-outline-primary fa fa-inbox align-self-baseline";
        unarchiveButton.id = "unarchive";
        
        element.innerHTML = `
          <div class="d-flex w-100 justify-content-between">
            <h5 class="mb-1" href="/emails/${email.id}">${email.subject}</h5>
            <small>${mailbox === "sent" ? email.recipients : email.sender}</small>
          </div>
          <p class="mb-1">${email.body}</p>
          <div id="archive-group" class="d-flex w-100 justify-content-between">
            <small class="align-self-baseline">${email.timestamp}</small>
            <div>
              ${mailbox === "inbox" ? button.outerHTML : ""}
              ${mailbox === "archive" ? unarchiveButton.outerHTML : ""}
              ${mailbox !== "sent" ? `<button id="reply" class="btn btn-outline-primary fa fa-reply align-self-baseline"></button>` : ""}
              <button id="show" class="btn btn-outline-primary fa fa-eye align-self-baseline"></button>
            </div>
          </div>`;
        if (email.read) {
          element.style = "background-color: lightgray;";
        }
        if (element.querySelector('#archive')) {
          element.querySelector('#archive').addEventListener('click', () => {archive_email(email.id, true)});
        }
        if (element.querySelector('#unarchive')) {
          element.querySelector('#unarchive').addEventListener('click', () => {archive_email(email.id, false)});
        }
        element.querySelector('#show').addEventListener('click', () => {load_email(email.id)});
        emailsView.appendChild(element);
        if (element.querySelector('#reply')) {
          element.querySelector('#reply').addEventListener('click', () => {
            compose_email();
            document.querySelector("#compose-recipients").value = email.sender;
            document.querySelector("#compose-subject").value = email.subject.startsWith("Re: ") ? email.subject : `Re: ${email.subject}`;
            document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
          });
        }
      });
    });
  

  document.querySelector("#emails-view").style.display = "block";
  document.querySelector("#compose-view").style.display = "none";
  document.querySelector("#email-view").style.display = "none";
}


function load_email(id) {
  fetch(`/emails/${id}`)
    .then((response) => response.json())
    .then((email) => {
      document.querySelector("#emails-view").style.display = "none";
      document.querySelector("#compose-view").style.display = "none";
      document.querySelector("#email-view").style.display = "block";
      document.querySelector("#email-view").innerHTML = `
      <div class="card">
        <div class="card-header">
          <h5>${email.subject}</h5>
          <small>${email.sender}</small>
        </div>
        <div class="card-body">
          <p>${email.body}</p>
        </div>
        <div class="card-footer">
          <small>${email.timestamp}</small>
          ${
            email.archived
              ? `<button id="unarchive" class="btn btn-outline-primary fa fa-inbox align-self-baseline"></button>`
              : `<button id="archive" class="btn btn-outline-primary fa fa-archive align-self-baseline"></button>`
          }

        </div>
      </div>
      `;
    });
    fetch(`/emails/${id}`, {
      method: "PUT",
      body: JSON.stringify({
        read: true,
      }),
    });
}

function archive_email(id, archive) {
  fetch(`/emails/${id}`, {
    method: "PUT",
    body: JSON.stringify({
      archived: archive,
    }),
  }).then(() => {
    load_mailbox("inbox");
  });
}