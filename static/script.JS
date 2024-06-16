const dialogue = document.getElementById("dialog");
function close_dialog() {
  event.preventDefault();
  dialogue.close();
}
function open_dialog() {
  dialogue.showModal();
}