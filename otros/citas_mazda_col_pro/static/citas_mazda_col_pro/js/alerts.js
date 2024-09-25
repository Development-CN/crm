class SweetAlert {
    constructor(title, message = "") {
        this.settings = {
            title: title,
            text: message,
            // Misc settings
            allowOutsideClick: false,
            buttonsStyling: false,
            focusConfirm: false,
            focusCancel: false,
            reverseButtons: true,
            // Custom CSS classes
            customClass: {
                popup: "card bg-light",
                confirmButton: "btn btn-primary mx-3",
                denyButton: "btn btn-dark mx-3",
                cancelButton: "btn btn-dark mx-3",
                closeButton: "btn btn-light mx-3",
            },
            // Alert type settings
            icon: undefined, // warning, error, success, info, question
            // Hide or show buttons
            showDenyButton: false,
            showCancelButton: false,
            showCloseButton: false,
            // Buttons text
            confirmButtonText: "Aceptar",
            denyButtonText: "No",
            cancelButtonText: "Cancelar",
        }
    }

    question() {
        this.settings.icon = "question";
        this.settings.showDenyButton = true;
        this.settings.confirmButtonText = "Si";
        this.settings.denyButtonText = "No";
        Swal.fire(this.settings);
    }

    info() {
        this.settings.icon = "info";
        this.settings.showCloseButton = true;
        Swal.fire(this.settings);
    }

    warning() {
        Swal.fire(this.settings);
    }

    error() {
        Swal.fire(this.settings).then((result) => {
            if (result.value) {
                window.location.reload();
            }
        });
    }

    success() {
        this.settings.icon = "success";
        Swal.fire(this.settings);
    }
}
