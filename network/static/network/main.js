document.addEventListener("DOMContentLoaded", () => {
  const edit_button = document.querySelectorAll(".edit-btn");

  const getCookie = (name) => {
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
  };

  edit_button.forEach((el) => {
    el.addEventListener("click", (e) => {
      e.preventDefault();
      const postId = el.dataset.postId;

      const bl_1 = document.querySelector(`[data-block1-id="${postId}"]`);
      const bl_2 = document.querySelector(`[data-block2-id="${postId}"]`);

      if (bl_1.style.display === "block" || bl_1.style.display === "") {
        bl_1.style.display = "none";
        bl_2.style.display = "block";

        const formButton = document.querySelector(
          `[data-button-id="${postId}"]`
        );

        formButton.addEventListener("click", (e) => {
          e.preventDefault();

          const new_post_text = document.querySelector(
            `[data-text-id="${postId}"]`
          ).value;
          bl_1.style.display = "block";
          bl_2.style.display = "none";

          sendUpdate(postId, new_post_text);

          console.log("Edit worked");
        });
      } else {
        bl_1.style.display = "block";
        bl_2.style.display = "none";
      }
    });
  });

  const sendUpdate = async (postId, postText) => {
    const response = await fetch("/edit_post/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        post_id: postId,
        post_text: postText,
      }),
    });
    const data = await response.json();

    if (data.success) {
      const textElement = document.querySelector(
        `[data-block1-id="${postId}"] p:first-child`
      );
      if (textElement) {
        textElement.textContent = data.PostText;
      }
    }
  };
});
