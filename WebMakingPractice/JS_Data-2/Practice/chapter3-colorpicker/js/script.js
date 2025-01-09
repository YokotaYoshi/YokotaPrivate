console.log(document.querySelector("#colorPicker").value);
/*document.querySelector("#colorText").textContent = "カラーコード："+document.querySelector("#colorPicker").value;*/
/*document.querySelector("#colorText").textContent=`カラーコード：${document.querySelector("#colorPicker").value}`;*/

const name="Mana";
const text=document.querySelector("#colorText");
const color=document.querySelector("#colorPicker");
console.log(name);

text.textContent=`カラーコード：${color.value}`;

//1行コメントアウト
/*
複数行コメントアウト
*/