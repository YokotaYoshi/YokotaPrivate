const text = document.querySelector('#colorText');
const color = document.querySelector('#colorPicker');

// カラーピッカーを操作したときの一連の動作
const colorBg = () => {
  // 選択した色を背景色に設定
  document.body.style.backgroundColor = color.value;
  
  // カラーコードを表示
  if (color.value === '#ffffff') {
    text.textContent = `カラーコード: ${color.value} (white)`;
  }
};

// カラーピッカーが変更されたら colorBg を発動させる
color.addEventListener('input', colorBg);