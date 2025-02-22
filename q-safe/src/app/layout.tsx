"use client";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import "./globals.css";
import { UAParser } from "ua-parser-js";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loginStats, setLoginStats] = useState({
    failedLoginAttempts: 0,
    successfulLoginAttempts: 0,
  });
  const [loginStatsSession, setLoginStatsSession] = useState({
    failedLoginAttempts: 0,
    successfulLoginAttempts: 0,
  });
  const [userInfo, setUserInfo] = useState({
    ipAddress: "",
    userAgent: "",
    domainName: "",
  });
  const [sessionId, setSessionId] = useState("");

  const parser = new UAParser();
  const browserResult = parser.getResult();
  const userAgent = browserResult.browser.name || "Unknown";

  // Add IP fetching in useEffect
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

        // Get session ID from cookies
        const sessionId = Cookies.get("sessionId");
        setSessionId(sessionId || "No session ID found");
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch("/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
      });

      if (response.ok) {
        setLoginStatsSession((prev) => ({
          ...prev,
          successfulLoginAttempts: prev.successfulLoginAttempts + 1,
        }));
        setIsLoggedIn(true);
        setError("");
        // Record successful login attempt
        await fetch("/api/loginAttempts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ success: true }),
        });
        // Update login stats
        setLoginStats((prev) => ({
          ...prev,
          successfulLoginAttempts: prev.successfulLoginAttempts + 1,
        }));
      } else {
        setError("Invalid username or password");
        setLoginStatsSession((prev) => ({
          ...prev,
          failedfulLoginAttempts: prev.failedLoginAttempts + 1,
        }));
        // Record failed login attempt
        await fetch("/api/loginAttempts", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ success: false }),
        });
        // Update login stats
        setLoginStats((prev) => ({
          ...prev,
          failedLoginAttempts: prev.failedLoginAttempts + 1,
        }));
      }
    } catch (error) {
      console.error("Login error:", error);
      setError("An error occurred during login");
    }
  };

  useEffect(() => {
    const fetchLoginStats = async () => {
      const response = await fetch("/api/loginAttempts");
      const data = await response.json();
      setLoginStats(data);
    };

    const fetchUserInfo = async () => {
      const response = await fetch("/api/userInfo");
      const data = await response.json();
      setUserInfo(data);
    };

    fetchLoginStats();
    fetchUserInfo();
  }, []);

  useEffect(() => {
    const fetchLoginStats = async () => {
      const response = await fetch("/api/loginAttempts");
      const data = await response.json();
      setLoginStats(data);
    };

    const fetchUserInfo = async () => {
      const response = await fetch("/api/userInfo");
      const data = await response.json();
      setUserInfo(data);
    };

    fetchLoginStats();
    fetchUserInfo();
  }, []);

  useEffect(() => {
    const fetchLoginStats = async () => {
      const response = await fetch("/api/loginAttempts");
      const data = await response.json();
      setLoginStats(data);
    };

    const fetchUserInfo = async () => {
      const response = await fetch("/api/userInfo");
      const data = await response.json();
      setUserInfo(data);
    };

    fetchLoginStats();
    fetchUserInfo();
  }, []);

  useEffect(() => {
    const fetchLoginStats = async () => {
      const response = await fetch("/api/loginAttempts");
      const data = await response.json();
      setLoginStats(data);
    };

    const fetchUserInfo = async () => {
      const response = await fetch("/api/userInfo");
      const data = await response.json();
      setUserInfo(data);
    };

    fetchLoginStats();
    fetchUserInfo();
  }, []);
  const sendToFlask = async () => {
    try {
      const response = await fetch(
        "http://192.168.175.27:5000/api/send_preliminary_data",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Add CORS headers if needed
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            userInfo: {
              ipAddress: userInfo.ipAddress,
              userAgent: userInfo.userAgent,
              domainName: userInfo.domainName,
            },
            loginStats: {
              failedAttempts: loginStats.failedLoginAttempts,
              successfulAttempts: loginStats.successfulLoginAttempts,
              totalAttempts:
                loginStats.failedLoginAttempts +
                loginStats.successfulLoginAttempts,
            },
            timestamp: new Date().toISOString(),
          }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Data sent successfully:", data);
      return data;
    } catch (error) {
      console.error("Error sending data to Flask:", error);
      throw error;
    }
  };

  return (
    <html lang="en">
      <head>
        <title>Q‑Safe | Secure Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta
          name="description"
          content="Login to Q‑Safe, your secure solution."
        />
      </head>
      <body>
        {!isLoggedIn ? (
          <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
            <div className="bg-white rounded-lg shadow-lg p-10 w-full max-w-md">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-800">Q‑Safe</h1>
                <p className="text-gray-600 mt-2">Secure Login</p>
              </div>
              <form onSubmit={handleLogin}>
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
                  />
                </div>
                <div className="mb-6">
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
                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
                  />
                </div>
                {error && (
                  <p className="text-red-500 text-xs italic">{error}</p>
                )}
                <div className="flex items-center justify-between">
                  <button
                    type="submit"
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  >
                    Sign In
                  </button>
                </div>
              </form>
              <div className="mt-8">
                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                  onClick={sendToFlask}
                >
                  Send to Flask
                </button>
              </div>
              <div className="mt-8">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                  Login Statistics
                </h2>
                <p className="text-gray-600">
                  <strong>Failed Login Attempts:</strong>{" "}
                  {loginStats.failedLoginAttempts}
                </p>
                <p className="text-gray-600">
                  <strong>Total Login Attempts:</strong>{" "}
                  {loginStats.successfulLoginAttempts +
                    loginStats.failedLoginAttempts}
                </p>
                <p className="text-gray-600">
                  <strong>Session Failed Login Attempts:</strong>{" "}
                  {loginStatsSession.failedLoginAttempts}
                </p>
                <p className="text-gray-600">
                  <strong>Session Total Login Attempts:</strong>{" "}
                  {loginStatsSession.successfulLoginAttempts +
                    loginStatsSession.failedLoginAttempts}
                </p>
                <p className="text-gray-600">
                  <strong>IP Address:</strong> {userInfo.ipAddress}
                </p>
                <p className="text-gray-600">
                  <strong>Browser:</strong> {userInfo.userAgent}
                </p>
                <p className="text-gray-600">
                  <strong>Domain:</strong> {userInfo.domainName}
                </p>
                <p className="text-gray-600">
                  <strong>Session ID:</strong> {sessionId}
                </p>
              </div>
            </div>
          </div>
        ) : (
          <div>
            <h1>Welcome, {username}!</h1>
            {children}
          </div>
        )}
      </body>
    </html>
  );
}
