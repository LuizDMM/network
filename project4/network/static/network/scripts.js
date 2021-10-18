document.addEventListener("DOMContentLoaded", function () {
  // Add listeners to the "Edit Post" and "Like" buttons
  addEditButtonsEventListeners();
  addLikeButtonsEventListeners();
});

function addEditButtonsEventListeners() {
  document.querySelectorAll(".editPostButton").forEach((button) =>
    button.addEventListener("click", function () {
      postDiv = button.parentElement.parentElement.parentElement; // Select the post DIV element to have the post info
      // Clone the post DIV to keep the post info in memory while updating data
      postDivClone = postDiv.cloneNode(true);
  
      showEditPostForm(postDivClone);
    })
  );
}

function addLikeButtonsEventListeners() {
  document.querySelectorAll(".likeButton").forEach((button) =>
    button.addEventListener("click", function () {
      let postDiv = button.parentElement.parentElement.parentElement; // Select the post DIV element to have the post info
      // Fetch the API to like or unlike the post
      fetch(`/post/${postDiv.id}`, {
        method: "PUT",
      })
        .then((response) => response.text())
        .then((response) => {
          postDiv.innerHTML = response;
          addLikeButtonsEventListeners();
        });
    })
  );
}

function showEditPostForm(postDiv) {
  // Fetch the API to get the form
  fetch(`/post/${postDiv.id}/edit`)
    .then((response) => response.text())
    .then((response) => {
      // Create the form object and append the form got from the API
      let div = document.querySelector(`#${postDiv.id}`);
      let form = document.createElement("form");
      let id = postDiv.id.split("-")[1];
      form.setAttribute("id", `editPost-${id}`);
      form.setAttribute("action", `/post/${postDiv.id}/edit`);
      form.setAttribute("method", "POST");
      form.innerHTML = response;
      div.innerHTML = "";
      div.appendChild(form);
      // Add the form submtion Event listener
      addFormEventListener(id);
    });
}

// Function from "https://docs.djangoproject.com/en/3.2/ref/csrf/"
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

function addFormEventListener(id) {
  // Submit the form without redirecting the page
  $(`#editPost-${id}`).submit(function () {
    $.ajax({
      data: $(this).serialize(), // get the form data
      type: $(this).attr("method"),
      url: $(this).attr("action"),
      success: function (response) {
        $(`#post-${id}`).html(response); // update the DIV
        addEditButtonsEventListeners(); // Add the event listener to the new button
      },
    });

    return false; // cancel original event to prevent form submitting
  });
}
