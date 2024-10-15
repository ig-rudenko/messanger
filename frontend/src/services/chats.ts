enum ChatType {
    USER = "user",
    GROUP = "group"
}

export interface ChatElementType {
    id: string
    name: string
    image: string
    lastMessage: string
    lastDatetime: string
    type: ChatType
    online?: boolean
}

export interface ChatMessageType {
    senderUsername: string
    recipientUsername: string
    timestamp: number
    message: string
}


export class ChatService {
    constructor() {
    }

    async getChats(): Promise<ChatElementType[]> {
        return [
            {
                type: ChatType.USER,
                id: "alena",
                name: "Алёна",
                image: "https://primefaces.org/cdn/primevue/images/avatar/asiyajavayant.png",
                lastMessage: "Привет! Как дела?",
                lastDatetime: "16:36",
                online: true,
            },
            {
                type: ChatType.USER,
                id: "sznachkov",
                name: "Сергей Значков",
                image: "https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png",
                lastMessage: "Мог быть закрыт, но я проверил сейчас",
                lastDatetime: "16:26",
            },
            {
                type: ChatType.USER,
                id: "ayastremskoy",
                name: "Александр Ястремской",
                image: "https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png",
                lastMessage: "Хорошо, что перепутали",
                lastDatetime: "16:06",
            },
            {
                type: ChatType.USER,
                id: "noc",
                name: "ЦУС",
                image: "https://www.gravatar.com/avatar/05dfd4b41340d09cae045235eb0893c3?d=mp",
                lastMessage: "А вот и нашли!",
                lastDatetime: "14:31",
            },
        ]
    }

    async getChatMessages(username: string): Promise<ChatMessageType[]> {
        return [
            {
                recipientUsername: "igor",
                senderUsername: "alena",
                timestamp: 1729001441311,
                message: "Привет ♥"
            },
            {
                recipientUsername: "alena",
                senderUsername: "igor",
                timestamp: 1729001441321,
                message: "Привет ☻♥"
            },
            {
                recipientUsername: "igor",
                senderUsername: "alena",
                timestamp: 1729001441331,
                message: "Чем занимаешься?"
            },
            {
                recipientUsername: "alena",
                senderUsername: "igor",
                timestamp: 1729001441341,
                message: "Я покушал недавно"
            },
            {
                recipientUsername: "igor",
                senderUsername: "alena",
                timestamp: 1729001441351,
                message: "Я спала, пока коты меня не разбудили"
            },
            {
                recipientUsername: "igor",
                senderUsername: "alena",
                timestamp: 1729001441361,
                message: "Сейчас буду чай пить"
            },
        ]
    }
}