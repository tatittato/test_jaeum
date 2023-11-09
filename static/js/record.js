// HTML 문서에서 camera id를 가진 비디오 요소를 가져옵니다.
const videoElement = document.getElementById("camera");
// captureButton id를 가진 버튼 요소를 가져옵니다.
const captureButton = document.getElementById("captureButton");
// endButton id를 가진 버튼 요소를 가져옵니다.
const endButton = document.getElementById("endButton");

let mediaStream; // 비디오 스트림 객체
let captureStartTime; // 촬영 시작 시간
let captureEndTime; // 촬영 종료 시간
let intervalId; // Interval 핸들러 ID를 저장할 변수
let timeoutHandlerId = null;
let latestPosture = null;
let changedPostureCount = 0;
let changingPosture = null;

const nickname = localStorage.getItem("nickname");
console.log("home에서 로컬에 저장한 닉넴", nickname);

// 촬영 시작 및 종료 시간을 Date 객체로 변환

// 초를 시, 분, 초로 변환하는 함수
function secondsToHMS(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  return `${hours.toString().padStart(2, "0")}:${minutes
    .toString()
    .padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

// 시, 분, 초를 추출하여 HH:MM:SS 형식으로 포맷팅
function formatTime(date) {
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");
  const seconds = date.getSeconds().toString().padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
}

captureButton.addEventListener("click", function () {
  // 웹 카메라에 액세스하여 비디오 스트림 가져오기
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then(function (stream) {
      mediaStream = stream; // 비디오 스트림 저장
      videoElement.srcObject = stream;
      captureStartTime = new Date(); // 촬영 시작 시간 저장
      const startTime = new Date(captureStartTime);
      const startSleepTime = formatTime(startTime);

      const urlParams = new URLSearchParams(window.location.search);
      const nickname = urlParams.get("nickname"); // URL에서 닉네임 가져오기

      // 데이터를 JSON 형식으로 준비
      const sleepInfoData = {
        nickname: nickname,
        start_sleep: startSleepTime,
      };
      console.log(JSON.stringify(sleepInfoData));

      // 데이터를 JSON 문자열로 변환
      const sleepInfoJSON = JSON.stringify(sleepInfoData);

      /// create_sleep_info 요청 보내기
      fetch("/record/create_sleep_info", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: sleepInfoJSON,
      })
        .then(function (createResponse) {
          // create_sleep_info 요청의 응답을 처리
          if (createResponse.ok) {
            return createResponse.json(); // JSON 데이터로 파싱
          } else {
            throw new Error("create_sleep_info 요청 실패");
          }
        })
        .then(function (createData) {
          console.log("서버에서 받은 데이터 (create_sleep_info):", createData);

          // create_sleep_info 요청이 완료된 후에 get_info_id 요청 실행
          return fetch("/record/get_info_id", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ nickname: nickname }),
          });
        })
        .then(function (getInfoIdResponse) {
          console.log("보내는 데이터:", JSON.stringify({ nickname: nickname }));
          // get_info_id 요청의 응답을 처리
          if (getInfoIdResponse.ok) {
            return getInfoIdResponse.json(); // JSON 데이터로 파싱
          } else {
            throw new Error("get_info_id 요청 실패");
          }
        })
        .then(function (getInfoIdData) {
          console.log(
            "서버에서 받은 sleep_info_id (get_info_id):",
            getInfoIdData
          );
          // 서버에서 받은 sleep_info_id 값을 가져온다고 가정
          const sleep_info_id = getInfoIdData.sleep_info_id;

          const sleepInfoIdInput = document.getElementById("sleep_info_id");
          sleepInfoIdInput.value = sleep_info_id;

          // 이제 create_sleep_info와 get_info_id가 모두 완료되었음
        })
        .catch(function (error) {
          console.error("에러:", error);
        });

      // 10분 후부터 프레임 전송 시작
      // timeoutHandlerId = setTimeout(captureAndUploadFrame, 600000);

      // // 랜덤 음악 파일 경로 목록
      // const musicFiles = [
      //   "Astor Piazzolla - The Four Seasons of Buenos Aires.mp3",
      //   "ES_A Travelers' Gloom - Dew Of Light.mp3",
      // ];

      // // 랜덤 음악 파일 선택
      // const randomIndex = Math.floor(Math.random() * musicFiles.length);
      // const randomMusic = musicFiles[randomIndex];

      // // 10초 후에 음악을 재생
      // setTimeout(function () {
      //   document.getElementById(
      //     "backgroundMusic"
      //   ).src = `static/music/${randomMusic}`;
      // }, 10000); // 10000 밀리초(10초) 후에 실행

      intervalId = setInterval(captureAndUploadFrame, 5000);
    })
    .catch(function (error) {
      console.error("웹 카메라 액세스 오류:", error);
    });
});

// "종료" 버튼 클릭 시 비디오 중지 및 촬영 종료 시간 저장
endButton.addEventListener("click", function () {
  const feedbackElement = document.getElementById("feedback");
  const loaderElement = document.querySelector(".loader");
  feedbackElement.innerHTML = "오늘의 피드백을 생성중입니다.";
  loaderElement.style.display = "block";
  if (mediaStream) {
    mediaStream.getTracks().forEach(function (track) {
      track.stop(); // 비디오 스트림 중지
    });
    videoElement.srcObject = null; // 비디오 정지
    captureEndTime = new Date(); // 촬영 종료 시간 저장

    if (timeoutHandlerId) {
      clearTimeout(timeoutHandlerId);
    }
    // 종료 버튼을 누르면 음악을 정지
    const backgroundMusic = document.getElementById("backgroundMusic");
    if (!backgroundMusic.paused) {
      backgroundMusic.pause();
    }
    // 촬영 중지를 위해 Interval을 제거
    if (intervalId) {
      clearInterval(intervalId);
    }

    const endTime = new Date(captureEndTime);
    const endSleepTime = formatTime(endTime);

    const startTimeInSeconds = Math.floor(captureStartTime.getTime() / 1000);
    const endTimeInSeconds = Math.floor(captureEndTime.getTime() / 1000);

    const totalSleepInSeconds = endTimeInSeconds - startTimeInSeconds;
    const totalSleepTime = secondsToHMS(totalSleepInSeconds);

    const urlParams = new URLSearchParams(window.location.search);
    const nickname = urlParams.get("nickname");

    const sleepInfoData = {
      nickname: nickname,
      end_sleep: endSleepTime,
      total_sleep: totalSleepTime,
    };

    console.log(JSON.stringify(sleepInfoData));
    const sleepInfoJSON = JSON.stringify(sleepInfoData);

    fetch(`/record/update/${nickname}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: sleepInfoJSON,
    })
      .then(function (response) {
        if (response.ok) {
          console.log("촬영 정보가 서버로 전송되었습니다.");
          return response.json(); // 첫 번째 요청이 완료되면 응답을 반환
        } else {
          console.error("촬영 정보 전송 실패", response);
        }
      })
      .then((data) => {
        fetchData();
        // 첫 번째 요청이 완료된 후에 두 번째 세션 요청을 수행
        console.log("받은 데이터:", data);
        console.log("닉네임 값:", nickname);
        const sleepInfoId = document.getElementById("sleep_info_id").value;
        console.log("수면정보아이디 값", sleepInfoId);
        const requestData = {
          nickname: nickname,
          sleep_info_id: sleepInfoId,
        };
        return fetch("/record/info_and_event", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });
      })
      .then((secondResponse) => {
        if (secondResponse.ok) {
          return secondResponse.json();
        } else {
          throw new Error("두 번째 요청에 문제가 있습니다.");
        }
      })
      .then((secondData) => {
        console.log("두 번째 요청으로 받은 데이터:", secondData);
        // 받은 데이터를 처리하거나 표시
        console.log("두 번째 요청으로 받은 닉네임:", nickname);
        const feedback = secondData;
        feedbackElement.innerHTML = feedback;
        loaderElement.style.display = "none";

        const feedbackData = {
          nickname: nickname,
          sleep_feedback: secondData,
        };
        return fetch(`/feedback/${nickname}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(feedbackData),
        });
      })
      .then((thirdResponse) => {
        if (thirdResponse.ok) {
          return thirdResponse.json();
        } else {
          throw new Error("세 번째 요청에 문제가 있습니다.");
        }
      })
      .then((thirdData) => {
        console.log("세 번째 요청으로 받은 데이터:", thirdData);
        // Handle the data received from the third request
      })
      .catch((error) => {
        console.error("요청에 문제가 있습니다:", error);
      });
  }
});

// 이미지 업로드 함수
function captureAndUploadFrame() {
  // HTML <canvas> 요소를 동적으로 생성합니다. 이 캔버스는 이미지를 그리기 위한 렌더링 대상이 됩니다.
  const canvas = document.createElement("canvas");
  // 캔버스 크기 설정
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;

  canvas
    // 2D 그래픽 컨텍스트를 가져옵니다.
    .getContext("2d")
    // videoElement의 비디오 프레임을 캔버스에 그립니다.
    .drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  // 캡처된 이미지를 Blob 형태로 변환
  canvas.toBlob(function (blob) {
    // Blob 데이터를 image(key)로 FormData에 추가
    const formData = new FormData();
    formData.append("image", blob, "captured_image.jpg");
    console.log("formData : ", formData);

    // FormData의 key 확인
    for (let key of formData.keys()) {
      console.log("key : ", key);
    }

    // FormData의 value 확인
    for (let value of formData.values()) {
      console.log("value : ", value);
    }

    // 서버로 이미지 데이터 전송 (fetch API 사용)
    sendImageToServer(formData);
  }, "image/jpg"); // jpg로 이미지 저장
}

function sendImageToServer(formData) {
  fetch("/record/return_posture", {
    method: "POST",
    body: formData,
  })
    .then(function (response) {
      // 서버 응답이 JSON 형식일 경우
      return response.json();
    })
    .then(function (data) {
      console.log("서버에서 받은 데이터:", data);

      var currentPosture = data;

      console.log("현재 자세:", currentPosture);
      console.log("이전 자세:", latestPosture);
      // 이전 자세와 현재 자세를 비교하여 로직을 추가합니다.
      if (latestPosture == null) {
        callSavePostureApi(formData, data);
        // 최근 자세 정보 업데이트
        latestPosture = currentPosture;
      }
      if (latestPosture !== null) {
        if (latestPosture !== currentPosture) {
          // 자세가 바뀌었을 때 처리할 코드
          changedPostureCount++; // 자세 변경 횟수 증가
          console.log("다른 횟수:", changedPostureCount);

          if (changedPostureCount >= 3) {
            // 자세가 3번 이상 변경되었을 때 처리할 코드
            latestPosture = currentPosture;
            changedPostureCount = 0;
            callSavePostureApi(formData, data);
          }
        } else {
          // 자세가 같을 때
          changedPostureCount = 0; // 자세 변경 횟수 초기화
        }
      }
    })
    .catch(function (error) {
      console.error("이미지 업로드 중 오류 발생:", error);
    });
}

// HTML 문서에서 id가 "sleep_info_id"인 요소의 값을 가져와서 sleepInfoId 변수에 저장합니다.

// 이미지 저장 함수
function callSavePostureApi(imageData, data) {
  const sleepInfoId = document.getElementById("sleep_info_id").value;
  // FormData 객체를 생성합니다.
  const formData = new FormData();
  formData.append("sleep_info_id", sleepInfoId);
  formData.append("data", data);
  formData.append("image", imageData.get("image"), "captured_image.jpg");

  console.log("sleep_info_id:", sleepInfoId);
  console.log("data:", data);
  console.log("imageData:", imageData.get("image"));

  fetch("/record/event_save", {
    method: "POST",
    body: formData,
  })
    .then(function (response) {
      if (response.ok) {
        console.log("Image saved successfully.");
      } else {
        console.error("Error saving the image.");
      }
    })
    .catch(function (error) {
      console.error("Error saving the image:", error);
    });
}

// 점수 저장함수
async function fetchData() {
  return new Promise(async (resolve, reject) => {
    try {
      const response = await fetch(`/score/${nickname}`, {
        method: "get",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const responseData = await response.json();
      console.log("responseData", responseData);

      fetch(`/record/update/score/${nickname}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(responseData),
      })
        .then(function (response) {
          if (response.ok) {
            console.log("수면 점수가 저장되었습니다");
            resolve(); // Promise가 성공했음을 알림
          } else {
            console.error("수면 점수 전송 실패", response);
            reject(); // Promise가 실패했음을 알림
          }
        })
        .catch(function (error) {
          console.error("수면 점수 전송중 오류 발생:", error);
          reject(); // Promise가 실패했음을 알림
        });
    } catch (error) {
      console.error("Error:", error);
      reject(); // Promise가 실패했음을 알림
    }
  });
}
