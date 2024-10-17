export function verboseDatetime(timestamp: number): string {
    // multiplied by 1000 so that the argument is in milliseconds, not seconds
    const milliseconds = new Date(timestamp * 1000);
    const dateObject = new Date(milliseconds);

    const currentDate = new Date();

    const hour = dateObject.toLocaleString("ru-RU", {hour: "2-digit"});
    let minute = dateObject.toLocaleString("ru-RU", {minute: "2-digit"});
    if (minute.length == 1) minute += "0";

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