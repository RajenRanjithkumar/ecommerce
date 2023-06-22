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
        //console.log("User logged in")
        updateUserOrder(productId, action)

      }

      
    });
  }

  function updateUserOrder(productId, action){


    console.log("User is loggged in, sendind data..")

    var url = "/update_item/"

    fetch(url, {
        method: 'POST',
        headers:{
                'Content-Type':'application/json',
                "X-CSRFToken" : csrftoken
        },
        body:JSON.stringify({

            'productID': productId,
            'action': action
        
        })

    })
    .then((response) =>{

            return response.json()
    })

    .then((data) =>{

        console.log('data:', data)
    })



  } 
  