const loading = document.querySelector("#loading");

window.addEventListener("loaded", ()=>{
    //ローディングが終わった後の処理
    loading.classList.add("loaded");
});