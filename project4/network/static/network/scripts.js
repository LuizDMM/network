document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".editPost").forEach((button) =>
    button.addEventListener("click", function () {
      postDiv = button.parentElement.parentElement.parentElement;
      postDivClone = postDiv.cloneNode(true);
      postDiv.innerHTML = '';
      postDiv.appendChild(editPostForm(postDivClone));
      postDiv.childNodes[0].addEventListener("submit", submitEditPostForm(postDivClone));
    })
  );
});


function submitEditPostForm(postDiv) {
  fetch(`/post/${postDiv.id}/edit`, {
    method: 'POST',
    body: JSON.stringify({
      content: document.querySelector(`#content${postDiv.id}`).value
    })
  })
}


function editPostForm(postDiv) {
  form = document.createElement("form");
  textarea = document.createElement("textarea");
  textarea.setAttribute("name", "content");
  textarea.setAttribute("id", `content${postDiv.id}`);
  textarea.setAttribute("cols", "40");
  textarea.setAttribute("rows", "10");
  textarea.setAttribute("class", "form-control");
  textarea.setAttribute("id", "postContent");
  textarea.setAttribute("required", "true");
  textarea.innerHTML = postDiv.childNodes[1].innerText;
  submitButton = document.createElement("input");
  submitButton.setAttribute("type", "submit");
  submitButton.setAttribute("value", "Save");
  submitButton.setAttribute("class", "btn btn-primary");
  form.appendChild(textarea);
  form.appendChild(submitButton);
  return form;
}
