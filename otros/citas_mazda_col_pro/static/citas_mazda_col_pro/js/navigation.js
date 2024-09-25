class Navigation {
    constructor() {
        // Get the slides
        this.slides = document.querySelectorAll("slide");
        this.current_slide = document.querySelector("slide");
        this.previous_slide = this.current_slide.previousElementSibling;
        this.next_slide = this.current_slide.nextElementSibling;

        // Get the navigation buttons
        this.button_finish = document.querySelector("#button_finish");
        this.button_continue = document.querySelector("#button_continue");
        this.button_back = document.querySelector("#button_back");

        this.button_finish_col = document.querySelector("#col_button_finish");
        this.button_continue_col = document.querySelector("#col_button_continue")
        this.button_back_col = document.querySelector("#col_button_back")

        // Set the event listeners
        this.button_finish.addEventListener("click", this.go_next_slide.bind(this));
        this.button_continue.addEventListener("click", this.go_next_slide.bind(this));
        this.button_back.addEventListener("click", this.go_back_slide.bind(this));

        // Show the current slide
        this.current_slide.style.display = "block";

        // Set the navigation buttons
        this.set_navigation_buttons();
    }

    // Disable or enable the navigation buttons
    disable_buttons(boolean) {
        this.button_continue.disabled = boolean;
        this.button_back.disabled = boolean;
        this.button_finish.disabled = boolean;
    }

    // Hide the corresponding navigation button
    set_navigation_buttons() {
        let slides_count = this.slides.length;

        // Check if the current slide is the first slide, if so hide the back button, otherwise show it
        if ([].indexOf.call(this.slides, this.current_slide) == 0) {
            fadeOut(this.button_back_col);
        } else {
            fadeIn(this.button_back_col);
        }

        // Check if the current slide is the last slide, if so hide the continue button, otherwise show it
        if ([].indexOf.call(this.slides, this.current_slide) >= slides_count - 2) {
            fadeOut(this.button_continue_col);
            fadeIn(this.button_finish_col);
        } else {
            fadeIn(this.button_continue_col);
            fadeOut(this.button_finish_col);
        }

        // Check if the current slide is the last slide, if so hide the navigation buttons, otherwise show them
        if ([].indexOf.call(this.slides, this.current_slide) == slides_count - 1) {
            fadeOut(this.button_back_col);
            fadeOut(this.button_continue_col);
            fadeOut(this.button_finish_col);
        }
    }

    // Function to go to the next slide
    go_next_slide() {
        // Disable the navigation buttons
        this.disable_buttons(true);

        // Create a verification object for the current slide
        let slide_is_valid = false;
        if (window.debug) {
            slide_is_valid = true;
        } else {
            let VerifySlide = new Verification(this.current_slide);
            slide_is_valid = VerifySlide.validate();
        }

        let VerifySlide = new Verification(this.current_slide);
        slide_is_valid = VerifySlide.validate();

        // Check if the current slide is valid and if the next slide exists
        if (slide_is_valid && this.next_slide) {

            // Fade out the current slide and fade in the next slide
            fadeOut(this.current_slide);
            setTimeout(() => { }, 10);
            fadeIn(this.next_slide);

            // Set the previous, current and next slides
            this.previous_slide = this.current_slide;
            this.current_slide = this.next_slide;
            this.next_slide = this.next_slide.nextElementSibling;

            // Set the navigation buttons
            this.set_navigation_buttons();
        }

        // Enable the navigation buttons
        this.disable_buttons(false);
    }

    // Function to go to the previous slide
    go_back_slide() {
        // Disable the navigation buttons
        this.disable_buttons(true);

        // Check if the previous slide exists
        if (this.previous_slide) {

            // Fade out the current slide and fade in the previous slide
            fadeOut(this.current_slide);
            setTimeout(() => { }, 10);
            fadeIn(this.previous_slide);

            // Set the next, current and previous slides
            this.next_slide = this.current_slide;
            this.current_slide = this.previous_slide;
            this.previous_slide = this.previous_slide.previousElementSibling;

            // Set the navigation buttons
            this.set_navigation_buttons();
        }

        // Enable the navigation buttons
        this.disable_buttons(false);
    }
}

// Initialize the navigation object after the page loads
document.addEventListener('DOMContentLoaded', function () {
    // Make the navigation object available globally
    const navigation = new Navigation();
});
