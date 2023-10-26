// Chart를 생성할 js들
// 그래프 위에 label 출력용 코드
Chart.register(ChartDataLabels);

const urlParams = new URLSearchParams(window.location.search);
const nickname = urlParams.get("nickname"); // URL에서 닉네임 가져오기

// 각종 변수들 전역선언
let period;
let period_canvas;
let sevendays_canvas;
let pose_canvas;
let rawData;
let chart_label;
let sleeptime;

// 일일 수면결과는 가져오는 함수가 있겠지? 거기서 나오는거 넣어서 하면댐; 

// period_button, pose_button 눌렀을 때 active 된 것 바꿔주기 
$(document).on('click', '.period_button', function () {
  $('.period_button').parent('label').removeClass('active');
  $(this).parent('label').addClass('active');
  $('.pose_buttons').children('label').removeClass('active');
  $('input#front').parent('label').addClass('active');
});

$(document).on('click', '.pose_button', function(){
  $('.pose_button').parent('label').removeClass('active');
  $(this).parent('label').addClass('active');
});

// 가장 위에 출력되는 7일간 수면현황 차트
function get_default_chart(endpoint) {
  period = endpoint;
  fetch("/statistics/" + nickname + "/" + endpoint + "/") // period를 변수로 선언
      .then(response => response.json())
    .then(data => {
        console.log("get_default_chart내의 닉네임/엔드포인트(기간) " , nickname, "/", period, " = ", endpoint)
        let total_sleep_time = data.period_total;
        let average_sleep_time = data.period_average;
        let average_score = data.score_average;
        let chart_data = data.chart_data;

        first_day = data.period_first_last[0];
        last_day = data.period_first_last[1];
        document.querySelector('#first_date').textContent = first_day;
        document.querySelector('#last_date').textContent = last_day;

        console.log('get_default_chart 함수내의 패치함수에서 받아오는 chart_data ▼▼▼')
        console.log(chart_data)
        console.log("keys", Object.keys(chart_data))
        console.log("values", Object.values(chart_data))
        generate_table_data(total_sleep_time, average_sleep_time, average_score);
        generate_table_data_period(total_sleep_time, average_sleep_time, average_score);

        create_default_chart(Object.keys(chart_data), Object.values(chart_data));
        let total = Object.values(chart_data).map(value => value[2]);
        console.log('get_default_chart 함수내의 패치함수에서 받아오는 total', total)
        create_period_chart(Object.keys(chart_data), total);
      })
      .catch(error => {
          console.log('데이터 에러:', error);
      });
}

// 7일간 수면현황 테이블에 값을 넣어주기
function generate_table_data(total_sleep_time, average_sleep_time, average_score){
  document.querySelector('#sevendays_total_sleep_time').textContent = secondsToHMS_total(total_sleep_time);
  document.querySelector('#sevendays_average_sleep_time').textContent = secondsToHMS(average_sleep_time);
  document.querySelector('#sevendays_sleep_score_average').textContent = average_score;  // 평균 수면점수로 바꿔줘야됨
}

// 기간별 수면현황 테이블에 값을 넣어주기
function generate_table_data_period(total_sleep_time, average_sleep_time, average_score){
  document.querySelector('#period_total_sleep_time').textContent = secondsToHMS_total(total_sleep_time);
  document.querySelector('#period_average_sleep_time').textContent = secondsToHMS_total(average_sleep_time);
  document.querySelector('#period_average_sleep_score').textContent = average_score;
}

function get_period_data(endpoint){
  period = endpoint;
  fetch("/statistics/" + nickname + "/" + endpoint + "/") // period를 변수로 선언
      .then(response => response.json())
      .then(data => {
        // 기간별 수면현황에 날짜 찍어주기 (시작날짜 ~ 종료날짜)
        first_day = data.period_first_last[0];
        last_day = data.period_first_last[1];

        document.querySelector('#first_date').textContent = first_day;
        document.querySelector('#last_date').textContent = last_day;

        generate_table_data_period(data.period_total, data.period_average, data.score_average);
        
        let chart_data = data.chart_data;
        let firstKey = Object.keys(chart_data)[0];

        if (typeof chart_data[firstKey] === "object" && "total" in chart_data[firstKey]) {
          // (2) 형식의 데이터 처리
          let total = Object.values(chart_data).map(value => value.total);
          let average = Object.values(chart_data).map(value => value.average);
          console.log("create_period_chart average1111", average)
          console.log(Object.keys(chart_data))
          console.log('if문')
          create_period_chart(Object.keys(chart_data), average);
        } else if (Array.isArray(chart_data[firstKey])) {
          // (1) 형식의 데이터 처리
          let total = Object.values(chart_data).map(value => value[2]);
          create_period_chart(Object.keys(chart_data), total);
          console.log('else문')
        } else {
          // 데이터가 없는 기간 데이터(?) 예외처리
          let average = 0;
          create_period_chart("-", average)
          console.log('아무것도해당안댐ㅋ')
        }
        
        // 기간을 새로 선택하면 선택한 기간의 정면잠 발생 횟수차트로 변경됨(default)
        get_pose_chart(endpoint, "front");
        $('.pose_button').parent('label').removeClass('active');
        $('input#front').parent('label').addClass('active');
      })
      .catch(error => {
          console.log('데이터 에러:', error);
      });
};

// ▼▼▼▼▼▼ 주간 수면현황 차트 시작 ▼▼▼▼▼▼
// 초로 환산시 : 0 ~ 24:00 =>  86,400초
function create_default_chart(chart_label, sleeptime) {
  console.log('sleeptime에 전체 잠잔 시간이 들어있지않나?')
  for (let i = 0; i < sleeptime.length; i++){
    sleepDurations = sleeptime.map(time => time[2]);
  }
  console.log(sleepDurations)

  // 수면 중간값 가져오기
  function find_midtime(start, end) {
    if (end > start) {
        return (start + end) / 2;
    } else {
        return (start + (end + 86400)) / 2;
    }
  }
  
  let midtimes = [];
  sleeptime.forEach(item => {
    // console.log("item[0]: ", item[0], "item[1]: ", item[1]);
    // console.log("Math.abs(item[1] - item[0]): ", Math.abs(item[1] - item[0]));
    // 잠잔 시간이 10분이하면 midtimes 안나오게..
    if (Math.abs(item[1] - item[0]) > 600) {
      midtimes.push(find_midtime(item[0], item[1]));
    } else {
      midtimes.push(null)
    }
  });

  console.log('midtimes 값을')
  console.log(midtimes)

  const minTime = Math.min(...sleeptime.map(time => time[0]));
  const maxTime = Math.max(...sleeptime.map(time => time[1])) + 86400;

const data = {
  labels: chart_label,
  datasets: [
    {
      label: '수면 중간시간',
      type: "line",
      data: midtimes,
      pointBackgroundColor: "#6666ff",
      tension: 0.5,
      backgroundColor: "#6666ff",
      fill: false,
      datalabels: { display:false }
    }, {
      label: '수면 시간',
      data: sleeptime.map((time, i) => [time[0], time[0] + sleepDurations[i]]),
      backgroundColor: 'rgba(237, 254, 255, 1)',
      datalabels: { display:false }
    }]
  };
  
  const config = {
    type: 'bar',
    data,
    options: {
      responsive: true,
      indexAxis: 'x',
      scales: {
        y: {
          type: "linear",
          reverse: true,
          beginAtZero: false,
          min: minTime, 
          max: maxTime,
          ticks: {
            display: false
          }
        }, x: {
          grid: { 
            color: 'rgba(250, 250, 255, 0.21)'
           },
          ticks: {
            color: '#fff'
          }
        }
      }, 
      elements: {
        line: {
          borderColor: "#66B2ff"
        },
        bar: {
          borderRadius: 5,
          borderSkipped: false  // 막대 양쪽에 radius 적용
        }
      },
    plugins: {
      tooltip: {
        displayColors: false,
        filter: function(tooltipItem, chartData) { // 'midtime' 툴팁만 숨기기
          if (tooltipItem.datasetIndex === 0) {
            return false;
          }
          return true;
        },
        callbacks: {
          label: function (tooltipItem) {
            let hours = Math.floor( midtimes[tooltipItem.dataIndex] / 3600);
            let minutes = Math.floor((midtimes[tooltipItem.dataIndex] % 3600) / 60);
            let secs = midtimes[tooltipItem.dataIndex] % 60;
            let midtime = " ";
        
            if (hours < 0) {
              midtime = " ";
            } else if (hours >= 24) {
              hours = hours - 24;
              midtime = `${String(hours)}시  `;
            } else {
              midtime = `${String(hours)}시 `;
            }
            // 00분, 00초는 출력하지않음
            if (minutes > 0) {
              midtime += `${String(minutes).padStart(2, '0')}분 `
            } else { 
              // console.log(minutes);
            }
        
            if (secs > 0) {
              // console.log("secoundsToHMS secs");
              // console.log(secs);
              midtime += `${String(secs).padStart(2,'0')}초`;
            } else {
              // console.log(secs);
            }
            
            if (sleepDurations[tooltipItem.dataIndex] < 180) {
              duration = " ";
            }
        
            duration = secondsToHMS_total(sleepDurations[tooltipItem.dataIndex]);
            return [`수면시간: ${duration}`, `수면 중간시간: ${midtime}`];
          }
        }
      },
      legend: {
        labels: {
          color: '#fff'
        }
      }
    }
  }
};

const seven_days_chart = new Chart(sevendays_canvas, config);
}

// ★ 이벤트 리스너 (즉시실행) page 로드되면 실행할 것 ★
document.addEventListener("DOMContentLoaded", function () {
  sevendays_canvas = document.querySelector('#seven_days_chart').getContext('2d');
  period_canvas = document.querySelector('#period_chart').getContext('2d');
  pose_canvas = document.querySelector('#sleep_pose_chart').getContext('2d');

  // 디폴트 차트 출력: 기간별(week) + 포즈(shrimp) 
  get_default_chart("week");
  get_pose_chart("week", "front");
});

let sleepDateChart;

  // 초를 시간단위로 변환하는 함수
  function secondsToHMS(seconds) {
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;
    if (hours < 0) {
      phrase = " ";
    } else if (hours > 24) {
      hours = hours - 24;
      phrase = `${String(hours)}시간 `;
    } else {
      phrase = `${String(hours)}시간 `;
    }
    // 00분, 00초는 출력하지않음
    if (minutes > 0) {
      phrase += `${String(minutes).padStart(2, '0')}분 `
    } 

    if (secs > 0) {
      // console.log("secoundsToHMS secs");
      // console.log(secs);
      phrase += `${String(secs).padStart(2,'0')}초`;
    }
    
    return phrase;
  };

   // 초를 시간단위로 변환하는 함수 (전체시간용으로 hours에서 -24를 하지않음)
function secondsToHMS_total(seconds) {
  let hours = Math.floor(seconds / 3600);
  let minutes = Math.floor((seconds % 3600) / 60);
  let secs = seconds % 60;

  phrase = `${String(hours)}시간 `;
  
  if (secs > 0) {
    phrase += `${String(minutes).padStart(2, '0')}분 ${String(secs).padStart(2,'0')}초`;
  } else {
    phrase += `${String(minutes).padStart(2, '0')}분`;
  }
  
  return phrase;
};
  
  // ▼▼▼▼▼▼ 기간별 평균 수면시간 ▼▼▼▼▼▼
  function create_period_chart(chart_label, sleeptime){ // keys, value에서 토탈값만
    if(sleepDateChart){
      sleepDateChart.destroy();
    }

    if (sleeptime < 180) {
      sleeptime = 0;
    }

    console.log("create_period_chart 함수 내의 sleeptime 받아오는가? ");
    console.log(sleeptime);

    sleepDateChart = new Chart(period_canvas, {
      type : "bar",
      data : {
        labels: chart_label,
        datasets: [{
              label: '기간별 평균 수면시간',
              data: sleeptime,
              backgroundColor: 'rgba(237, 254, 255, 1)'
          }]
      }, options: {
        responsive: true,
        indexAxis: 'y',
        scales: {
          x: {
            grid: {
              color: 'rgba(250, 250, 255, 0.21)'
            },
            min: 0,
            stepSize: 1,
            ticks: {
              color: '#fff',
              callback: function (value, index, values) {
                hours = Math.floor(value / 3600);
                return `${String(hours)}시간`;
              }
            }
          },
          y: {
            grid: { display: false },
            ticks: {
              color: '#fff'
            }
          }
        },
        elements: {
          bar: {
            borderRadius: 5
          }  
        },
        plugins: {
          tooltip: {
            enabled: false,
          },
          datalabels: {
            color: '#232324',
            formatter: (value) => {
              if (value == " ") {
                return value
              } else if (value < 600) {
                return " "
              } else { avg_value = secondsToHMS(value) }
              
                return secondsToHMS(value);
            }
          },
          legend: {
            display:false,
          }
        }
      }
    });
};
  
// 자세별 발생횟수 차트
function create_pose_chart(pose_label, pose_values){
  if(sleepPoseChart){
    sleepPoseChart.destroy();
  }

  console.log('자세별 발생횟수 차트의  라벨', pose_label);

  sleepPoseChart = new Chart(pose_canvas, {
    type: 'bar',
    data: {
        labels: pose_label,
        datasets: [{
            label: '자세별 발생 횟수',
            data: pose_values,
            backgroundColor: 'rgba(237, 254, 255, 1)'
        }]
    }, options: {
        scales: {
          y: {
            grid: {
              color: 'rgba(250, 250, 255, 0.21)'
            },
            beginAtZero: true,
            ticks: {
                stepSize: 1,
                precision: 0,
                color: '#fff'
            }
          },
        x: {
          grid: { display: false },
          ticks: {
            color: '#fff'
          }
        }
      },
      elements: {
        bar: {
          borderRadius: 5
        }
      },
      plugins: {
          tooltip: {
            enabled: false
          },
          datalabels: {
              align: 'center',
              anchor: 'center',
              color: '#232324',
              font: {
                  weight: 'bold'
          }, formatter: (value) => {
                if (value==0) {
                  value = ""; 
                  }
                  return value;
              }
        },
        legend: {
          display: false,
          }
        }
    }
  });
}

let sleepPoseChart; 

// 포즈차트 비동기(fetch)
function get_pose_chart(period, endpoint){
  fetch("/statistics/" + nickname + "/" + period + "/" + endpoint + "/")
      .then(response => response.json())
    .then(data => {
      console.log('get_pose_chart의 닉네임/기간/엔드포인트', nickname, '/', period, '/', endpoint)
      let chart_data = data.chart_data;

      // key값은 날짜
      let pose_labels = Object.keys(chart_data); 
      // 밸류는 endpoint에 따라 key값에 맞게 가져온다
      let pose_values = pose_labels.map(date => chart_data[date][endpoint]); 

      create_pose_chart(pose_labels, pose_values);
      })
      .catch(error => {
          console.log('데이터 에러:', error);
      });
};

// 페이지 상단으로 가는 버튼
function scrollToTop() {
  const scrollDuration = 250; 
  const scrollStep = -window.scrollY / (scrollDuration / 15),
        scrollInterval = setInterval(function(){
          if (window.scrollY != 0) {
              window.scrollBy(0, scrollStep);
          }
          else clearInterval(scrollInterval); 
        },15);
}