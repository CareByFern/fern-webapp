

function wait(cb, ms) {
  setTimeout(function(){ cb(); }, ms);
}

// Run a phase sequence
function run_phases(phasearr, idx) {

  // Check if we have something to do
  if (idx >= phasearr.length) return;

  // Get and run the function with a callback to trigger next phase
  var self = this;
  var fn = phasearr[idx];
  fn(function(){
    setTimeout(function(){
      self.run_phases(phasearr, idx+1);
    }, 1);
  });

};

function move(direction, delay=1000) {
  var phases = [
    function(cb) {
      // What does setWheelTorqueEnabled do? I assume (1) is on
      // and 0 is off...
      Ohmni.setWheelTorqueEnabled(1);
      wait(cb, delay);
    },
    function(cb) {
      Ohmni.move(direction*400, -1*direction*400, 500);
      wait(cb, delay);
    },
  ];
  run_phases(phases, 0);
}

function turn(direction, delay=100) {
  var phases = [
    function(cb) {
      // What does setWheelTorqueEnabled do? I assume (1) is on
      // and 0 is off...
      Ohmni.setWheelTorqueEnabled(1);
      wait(cb,delay);
    },
    function(cb) {
      Ohmni.move(-direction*400, -direction*400, 500);
      wait(cb, delay);
    },
  ];
  run_phases(phases, 0);
}

function moveHead(direction) {
  Ohmni.move(-direction*400, -direction*400, 100);
}





Pusher.logToConsole = true;

var pusher = new Pusher('3ae6efd2a964f03f1f82', {
      cluster: 'us2',
      encrypted: true
    });

var channel = pusher.subscribe('my-channel');
    channel.bind('my-event', function(data) {
      console.log("got key " + data.key);
      if (data.key === 'ArrowUp') {
        move(1);
      } else if (data.key === 'ArrowDown') {
        move(-1);
      } else if (data.key === 'ArrowLeft') {
        turn(1);
      } else if (data.key === 'ArrowRight') {
        turn(-1);
      }
    });
