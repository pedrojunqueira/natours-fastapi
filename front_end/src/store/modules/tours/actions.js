import axios from "axios";

export default {
  async loadTours(context) {
    const response = await axios("http://127.0.0.1:8000/api/v1/tours/");
    const tours = response.data.data;
    context.commit("setTours", tours);
  },
  async loadTour(context, Id) {
    const url = `http://127.0.0.1:8000/api/v1/tours/${Id}`;
    const response = await axios(url);
    if (response.status == 200) {
      const tour = response.data.data;
      context.commit("setTour", tour);
    }
  },
};
