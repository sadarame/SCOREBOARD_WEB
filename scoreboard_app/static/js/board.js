// ウィンドウの幅が798px以下の場合に実行する関数
function swapElements() {
    var container = document.querySelector('.container');
    var sidebar = container.querySelector('.l-sidebar');
    var boardSection = container.querySelector('.board-section');

    if (window.innerWidth <= 798) {
        // 798px以下の場合はサイドバーとメインセクションを入れ替える
        container.insertBefore(boardSection, sidebar);
    } else {
        // 798pxより広い場合は元の順序に戻す
        container.insertBefore(sidebar, boardSection);
    }
}

// 初期読み込み時とウィンドウサイズ変更時に関数を実行
window.addEventListener('load', swapElements);
window.addEventListener('resize', swapElements);