const baseUrl = (import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000").replace(/\/$/, "");

interface ApiOptions {
  headers?: HeadersInit;
}

function buildNetworkError(path: string, cause: unknown): Error {
  const detail = cause instanceof Error && cause.message.length > 0 ? ` (${cause.message})` : "";
  return new Error(
    `API server is unreachable: ${baseUrl}${path}. Start backend and verify /health endpoint.${detail}`
  );
}

export async function apiGet<T>(path: string, options?: ApiOptions): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, {
      headers: options?.headers
    });
  } catch (error) {
    throw buildNetworkError(path, error);
  }

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`GET ${path} failed with status ${response.status}${detail ? `: ${detail}` : ""}`);
  }
  return (await response.json()) as T;
}

export async function apiPost<T>(path: string, body: unknown, options?: ApiOptions): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers ?? {})
      },
      body: JSON.stringify(body)
    });
  } catch (error) {
    throw buildNetworkError(path, error);
  }

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`POST ${path} failed with status ${response.status}${detail ? `: ${detail}` : ""}`);
  }
  return (await response.json()) as T;
}

export async function apiPostForm<T>(path: string, formData: FormData, options?: ApiOptions): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, {
      method: "POST",
      headers: options?.headers,
      body: formData
    });
  } catch (error) {
    throw buildNetworkError(path, error);
  }

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(
      `POST form ${path} failed with status ${response.status}${detail ? `: ${detail}` : ""}`
    );
  }
  return (await response.json()) as T;
}

export async function apiPut<T>(path: string, body: unknown, options?: ApiOptions): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${baseUrl}${path}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers ?? {})
      },
      body: JSON.stringify(body)
    });
  } catch (error) {
    throw buildNetworkError(path, error);
  }

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(`PUT ${path} failed with status ${response.status}${detail ? `: ${detail}` : ""}`);
  }
  return (await response.json()) as T;
}
