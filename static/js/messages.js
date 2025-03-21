const messageContainer = document.querySelector(".messages")
const closeButton = document.querySelector(".alert button")

function removeMessageContainer() {
    setInterval(() => {
        messageContainer.remove()
    }, 200)
}

if (messageContainer) {
    closeButton.addEventListener("click", () => {
        messageContainer.style.opacity = "0"
        removeMessageContainer()

    })

    setInterval(() => {
        messageContainer.style.opacity = "0"
        removeMessageContainer()
    }, 3000)
}