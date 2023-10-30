//첫화면은 오늘 날짜의 수면점수를 보여줌

       
document.addEventListener("DOMContentLoaded", function() {
  //한국시간에 맞추기 위해서 realdate 변수에 9시간 빼서 넣음
  const offset = new Date().getTimezoneOffset() * 60000;
  const realdate = new Date(Date.now() - offset);

  document.getElementById('selectedDate').value = realdate.toISOString().substring(0, 10);
  const today = realdate.toISOString().substring(0, 10);
  const selectedDate = today; // 선택한 날짜 가져오기
  const urlParams = new URLSearchParams(window.location.search);
  const nickname = urlParams.get("nickname"); // URL에서 닉네임 가져오기

  let data; 

  // 선택한 날짜를 기반으로 서버에서 데이터 가져오기
  fetch(`/score/${nickname}/${selectedDate}`)

      .then(response => response.json())
      .then(responseData => {
          data = responseData; // responseData를 data에 할당
          console.log(data);

          if (scoreChart) {
            scoreChart.destroy();
          }

          drawChart(data);

          document.getElementById('sleep_score').textContent = data.total_sleep_score;
          document.getElementById('nickname').textContent = data.nickname;

      });

});

//input date 날짜를 선택하면 해당 유저의 날짜별 수면점수를 보여줌
document.getElementById('selectedDate').addEventListener('change', function() {

  const selectedDate = this.value; // 선택한 날짜 가져오기
  const urlParams = new URLSearchParams(window.location.search);
  const nickname = urlParams.get("nickname"); // URL에서 닉네임 가져오기

  let data; 
  // 선택한 날짜를 기반으로 서버에서 데이터 가져오기
  fetch(`/score/${nickname}/${selectedDate}`)

      .then(response => response.json())
      .then(responseData => {
          data = responseData; // responseData를 data에 할당
          console.log(data);

          if (scoreChart) {
              scoreChart.destroy();
          }

          drawChart(data);

          document.getElementById('sleep_score').textContent = data.total_sleep_score;
          document.getElementById('nickname').textContent = data.nickname;
      });
});


let scoreChart;


function drawChart(data) {

scoreChart = new Chart(
      document.getElementById('scoreChart'),
      {
      plugins : [ChartDataLabels],    
      type: 'bar', // 차트의 형태
      data: { // 차트에 들어갈 데이터
          labels: [
              //x 축

              ['잠잔 시간 ' , + data.total_sleep_time + '시간'],
              ['나쁜자세로 잔 시간 ', + data.bad_position_time + '시간'],
              ['자세가 바뀐 횟수', + data.position_changes + '회'],
              ['잠에 든 시간 ', + data.start_sleep_time + '시']
          ],
          datasets: [
              { //데이터
                  datalabels: {
                      color:"#fff"
                  },
                  label: '수면 점수',
                    //차트 제목
                  fill: false, // line 형태일 때, 선 안쪽을 채우는지 안채우는지
                  data: [
                      data.sleep_time_score,
                      data.bad_position_score,
                      data.position_change_score,
                      data.start_sleep_time_score
                  ],
                  backgroundColor: [
                      //색상
                      "#FF9999",
                      "#FF9999",
                      "#FF9999",
                      "#FF9999",
                  ],

              } 
          ]
      },
      options: {
          maintainAspectRatio : false,
          plugins: {
              datalabels: { // datalables 플러그인 세팅
              formatter: function (value, context) {
                  var idx = context.dataIndex; // 각 데이터 인덱스
                  // 출력 텍스트
                  return  value + '점';
                  },
                  font: { // font 설정
                  color:   '#FF0000',  
                  weight: 'bold',
                  size: '20px',
                  },
              },
              legend: {
                  labels: {
                    color: '#fff'
                  }
              },
          },
          scales: {
              y: {
                  grid: {
                      color:"#fff",
                  },
                  max:25,
                  ticks: {
                      color: "#fff",
                      font: {
                          size: 20,
                      }
                  }
              },
              x: {
                  grid: {
                      color:"#fff",
                  },
                  ticks:{
                      color: "#fff",
                      font: {
                          size: 10,
                      }
                  }
              }
          }
      },
  },
)};


// 토글 버튼 요소를 가져옵니다.
var scoreStandardButton = document.getElementById("scoreStandardButton");

// 토글할 요소를 가져옵니다.
var scoreStandardToggle = document.getElementById("scoreStandardToggle");

// 버튼 클릭 시 토글 함수를 호출합니다.
scoreStandardButton.addEventListener("click", function() {
// 현재 요소의 표시 상태를 확인하고 토글합니다.
if (scoreStandardToggle.style.display === "none") {
scoreStandardToggle.style.display = "block";
} else {
scoreStandardToggle.style.display = "none";
}
});