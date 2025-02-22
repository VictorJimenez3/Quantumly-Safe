import { NextApiRequest, NextApiResponse } from "next";

let failedLoginAttempts = 0;

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "POST") {
    failedLoginAttempts += 1;
    res.status(200).json({ message: "Failed login attempt recorded" });
  } else if (req.method === "GET") {
    res.status(200).json({ failedLoginAttempts });
  } else {
    res.setHeader("Allow", ["GET", "POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
