<template>
  <main class="main">
    <div class="user-view">
      <nav class="user-view__menu">
        <ul class="side-nav">
          <li class="side-nav--active">
            <a href="#"
              ><svg>
                <use xlink:href="img/icons.svg#icon-settings"></use></svg
              >Settings</a
            >
          </li>
          <li>
            <a href="#"
              ><svg>
                <use xlink:href="img/icons.svg#icon-briefcase"></use></svg
              >My bookings</a
            >
          </li>
          <li>
            <a href="#"
              ><svg>
                <use xlink:href="img/icons.svg#icon-star"></use></svg
              >My reviews</a
            >
          </li>
          <li>
            <a href="#"
              ><svg>
                <use xlink:href="img/icons.svg#icon-credit-card"></use></svg
              >Billing</a
            >
          </li>
        </ul>
        <div v-if="isAdmin" class="admin-nav">
          <h5 class="admin-nav__heading">Admin</h5>
          <ul class="side-nav">
            <li>
              <a href="#"
                ><svg>
                  <use xlink:href="img/icons.svg#icon-map"></use></svg
                >Manage tours</a
              >
            </li>
            <li>
              <a href="#"
                ><svg>
                  <use xlink:href="img/icons.svg#icon-users"></use></svg
                >Manage users</a
              >
            </li>
            <li>
              <a href="#"
                ><svg>
                  <use xlink:href="img/icons.svg#icon-star"></use></svg
                >Manage reviews</a
              >
            </li>
            <li>
              <a href="#"
                ><svg>
                  <use xlink:href="img/icons.svg#icon-briefcase"></use></svg
              ></a>
            </li>
          </ul>
        </div>
      </nav>
      <div class="user-view__content">
        <div class="user-view__form-container">
          <h2 class="heading-secondary ma-bt-md">Your account settings</h2>
          <form class="form form-user-data">
            <div class="form__group">
              <h1>username : {{ username }}</h1>
            </div>
            <div class="form__group">
              <label class="form__label" for="name">Name</label
              ><input
                class="form__input"
                id="name"
                type="text"
                required="required"
                v-model="name"
              />
            </div>
            <div class="form__group">
              <label class="form__label" for="name">Last Name</label
              ><input
                class="form__input"
                id="lastname"
                type="text"
                required="required"
                v-model="lastname"
              />
            </div>
            <div class="form__group ma-bt-md">
              <label class="form__label" for="email">Email address</label
              ><input
                class="form__input"
                id="email"
                type="email"
                required="required"
                v-model="email"
              />
            </div>
            <div class="form__group form__photo-upload">
              <img class="form__user-photo" :src="image" alt="User photo" />
            </div>
            <input type="file" @change="onFileSelected" />
            <div class="form__group right">
              <button
                @click.prevent="uploadPhoto"
                class="btn btn--small btn--green"
              >
                Upload Photo
              </button>
            </div>

            <div class="form__group right">
              <button
                @click.prevent="updateMe"
                class="btn btn--small btn--green"
              >
                Save settings
              </button>
            </div>
            <div
              v-if="flashMessageDetail"
              class="alert"
              :class="{ 'alert-success': isSuccess, 'alert-danger': isError }"
            >
              {{ message }}
            </div>
          </form>
        </div>
        <div class="line">&nbsp;</div>
        <div class="user-view__form-container">
          <h2 class="heading-secondary ma-bt-md">Password change</h2>
          <form class="form form-user-settings">
            <div class="form__group">
              <label class="form__label" for="password-current"
                >Current password</label
              ><input
                class="form__input"
                id="password-current"
                type="password"
                placeholder="••••••••"
                required="required"
                minlength="4"
                v-model="current_password"
              />
            </div>
            <div class="form__group">
              <label class="form__label" for="password">New password</label
              ><input
                class="form__input"
                id="password"
                type="password"
                placeholder="••••••••"
                required="required"
                minlength="4"
                v-model="password"
              />
            </div>
            <div class="form__group ma-bt-lg">
              <label class="form__label" for="password-confirm"
                >Confirm password</label
              ><input
                class="form__input"
                id="password-confirm"
                type="password"
                placeholder="••••••••"
                required="required"
                minlength="4"
                v-model="confirm_password"
              />
            </div>
            <div class="form__group right">
              <button
                @click.prevent="updateMyPassword"
                class="btn btn--small btn--green"
              >
                Save password
              </button>
            </div>
            <div
              v-if="flashMessagePassword"
              class="alert"
              :class="{ 'alert-success': isSuccess, 'alert-danger': isError }"
            >
              {{ message }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      name: "",
      lastname: "",
      username: "",
      email: "",
      photo: "",
      user: null,
      userId: null,
      current_password: "",
      password: "",
      confirm_password: "",
      role: null,
      message: "",
      flashMessageDetail: false,
      flashMessagePassword: false,
      isSuccess: false,
      isError: false,
      selectedFile: null,
    };
  },
  async created() {
    if (this.$route.params.id) {
      this.userId = this.$route.params.id;
      await this.loadUser(this.userId);
      return;
    }
    await this.$store.dispatch("fetchMe");
    const user = this.$store.getters.me;
    this.populateUser(user);
  },
  computed: {
    isAdmin() {
      return this.role == "admin";
    },
    image() {
      const photo = this.photo;
      try {
        const folder_photo = require(`@/assets/img/users/${photo}`);
        return folder_photo;
      } catch (err) {
        console.log(err.message);
      }
      return require(`@/assets/img/users/default.jpg`);
    },
    savedDetail() {
      return false;
    },
    updatedPassword() {
      return false;
    },
  },
  methods: {
    populateUser(user) {
      this.user = user;
      this.name = user.name;
      this.lastname = user.lastname;
      this.email = user.email;
      this.username = user.username;
      this.role = user.role;
      this.photo = user.photo;
    },
    async loadUser(Id) {
      const token = this.$store.getters.token;

      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios({
        method: "get",
        url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/${Id}`,
        headers,
      });
      if (!response.status == 200) {
        const error = new Error("Failed load user Check your credentials.");
        throw error;
      }

      const user = response.data.user;
      this.populateUser(user);
    },
    async updateMe() {
      try {
        const newMe = {
          name: this.name,
          lastname: this.lastname,
          email: this.email,
        };
        const token = this.$store.getters.token;
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios({
          method: "patch",
          url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/updateme`,
          data: newMe,
          headers: headers,
        });
        if (response.status == 200) {
          this.message = "Details Updated Successfully";
          this.flashMessageDetail = true;
          this.isSuccess = true;
        }
      } catch (err) {
        console.log(err);
      }
    },
    async updateMyPassword() {
      try {
        const newPassword = {
          current_password: this.current_password,
          password: this.password,
          confirm_password: this.confirm_password,
        };
        const token = this.$store.getters.token;
        const headers = { Authorization: `Bearer ${token}` };
        const response = await axios({
          method: "patch",
          url: "{process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/updatemypassword",
          data: newPassword,
          headers: headers,
        });
        if (response.status == 200) {
          this.message = "Password Successfully Updated";
          this.flashMessagePassword = true;
          this.isError = false;
          this.isSuccess = true;
        }
      } catch (err) {
        this.message = err.response.data.detail;
        this.flashMessagePassword = true;
        this.isSuccess = false;
        this.isError = true;
      }
    },
    onFileSelected(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadPhoto() {
      try {
        const photoData = new FormData();
        photoData.append("files", this.selectedFile);
        const token = this.$store.getters.token;
        const config = {
          method: "post",
          url: `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/users/upload_user_image/`,
          headers: {
            Authorization: `Bearer ${token}`,
          },
          data: photoData,
        };
        const response = await axios(config);
        if (response.status == 200) {
          this.message = response.data.message;
          this.flashMessageDetail = true;
          this.isError = false;
          this.isSuccess = true;
        }
      } catch (err) {
        this.message = err.response.data.detail;
        this.flashMessageDetail = true;
        this.isSuccess = false;
        this.isError = true;
      }
    },
  },
};
</script>
