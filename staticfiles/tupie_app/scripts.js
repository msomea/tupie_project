document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('id_region');
    const districtSelect = document.getElementById('id_district');
    const wardSelect = document.getElementById('id_ward');
    const placeSelect = document.getElementById('id_place');
    const locationLine = document.getElementById('location-line');

    function populateDropdown(selectElement, options, valueKey, labelKey) {
        selectElement.innerHTML = '<option value="">Select</option>';
        options.forEach(option => {
            const opt = document.createElement('option');
            opt.value = option[valueKey];
            opt.textContent = option[labelKey];
            selectElement.appendChild(opt);
        });
    }

    function fetchData(url, selectElement, valueKey, labelKey) {
        fetch(url)
            .then(response => response.json())
            .then(data => populateDropdown(selectElement, data, valueKey, labelKey))
            .catch(error => console.error('Error:', error));
    }

    function updateLocationLine() {
        const regionText = regionSelect.options[regionSelect.selectedIndex]?.text || '';
        const districtText = districtSelect.options[districtSelect.selectedIndex]?.text || '';
        const wardText = wardSelect.options[wardSelect.selectedIndex]?.text || '';
        const placeText = placeSelect.options[placeSelect.selectedIndex]?.text || '';

        const locationPreview = [regionText, districtText, wardText, placeText]
            .filter(Boolean)
            .join(' > ');

        if (locationLine) {
            locationLine.textContent = locationPreview || 'No location selected yet.';
        }
    }

    regionSelect.addEventListener('change', function () {
        const regionId = this.value;
        if (regionId) {
            fetchData(`/get_districts/?region=${regionId}`, districtSelect, 'district_code', 'district_name');
            wardSelect.innerHTML = '<option value="">Select Ward</option>';
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        } else {
            districtSelect.innerHTML = '<option value="">Select District</option>';
            wardSelect.innerHTML = '<option value="">Select Ward</option>';
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        }
        updateLocationLine();
    });

    districtSelect.addEventListener('change', function () {
        const districtId = this.value;
        if (districtId) {
            fetchData(`/get_wards/?district=${districtId}`, wardSelect, 'ward_code', 'ward_name');
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        } else {
            wardSelect.innerHTML = '<option value="">Select Ward</option>';
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        }
        updateLocationLine();
    });

    wardSelect.addEventListener('change', function () {
        const wardId = this.value;
        if (wardId) {
            fetchData(`/get_places/?ward=${wardId}`, placeSelect, 'id', 'place_name');
        } else {
            placeSelect.innerHTML = '<option value="">Select Place</option>';
        }
        updateLocationLine();
    });

    placeSelect.addEventListener('change', updateLocationLine);
});
