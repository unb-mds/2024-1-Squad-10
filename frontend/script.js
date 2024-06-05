const title = document.querySelector('.title')
const title2 = document.querySelector('.subtitle')
const title3 = document.querySelector('.botao-arredondado')

document.addEventListener('scroll', function() {
    let value = window.scrollY
    title.style.marginTop = value * 1.1 + 'px'
    title2.style.marginTop = value * 1.1 + 'px'
    title3.style.marginTop = value * 1.1 + 'px'
})
