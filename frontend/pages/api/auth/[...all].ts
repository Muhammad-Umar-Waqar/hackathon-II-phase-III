import { auth } from "../../../lib/auth";
import type { NextApiRequest, NextApiResponse } from "next";

export const config = {
  api: {
    bodyParser: false,
  },
};

function getBody(req: NextApiRequest): Promise<string> {
  return new Promise((resolve) => {
    const chunks: Uint8Array[] = [];
    req.on("data", (chunk) => chunks.push(chunk));
    req.on("end", () => {
      const buffer = Buffer.concat(chunks);
      resolve(buffer.toString("utf-8"));
    });
  });
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const protocol = req.headers["x-forwarded-proto"] || "http";
    const host = req.headers.host || "localhost:3000";
    const url = `${protocol}://${host}${req.url}`;

    const body =
      req.method !== "GET" && req.method !== "HEAD"
        ? await getBody(req)
        : undefined;

    const headers = new Headers();
    Object.entries(req.headers).forEach(([key, value]) => {
      if (value) {
        headers.set(key, Array.isArray(value) ? value[0] : value);
      }
    });

    const request = new Request(url, {
      method: req.method || "GET",
      headers,
      body,
    });

    const response = await auth.handler(request);
    const text = await response.text();

    res.status(response.status);
    response.headers.forEach((value, key) => {
      res.setHeader(key, value);
    });
    res.send(text);
  } catch (error) {
    console.error("[Better Auth Error]:", error);
    res.status(500).json({
      error: "Internal server error",
      message: error instanceof Error ? error.message : String(error),
    });
  }
}
