document.addEventListener("DOMContentLoaded", (e) => {
  e.preventDefault();
  const likeButtons = document.querySelectorAll(".like-btn");

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

  likeButtons.forEach(async (el) => {
    el.addEventListener("click", async (e) => {
      e.preventDefault();
      const post_id = el.dataset.likePostId;
      const creator_id = el.dataset.creatorId;
      const like_count_el = el.querySelector(".like_count");
      const like_button_el = e.currentTarget;

      const response = await fetch("/like_or_unlike/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
          creator_id: creator_id,
          post_id: post_id,
        }),
      });

      const data = await response.json();

      // console.log("Data: ", data);
      // console.log("Button now: ", like_button_el.innerHTML);

      let num_likes = parseInt(like_count_el.innerHTML);

      if (data.liked) {
        like_button_el.querySelector("i").className = "bi bi-heart-fill";
        like_count_el.innerHTML = num_likes + 1;
      } else if (num_likes < 1) {
        num_likes = 0;
      } else {
        like_button_el.querySelector("i").className = "bi bi-heart";
        like_count_el.innerHTML = num_likes - 1;
      }
    });
  });
});
