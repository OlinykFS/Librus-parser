
$(document).ready(function () {
  $(".klasy-link").click(function (e) {
    e.preventDefault();
    $.ajax({
      url: "/klasy",
      type: "GET",
      beforeSend: function () {
        $(".dynamic-content").html("<p>Ladownaie...</p>");
      },
      success: function (response) {
        $(".dynamic-content").html(response);
      },
      error: function (error) {
        console.log("Error:", error);
        $(".dynamic-content").html("<p>Error</p>");
      },
    });
  });

  $(".ndst-link").click(function (e) {
    e.preventDefault();

    $.ajax({
      url: "/ocfr_niedostateczne",
      type: "GET",
      beforeSend: function () {
        $(".dynamic-content").html("<p>Ładowanie...</p>");
      },
      success: function (response) {
        $(".dynamic-content").html(response);
      },
      error: function (error) {
        console.log("Error:", error);
        $(".dynamic-content").html("<p>Error</p>");
      },
    });
  });

  $(document).on("click", ".load-students", function (e) {
    e.preventDefault();
    const classId = $(this).data("class-id");
    const className = $(this).data("class-name");
    $.ajax({
      url: `/lista_uczniow/${classId}`,
      type: "GET",
      beforeSend: function () {
        $(".dynamic-content").html("<p>Ładowanie...</p>");
      },
      success: function (response) {
        $(".dynamic-content").html(response);
        $(".dynamic-content-stats-klasa").html(className);
      },
      error: function (error) {
        console.log("Error:", error);
        $(".dynamic-content").html("<p>Error</p>");
      },
    });
  });

  $(document).on("click", ".load-students-data", function (e) {
    e.preventDefault();
    const uczenName = $(this).data("class-name");
    const student_id = $(this).data("class-id");
    const uczenId = $(this).data("class-uczenid");

    $.ajax({
      url: `/uczen_data/${student_id}`,
      type: "GET",
      beforeSend: function () {
        $(".dynamic-content").html("<p>Ładowanie...</p>");
      },
      success: function (response) {
        $(".dynamic-content-stats-uczen").html(uczenName);
        $(".dynamic-content-stats-uczenId").html(uczenId);
        $(".dynamic-content").html(response);
      },
      error: function (error) {
        console.log("Error:", error);
        $(".dynamic-content").html("<p>Error</p>");
      },
    });
  });
  $(document).ready(function () {
    $.ajax({
      url: "/teacher_schedule",
      type: "GET",
      beforeSend: function () {
        $(".dynamic-content").html("<p>Ładowanie...</p>");
      },
      success: function (response) {
        $(".dynamic-content").html(response);
      },
      error: function (error) {
        console.log("Error:", error);
        $(".dynamic-content").html("<p>Error</p>");
      },
    });
  });
  $("#logout-link").click(function (e) {
    e.preventDefault();
    if (confirm("Czy na pewno chcesz się wylogować?")) {
      $.ajax({
        url: "/logout",
        type: "POST",
        success: function (response) {
          if (response.success) {
            window.location.href = response.redirect;
          }
        },
        error: function (xhr, status, error) {
          alert("Wystąpił błąd. Spróbuj ponownie.");
        },
      });
    }
  });
});
