import api from "./api";
import {tokenService} from "./token.service";
import {LoginUser, RegisterUser, UserTokens} from "./user";
import UserService from "./user.service";

class AuthService {
    login(user: LoginUser) {
        return api
            .post("/auth/token", {
                username: user.username,
                password: user.password
            })
            .then(
                response => {
                    if (response.data.accessToken) {
                        tokenService.setUser(new UserTokens(response.data.accessToken, response.data.refreshToken || null));
                    }
                    return response
                },
                reason => {
                    return reason
                }
            );
    }

    logout() {
        tokenService.removeUser();
        UserService.removeUser();
    }

    register(user: RegisterUser) {
        return api.post("/auth/users", {
            username: user.username,
            email: user.email,
            password: user.password,
            recaptchaToken: user.recaptchaToken,
        });
    }
}

export default new AuthService();