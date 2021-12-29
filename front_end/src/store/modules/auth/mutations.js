export default {
  setUser(state, payload) {
    state.username = payload.username;
    state.token = payload.token;
    state.expires = payload.expires;
    state.didAutoLogout = false;
  },
  resetUser(state) {
    state.username = null;
    state.token = null;
    state.me = null;
    state.didAutoLogout = true;
  },
  setMe(state, payload) {
    state.me = payload;
  },
  setAutoLogout(state) {
    state.didAutoLogout = true;
  },
};
