$(document).ready(function() {
    require([
    "esri/config",
    "esri/Map",
    "esri/views/MapView",
    "esri/widgets/Locate",
    "esri/widgets/Search",
    "esri/rest/locator"
], function (esriConfig, Map, MapView, Locate, Search, locator) {
    esriConfig.apiKey = arcgis_key;

    const map = new Map({
        basemap: "arcgis-navigation"
    });

    const view = new MapView({
        container: "viewDiv",
        map: map,
        center: [-74.034775, 40.745255],
        zoom: 15
    });

    const locate = new Locate({
        view: view,
        rotationEnabled: false,
        goToOverride: function (view, options) {
            options.target.scale = 1500;
            return view.goTo(options.target);
        }
    });

    view.ui.add(locate, "top-left");

    const serviceUrl = "http://geocode-api.arcgis.com/arcgis/rest/services/World/GeocodeServer";

    function handleClick(evt) {
        infoPopup.style.display = "none";

        const params = {
            location: evt.mapPoint
        };

        locator.locationToAddress(serviceUrl, params).then(
            function (response) {
                const address = response.address;
                showAddress(address, evt.mapPoint);
            },
            function (err) {
                showAddress("No address found.", evt.mapPoint);
            }
        );
        
        // User clicks map and we are sending the address to Flask
        const address = response.address;

        // Save to JSON file through server-side
        $.ajax({
            url: '/save_address',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ address: address }),
        }).done(function(response) {
            console.log("Address saved: ", response);
        });
    }

    function showAddress(address, pt) {
        view.openPopup({
            title: "Address Selected",
            content: address,
            location: pt,
            actions: [],
            dockEnabled: false,
            visible: false
        });
    }

    view.on("click", handleClick);

    const search = new Search({
        view: view
    });

    view.ui.add(search, "top-right");


    $('#street').on('change', function() {
        let selected_street = $(this).val();
        $.getJSON(`/get_side/${selected_street}`, function(data) {
            updateDropdown('#side', data.side);
        });
    });

    $('#side').on('change', function() {
        let selected_street = $('#street').val();
        let selected_side = $(this).val();
        $.getJSON(`/get_data/${selected_street}/${selected_side}`, function(data) {
            updateDropdown('#location', Object.keys(data));
        });
    });

    $('#location').on('change', function() {
        let selected_location = $(this).val();
        let selected_street = $('#street').val();
        let selected_side = $('#side').val();
        $.getJSON(`/get_data/${selected_street}/${selected_side}`, function(data) {
            $('#days-hours').text(data[selected_location]);
        });
    });

    function updateDropdown(dropdownId, values) {
        $(dropdownId).empty();
        values.forEach(val => {
            $(dropdownId).append(new Option(val, val));
        });
        $(dropdownId).trigger('change');
    }

    $('#street').trigger('change');
    });

    function waitForElement(selector, callback) {
        if (document.querySelector(selector)) {
          callback();
        } else {
          setTimeout(() => waitForElement(selector, callback), 300);
        }
    }

    // Add text to explain the current location button
    waitForElement('.esri-locate', function() {
        const targetButton = document.querySelector('.esri-locate');
        const infoPopup = document.createElement('div');
        infoPopup.id = 'infoPopup';
        infoPopup.textContent = 'Press this button to find your current location';
        // Styling
        infoPopup.style.position = 'relative';
        infoPopup.style.fontFamily = 'Tahoma, Geneva, sans-serif';
        infoPopup.style.fontSize = '20px';
        infoPopup.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
        infoPopup.style.color = 'black';
        infoPopup.style.padding = '1px';
        infoPopup.style.borderRadius = '5px';   
        infoPopup.style.boxShadow = '0 2px 4px rgba(0,0,0,0.1)';
        
        targetButton.parentNode.insertBefore(infoPopup, targetButton.nextSibling);
    
        // Add event listeners to hide the text on various interactions
        document.addEventListener('mousedown', function() {
            const infoPopup = document.getElementById('infoPopup');
            if (infoPopup) {
                infoPopup.style.display = 'none';
        }
        });
    });
});
