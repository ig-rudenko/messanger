import api from "@/services/api.ts";

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
}

export class FriendshipsService {
    public friendships: FriendshipEntityType[]

    constructor() {
        this.friendships = [];
    }

    async findFriendship(search: string) {
        const resp = await api.get<FriendshipEntityType[]>("/friendships/search?search="+search);
        return resp.data;
    }

    async createFriendship(username: string) {
        const resp = await api.post<FriendshipEntityType>(
            "/friendships", {username: username}
        );
        this.friendships.push(resp.data)
        return resp.data;
    }

    async getMyFriendships(): Promise<FriendshipEntityType[]> {
        const resp = await api.get<FriendshipEntityType[]>("/friendships");
        this.friendships = resp.data;
        return this.friendships
    }

    getFriendshipById(id: number): FriendshipEntityType|null {
        for (const friendship of this.friendships) {
            if (friendship.id == id) return friendship;
        }
        return null;
    }

    getFriendshipByUsername(username: string): FriendshipEntityType|null {
        for (const friendship of this.friendships) {
            if (friendship.username == username) return friendship;
        }
        return null;
    }

}

export const friendshipService = new FriendshipsService();
