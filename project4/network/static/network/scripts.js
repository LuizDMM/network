document.addEventListener("DOMContentLoaded", function () {
  // Add listeners to the "Edit Post" buttons
  document.querySelectorAll(".editPostButton").forEach((button) =>
    button.addEventListener("click", function () {
      let postDiv = button.parentElement.parentElement.parentElement;
      let postDivClone = postDiv.cloneNode(true);
      showEditPostForm(postDivClone);
    })
  );
});

function showEditPostForm(postDiv) {
  fetch(`/post/${postDiv.id}/edit`)
    .then((response) => response.text())
    .then((response) => {
      let div = document.querySelector(`#${postDiv.id}`);
      let form = document.createElement("form");
      /* form.setAttribute("action", `/post/${postDiv.id}/edit`);
      form.setAttribute("method", "post"); */
      let id = postDiv.id.split("-")[1];
      form.setAttribute("id", `editPost-${id}`);
      form.setAttribute("onsubmit", `submitEditPostForm(${id})`);
      form.innerHTML = response;
      div.innerHTML = "";
      div.appendChild(form);
    });
}

// Function from "https://docs.djangoproject.com/en/3.2/ref/csrf/"
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

function submitEditPostForm(id) {
  let form = document.querySelector(`#editPost-${id}`);
  let div = document.querySelector(`#post-${id}`);

  fetch(`/post/post-${id}/edit`, {
    method: "POST",
    body: JSON.stringify({
      csrfmiddlewaretoken: form.children[0].value,
      content: form.children[1].value,
      credentials: "same-origin",
    }),
    headers: { "X-CSRFToken": csrftoken },
  }).then((response) => {
    if (response.status == 400) {
      alert(`Error: ${response.error}`);
    } else {
      fetch(`/post/post-${id}`)
        .then((response) => response.text())
        .then((response) => {
          div.innerHTML = response;
        });
    }
  });

  return false;
}
