var copyVideo = false;

function setupVideo(url) {
  const video = document.createElement('video');

  var playing = false;
  var timeupdate = false;

  video.autoplay = true;
  video.muted = true;
  video.loop = true;

  video.addEventListener('playing', function() {
    playing = true;
    checkReady();
  }, true);

  video.addEventListener('timeupdate', function() {
    timeupdate = true;
    checkReady();
  }, true);

  video.src = url;
  video.play();

  function checkReady() {
    if(playing && timeupdate) {
      copyVideo = true;
    }
  }

  return video;
}
