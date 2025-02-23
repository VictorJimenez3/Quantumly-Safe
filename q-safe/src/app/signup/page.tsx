"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { UAParser } from "ua-parser-js";
import SHA256 from "crypto-js/sha256";
import Link from "next/link"; // Add this import
import Cookies from "js-cookie"; // Add this import

// Add this before the useEffect
if (!process.env.NEXT_PUBLIC_BACKEND_URL) {
  console.error("Backend URL not configured");
}
const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

export default function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState(""); // Add this
  const [loginStats, setLoginStats] = useState({
    // Add this
    failedLoginAttempts: 0,
    successfulLoginAttempts: 0,
  });
  const router = useRouter();
  const [userInfo, setUserInfo] = useState({
    ipAddress: "",
    userAgent: "",
    domainName: "",
  });

  const parser = new UAParser();
  const browserResult = parser.getResult();
  const userAgent = browserResult.browser.name || "Unknown";

  const hashPassword = (password: string): string => {
    return SHA256(password).toString();
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch IP address
        const ipResponse = await fetch("https://api.ipify.org?format=json");
        const ipData = await ipResponse.json();

        // Update userInfo with the IP address
        setUserInfo((prev) => ({
          ...prev,
          ipAddress: ipData.ip,
          userAgent: userAgent,
          domainName: window.location.hostname,
        }));

        // Fetch login stats
        const statsResponse = await fetch("/api/loginAttempts");
        const statsData = await statsResponse.json();
        setLoginStats(statsData);
        console.log("Login stats:", loginStats);

        // Get session ID from cookies
        const sessionId = Cookies.get("sessionId");
        setSessionId(sessionId || crypto.randomUUID());
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, [userAgent]);

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!username || !password) {
      setError("Username and password are required");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    const hashedPassword = hashPassword(password);

    try {
      if (!BACKEND_URL) {
        throw new Error("Backend URL not configured");
      }

      const response = await fetch(`${BACKEND_URL}/api/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
          username,
          password: hashedPassword,
          userAgent,
          domainName: window.location.hostname,
          ip: userInfo.ipAddress,
          sessionId,
        }),
      });

      if (response.ok) {
        // Clear form and show success
        setUsername("");
        setPassword("");
        setConfirmPassword("");
        setError("");
        router.push("/"); // Redirect to login page
      } else {
        const data = await response.json();
        setError(data.message || "Error creating account");
      }
    } catch (error) {
      console.error("Signup error:", error);
      setError("An error occurred during signup");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-lg p-10 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800">Sign Up</h1>
          <p className="text-gray-600 mt-2">Create your Q‑Safe account</p>
        </div>
        <form onSubmit={handleSignup}>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="username"
            >
              Username
            </label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            />
          </div>
          <div className="mb-4">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="password"
            >
              Password
            </label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            />
          </div>
          <div className="mb-6">
            <label
              className="block text-gray-700 text-sm font-bold mb-2"
              htmlFor="confirm-password"
            >
              Confirm Password
            </label>
            <input
              type="password"
              id="confirm-password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
              required
            />
          </div>
          {error && <p className="text-red-500 text-xs italic mb-4">{error}</p>}
          <div className="flex items-center justify-between">
            <button
              type="submit"
              className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
            >
              Sign Up
            </button>
          </div>
        </form>
        <div className="mt-4 text-center">
          <p className="text-gray-600">
            Already have an account?{" "}
            <Link // Change from 'link' to 'Link'
              href="/"
              className="text-blue-500 hover:text-blue-700 font-semibold"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
