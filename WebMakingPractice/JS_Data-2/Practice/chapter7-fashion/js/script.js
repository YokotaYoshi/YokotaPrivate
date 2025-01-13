//ローディングから画面遷移

const loadingAreaGrey = document.querySelector("#loading");

window.addEventListener("load",()=>{
    loadingAreaGrey.animate(
        {
            opcity:[1,0],
            visibility:"hidden",
        },
        {
            duration: 2000,
            delay: 1200,
            easing: "ease",
            fill:"forwards",
        }
    );
});