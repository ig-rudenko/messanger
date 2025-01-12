export function verboseDatetime(timestamp: number): string {
    const dateObject = new Date(timestamp);
    const currentDate = new Date();

    const hour = dateObject.toLocaleString("ru-RU", {hour: "2-digit"});
    let minute = dateObject.toLocaleString("ru-RU", {minute: "2-digit"});
    if (minute.length == 1) minute = "0" + minute;

    // Если дате сегодняшняя, то возвращаем только время.
    if (currentDate.getDate() == dateObject.getDate()) {
        return `${hour}:${minute}`
    }

    const month = dateObject.toLocaleString("ru-RU", {month: "short"});

    // Если год одинаковый, то возвращаем день и месяц.
    if (currentDate.getFullYear() == dateObject.getFullYear()) {
        return `${dateObject.getDay()} ${month} ${hour}:${minute}`
    }

    return dateObject.toLocaleString("ru-RU")
}

export function getAvatar(username: string, image?: string, size: number = 64) {
    if (image) return image;
    return `https://ui-avatars.com/api/?size=${size}&name=${username}&font-size=0.33&background=random&rounded=true`
}

export function textToHtml(text: string): string {
    const r = /\n/g
    return text.replace(r, "<br>")
}