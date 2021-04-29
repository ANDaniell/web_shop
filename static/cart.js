$(document).ready(function () {
  $(".btn-add-cart").click(function () {
    var id = $(this).attr("value");
    $.ajax({
      type: "POST",
      url: '/addtocart',
      // dataType: "json",
      contentType: "application/json",
      data: JSON.stringify({id_tov: id})
      });
  });
});