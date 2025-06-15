document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("toggleSidebar");
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("main-content");

  toggleBtn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");
  });
});
