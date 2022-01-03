import axios from "axios";

export default {
  async loadTours(context) {
    const response = await axios(
      `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/tours/`
    );
    const tours = response.data.data;
    context.commit("setTours", tours);
  },
  async loadTour(context, Id) {
    const url = `${process.env.VUE_APP_BACKEND_SERVER}/api/v1/tours/${Id}`;
    const response = await axios(url);
    if (response.status == 200) {
      const tour = response.data.data;
      context.commit("setTour", tour);
    }
  },
};
