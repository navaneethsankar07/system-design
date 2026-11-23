import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
};

export default function () {
  const response = http.get(`${__ENV.BASE_URL}/info`);

  check(response, {
    "status is 200": (r) => r.status === 200,
    "backend identity exists": (r) => {
      try {
        return Boolean(JSON.parse(r.body).instance_id);
      } catch {
        return false;
      }
    },
  });
}
