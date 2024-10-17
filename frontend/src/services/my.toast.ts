import {app} from '@/main';

const basicLifeTime = 3000;

export function newMessageToast(id: number, verboseFrom: string, message: string, avatar: string, lifeTime: number = basicLifeTime): void {
    let shortMessage = message.length>53?message.slice(0, 50)+"...":message;

    app.config.globalProperties.$toast.add({
        severity: "info",
        summary: verboseFrom,
        detail: {
            id: id,
            message: shortMessage,
            avatar: avatar,
        },
        group: "message",
        life: lifeTime
    });
}

export function infoToast(title: string, body: string, lifeTime: number = basicLifeTime): void {
    app.config.globalProperties.$toast.add({
        severity: "info",
        summary: title,
        detail: body,
        life: lifeTime
    });
}

export function successToast(title: string, body: string, lifeTime: number = basicLifeTime): void {
    app.config.globalProperties.$toast.add({
        severity: "success",
        summary: title,
        detail: body,
        life: lifeTime
    });
}

export function errorToast(title: string, body: string, lifeTime: number = basicLifeTime): void {
    app.config.globalProperties.$toast.add({
        severity: "error",
        summary: title,
        detail: body,
        life: lifeTime
    });
}