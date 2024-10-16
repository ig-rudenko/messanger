import {refreshAccessToken} from "@/services/token.refresh";
import {tokenService} from "@/services/token.service";
import api from "@/services/api";

enum ChatType {
    USER = "user",
    GROUP = "group"
}

export interface ChatElementType {
    id: number
    username: string
    firstName: string
    lastName: string
    image?: string
    lastMessage?: string
    lastDatetime?: string
    type: ChatType
    online?: boolean
}

export interface ChatMessageType {
    senderId: number
    recipientId: number
    createdAt: number
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

    async getChats(): Promise<ChatElementType[]> {
        const resp = await api.get<ChatElementType[]>("/subscribers");
        return resp.data;
    }

    async getChatMessages(chat_id: number): Promise<ChatMessageType[]> {
        const resp = await api.get<ChatMessageType[]>("/subscribers/chat/"+chat_id+"/lastMessages");
        return resp.data;
    }
}