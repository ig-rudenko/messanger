import {refreshAccessToken} from "@/services/token.refresh.ts";
import {tokenService} from "@/services/token.service.ts";

enum ChatType {
    USER = "user",
    GROUP = "group"
}

export interface ChatElementType {
    id: number
    username: string
    name: string
    image: string
    lastMessage: string
    lastDatetime: string
    type: ChatType
    online?: boolean
}

export interface ChatMessageType {
    senderId: number
    recipientId: number
    timestamp: number
    message: string
}

export interface RequestMessageType {
    type: string
    status: string
    recipientId: number
    message: string
}

export interface ResponseMessageType extends RequestMessageType{
    senderId: number
    createdAt: number
}


export async function handleMessage(data: any): Promise<ResponseMessageType> {
    const msg: ResponseMessageType = JSON.parse(data);
    if (msg.status == "exception") {
        console.log(msg.message)
        if (msg.message == "Invalid access token") {
            await refreshAccessToken(tokenService)
        }
    }
    return msg

}


export class ChatService {
    constructor() {
    }

    async getChats(): Promise<ChatElementType[]> {
        return [
            {
                type: ChatType.USER,
                id: 1,
                username: "alena",
                name: "Алёна",
                image: "https://primefaces.org/cdn/primevue/images/avatar/asiyajavayant.png",
                lastMessage: "Привет! Как дела?",
                lastDatetime: "16:36",
                online: true,
            },
            {
                type: ChatType.USER,
                id: 2,
                username: "sznachkov",
                name: "Сергей Значков",
                image: "https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png",
                lastMessage: "Мог быть закрыт, но я проверил сейчас",
                lastDatetime: "16:26",
            },
            {
                type: ChatType.USER,
                id: 3,
                username: "ayastremskoy",
                name: "Александр Ястремской",
                image: "https://primefaces.org/cdn/primevue/images/avatar/onyamalimba.png",
                lastMessage: "Хорошо, что перепутали",
                lastDatetime: "16:06",
            },
            {
                type: ChatType.USER,
                id: 4,
                username: "noc",
                name: "ЦУС",
                image: "https://www.gravatar.com/avatar/05dfd4b41340d09cae045235eb0893c3?d=mp",
                lastMessage: "А вот и нашли!",
                lastDatetime: "14:31",
            },
        ]
    }

    async getChatMessages(chat_id: number): Promise<ChatMessageType[]> {
        console.log(chat_id)
        return [
            {
                recipientId: 5,
                senderId: 1,
                timestamp: 1729001441311,
                message: "Привет ♥"
            },
            {
                recipientId: 1,
                senderId: 5,
                timestamp: 1729001441321,
                message: "Привет ☻♥"
            },
            {
                recipientId: 5,
                senderId: 1,
                timestamp: 1729001441331,
                message: "Чем занимаешься?"
            },
            {
                recipientId: 1,
                senderId: 5,
                timestamp: 1729001441341,
                message: "Я покушал недавно"
            },
            {
                recipientId: 5,
                senderId: 1,
                timestamp: 1729001441351,
                message: "Я спала, пока коты меня не разбудили"
            },
            {
                recipientId: 5,
                senderId: 1,
                timestamp: 1729001441361,
                message: "Сейчас буду чай пить"
            },
        ]
    }
}