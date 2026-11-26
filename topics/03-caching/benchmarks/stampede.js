import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 50,
  iterations: 50,
};

export default function () {
  const response = http.get("http://localhost:8000/products/1/");

  check(response, {
    "status is 200": (r) => r.status === 200,
    "cache header exists": (r) => r.headers["X-Cache"] !== undefined,
  });
}
