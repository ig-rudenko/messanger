export function scrollChatContainerToEnd() {
    // Автопрокрутка к нижнему сообщению при открытии
    setTimeout(() => {
        const container = document.getElementById('messages-container')!;
        container.scrollTop = container.scrollHeight;
    }, 100)
}