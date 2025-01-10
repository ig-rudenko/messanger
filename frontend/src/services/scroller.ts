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

export function scrollChatContainerToMessageByTime(time: number) {
    setTimeout(() => {
        const container = document.getElementById('messages-container')!;
        for (const element of container.getElementsByTagName('div')) {
            if (element.getAttribute('data-created-at') === time.toString()) {
                console.log(element)
                element.scrollIntoView({block: 'start', behavior: "instant", inline: "start"});
                break;
            }
        }
        // document.getElementById('messages-container')!.style.overflow = "";
    }, 200)
}