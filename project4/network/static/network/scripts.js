document.addEventListener("DOMContentLoaded", function () {
  // Add listeners to the "Edit Post" buttons
  document.querySelectorAll(".editPostButton").forEach((button) =>
    button.addEventListener("click", function () {
      postDiv = button.parentElement.parentElement.parentElement;
      postDivClone = postDiv.cloneNode(true);
      showEditPostForm(postDivClone);
    })
  );

  // Add listeners to the "Edit Post" form submissions
  document
    .querySelectorAll(".editPostForm")
    .forEach((form) => form.addEventListener("submit", function () {
      postDiv = form.parentElement;
      console.log(postDiv);
      fetch(`/post/${postDiv.id}/edit`, );
    }));
});

function showEditPostForm(postDiv) {
  fetch(`/post/${postDiv.id}/edit`)
    .then((response) => response.text())
    .then((response) => {
      div = document.querySelector(`#${postDiv.id}`);
      div.innerHTML = response;
    });

  return true;
}
