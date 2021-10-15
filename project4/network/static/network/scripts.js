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
      form.setAttribute("action", `/post/${postDiv.id}/edit`);
      form.setAttribute("method", "post");
      let id = postDiv.id.split("-")[1];
      form.setAttribute("id", `editPost-${id}`);
      form.innerHTML = response;
      div.innerHTML = "";
      div.appendChild(form);
      form.onsubmit = () => {
        return submitEditPostForm(postDiv, div);
      };
    });
}

function submitEditPostForm(postDiv, div) {
  let id = postDiv.id.split("-")[1];
  let form = document.querySelector(`#editPost-${id}`);
  fetch(`/post/${postDiv.id}/edit`, {
    method: "POST",
    body: JSON.stringify({
      csrfmiddlewaretoken: form.children[0].value,
      content: form.children[1].value,
      credentials: "same-origin",
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      if (response.status == 400) {
        alert(`Error: ${response.error}`);
      } else {
        fetch(`/post/${postDiv.id}`)
          .then((response) => response.text())
          .then((response) => {
            div.innerHTML = response;
          });
      }
    });

  return false;
}

