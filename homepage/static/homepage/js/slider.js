
$(document).ready(function () {
    $('.image-slider').slick({
        slidesToShow: 4,
        slidesToScroll: 1,
        infinite: true,
        autoplay: true,
        autoplaySpeed: 3500,
        prevArrow: "<button type='button' class='slick-prev slick-arrow'><i class='mdi mdi-chevron-left' aria-hidden='true'></i></button>",
        nextArrow: "<button type='button' class='slick-next slick-arrow'><i class='mdi mdi-chevron-right' aria-hidden='true'></i></button>",
        dots: true,
        responsive: [
            {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 600,
                settings: {
                    slidesToShow: 2,
                    // slidesToScroll: 1,
                    arrows: false,
                    infinite: false,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 1,
                    // slidesToScroll: 1,
                    infinite: false,
                    arrows: false,
                }
            }
        ],
    });
});
