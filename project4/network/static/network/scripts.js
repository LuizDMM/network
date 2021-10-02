document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".editPost").forEach((button) =>
    button.addEventListener("click", function () {
      postDiv = button.parentElement.parentElement.parentElement;
      postDiv.innerHTML = editPostForm(postDiv.id);
    })
  );
});

function editPostForm(id) {
  return '<form><textarea name="content" cols="40" rows="10" class="form-control" id="postContent" required=""></textarea><input type="submit" value="Save" class="btn btn-primary"></form>';
}
