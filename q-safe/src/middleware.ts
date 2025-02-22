import { NextResponse } from "next/server";

const customMiddleware = async (req, ev) => {
  const url = req.nextUrl.clone();

  // Check if the request is a login attempt
  if (url.pathname === "/api/auth/login") {
    // Simulate a login attempt for demonstration purposes
    const isLoginFailed = true; // Replace with actual login failure check

    // Get IP address
    const ipAddress = req.headers.get("x-forwarded-for") || req.ip;

    // Get user agent (browser type)
    const userAgent = req.headers.get("user-agent");

    // Get domain name
    const domainName = req.headers.get("host");

    const response = await fetch("/api/loginAttempts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ success: !isLoginFailed }),
    });

    if (isLoginFailed) {
      console.log("Failed login attempt detected");
      console.log(`IP Address: ${ipAddress}`);
      console.log(`User Agent: ${userAgent}`);
      console.log(`Domain Name: ${domainName}`);
    } else {
      console.log("Successful login attempt detected");
      console.log(`IP Address: ${ipAddress}`);
      console.log(`User Agent: ${userAgent}`);
      console.log(`Domain Name: ${domainName}`);
    }
  }

  return NextResponse.next();
};

export default customMiddleware;

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    "/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    // Always run for API routes
    "/(api|trpc)(.*)",
  ],
};
