// Initialize the pikaday object after the page loads
document.addEventListener("DOMContentLoaded", function () {
    // Set the options for the datepicker
    let pikaday_options = {
        field: document.querySelector("#appointment_date"),
        bound: false,
        container: document.querySelector("#appointment_datepicker_container"),
        firstDay: 0,
        minDate: new Date(),
        i18n: {
            previousMonth: "Mes anterior",
            nextMonth: "Próximo mes",
            months: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
            weekdays: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
            weekdaysShort: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sá"]
        },
        toString(date, format) {
            const day = ("0" + date.getDate()).slice(-2);
            const month = ("0" + (date.getMonth() + 1)).slice(-2);
            const year = date.getFullYear();
            return `${year}-${month}-${day}`;
        },
    }

    // Make the pikaday object available globally
    const picker = new Pikaday(pikaday_options);
});
