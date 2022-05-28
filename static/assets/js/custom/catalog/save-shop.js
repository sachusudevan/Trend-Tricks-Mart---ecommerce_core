"use strict";

// Class definition
var KTAppEcommerceSaveProduct = function () {
    var Delta = Quill.import('delta');

    // Init quill editor
    const initQuill = () => {
        // Define all elements for quill editor
        const elements = [
            '#kt_ecommerce_add_shop_description',
            '#kt_ecommerce_add_shop_meta_description'
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
        const form = document.getElementById('ecommerce-shop-form');
        const submitButton = document.getElementById('ecommerce_add_shop_submit');

        validator = FormValidation.formValidation(
            form,
            {
                fields: {
                    'shop_name': {
                        validators: {
                            notEmpty: {
                                message: 'Shop name is required'
                            }
                        }
                    },
                    'country': {
                        validators: {
                            notEmpty: {
                                message: 'Country name is required'
                            }
                        }
                    },
                    'state': {
                        validators: {
                            notEmpty: {
                                message: 'State name is required'
                            }
                        }
                    },
                    'city': {
                        validators: {
                            notEmpty: {
                                message: 'City name is required'
                            }
                        }
                    },
                    'zip_code': {
                        validators: {
                            notEmpty: {
                                message: 'Zip code is required'
                            }
                        }
                    },
                    'street_address': {
                        validators: {
                            notEmpty: {
                                message: 'Street address is required'
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


            var shopDescription = document.querySelector('#kt_ecommerce_add_shop_description')
            $('#shop_description').val(shopDescription.children[0].innerHTML);

            var shopMetaDescription = document.querySelector('#kt_ecommerce_add_shop_meta_description')
            $('#shop_meta_description').val(shopMetaDescription.children[0].innerHTML);

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