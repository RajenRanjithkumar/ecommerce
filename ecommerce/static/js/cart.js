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

        //guest user
        addCookieItem(productId, action)

      }else{
        //console.log("User logged in")
        updateUserOrder(productId, action)

      }

      
    });
  }

  function addCookieItem(productId, action){

    console.log("Not logged in")


    if (action == 'add'){
      //since the cart variable is in main.html we have access to it
      if (cart[productId] == undefined){

        cart[productId] = {'quantity': 1}

      }else{

        cart[productId]['quantity'] += 1

      }

    }


    if (action == 'remove'){
      //since the cart variable is in main.html we have access to it

        // add a button to delete the quantity
        if(cart[productId]['quantity'] <= 0){

          console.log("Remove Item")
          delete cart[productId];
        }else{

          cart[productId]['quantity'] -= 1
        
        }  

    }

    if (action == 'delete'){
      //since the cart variable is in main.html we have access to it

      // delete the item
      console.log("Remove Item")
      delete cart[productId];

    }

    

    console.log("Cart:", cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()


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
        //history.go(0)
        location.reload()

    })



  } 
  