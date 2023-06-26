"use strict";

// Class Definition
var KTLogin = function() {
	var _buttonSpinnerClasses = 'spinner spinner-right spinner-white pr-15';

	var _handleFormSignin = function() {
		var form = KTUtil.getById('kt_login_singin_form');
		var formSubmitUrl = KTUtil.attr(form, 'action');
		var formSubmitButton = KTUtil.getById('kt_login_singin_form_submit_button');

		//$('#kt_login_singin_form_submit_button').on('click', function () {

		//	KTUtil.btnWait(formSubmitButton, _buttonSpinnerClasses, "Please wait");

		//	// Simulate Ajax request
		//	setTimeout(function () {
		//		KTUtil.btnRelease(formSubmitButton);
		//	}, 3000);
		//});

		//if (!form) {
		//	return;
		//}

		//FormValidation
		//    .formValidation(
		//        form,
		//        {
		//            fields: {
		//				username: {
		//					validators: {
		//						notEmpty: {
		//							message: 'Username is required'
		//						}
		//					}
		//				},
		//				password: {
		//					validators: {
		//						notEmpty: {
		//							message: 'Password is required'
		//						}
		//					}
		//				}
		//            },
		//            plugins: {
		//				trigger: new FormValidation.plugins.Trigger(),
		//				submitButton: new FormValidation.plugins.SubmitButton(),
	 //           		//defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // Uncomment this line to enable normal button submit after form validation
		//				bootstrap: new FormValidation.plugins.Bootstrap({
		//				//	eleInvalidClass: '', // Repace with uncomment to hide bootstrap validation icons
		//				//	eleValidClass: '',   // Repace with uncomment to hide bootstrap validation icons
		//				})
		//            }
		//        }
		//    )
		//    .on('core.form.valid', function() {
		//		// Show loading state on button
		//		KTUtil.btnWait(formSubmitButton, _buttonSpinnerClasses, "Please wait");

		//		// Simulate Ajax request
		//		setTimeout(function() {
		//			KTUtil.btnRelease(formSubmitButton);
		//		}, 2000);

		//		// Form Validation & Ajax Submission: https://formvalidation.io/guide/examples/using-ajax-to-submit-the-form
		//		/**
		//        FormValidation.utils.fetch(formSubmitUrl, {
		//            method: 'POST',
		//			dataType: 'json',
		//            params: {
		//                name: form.querySelector('[name="username"]').value,
		//                email: form.querySelector('[name="password"]').value,
		//            },
		//        }).then(function(response) { // Return valid JSON
		//			// Release button
		//			KTUtil.btnRelease(formSubmitButton);

		//			if (response && typeof response === 'object' && response.status && response.status == 'success') {
		//				Swal.fire({
		//	                text: "All is cool! Now you submit this form",
		//	                icon: "success",
		//	                buttonsStyling: false,
		//					confirmButtonText: "Ok, got it!",
		//					customClass: {
		//						confirmButton: "btn font-weight-bold btn-light-primary"
		//					}
		//	            }).then(function() {
		//					KTUtil.scrollTop();
		//				});
		//			} else {
		//				Swal.fire({
		//	                text: "Sorry, something went wrong, please try again.",
		//	                icon: "error",
		//	                buttonsStyling: false,
		//					confirmButtonText: "Ok, got it!",
		//					customClass: {
		//						confirmButton: "btn font-weight-bold btn-light-primary"
		//					}
		//	            }).then(function() {
		//					KTUtil.scrollTop();
		//				});
		//			}
		//        });
		//		**/
		//    })
		//	.on('core.form.invalid', function() {
		//		Swal.fire({
		//			text: "Sorry, looks like there are some errors detected, please try again.",
		//			icon: "error",
		//			buttonsStyling: false,
		//			confirmButtonText: "Ok, got it!",
		//			customClass: {
		//				confirmButton: "btn font-weight-bold btn-light-primary"
		//			}
		//		}).then(function() {
		//			KTUtil.scrollTop();
		//		});
		//    });
    }

	var _handleFormForgot = function() {
		var form = KTUtil.getById('kt_login_forgot_form');
		var formSubmitUrl = KTUtil.attr(form, 'action');
		var formSubmitButton = KTUtil.getById('kt_login_forgot_form_submit_button');

		if (!form) {
			return;
		}

		FormValidation
		    .formValidation(
		        form,
		        {
		            fields: {
						email: {
							validators: {
								notEmpty: {
									message: 'Required Field'
								},
								emailAddress: {
									message: 'The value is not a valid email address'
								}
							}
						}
		            },
		            plugins: {
						trigger: new FormValidation.plugins.Trigger(),
						submitButton: new FormValidation.plugins.SubmitButton(),
	            		//defaultSubmit: new FormValidation.plugins.DefaultSubmit(), // Uncomment this line to enable normal button submit after form validation
						bootstrap: new FormValidation.plugins.Bootstrap({
						//	eleInvalidClass: '', // Repace with uncomment to hide bootstrap validation icons
						//	eleValidClass: '',   // Repace with uncomment to hide bootstrap validation icons
						})
		            }
		        }
		    )
		    .on('core.form.valid', function() {
				// Show loading state on button
				KTUtil.btnWait(formSubmitButton, _buttonSpinnerClasses, "Please wait");

				// Simulate Ajax request
				setTimeout(function() {
					KTUtil.btnRelease(formSubmitButton);
				}, 2000);
		    })
			.on('core.form.invalid', function() {
				Swal.fire({
					text: "Sorry, looks like there are some errors detected, please try again.",
					icon: "error",
					buttonsStyling: false,
					confirmButtonText: "Ok, got it!",
					customClass: {
						confirmButton: "btn font-weight-bold btn-light-primary"
					}
				}).then(function() {
					KTUtil.scrollTop();
				});
		    });
    }

	var _handleFormSignup = function() {
		// Base elements
		var wizardEl = KTUtil.getById('kt_login');
		var form = KTUtil.getById('kt_login_signup_form');
		var wizardObj;
		var validations = [];

		if (!form) {
			return;
		}

		// Init form validation rules. For more info check the FormValidation plugin's official documentation:https://formvalidation.io/
		// Step 1
		validations.push(FormValidation.formValidation(
			form,
			{
				fields: {
					FirstName: {
						validators: {
							notEmpty: {
								message: 'Required Field'
							}
						}
					},
					LastName: {
						validators: {
							notEmpty: {
								message: 'Required Field'
							}
						}
					},
					Phone: {
						validators: {
							notEmpty: {
								message: 'Required Field'
							}
						}
					},
					CompanyName: {
						validators: {
							notEmpty: {
								message: 'Required Field'
							}
						}
					},
					Password: {
						validators: {
							notEmpty: {
								message: 'Required Field'
							},
							callback: {
								message: 'Password length must be greater than or equal 6',
								callback: function (input) {
									debugger;
									const Password = $("input[name=Password").val();
									return Password.length >= 6 ? true : false;
								}
							}
						}
					},
					ConfirmPassword: {
						validators: {
							identical: {
								compare: function () {
									return form.querySelector('[name="Password"]').value;
								},
								message: 'The password and its confirm are not the same'
							}
						}
					},
					Email: {
						validators: {
							notEmpty: {
								message: 'Email is required'
							},
							emailAddress: {
								message: 'The value is not a valid email address'
							}
						}
					}
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		));

		// Step 2
		validations.push(FormValidation.formValidation(
			form,
			{
				fields: {
					address1: {
						validators: {
							notEmpty: {
								message: 'Address is required'
							}
						}
					},
					postcode: {
						validators: {
							notEmpty: {
								message: 'Postcode is required'
							}
						}
					},
					city: {
						validators: {
							notEmpty: {
								message: 'City is required'
							}
						}
					},
					state: {
						validators: {
							notEmpty: {
								message: 'State is required'
							}
						}
					},
					country: {
						validators: {
							notEmpty: {
								message: 'Country is required'
							}
						}
					}
				},
				plugins: {
					trigger: new FormValidation.plugins.Trigger(),
					bootstrap: new FormValidation.plugins.Bootstrap()
				}
			}
		));

		 
		// Initialize form wizard
		wizardObj = new KTWizard(wizardEl, {
			startStep: 1, // initial active step number
			clickableSteps: false // to make steps clickable this set value true and add data-wizard-clickable="true" in HTML for class="wizard" element
		});

		// Validation before going to next page
		wizardObj.on('beforeNext', function (wizard) {
			validations[wizard.getStep() - 1].validate().then(function (status) {
				if (status == 'Valid') {
					wizardObj.goNext();
					KTUtil.scrollTop();
				} else {
					Swal.fire({
						text: "Sorry, looks like there are some errors detected, please try again.",
						icon: "error",
						buttonsStyling: false,
						confirmButtonText: "Ok, got it!",
						customClass: {
							confirmButton: "btn font-weight-bold btn-light-primary"
						}
					}).then(function () {
						KTUtil.scrollTop();
					});
				}
			});

			wizardObj.stop();  // Don't go to the next step
		});

		// Change event
		wizardObj.on('change', function (wizard) {
			KTUtil.scrollTop();
		});
    }

    // Public Functions
    return {
        init: function() {
            _handleFormSignin();
			_handleFormForgot();
			_handleFormSignup();
        }
    };
}();

// Class Initialization
jQuery(document).ready(function() {
	KTLogin.init();

	$("[name='FirstName']").keyup(function () {
		$('#FName').html($(this).val()); // <-- reverse your selectors here
	});
	$("[name='LastName']").keyup(function () {
		$('#LName').html($(this).val()); // <-- reverse your selectors here
	});
	$("[name='Email']").keyup(function () {
		$('#email').html($(this).val()); // <-- reverse your selectors here
	});
	$("[name='Phone']").keyup(function () {
		$('#phone').html($(this).val()); // <-- reverse your selectors here
	});
	$("[name='CompanyName']").keyup(function () {
		$('#Company').html($(this).val()); // <-- reverse your selectors here
	});
	$(".form-control").keyup(function () {
		$('.text-danger').hide(); // <-- reverse your selectors here
	});


});
