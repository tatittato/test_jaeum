// 데이터 순환 자동으로 모든 값 불러오는 명령어

// ...mysql_data.sleep_events.map((event, index, arr) => {
//   let startTime;
//   let endTime;

//   if (index < arr.length - 1) {
//     // 현재 항목이 마지막이 아닌 경우, 다음 항목의 시작 시간을 종료 시간으로 사용
//     startTime = new Date(
//       selectedDate + "T" + arr[index].event_time
//     );

//     if (startTime === undefined) {
//       // startTime이 undefined인 경우 endTime을 설정
//       endTime = new Date(
//         selectedDate + "T" + mysql_data.sleep_info[0].end_sleep
//       );
//     } else {
//       // startTime이 정의된 경우 다음 항목의 event_time을 endTime으로 사용
//       endTime = new Date(
//         selectedDate + "T" + arr[index + 1].event_time
//       );
//     }
//   } else {
//     startTime = new Date(
//       selectedDate + "T" + arr[arr.length - 1].event_time
//     );
//     endTime = new Date(
//       selectedDate + "T" + mysql_data.sleep_info[0].end_sleep
//     );
//   }

//   return {
//     label: event.sleep_event,
//     data: [startTime, endTime],
//     barThickness: 20,
//     backgroundColor: "#99ccff",
//     borderRadius: 10,
//     borderSkipped: false,
//   };
// }),
