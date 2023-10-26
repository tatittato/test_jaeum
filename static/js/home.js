document.getElementById("saveButton").addEventListener("click", function () {
  const nickname = document.getElementById("nickname").value;

  // 데이터를 JSON 형식으로 준비
  const userData = {
    nickname: nickname,
  };

  // 서버로 데이터를 POST 요청으로 전송
  fetch("/record/create_user", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  })
    .then((response) => response.json())
    .then((data) => {
      // 서버에서 받은 응답을 처리할 수 있습니다.
      console.log("서버에서 받은 데이터:", data);
      alert("사용자가 생성되었습니다.");

      // 페이지 reload
      location.reload();
    })
    .catch((error) => {
      console.error("서버 요청 오류:", error);
      alert("사용자 생성에 실패했습니다.");
    });
});

document.getElementById("capButton").addEventListener("click", function () {
  const nickname = document.getElementById("nickname").value;

  // 닉네임이 비어 있는 경우 경고 메시지 표시하고 리다이렉트를 실행하지 않음
  if (nickname.trim() === "") {
    alert("닉네임을 입력해주세요.");
  } else {
    // 리다이렉트 URL을 생성하여 /record?nickname=에 닉네임을 추가합니다
    const redirectURL = "/record?nickname=" + nickname;

    // 페이지를 리다이렉트합니다
    window.location.href = redirectURL;
  }
});

document.getElementById("scoreButton").addEventListener("click", function () {
  const nickname = document.getElementById("nickname").value;

  // 닉네임이 비어 있는 경우 경고 메시지 표시하고 리다이렉트를 실행하지 않음
  if (nickname.trim() === "") {
    alert("닉네임을 입력해주세요.");
  } else {
    // 리다이렉트 URL을 생성하여 /record?nickname=에 닉네임을 추가합니다
    const redirectURL = "/score?nickname=" + nickname;

    // 페이지를 리다이렉트합니다
    window.location.href = redirectURL;
  }
});

document
  .getElementById("statisticsButton")
  .addEventListener("click", function () {
    const nickname = document.getElementById("nickname").value;

    // 닉네임이 비어 있는 경우 경고 메시지 표시하고 리다이렉트를 실행하지 않음
    if (nickname.trim() === "") {
      alert("닉네임을 입력해주세요.");
    } else {
      // 리다이렉트 URL을 생성하여 /record?nickname=에 닉네임을 추가합니다
      const redirectURL = "/statistics?nickname=" + nickname;

      // 페이지를 리다이렉트합니다
      window.location.href = redirectURL;
    }
  });

document
  .getElementById("timelineButton")
  .addEventListener("click", function () {
    const nickname = document.getElementById("nickname").value;

    // 닉네임이 비어 있는 경우 경고 메시지 표시하고 리다이렉트를 실행하지 않음
    if (nickname.trim() === "") {
      alert("닉네임을 입력해주세요.");
    } else {
      // 리다이렉트 URL을 생성하여 /record?nickname=에 닉네임을 추가합니다
      const redirectURL = "/timeline?nickname=" + nickname;

      // 페이지를 리다이렉트합니다
      window.location.href = redirectURL;
    }
  });
