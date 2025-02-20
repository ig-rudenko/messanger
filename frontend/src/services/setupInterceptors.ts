import axiosInstance from "./api";
import {tokenService} from "./token.service";
import {refreshAccessToken} from "@/services/token.refresh.ts";

const setup = () => {
    axiosInstance.interceptors.request.use(
        (config) => {
            const token = tokenService.getLocalAccessToken();
            if (token) config.headers["Authorization"] = 'Bearer ' + token;
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    axiosInstance.interceptors.response.use(
        (res) => {
            return res;
        },
        async (err) => {
            const originalConfig = err.config;

            if ((originalConfig.url !== "/api/v1/auth/token" || originalConfig.url !== "/api/v1/auth/users") && err.response) {
                // Access Token was expired
                if (err.response.status === 401 && !originalConfig._retry) {
                    originalConfig._retry = true;
                    originalConfig.headers["Content-Type"] = "application/json";

                    try {
                        // const refreshToken = TokenService.getLocalRefreshToken()
                        // if (!refreshToken) return;
                        // const rs = await axiosInstance.post(
                        //     "auth/token/refresh",
                        //     { refreshToken: refreshToken },
                        //     originalConfig
                        // )
                        //     .then(value => value, reason => reason.response)
                        //     .catch(reason => reason.response);
                        //
                        // if (rs.status !== 200) {
                        //     store.dispatch("auth/logout")
                        //     await router.push("/login");
                        //     return Promise.reject(err)
                        // }
                        //
                        // const { accessToken } = rs.data;
                        //
                        // store.dispatch('auth/refreshToken', accessToken);
                        // TokenService.updateLocalAccessToken(accessToken);

                        const status = await refreshAccessToken(tokenService)

                        if (status) return axiosInstance(originalConfig);

                        return Promise.reject(err)
                    } catch (_error) {
                        localStorage.removeItem("user")
                        return Promise.reject(_error);
                    }
                }
            }

            return Promise.reject(err);
        }
    );
};

export default setup;