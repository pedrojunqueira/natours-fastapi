import axios from "axios";
import jwt_decode from "jwt-decode";

let timer;

export default {
  async auth(context, payload) {
    try {
      const config = {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      };
      const params = new URLSearchParams();
      params.append("username", payload.username);
      params.append("password", payload.password);
      const response = await axios({
        method: "post",
        url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/token`,
        data: params,
        config,
      });
      if (response.status == 200) {
        const token = response.data.access_token;
        const expires = jwt_decode(token).exp;
        localStorage.setItem("token", token);
        localStorage.setItem("username", payload.username);
        localStorage.setItem("expires", expires);
        const expiresIn = (+expires - new Date().getTime() / 1000) * 1000;

        timer = setTimeout(function () {
          context.dispatch("autoLogout");
        }, expiresIn);

        const user = {
          username: payload.username,
          token: response.data.access_token,
          expires: jwt_decode(token).exp,
        };
        context.commit("setUser", user);
        await context.dispatch("fetchMe");
        return response;
      }
    } catch (err) {
      //console.log(err.response.data.detail);
    }
  },
  async login(context, payload) {
    const response = await context.dispatch("auth", payload);
    return response;
  },
  logout(context) {
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    localStorage.removeItem("expires");

    clearTimeout(timer);

    context.commit("resetUser");
  },
  async fetchMe(context) {
    try {
      const headers = { Authorization: `Bearer ${context.getters.token}` };
      const response = await axios({
        method: "get",
        url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/me`,
        headers,
      });
      const me = response.data;
      context.commit("setMe", me);
    } catch (err) {
      console.log(err.response);
    }
  },
  async tryLogin(context) {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");
    const expires = localStorage.getItem("expires");
    const expiresIn = (+expires - new Date().getTime() / 1000) * 1000;

    if (expiresIn < 0) {
      return;
    }

    timer = setTimeout(function () {
      context.dispatch("autoLogout");
    }, expiresIn);

    if (token && username) {
      const user = { username, token };
      context.commit("setUser", user);
      await context.dispatch("fetchMe");
    }
  },
  async signUp(context, payload) {
    try {
      const response = await axios({
        method: "post",
        url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/signup`,
        data: payload,
      });
      if (response.status == 200) {
        await context.dispatch("login", {
          username: payload.username,
          password: payload.password,
        });
      }
    } catch (err) {
      console.log(err.response);
    }
  },
  autoLogout(context) {
    context.dispatch("logout");
    context.commit("setAutoLogout");
  },
};
