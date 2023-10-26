let myChart;

document.addEventListener("DOMContentLoaded", function () {
  let today = new Date().toISOString().substr(0, 10);
  document.querySelector("#dateInput").value = today;
});

document.querySelector(".timeline_btn").addEventListener("click", function () {
  let selectedDate = document.querySelector(".select_date").value;
  let dateParts = selectedDate.split("-"); // ["YYYY", "MM", "DD"]
  let dateWithoutYear = dateParts.slice(1).join("-").replace("DD", "dd"); // "MM-dd"

  const urlParams = new URLSearchParams(window.location.search);
  const nickname = urlParams.get("nickname"); // URL에서 닉네임 가져오기

  console.log(nickname);

  fetch("/timeline/search?date=" + selectedDate + "&nickname=" + nickname)
    .then((response) => response.json())
    .then((mysql_data) => {
      var ctx = document.getElementById("myChart").getContext("2d");

      if (!mysql_data.sleep_info || !mysql_data.sleep_info.length) {
        alert("데이터가 존재하지 않습니다!");
        return; // 데이터가 없으면 차트를 그리지 않음
      }

      // 차트가 이미 있다면 삭제
      if (myChart) {
        myChart.destroy();
      }

      const datasets = [
        {
          label: "총 녹화 시간",
          data: mysql_data.sleep_info.map((item) => [
            new Date(selectedDate + "T" + item.start_sleep),
            new Date(selectedDate + "T" + item.end_sleep),
          ]),
          backgroundColor: "#ffff99",
          barThickness: 20,
          borderRadius: 10,
          borderSkipped: false,
        },
      ];

      mysql_data.sleep_events.forEach((event, index, arr) => {
        const nextEvent = arr[index + 1];

        if (nextEvent) {
          const startTime = new Date(selectedDate + "T" + event.event_time);
          const endTime = new Date(selectedDate + "T" + nextEvent.event_time);
          datasets.push({
            label: event.sleep_event,
            data: [[startTime, endTime]],
            backgroundColor: "#ff9999",
            barThickness: 20,
            borderRadius: 10,
            borderSkipped: false,
          });
        } else {
          // 마지막 이벤트의 경우 end_sleep을 사용
          const startTime = new Date(selectedDate + "T" + event.event_time);
          const endTime = new Date(
            selectedDate + "T" + mysql_data.sleep_info[0].end_sleep
          );
          datasets.push({
            label: event.sleep_event,
            data: [[startTime, endTime]],
            backgroundColor: "#ff9999",
            barThickness: 20,
            borderRadius: 10,
            borderSkipped: false,
          });
        }
      });

      myChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: [dateWithoutYear],
          datasets,
        },
        options: {
          indexAxis: "y",
          plugins: {
            tooltip: {
              callbacks: {
                label: function (context) {
                  var label = context.dataset.label || ""; // 데이터셋의 라벨 가져오기
                  return label;
                },
              },
            },
            legend: {
              display: false,
            },
          },
          scales: {
            x: {
              position: "right",
              type: "time",
              time: {
                // Luxon format string
                tooltipFormat: "dd",
                unit: "hour", // x축 단위를 'hour'로 설정
                stepSize: 1, // 각 틱(tick)이 1시간 간격으로 표시됨
              },
              min: new Date(selectedDate + "T00:00:00"),
              max: new Date(selectedDate + "T08:00:00"),
              ticks: {
                color: "white",
                font: {
                  size: 16,
                },
              },
            },
            y: {
              ticks: {
                color: "white", // y축 라벨 색상
                font: {
                  size: 16, // y축 라벨 폰트 크기
                },
              },
            },
          },
        },
      });
      // 지정한 시간 호출
      var startTime = document.querySelector(".select_box1").value;
      var endTime = document.querySelector(".select_box2").value;
      // 시작 시간과 종료 시간을 기반으로 새로운 x축 범위 생성
      var newMinDate = new Date(selectedDate + "T" + startTime + ":00:00");
      var newMaxDate = new Date(selectedDate + "T" + endTime + ":00:00");
      // 그래프의 x축 범위 업데이트
      myChart.options.scales.x.min = newMinDate;
      myChart.options.scales.x.max = newMaxDate;
      // 그래프 다시 그리기
      myChart.update();
      console.log(mysql_data); // 데이터 확인용
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});

const toggleImagesButton = document.getElementById("toggle-images-button");
const imageContainer = document.getElementById("image-container");

let imagesVisible = false; // 초기에는 이미지 루프 숨김

toggleImagesButton.addEventListener("click", () => {
  imagesVisible = !imagesVisible;
  imageContainer.style.display = imagesVisible ? "block" : "none";
});

// 페이지 로드시 이미지 루프를 숨김
imageContainer.style.display = "none";
