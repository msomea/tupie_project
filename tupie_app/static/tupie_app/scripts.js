document.addEventListener('DOMContentLoader', function(){
    const regionSelect = document.getElementById('id_region');
    const districtSelect = document.getElementById('id_district');
    const wardSelect = document.getElementById('id_ward');
    const placeSelect = document.getElementById('id_place');

    function populateDropdown(selectElement, options) {
        selectElement.innerHTML = '<option value="">Select</option>';
        options.forEach(option =>{
            const opt = document.createElement('option');
            opt.value = option.id; // Use id or code based on model
            opt.textContent = option.name; //Adjust based on API response
            selectElement.appendChild(opt);
        });
    }

    function fetchDistricts(regionCode) {
        fetch('/get_districts/?region=${regionCode}')
        .then(response => response.json())
        then(data => populateDropdown(districtSelect, data))
        .catch(error => console.error('Error:', error));
    }

    function fetchWards(districtCode) {
        fetch('/get_wards/?district=${districtCode}')
        .then(response => response.json())
        then(data => populateDropdown(wardSelect, data))
        .catch(error => console.error('Error:', error));
    }

    function fetchPlaces(districtCode) {
        fetch('/get_places/?ward=${wardCode}')
        .then(response => response.json())
        then(data => populateDropdown(placeSelect, data))
        .catch(error => console.error('Error:', error));
    }

    regionSelect.addEventListener('change', function(){
        const regionCode  = this.value;
        if (regionCode) {
            fetchDistricts(regionCode);
            wardSelect.innerHTML = '<option value="">Select Ward</option>';
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        } else {
            districtSelect.innerHTML = '<option value="">Select District</option>';
            wardSelect.innerHTML = '<option value="">Select Ward</option>';
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        }
    });

    districtSelect.addEventListener('change', function(){
        const districtCode  = this.value;
        if (districtCode) {
            fetchWards(districtCode);
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        } else {
            wardSelect.innerHTML = '<option value="">Select Ward</option>';
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        }
    });

    wardSelect.addEventListener('change', function(){
        const wardCode  = this.value;
        if (wardCode) {
            fetchPlaces(wardCode);
        } else {
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        }
    });
});