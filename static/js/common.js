const redirectTo = (endpoint) => {
  const nickname = localStorage.getItem('nickname');
  if (!nickname) {
    alert("닉네임을 입력해주세요.");
    return;
  }
  window.location.href = `${endpoint}?nickname=${nickname}`;
};