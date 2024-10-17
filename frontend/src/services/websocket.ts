import {tokenService} from "@/services/token.service.ts";
import {errorToast} from "@/services/my.toast.ts";
import {RequestMessageType} from "@/services/chats.ts";
import {Ref, ref} from "vue";


export default class WebSocketConnector {
    private socket: WebSocket;
    private readonly url: string
    private readonly reconnectionTimeout: number = 1000 //ms
    private connecting: boolean = true
    public isConnected: Ref<boolean>
    private messageCallback?: (ev: MessageEvent<any>) => any = undefined

    constructor(url: string) {
        this.url = url
        this.socket = new WebSocket(url);
        this.socket.onopen = () => this.onOpen();
        this.socket.onerror = () => this.onError();
        this.isConnected = ref(false)
    }

    private reconnect() {
        // console.log('RECONNECTING')
        this.connecting = true;
        this.socket = new WebSocket(this.url);
        this.socket.onopen = () => this.onOpen();
        this.socket.onerror = () => this.onError();
    }

    private onOpen() {
        // console.log("OPEN!!!",this.messageCallback)
        this.connecting = false;
        this.isConnected.value = true;

        if (this.messageCallback) this.setOnMessage(this.messageCallback);

        this.socket.onclose = () => this.onClose()

        const token = tokenService.getLocalAccessToken()
        if (token) {
            this.socket.send(token);
        } else {
            errorToast("Ошибка", "Не удалось подключиться, перезайдите в аккаунт")
        }
    }

    private onClose() {
        // console.log("CLOSE")
        this.reconnectIfFail();
    }

    private onError() {
        this.connecting = false;
        this.reconnectIfFail();
    }

    reconnectIfFail() {
        // console.log("reconnectIfFail")
        this.isConnected.value = false;
        if (this.connecting) {
            console.log("already connecting")
            setTimeout(this.reconnectIfFail, this.reconnectionTimeout);
            return;
        }
        try {
            if ((this.socket.CLOSED && !this.socket.CONNECTING)) {
                setTimeout(() => this.reconnect(), this.reconnectionTimeout)
            }
        } catch (e) {}
    }

    sendMessage(msg: RequestMessageType) {
        this.socket.send(JSON.stringify(msg))
    }

    setOnMessage(callback: (ev: MessageEvent<any>) => any) {
        this.messageCallback = callback;
        this.socket.onmessage = callback;
    }
}
