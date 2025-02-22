import { NextApiRequest, NextApiResponse } from "next";

let failedLoginAttempts = 0;
let successfulLoginAttempts = 0;

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === "GET") {
    // Return current stats
    res.status(200).json({
      failedLoginAttempts,
      successfulLoginAttempts,
    });
  } else if (req.method === "POST") {
    // Update stats based on login success
    const { success } = req.body;
    if (success) {
      successfulLoginAttempts++;
    } else {
      failedLoginAttempts++;
    }
    res.status(200).json({
      failedLoginAttempts,
      successfulLoginAttempts,
    });
  } else {
    res.setHeader("Allow", ["GET", "POST"]);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
