(() => {
    function dynamicThingieImageInputs() {
        const form = document.querySelector('#add-product');

        if (!form.length) return;

        const addImageBtn = document.querySelector('#add-image');
        const totalFormsets = document.querySelector(
            '#id_image_set-TOTAL_FORMS'
        );
        const maxFormsets = parseInt(
            document.querySelector('#id_image_set-MAX_NUM_FORMS').value
        );
        let formCount = parseInt(totalFormsets.value);
        // deliberate use of a live nodelist
        const formsets = form.getElementsByClassName('image-form');

        addImageBtn.addEventListener('click', (e) => {
            if (formCount >= maxFormsets) return;

            if (formCount === maxFormsets - 1) {
                addImageBtn.style.display = 'none';
            }

            const newFormset = formsets[0].cloneNode(true);
            newFormset.innerHTML = newFormset.innerHTML.replace(
                /set-0/g,
                `set-${formCount}`
            );
            const lastFormset = formsets[formsets.length - 1];
            lastFormset.insertAdjacentElement('afterend', newFormset);
            formCount++;
            totalFormsets.setAttribute('value', formCount);
        });
    }

    dynamicThingieImageInputs();
})();
