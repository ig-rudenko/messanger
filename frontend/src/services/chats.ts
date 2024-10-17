import {refreshAccessToken} from "@/services/token.refresh";
import {tokenService} from "@/services/token.service";
import api from "@/services/api";

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
    public chats: Map<number, ChatMessageType[]>

    constructor() {
        this.chats = new Map();
    }

    getStoredChat(chat_id: number): ChatMessageType[] {
        return this.chats.get(chat_id) || []
    }

    saveChat(chat_id: number, messages: ChatMessageType[]) {
        this.chats.set(chat_id, messages)
    }

    async getLastChatMessages(chat_id: number): Promise<ChatMessageType[]> {
        const resp = await api.get<ChatMessageType[]>("/chats/"+chat_id+"/lastMessages");
        this.chats.set(chat_id, resp.data);
        return resp.data;
    }
}

export const chatService = new ChatService();
