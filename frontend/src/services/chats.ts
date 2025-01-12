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
        if (msg.message == "Invalid access token") {
            await refreshAccessToken(tokenService)
        }
    }
    return msg
}


export class ChatService {
    private _chats: Ref<Map<number, ChatMessageType[]>>
    private _lastReadTimes: Map<number, number>

    constructor() {
        this._chats = ref(new Map());
        this._lastReadTimes = new Map();
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
        const {data} = await api.get<{timestamp: number}>("/chats/"+chat_id+"/lastRead");
        this._lastReadTimes.set(chat_id, data.timestamp);

        let response = await api.get<ChatMessageType[]>("/chats/"+chat_id+"/lastMessages");

        this.chats.set(chat_id, response.data);
        return response.data;
    }

    async getChatMessages(chat_id: number, timeTo: number, limit: number = 100): Promise<ChatMessageType[]> {
        const {data} = await api.get<ChatMessageType[]>(
            "/chats/"+chat_id+"/lastMessages",
            {params: {timeTo: timeTo, limit: limit, withUnread: false}}
        );

        return data;
    }

    async getLastReadTime(chat_id: number): Promise<number> {
        let lastRead = this._lastReadTimes.get(chat_id) || 0;
        if (!lastRead) {
            const {data} = await api.get<{timestamp: number}>("/chats/"+chat_id+"/lastRead");
            this._lastReadTimes.set(chat_id, data.timestamp);
            return data.timestamp;
        }
        return lastRead
    }

    async updateLastReadTime(chat_id: number, timestamp: number): Promise<void> {
        const lastRead = this._lastReadTimes.get(chat_id);
        if (!lastRead || timestamp > lastRead) {
            this._lastReadTimes.set(chat_id, timestamp);
            await api.post("/chats/"+chat_id+"/lastRead", {timestamp: timestamp});
        }
    }

}

export const chatService = new ChatService();
