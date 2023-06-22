var updateBtn = document.getElementsByClassName("update-cart")


for (var i = 0; i < updateBtn.length; i++) {

    // Add click event listener to current element
    updateBtn[i].addEventListener('click', function() {
      // Handle click event here

        // get the product values from the front end
        var productId = this.dataset.product
        var action = this.dataset.action
        
      console.log("productId:", productId, "action:", action);

      console.log("User", user)
      if(user == "AnonymousUser"){

        console.log("Not logged in")

      }else{
        console.log("User logged in")

      }

      
    });
  }