import http from "k6/http";
import { check } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
const ENDPOINT = __ENV.ENDPOINT || "/api/work/";
const ITERATIONS = __ENV.ITERATIONS || "1000000";

export const options = {
  vus: 10,
  duration: "30s",

  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],

  thresholds: {
    http_req_failed: ["rate<0.01"],
  },
};

export default function () {
  const url = `${BASE_URL}${ENDPOINT}?iterations=${ITERATIONS}`;

  const response = http.get(url);

  check(response, {
    "status is 200": (r) => r.status === 200,
  });
}
