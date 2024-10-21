export function scrollChatContainerToEnd(divideUnread: boolean = false) {
    // Автопрокрутка к нижнему сообщению при открытии
    setTimeout(() => {
        const container = document.getElementById('messages-container')!;
        container.scrollTop = container.scrollHeight;

        if (divideUnread) {
            const unread = document.getElementById('unread-messages');
            if (unread) unread.scrollIntoView({block: 'center'});
        }

    }, 100)
}