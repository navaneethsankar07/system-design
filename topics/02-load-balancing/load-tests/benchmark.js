import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    benchmark: {
      executor: "constant-vus",
      vus: 30,
      duration: "30s",
    },
  },

  thresholds: {
    http_req_failed: ["rate<0.01"],
  },

  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
};

export default function () {
  const response = http.get(`${__ENV.BASE_URL}/work?delay=0.1`);

  check(response, {
    "status is 200": (r) => r.status === 200,
  });
}
