"use strict";

// Class definition
var KTAppEcommerceSaveProduct = function () {
    var Delta = Quill.import('delta');

    // Init quill editor
    const initQuill = () => {
        // Define all elements for quill editor
        const elements = [
            '#kt_ecommerce_add_manufacture_description',
            '#kt_ecommerce_add_manufacture_meta_description'
        ];

        // Loop all elements
        elements.forEach(element => {
            // Get quill element
            let quill = document.querySelector(element);

            // Break if element not found
            if (!quill) {
                return;
            }

            // Init quill --- more info: https://quilljs.com/docs/quickstart/
            quill = new Quill(element, {
                modules: {
                    toolbar: [
                        [{
                            header: [1, 2, false]
                        }],
                        ['bold', 'italic', 'underline'],
                        ['image', 'code-block']
                    ]
                },
                placeholder: 'Type your text here...',
                theme: 'snow' // or 'bubble'
            });

        });
    }


    const handleSubmit = () => {
        let validator;

        // Get elements
        const form = document.getElementById('ecommerce-manufacture-form');
        const submitButton = document.getElementById('ecommerce_add_manufacture_submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'manufacture_name': {
                        validators: {
                            notEmpty: {
                                message: 'Manufacture name is required'
                            }
                        }
                    },
                    'group_id': {
                        validators: {
                            notEmpty: {
                                message: 'Group is required'
                            }
                        }
                    },
                },
                plugins: {
                    trigger: new FormValidation.plugins.Trigger(),
                    bootstrap: new FormValidation.plugins.Bootstrap5({
                        rowSelector: '.fv-row',
                        eleInvalidClass: '',
                        eleValidClass: ''
                    })
                }
            }
        );

        // Handle submit button
        submitButton.addEventListener('click', e => {
            e.preventDefault();


            var manufactureDescription = document.querySelector('#kt_ecommerce_add_manufacture_description')
            $('#manufacture_description').val(manufactureDescription.children[0].innerHTML);

            // Validate form before submit
            if (validator) {
                validator.validate().then(function (status) {
                    console.log('validated!');

                    if (status == 'Valid') {
                        submitButton.setAttribute('data-kt-indicator', 'on');

                        // Disable submit button whilst loading
                        submitButton.disabled = true;
                        submitButton.removeAttribute('data-kt-indicator');
                        // Enable submit button after loading
                        submitButton.disabled = false;

                        // Redirect to customers list page
                        form.submit();

                    } else {
                        Swal.fire({
                            html: "Sorry, looks like there are some errors detected, please try again.",
                            icon: "error",
                            buttonsStyling: false,
                            confirmButtonText: "Ok, got it!",
                            customClass: {
                                confirmButton: "btn btn-primary"
                            }
                        });
                    }
                });
            }
        })
    }

    
    // Public methods
    return {
        init: function () {
            // Init forms
            initQuill();

            handleSubmit();
        }
    };
}();

// On document ready
KTUtil.onDOMContentLoaded(function () {
    KTAppEcommerceSaveProduct.init();
});