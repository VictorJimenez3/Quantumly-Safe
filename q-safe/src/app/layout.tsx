"use client";

/**
 * Import Section
 * Organize imports by external libraries, internal modules, and styles
 */
import React from "react";
import { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { UAParser } from "ua-parser-js";
import SHA256 from "crypto-js/sha256";
import Popup from "./components/Popup";
import "./globals.css";

/**
 * RootLayout Component
 * Main layout component that handles authentication, user tracking, and data submission
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Child components to render
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  /**
   * State Management Section
   * Organize state declarations by functionality
   */
  // Authentication states
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);

  // Add to state management section
  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState("");

  // Login statistics states
  const [loginStats, setLoginStats] = useState({
    failedLoginAttempts: 0,
    successfulLoginAttempts: 0,
  });
  const [loginStatsSession, setLoginStatsSession] = useState({
    failedLoginAttempts: 0,
    successfulLoginAttempts: 0,
  });

  // User information states
  const [userInfo, setUserInfo] = useState({
    ipAddress: "",
    userAgent: "",
    domainName: "",
  });
  const [sessionId, setSessionId] = useState("");

  /**
   * Browser Information Section
   * Initialize browser parser and get user agent information
   */
  const parser = new UAParser();
  const browserResult = parser.getResult();
  const userAgent = browserResult.browser.name || "Unknown";

  const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL;

  useEffect(() => {
    if (isLoggedIn) {
      handleRedirect();
    }
  }, [isLoggedIn]);
  /**
   * Utility Functions Section
   */

  /**
   * Hash a password using SHA-256
   * @param {string} password - The password to hash
   * @returns {string} The hashed password
   */
  const hashPassword = (password: string): string => {
    return SHA256(password).toString();
  };

  /**
   * API Communication Functions Section
   */

  /**
   * Send preliminary data to Flask backend
   * @returns {Promise<any>} Response data from the server
   */
  const send_preliminary_data = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/send_preliminary_data`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add CORS headers if needed
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
          userInfo: {
            ip: userInfo.ipAddress,
            userAgent: userInfo.userAgent,
            domainName: userInfo.domainName,
          },
        }),
      });

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

  /**
   * Send signin data to Flask backend
   * @returns {Promise<any>} Response data from the server
   */
  const send_signin_data = async () => {
    const hashedPassword = hashPassword(password);
    try {
      const response = await fetch(`${BACKEND_URL}api/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add CORS headers if needed
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
          failedAttempts: loginStatsSession.failedLoginAttempts,
          totalAttempts:
            loginStatsSession.failedLoginAttempts +
            loginStatsSession.successfulLoginAttempts,
          username: username,
          password: hashedPassword,
          domainName: userInfo.domainName,
          ip: userInfo.ipAddress,
        }),
      });
      const data = await response.json();
      console.log("data attacking", data.is_attacking);
      if (response.ok && data.is_attacking === undefined) {
        // Reset form fields after successful login

        setLoginStatsSession((prev) => ({
          ...prev,
          successfulLoginAttempts: prev.successfulLoginAttempts + 1,
        }));
        setIsLoggedIn(true);

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
        setPassword("");
        setError("Invalid username or password");
        setLoginStatsSession((prev) => ({
          ...prev,
          failedLoginAttempts: prev.failedLoginAttempts + 1,
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

      console.log("Data sent successfully:", data);
      return { response, data };
    } catch (error) {
      console.error("Error sending data to Flask:", error);
      throw error;
    }
  };

  // const send_signin_data = async () => {
  //   const hashedPassword = hashPassword(password);
  //   try {
  //     const response = await fetch(`${BACKEND_URL}api/login`, {
  //       method: "POST",
  //       headers: {
  //         "Content-Type": "application/json",
  //         "Access-Control-Allow-Origin": "*",
  //       },
  //       body: JSON.stringify({
  //         failedAttempts: loginStatsSession.failedLoginAttempts,
  //         totalAttempts:
  //           loginStatsSession.failedLoginAttempts +
  //           loginStatsSession.successfulLoginAttempts,
  //         username: username,
  //         password: hashedPassword,
  //         domainName: userInfo.domainName,
  //       }),
  //     });

  //     const data = await response.json();
  //     return { response, data };
  //   } catch (error) {
  //     console.error("Error sending data to Flask:", error);
  //     throw error;
  //   }
  // };

  /**
   * Send signup data to Flask backend
   * @returns {Promise<any>} Response data from the server
   */
  const send_signup_data = async () => {
    const hashedPassword = hashPassword(password);
    try {
      const response = await fetch(`${BACKEND_URL}api/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          // Add CORS headers if needed
          "Access-Control-Allow-Origin": "*",
        },
        body: JSON.stringify({
          username: username,
          password: hashedPassword,
          userAgent: userAgent,
          ip: userInfo.ipAddress,
          domainName: userInfo.domainName,
        }),
      });
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

  /**
   * Event Handlers Section
   */

  /**
   * Handle form submission for both login and signup
   * @param {React.FormEvent} e - Form submission event
   */
  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSignUp) {
      try {
        await send_signup_data();
        // Reset form fields after successful signup
        setUsername("");
        setPassword("");
        setPopupMessage("Successfully Signed Up!");
        setShowPopup(true);
        setIsSignUp(false); // Switch back to login view
      } catch (error) {
        console.error("Signup error:", error);
        setError("Failed to sign up. Please try again.");
      }
    } else {
      await handleLogin(e);
    }
  };

  /**
   * Handle login process and update statistics
   * @param {React.FormEvent} e - Form submission event
   */
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    send_signin_data();
    // try {
    //   const response = await fetch("/api/login", {
    //     method: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({ username, password }),
    //   });

    //   if (response.ok) {
    //     // Reset form fields after successful login

    //     setLoginStatsSession((prev) => ({
    //       ...prev,
    //       successfulLoginAttempts: prev.successfulLoginAttempts + 1,
    //     }));
    //     setIsLoggedIn(true);
    //     setError("");
    //     // Record successful login attempt
    //     await fetch("/api/loginAttempts", {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify({ success: true }),
    //     });
    //     // Update login stats
    //     setLoginStats((prev) => ({
    //       ...prev,
    //       successfulLoginAttempts: prev.successfulLoginAttempts + 1,
    //     }));
    //   } else {
    //     setPassword("");
    //     setError("Invalid username or password");
    //     setLoginStatsSession((prev) => ({
    //       ...prev,
    //       failedLoginAttempts: prev.failedLoginAttempts + 1,
    //     }));
    //     // Record failed login attempt
    //     await fetch("/api/loginAttempts", {
    //       method: "POST",
    //       headers: {
    //         "Content-Type": "application/json",
    //       },
    //       body: JSON.stringify({ success: false }),
    //     });
    //     // Update login stats
    //     setLoginStats((prev) => ({
    //       ...prev,
    //       failedLoginAttempts: prev.failedLoginAttempts + 1,
    //     }));
    //   }
    // } catch (error) {
    //   console.error("Login error:", error);
    //   setError("An error occurred during login");
    // }
  };

  /**
   * Effects Section
   */

  /**
   * Fetch initial user data and set up session
   */
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
        setSessionId(sessionId || crypto.randomUUID());
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  /**
   * Fetch login statistics and user information
   */
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
  const handleRedirect = (): void => {
    window.open("https://quantum-ly-safe.tech/", "_blank");
  };

  return (
    <html lang="en">
      <head>
        <title>Auth Logger| Secure Login</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" content="Login, your secure solution." />
      </head>
      <body>
        <Popup
          message={popupMessage}
          isVisible={showPopup}
          onClose={() => setShowPopup(false)}
        />
        {!isLoggedIn ? (
          <div className="min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
            <div className="bg-white rounded-lg shadow-lg p-10 w-full max-w-md">
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-gray-800">
                  Test Signin Page!!!!{" "}
                </h1>
                <p className="text-gray-600 mt-2">
                  Secure {isSignUp ? "Sign Up" : "Login"}
                </p>
              </div>
              <form onSubmit={handleFormSubmit}>
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
                    {isSignUp ? "Sign Up" : "                    Sign In"}
                  </button>
                </div>
              </form>
              <div className="mt-4 text-center">
                <p className="text-gray-600">
                  {isSignUp
                    ? "Already have an account?"
                    : "                  Don't have an account?"}{" "}
                  <button
                    onClick={() => setIsSignUp(!isSignUp)}
                    className="text-blue-500 hover:text-blue-700 font-semibold"
                  >
                    {isSignUp ? "Login" : "                    Sign up"}
                  </button>
                </p>
              </div>
              <div className="mt-8 space-y-4">
                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                  onClick={send_preliminary_data}
                >
                  Send Preliminary Data
                </button>

                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                  onClick={send_signup_data}
                >
                  Send Signup Data
                </button>

                <button
                  className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline w-full"
                  onClick={send_signin_data}
                >
                  Send Signin Data
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
          <div className="min-h-screen bg-gradient-to-r from-slate-900 to-slate-800 p-8">
            {children}
          </div>
        )}
      </body>
    </html>
  );
}
