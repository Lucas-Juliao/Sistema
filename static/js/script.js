document.querySelector('.open-btn').addEventListener('click', () => {
    document.querySelector('.sidebar').style.width = '250px';
    document.querySelector('.main-content').style.marginLeft = '250px';
});

document.querySelector('.close-btn').addEventListener('click', () => {
    document.querySelector('.sidebar').style.width = '0';
    document.querySelector('.main-content').style.marginLeft= '0';
});
