//
// Main js
//

"use strict";

(function () {
  $(".handle_tag").click(function (e) {
    e.preventDefault();

    const btn = $(this);
    const url = btn.attr("data-href");
    $("#modal_area").empty();

    $.ajax({
      method: "GET",
      dataType: "json",
      url: url,

      success: function (data) {
        $("#modal_area").html(data.result);
        $("#myModal").modal("show");
      },
    });
    //alert("aca Nestor Update");
  });
  var ano = new Date().getFullYear();
  $("#yearf").text(ano);
})();
