var CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;

var faceWindow;

function openFaceWindow() {
  faceWindow = window.open("/static/giver/face.html", 'face',
      'width=640,height=452,resizable,scrollbars=false,status');
}

function enableForm() {
  document.getElementById('status').disabled = false;
  document.getElementById('notes').disabled  = false;
  document.getElementById('update').disabled = false;
}

function disableForm() {
  document.getElementById('status').disabled = true;
  document.getElementById('notes').disabled  = true;
  document.getElementById('update').disabled = true;
}

function submitReport() {
  var statusElt = document.getElementById('status');
  var notesElt = document.getElementById('notes');
  var updateBtn = document.getElementById('update');
  if (statusElt.value === '') {
    console.log('not submitting empty status report');
    return;
  }
  console.log("submit report", statusElt.value);
  disableForm();

  fetch('/care/api/update_status.json', {
    method: 'post',
    headers: {
      "X-CSRFToken": CSRF_TOKEN,
      "Content-type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
    credentials: 'include',
    body: 'new_status=' + statusElt.value + '&new_notes=' + notesElt.value,
  })
  .then(
    function(resp) {
      if (resp.status !== 200) {
        console.error('Looks like there was a problem. Status Code: ' +
          resp.status);
        enableForm();
        return;
      }

      // Examine the text in the response
      resp.json().then(function(data) {
        console.log('success!!!');
        console.log(data);
        statusElt.value = '';
        notesElt.value = '';
        enableForm();
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    enableForm();
  });
}
