"use client";

import { useEffect, useState } from "react";
import { UAParser } from "ua-parser-js";

export default function Home() {
  interface User {
    id: string;
    emailAddresses: { emailAddress: string }[];
    firstName: string;
    lastName: string;
    username: string;
    createdAt: string;
    updatedAt: string;
    primaryPhoneNumber: { phoneNumber: string };
    primaryEmailAddress: { emailAddress: string };
  }

  interface Session {
    id: string;
    createdAt: string;
    updatedAt: string;
    lastActiveAt: string;
    expireAt: string;
  }

  interface BrowserInfo {
    browser: { name: string; version: string };
    os: { name: string; version: string };
    device: { type: string | undefined };
  }

  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [browserInfo, setBrowserInfo] = useState<BrowserInfo | null>(null);
  const [loginAttempts, setLoginAttempts] = useState({
    failed: 0,
    successful: 0,
  });

  useEffect(() => {
    // Simulate fetching user and session data
    const fetchUserData = async () => {
      // Replace with actual user fetching logic
      const userData = {
        id: "12345",
        emailAddresses: [{ emailAddress: "user@example.com" }],
        firstName: "John",
        lastName: "Doe",
        username: "johndoe",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        primaryPhoneNumber: { phoneNumber: "+1234567890" },
        primaryEmailAddress: { emailAddress: "user@example.com" },
      };
      setUser(userData);

      // Replace with actual session fetching logic
      const sessionData = {
        id: "67890",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        lastActiveAt: new Date().toISOString(),
        expireAt: new Date().toISOString(),
      };
      setSession(sessionData);
    };

    const fetchLoginAttempts = async () => {
      try {
        const response = await fetch("/api/loginAttempts");
        const data = await response.json();
        setLoginAttempts(data);
      } catch (error) {
        console.error("Error fetching login attempts:", error);
      }
    };

    fetchLoginAttempts();
    fetchUserData();

    // Get browser information
    const parser = new UAParser();
    const browserResult = parser.getResult();
    const browserInfo: BrowserInfo = {
      browser: {
        name: browserResult.browser.name || "Unknown",
        version: browserResult.browser.version || "Unknown",
      },
      os: {
        name: browserResult.os.name || "Unknown",
        version: browserResult.os.version || "Unknown",
      },
      device: {
        type: browserResult.device.type,
      },
    };
    setBrowserInfo(browserInfo);
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        {user && (
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              User Information
            </h2>
            <p className="text-gray-600">
              <strong>ID:</strong> {user.id}
            </p>
            <p className="text-gray-600">
              <strong>Email:</strong> {user.emailAddresses[0]?.emailAddress}
            </p>
            <p className="text-gray-600">
              <strong>First Name:</strong> {user.firstName}
            </p>
            <p className="text-gray-600">
              <strong>Last Name:</strong> {user.lastName}
            </p>
            <p className="text-gray-600">
              <strong>Username:</strong> {user.username}
            </p>
            <p className="text-gray-600">
              <strong>Created At:</strong>{" "}
              {user.createdAt
                ? new Date(user.createdAt).toLocaleDateString()
                : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>Updated At:</strong>{" "}
              {user.updatedAt
                ? new Date(user.updatedAt).toLocaleDateString()
                : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>Primary Phone Number:</strong>{" "}
              {user.primaryPhoneNumber?.phoneNumber}
            </p>
            <p className="text-gray-600">
              <strong>Primary Address:</strong>{" "}
              {user.primaryEmailAddress?.emailAddress}
            </p>
          </div>
        )}

        {session && (
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md mt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Session Information
            </h2>
            <p className="text-gray-600">
              <strong>ID:</strong> {session.id}
            </p>
            <p className="text-gray-600">
              <strong>Created At:</strong>{" "}
              {session.createdAt
                ? new Date(session.createdAt).toLocaleDateString()
                : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>Updated At:</strong>{" "}
              {session.updatedAt
                ? new Date(session.updatedAt).toLocaleDateString()
                : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>Last Active At:</strong>{" "}
              {session.lastActiveAt
                ? new Date(session.lastActiveAt).toLocaleDateString()
                : "N/A"}
            </p>
            <p className="text-gray-600">
              <strong>Expires At:</strong>{" "}
              {session.expireAt
                ? new Date(session.expireAt).toLocaleDateString()
                : "N/A"}
            </p>
          </div>
        )}

        {browserInfo && (
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md mt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Browser Information
            </h2>
            <p className="text-gray-600">
              <strong>Browser Name:</strong> {browserInfo.browser.name}
            </p>
            <p className="text-gray-600">
              <strong>Browser Version:</strong> {browserInfo.browser.version}
            </p>
            <p className="text-gray-600">
              <strong>OS Name:</strong> {browserInfo.os.name}
            </p>
            <p className="text-gray-600">
              <strong>OS Version:</strong> {browserInfo.os.version}
            </p>
            <p className="text-gray-600">
              <strong>Device Type:</strong> {browserInfo.device.type || "N/A"}
            </p>
          </div>
        )}

        {browserInfo && (
          <div className="bg-white rounded-lg shadow-lg p-6 w-full max-w-md mt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Login Attempts
            </h2>
            <p className="text-gray-600">
              <strong>Failed Login Attempts:</strong> {loginAttempts.failed}
            </p>
            <p className="text-gray-600">
              <strong>Successful Login Attempts:</strong>{" "}
              {loginAttempts.successful}
            </p>
          </div>
        )}
      </main>
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center"></footer>
    </div>
  );
}
