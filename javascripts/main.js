(function () {

  //
  // hide header and footer
  //

  var footer = document.getElementsByTagName('footer');
  if (footer.length) {
    footer[0].style.visibility = 'hidden';
  }

  var header = document.getElementsByTagName('header');
  if (header.length) {
    var maintained = header[0].lastElementChild;
    if (maintained) {
      maintained.style.visibility = 'hidden';
    }
  }

}());
