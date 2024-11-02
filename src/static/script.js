window.addEventListener("load", function () {

  var socket = io();

  socket.on('update', function (data) {
    console.log(data);
    let title = document.querySelector('#data-title');
    if (title)
      title.innerHTML = data.title;

    let artist = document.querySelector('#data-artist');
    if (artist)
      artist.innerHTML = data.artist;

    let output = document.querySelector("#data-output");
    if (output)
      output.innerHTML = data.output;

    let cover = document.querySelector('#data-cover');
    if (cover)
      cover.src = data.cover_link;

    // TODO: progress bar calculation
  });

});