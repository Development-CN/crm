class AppointmentData {
    constructor() {
        this.endpoint = window.api_appointment;

        this.form = document.querySelector("form");
        this.data = new FormData(this.form);

        this.headers = new Headers();
        this.headers.append("Content-Type", "application/json");
        this.headers.append("Accept", "application/json");

        this.request_options = {}
        this.request_options.method = "POST";
        //this.request_options.headers = this.headers;

        this.request_options.body = this.data;
    }

    other_service(cancellation_reason) {
        this.data.append("type", "other_service");
        this.data.append("cancellation_reason", cancellation_reason);
        let response_promise = this.send_request();
        return response_promise;

    }

    schedule() {
        this.data.append("type", "schedule");
        let response_promise = this.send_request();
        return response_promise;
    }

    send_request() {
        this.request_options.body = this.data;
        let request = new Request(this.endpoint, this.request_options);
        let response_promise = fetch(request);
        return response_promise;
    }
}

class AdvisorAvailability {
    constructor(advisor_id, date) {
        this.endpoint = window.api_appointment;

        this.headers = new Headers();
        this.headers.append("Content-Type", "application/json");
        this.headers.append("Accept", "application/json");

        this.request_options = {}
        this.request_options.method = "POST";
        this.request_options.headers = this.headers;

        this.request_options.body = {};
        this.request_options.body.advisor_id = advisor_id;
        this.request_options.body.date = date;
        this.request_options.body.type = "availability";
        this.request_options.body = JSON.stringify(this.request_options.body);
    }

    get_hours() {
        let request = new Request(this.endpoint, this.request_options);
        let available_hours = fetch(request).then(response => response.json()).then(available_hours => {
            return available_hours;
        }).catch(error => {
            console.log(error);
        });
        return available_hours;
    }
}
