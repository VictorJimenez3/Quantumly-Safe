import { NextApiRequest, NextApiResponse } from "next";
import { UAParser } from "ua-parser-js";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const ipAddress = req.headers["x-forwarded-for"] || req.socket.remoteAddress;
  const userAgent = req.headers["user-agent"];
  const domainName = req.headers["host"];

  const parser = new UAParser(userAgent);
  const browser = parser.getBrowser();

  res.status(200).json({
    ipAddress,
    userAgent: browser.name,
    domainName,
  });
}
