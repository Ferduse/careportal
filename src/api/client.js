const API_BASE_URL =
  process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

function getJsonHeaders(accessToken) {
  const headers = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }

  return headers;
}

async function parseResponse(response) {
  const contentType = response.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const payload = isJson ? await response.json() : null;

  if (!response.ok) {
    const detail = payload?.detail;
    const errorDetail = payload?.error?.details;
    const errorMessage = payload?.error?.message;
    let message = "Request failed";

    if (typeof detail === "string") {
      message = detail;
    } else if (Array.isArray(detail) && detail.length > 0) {
      const firstError = detail[0];
      if (typeof firstError?.msg === "string") {
        message = firstError.msg;
      }
    } else if (typeof detail?.message === "string") {
      message = detail.message;
    } else if (Array.isArray(errorDetail) && errorDetail.length > 0) {
      const firstError = errorDetail[0];
      if (typeof firstError?.msg === "string") {
        message = firstError.msg;
      }
    } else if (typeof errorMessage === "string") {
      message = errorMessage;
    }

    throw new Error(message);
  }

  return payload;
}

export async function apiGet(path, accessToken) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "GET",
    headers: getJsonHeaders(accessToken),
  });

  return parseResponse(response);
}

export async function apiPost(path, body, accessToken) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "POST",
    headers: getJsonHeaders(accessToken),
    body: JSON.stringify(body),
  });

  return parseResponse(response);
}

export async function apiPut(path, body, accessToken) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: "PUT",
    headers: getJsonHeaders(accessToken),
    body: JSON.stringify(body),
  });

  return parseResponse(response);
}

export { API_BASE_URL };
