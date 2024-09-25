class Verification {
    constructor(slide) {
        // Store the current slide
        this.slide = slide;

        // Consider the current slide valid by default
        this.valid = true;

        // Initialize the input and message variables
        this.input = null;
        this.message = null;

        // List of messages for the validation errors
        this.messages = {
            "terms": "Debe aceptar los términos y condiciones para continuar",
        }
    }

    // Check if the current slide has a phone input and if it is valid
    validate_phone() {
        // Get the phone input
        let phone = this.slide.querySelector("input[type='tel']");

        // Check if the phone input exists
        if (phone) {
            // Check if the phone input is valid
            if (!phone.checkValidity() || !phone.value.match(/^[0-9]{10}$/g)) {
                // Set the valid flag to false
                this.valid = false;
                this.input = phone;
            }
        }
    }

    // Check if the current slide has a email input and if it is valid
    validate_email() {
        // Get the email input
        let email = this.slide.querySelector("input[type='email']");

        // Check if the email input exists
        if (email) {
            // Check if the email input is valid
            if (!email.checkValidity() || !email.value.match(/[\w-\.]+@([\w-]+\.)+[\w-]{2,4}/g)) {
                // Set the valid flag to false
                this.valid = false;
                this.input = email;
            }
        }
    }

    // Check if the current slide has inputs and if they are valid
    validate_inputs() {
        // Get all the required inputs in the current slide
        let inputs = this.slide.querySelectorAll("input:required");

        // Iterate over the inputs
        inputs.forEach(input => {
            // Check if the input is valid
            if (!input.checkValidity()) {
                // Set the valid flag to false
                this.valid = false;
                this.input = input;
            }
        })
    }

    validate_contact_center() {
        let additional_service_input = this.slide.querySelector("#additional_service");
        let car_condition_input = this.slide.querySelector("input[name='car_condition']:checked");

        let input = additional_service_input || car_condition_input;
        if (input) {
            if (input.value) {
                this.valid = false;
                this.input = additional_service_input || car_condition_input;
            }
        }
    }

    // Evaluate the current slide
    validate() {
        // Run the validation functions, if any of them return false, the slide is invalid
        this.validate_phone();
        this.validate_email();
        this.validate_inputs();
        this.validate_contact_center();

        // If the current slide is invalid, trigger the error message and return false
        if (!this.valid) {
            // Focus the input that is invalid
            if (this.input) {
                this.input.focus();
            }

            // Check the type of validation error
            if (this.input.validity.valueMissing) {
                this.message = this.messages[this.input.name] ?? "El campo " + this.input.dataset.name + " es obligatorio"
                let sweet_alert = new SweetAlert(this.message);
                sweet_alert.warning();
            }
            else if (this.input.validity.patternMismatch) {
                this.message = "El campo " + this.input.dataset.name + " tiene un formato inválido"
                let sweet_alert = new SweetAlert(this.message);
                sweet_alert.warning();
            }
            else if (this.input.validity.typeMismatch) {
                this.message = "El valor del campo " + this.input.dataset.name + " no es del tipo correcto"
                let sweet_alert = new SweetAlert(this.message);
                sweet_alert.warning();
            }
            // Check for appointment process endings 
            else if (this.input.dataset.cancellation_reason) {
                // Send all the appointment data to the server
                let appointment_data = new AppointmentData();
                appointment_data.other_service(Number(this.input.dataset.cancellation_reason));

                // Show a message to the user and reload the page
                this.title = "OTRO SERVICIO";
                this.message = "Gracias por tomarse el tiempo de diligenciar este formato. Pronto será contactado por un asesor para continuar el proceso de agendamiento.";
                let sweet_alert = new SweetAlert(this.title, this.message);
                sweet_alert.error();
            }
            return false;
        }
        // If the current slide is valid, return true 
        else {
            return true;
        }
    }

}

class InputWatcher {
    constructor() {
        // Add event listeners to the inputs that need to be formatted on input
        document.querySelector("#license_plate").addEventListener("keyup", this.format_plate);
        document.querySelector("#car_mileage").addEventListener("keyup", this.format_mileage);
        document.querySelector("#car_model").addEventListener("change", this.set_years);

        // Add event listeners to the inputs that change the ui
        document.querySelector("#service_radio_other").addEventListener("change", this.set_additional_service_container);

        // Add event listeners to the services inputs
        document.querySelectorAll("input[name='service']").forEach(service => {
            service.addEventListener("change", this.set_service_summary);
        })
        document.querySelectorAll("input[name='other_services']").forEach(other_service => {
            other_service.addEventListener("change", this.set_service_summary);
        })

        // Add event listeners to the advisors radio buttons
        document.querySelectorAll("input[name='advisor_id']").forEach(advisor_radio_button => {
            advisor_radio_button.addEventListener("change", this.set_advisor_availability);
        })
        document.querySelector("#appointment_date").addEventListener("change", this.set_advisor_availability);

        // Add event listener to the finish button
        document.querySelector("#button_finish").addEventListener("click", this.finish_appointment);
    }

    // Format the car plate input
    format_plate() {
        this.value = this.value.toUpperCase().replace(/[^a-zA-Z0-9]/g, '');
    }

    // Format the mileage input
    format_mileage() {
        this.value = this.value.replace(/[^0-9]/g, '');
    }

    // Set the visibility of the additional service container
    set_additional_service_container(event) {
        let other_service_input = event.currentTarget;
        if (other_service_input.checked) {
            document.querySelector("#additional_service_container").style.display = "block";
        } else {
            document.querySelector("#additional_service_container").style.display = "none";
        }
    }

    // Set years
    set_years() {
        // Get the current option selected
        let car_model = document.querySelector(".car-model-option:checked");
        let year_start = Number(car_model.dataset.year_start);
        let year_end = Number(car_model.dataset.year_end);

        let car_year_select = document.querySelector("#car_model_year");
        // Clear the options
        document.querySelectorAll(".car-year-option").forEach(option => { option.remove() });
        // Add the options
        for (year_start; year_start <= year_end; year_start++) {
            let option = document.createElement("option");
            option.className = "car-year-option";
            option.value = year_start;
            option.innerText = year_start;
            car_year_select.appendChild(option);
        }
    }

    // Set service summary
    set_service_summary(event) {
        let service_input = event.currentTarget;
        let service_name = service_input.closest(".list-group-item").querySelector(".service-name").innerText;
        let service_id = service_input.value;

        let required_services_container = document.querySelector("#required_services_container");

        if (service_input.checked) {
            let service_summary_entry = document.createElement("li");
            service_summary_entry.className = "list-group-item";
            service_summary_entry.id = "service_summary_entry_" + service_id;
            service_summary_entry.innerText = service_name;
            required_services_container.appendChild(service_summary_entry);
        } else if (!service_input.checked) {
            required_services_container.querySelector("#service_summary_entry_" + service_id).remove();
        }
    }

    // Set advisor availability
    set_advisor_availability(event) {
        let advisor_id = document.querySelector("input[name='advisor_id']:checked").value;
        let date = document.querySelector("#appointment_date").value;
        let advisor_availability = new AdvisorAvailability(advisor_id, date);
        let hours = advisor_availability.get_hours();

        if (advisor_id && date) {
            Swal.fire({
                title: 'Obteniendo horarios disponibles',
                allowOutsideClick: false,
                allowEscapeKey: false,
                didOpen: () => {
                    Swal.showLoading();

                    hours.then(hours => {
                        // Clear the current hours
                        let availability_hours_container = document.querySelector("#availability_hours_container");
                        availability_hours_container.innerHTML = "";

                        // Add the new hours
                        hours.forEach((hour, index) => {
                            let hour_radio_check = document.createElement("div");
                            hour_radio_check.className = "col-6";
                            hour_radio_check.innerHTML = `
                            <div class="form-check">
                                <input class="form-check-input" type="radio" name="appointment_time" id="appointment_time_${index}" value="${hour}" required>
                                <label class="form-check-label" for="appointment_time_${index}">
                                    ${hour}
                                </label>
                            </div>
                        `;
                            availability_hours_container.appendChild(hour_radio_check);
                        })
                        Swal.close();
                    })

                }
            });
        }
    }

    // Finish the appointment process
    finish_appointment() {
        // Get the appointment data
        Swal.fire({
            title: 'Agendando cita',
            allowOutsideClick: false,
            allowEscapeKey: false,
            didOpen: () => {
                Swal.showLoading();
                let appointment_data = new AppointmentData();
                let response_promise = appointment_data.schedule();
                response_promise.then(response => {
                    Swal.close();
                    if (!response.ok) {
                        Swal.fire({
                            title: "Ha ocurrido un error al agendar la cita",
                            text: response.statusText,
                            allowEscapeKey: false,
                            allowOutsideClick: false,
                            showConfirmButton: false,
                            showCancelButton: false,
                            showCloseButton: false,
                        })
                    }
                })
            }
        })
    }
}

// Initialize the input watcher after the page loads
document.addEventListener("DOMContentLoaded", () => {
    // Make the input watcher object available globally
    const input_watcher = new InputWatcher();
});
