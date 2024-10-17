import api from "@/services/api.ts";
import {Ref, ref} from "vue";

enum EntityType {
    USER = "user",
    GROUP = "group"
}

export interface FriendshipEntityType {
    id: number
    username: string
    firstName: string
    lastName: string
    image?: string
    lastMessage?: string
    lastDatetime?: number
    type: EntityType
    online?: boolean
    newMessagesCount?: number
}

export class FriendshipsService {
    public friendships: Ref<FriendshipEntityType[]>

    constructor() {
        this.friendships = ref([]);
    }

    async findFriendship(search: string) {
        const resp = await api.get<FriendshipEntityType[]>("/friendships/search?search="+search);
        return resp.data;
    }

    async findFriendshipEntityById(id: number) {
        const resp = await api.get<FriendshipEntityType[]>("/friendships/search?entity_id="+id);
        if (resp.data.length > 0) return resp.data[0];
        return null
    }

    get friendshipsOrderedList(): FriendshipEntityType[] {
        return this.friendships.value.sort(
            (a, b) => {
                return (a?.lastDatetime || 0) < (b?.lastDatetime || 0) ? 1 : -1
            }
        )
    }

    async createFriendship(username: string) {
        const resp = await api.post<FriendshipEntityType>(
            "/friendships", {username: username}
        );
        this.friendships.value.push(resp.data)
        return resp.data;
    }

    async getMyFriendships(): Promise<FriendshipEntityType[]> {
        const resp = await api.get<FriendshipEntityType[]>("/friendships");
        this.friendships.value = resp.data;
        return this.friendships.value
    }

    getFriendshipById(id: number): FriendshipEntityType|null {
        for (const friendship of this.friendships.value) {
            if (friendship.id == id) return friendship;
        }
        return null;
    }

    getFriendshipByUsername(username: string): FriendshipEntityType|null {
        for (const friendship of this.friendships.value) {
            if (friendship.username == username) return friendship;
        }
        return null;
    }

    updateLastMessageInfo(id: number, message: string, datetime: number) {
        const friendshipEntity = this.getFriendshipById(id)
        if (friendshipEntity) {
            friendshipEntity.lastMessage = message;
            friendshipEntity.lastDatetime = datetime;
        }
    }

    resetNewMessageCount(id: number) {
        const friendshipEntity = this.getFriendshipById(id)
        if (friendshipEntity) {
            friendshipEntity.newMessagesCount = 0
        }
    }

}

export const friendshipService = new FriendshipsService();
