import { createRouter, createWebHistory } from "vue-router";

import ToursList from "./pages/tours/ToursList.vue";
import TourDetail from "./pages/tours/TourDetail.vue";
import TourReview from "./pages/tours/TourReview.vue";
import UserLogin from "./pages/users/UserLogin.vue";
import UserSignUp from "./pages/users/UserSignUp.vue";
import UserAccount from "./pages/users/UserAccount.vue";
import UserForgotPassword from "./pages/users/UserForgotPassword.vue";
import UserResetPassword from "./pages/users/UserResetPassword.vue";
import NotFound from "./pages/NotFound.vue";
import store from "./store/index.js";

const router = createRouter({
  history: createWebHistory(),
  mode: "history",
  routes: [
    { path: "/", redirect: "/tours" },
    { path: "/tours", component: ToursList },
    { path: "/tours/:id", component: TourDetail, meta: { requiresAuth: true } },
    {
      path: "/tour_review/:id",
      component: TourReview,
      meta: { requiresAuth: true },
    },
    {
      path: "/tours/login",
      component: UserLogin,
      meta: { requiresUnAuth: true },
    },
    {
      path: "/tours/sign_up",
      component: UserSignUp,
      meta: { requiresUnAuth: true },
    },
    { path: "/user/:id", component: UserAccount, meta: { requiresAuth: true } },
    { path: "/user/me", component: UserAccount, meta: { requiresAuth: true } },
    { path: "/forgot_password", component: UserForgotPassword },
    { path: "/reset_password/:reset_token", component: UserResetPassword },
    { path: "/:catchAll(.*)", component: NotFound, name: "NotFound" },
  ],
});

router.beforeEach(function (to, _, next) {
  if (to.meta.requiresAuth && !store.getters.isAuthenticated) {
    next("/tours/login");
  } else if (to.meta.requiresUnAuth && store.getters.isAuthenticated) {
    next("/tours");
  } else {
    next();
  }
});

export default router;
