import axios from "axios";
import store from "@/store";
import router from "@/router.ts";
import {TokenService} from "@/services/token.service";


export async function refreshAccessToken(tokenService: TokenService) {
    const refreshToken = tokenService.getLocalRefreshToken()
    if (!refreshToken) return;
    const rs = await axios.post(
        "/api/v1/auth/token/refresh",
        { refreshToken: refreshToken },
    )
        .then(value => value, reason => reason.response)
        .catch(reason => reason.response);

    if (rs.status !== 200) {
        await store.dispatch("auth/logout")
        await router.push("/auth/login");
        return false
    }

    const { accessToken } = rs.data;

    await store.dispatch('auth/refreshToken', accessToken);
    tokenService.updateLocalAccessToken(accessToken);
    return true
}