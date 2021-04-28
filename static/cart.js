function addGoodToCart(productId) {
  var currentCart = localStorage.getItem("current_cart", null);
  if (currentCart == null) {
    currentCart = [];
  }
  if (typeof currentCart == "string") {
    var currentCart = currentCart.split(',');
  }

  if (currentCart.indexOf(productId.toString()) == -1) {
    currentCart.push(productId);
    localStorage.setItem("current_cart", currentCart);
    alert(localStorage.getItem("current_cart"));
  }
}
