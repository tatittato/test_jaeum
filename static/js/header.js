const setupDropdownMenu = () => {
  document.querySelector(".capButton")?.addEventListener("click", () => {
    redirectTo("/record");
  });
  document.querySelector(".scoreButton")?.addEventListener("click", () => {
    redirectTo("/score");
  });
  document.querySelector(".statisticsButton")?.addEventListener("click", () => {
    redirectTo("/statistics");
  });
  document.querySelector(".timelineButton")?.addEventListener("click", () => {
    redirectTo("/timeline");
  });
};

setupDropdownMenu();
