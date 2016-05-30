//To show/hide loading indicator
function toggleSpinner() {
  var $ele = $('.loading');

  if ($ele.hasClass("hide")) {
    $ele.removeClass("hide");
  }
  else {
    $ele.addClass("hide");
  }
}

//To call hackerNews API
$(function () {
  if (!navigator.onLine) {
    $("#turn-on-notification").attr("disabled", true);
    $(".custom-checkbox").addClass("offline");
    toggleSpinner();
  }
  else {
    getStories();
  }

  function getStories() {
    var url = "http://hacker-news.firebaseio.com/v0/newstories.json";

    $.ajax({
      url: url,
      method: "GET",
      success: function (response) {
        var response = response.splice(1, 20);
        response.map(function (contentId) {
          return(getContents(contentId));
        });

        toggleSpinner(); //To hide spinner
      },
      error: function (error) {
        console.error(error);
      }
    });
  }

  //To get stories in hackerNews
  function getContents(contentId) {
    var contentUrl = "https://hacker-news.firebaseio.com/v0/item/" + contentId + ".json";
    var contentUrl = "http://localhost:8000/get_listing"

    $.ajax({
      url: contentUrl,
      method: "GET",
      success: function (response) {
        $("#main").append(
          
                    "<div class='container'>" +
                    "<div class='mdl-card__title'>"+
                    "    <h2 class='mdl-card__title-text'>" + response['name'] + "</h2>"+
                    "</div>" +
                    "<span>" + response['user'] + "</span> trusted by <span class='author'>" + response['reviews'] + " users, 33 reviews</span>" +
                    "<button class='mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect'>"+
                    "<i class='material-icons'>vert</i>"+
                    "</button>"+
                    "<a href='/new_profile' target='_blank' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'> I'm trust</a>" +
                    "<a href='/new_profile' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'> Add a Review</a>"+

                    "</div>"
        );
        console.log(response['status'],response)
      },
      error: function (error) {
        console.error(error);
      }
    });
  }



  //To get stories in hackerNews
  function getContentsProfile() {

    var contentUrl = "http://localhost:8000/get_listing"

    $.ajax({
      url: contentUrl,
      method: "GET",
      success: function (response) {
        $("#main").append(
                    "<div class='container'>" +


                    ""+
                    "<div class='mdl-card__title'>"+
                    "    <img src='"+ response['picture'] +"' class='demo-avatar'>&nbsp;&nbsp;<h2 class='mdl-card__title-text'>" + response['name'] + "</h2>"+
                    "</div>" +
                    "<span>" + response['user'] + "</span> trusted by <span class='author'>" + response['reviews'] + " users, 33 reviews</span>" +
                    "<button class='mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect'>"+
                    "<i class='material-icons'>vert</i>"+
                    "</button>"+
                    "<a href='/new_profile' target='_blank' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'> I'm trust</a>" +
                    "<a href='/new_profile' class='mdl-button mdl-button--colored mdl-js-button mdl-js-ripple-effect'> Add a Review</a>"+

                    "</div>"
        );
        console.log(response['status'],response)
      },
      error: function (error) {
        console.error(error);
      }
    });
  }



  //Hamburger menu function
  $("#menu-overlay, .menu-icon, #menu a").on("click", function (event) {
    event.stopPropagation();

    var $menuEle = $('#menu');

    if ($menuEle.hasClass("visible")) {
      $menuEle.removeClass("visible");
      $("#menu-overlay").removeClass("visible");
    }
    else {
      $menuEle.addClass("visible");
      $("#menu-overlay").addClass("visible");
    }

  });


  /*
    To find device is online or offline
  */

  function onLineStatus(event) {
    console.log("Online: ", navigator.onLine);
    if (navigator.onLine) {
      $("#sw-offline-state").attr("data-offline", false);
      $("#sw-offline-state").html("✕");
      $("#turn-on-notification").attr("disabled", false);
      $(".custom-checkbox").removeClass("offline");
    }
    else {
      $("#sw-offline-state").attr("data-offline", true);
      $("#sw-offline-state").html("✓");
    }
  }

  //Event listener for offline/online events
  window.addEventListener("online", onLineStatus);
  window.addEventListener("offline", onLineStatus);
});
