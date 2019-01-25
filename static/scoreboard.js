   function toggle_visibility(event) {;
       let element = event.currentTarget;
       if(element.style.display == 'block') {
          element.style.display = 'none';
       } else {
          element.style.display = 'block';
       }
   }
