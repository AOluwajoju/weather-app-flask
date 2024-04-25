function updatePromptText() {
  var selectBox = document.getElementById("parameter");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  var prompt = document.getElementById("inputPrompt");

  // Update label based on selected value
  if (selectedValue === "coords") {
    prompt.innerHTML =
      "Enter Latitude & Longitude separated by a comma (eg. 4.55, 4.55).:";
  } else if (selectedValue === "city") {
    prompt.innerHTML = "Enter City/Location Name:";
  }
}

function detectLocation() {
  // detect current location with geolocation
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const pos = {
        lat: position.coords.latitude,
        long: position.coords.longitude,
      };

      document.getElementById("value").value = `${pos.long},${pos.lat}`;
      document.getElementById("parameter").value = "coords";
      document.getElementById("location").value = 1;

      // Trigger form submission
      document.getElementById("weatherForm").submit();
      document.getElementById("location").value = 0;
    },

    (error) => {
      // Error callback: Handle location error
      error = document.getElementById("detectError");
      if (error.code === error.PERMISSION_DENIED) {
        error.innerHTML = "Access Denied. Please Allow to location detection.";
      } else if (error.code === error.POSITION_UNAVAILABLE) {
        error.innerHTML = "Location information is unavailable.";
      } else if (error.code === error.TIMEOUT) {
        error.innerHTML = "The request to get user location timed out.";
      } else {
        error.innerHTML = "Something went wrong.";
      }
    }
  );
}

function viewLocation(longitude, latitude) {
  document.getElementById("value").value = `${longitude},${latitude}`;
  document.getElementById("parameter").value = "coords";

  // Trigger form submission
  document.getElementById("weatherForm").submit();
}
