function initMap() {
    const myLatLng = {
        lat: 53.3559,
        lng: -6.3298
    };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: myLatLng,
    });
    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "Restaurant",
    });
}