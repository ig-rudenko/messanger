import {refreshAccessToken} from "@/services/token.refresh";
import {tokenService} from "@/services/token.service";
import api from "@/services/api";
import {ref, Ref} from "vue";

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
    private _chats: Ref<Map<number, ChatMessageType[]>>

    constructor() {
        this._chats = ref(new Map());
    }

    get chats() {
        return this._chats.value
    }

    getStoredChat(chat_id: number): ChatMessageType[] {
        return this.chats.get(chat_id) || []
    }

    appendMessageToChat(chat_id: number, message: ChatMessageType) {
        this.getStoredChat(chat_id).push(message)
    }

    async getLastChatMessages(chat_id: number): Promise<ChatMessageType[]> {
        const resp = await api.get<ChatMessageType[]>("/chats/"+chat_id+"/lastMessages");
        this.chats.set(chat_id, resp.data);
        return resp.data;
    }
}

export const chatService = new ChatService();
