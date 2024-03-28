let counter = 0;
function count() {
    counter++;
    document.querySelector('h1').textContent = counter;
    localStorage.setItem('counter', counter);
    return counter;
}

document.addEventListener('DOMContentLoaded', () => {
    localStorage.getItem('counter') ? counter = localStorage.getItem('counter') : counter = 0;
    document.querySelector('button').onclick = count;
    document.querySelector('h1').innerHTML = counter;
});

