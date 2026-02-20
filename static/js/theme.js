(function () {
  var root = document.documentElement;
  var key = "theme";
  var toggle = function () {
    var isDark = root.classList.contains("dark");
    if (isDark) {
      root.classList.remove("dark");
      localStorage.setItem(key, "light");
    } else {
      root.classList.add("dark");
      localStorage.setItem(key, "dark");
    }
  };

  var stored = localStorage.getItem(key);
  if (stored === "dark") {
    root.classList.add("dark");
  }
  if (stored === "light") {
    root.classList.remove("dark");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var button = document.getElementById("theme-toggle");
    if (button) {
      button.addEventListener("click", toggle);
    }
  });
})();
