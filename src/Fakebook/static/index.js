//SIDEBAR
const menuItems = document.querySelectorAll('.menu-item');

//removing actie class from menu items
const changeActiveItem = () => {
    menuItems.forEach(item => {
        item.classList.remove('active');
    })
}

menuItems.forEach(item => {
    item.addEventListener('click', () => {
        changeActiveItem();
        item.classList.add('active');
    })
})

document.addEventListener('DOMContentLoaded', function () {
    var profileImg = document.getElementById('profileImg');
    var profileOptions = document.getElementById('profileOptions');

    // Toggle popup visibility
    profileImg.onclick = function () {
        profileOptions.style.display = profileOptions.style.display === 'block' ? 'none' : 'block';
    };

    // Close the popup when clicking outside of it
    window.onclick = function (event) {
        if (event.target !== profileImg && event.target !== profileOptions) {
            profileOptions.style.display = 'none';
        }
    };
});

// Edit bio function
function EditBio() {
    let textbox = document.getElementById("bio-textbox")
    let saveBtn = document.getElementById("bio-submit")

    if (textbox.readOnly === true) {
        textbox.readOnly = false
        saveBtn.removeAttribute("hidden")
    }
}