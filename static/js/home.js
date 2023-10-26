document.addEventListener('DOMContentLoaded', () => {
  const saveButton = document.getElementById("saveButton");
  const nicknameInput = document.getElementById("nickname");

  // 로컬 스토리지에서 nickname 불러오기
  const storedNickname = localStorage.getItem('nickname');
  if (storedNickname) {
    nicknameInput.value = storedNickname;
  }

  saveButton?.addEventListener("click", () => {
    const nickname = nicknameInput.value;
    const userData = { nickname };

    fetch("/record/create_user", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    })
      .then((response) => response.json())
      .then((data) => {
        alert("사용자가 생성되었습니다.");
        localStorage.setItem('nickname', nickname); // 닉네임 로컬 스토리지에 저장
        location.reload();
      })
      .catch((error) => {
        alert("사용자 생성에 실패했습니다.");
      });
  });

  document.querySelector('.capButton')?.addEventListener("click", () => {
    redirectTo('/record');
  });
  document.querySelector('.scoreButton')?.addEventListener("click", () => {
    redirectTo('/score');
  });
  document.querySelector('.statisticsButton')?.addEventListener("click", () => {
    redirectTo('/statistics');
  });
});
