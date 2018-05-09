
document.addEventListener('keydown', (event)=>{
  const keyName = event.key;
  $.post(window.location.pathname,{key:keyName});
});