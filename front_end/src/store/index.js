import { createStore } from "vuex";

import toursModule from "./modules/tours/index.js";
import authModule from "./modules/auth/index.js";

const store = createStore({
  modules: { tours: toursModule, auth: authModule },
});

export default store;
