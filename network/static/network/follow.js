document.addEventListener("DOMContentLoaded", (e) => {
  e.preventDefault();
  const followButton = document.getElementById("follow");
  console.log("Follow Button:", followButton.id);

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

  followButton.addEventListener("click", async (e) => {
    e.preventDefault();
    const userId = followButton.dataset.loggedUserId;
    const followingUserId = followButton.dataset.followingUserId;

    const button = e.currentTarget;
    console.log("Sending data:", {
      userId: userId,
      followingUserId: followingUserId,
    });
    const response = await fetch("/following_user/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        userId: userId,
        followingUserId: followingUserId,
      }),
    });

    const data = await response.json();
    console.log(data);

    if (data.follow) {
      button.className = "btn btn-danger";
      button.textContent = "Unfollow";
    } else {
      button.className = "btn btn-primary";
      button.textContent = "Follow";
    }
  });
});
