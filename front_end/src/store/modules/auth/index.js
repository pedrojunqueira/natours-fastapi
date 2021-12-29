import mutations from "./mutations.js";
import getters from "./getters.js";
import actions from "./actions.js";

export default {
  state() {
    return {
      username: null,
      token: null,
      expires: null,
      didAutoLogout: false,
      me: {},
    };
  },
  mutations,
  getters,
  actions,
};
