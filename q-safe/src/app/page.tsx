"use client";

import { useEffect, useState } from "react";
import { UAParser } from "ua-parser-js";
import Cookies from "js-cookie";

interface HomeProps {
  username?: string;
}
export default function Home({ username }: HomeProps) {
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

  const handleLogout = () => {
    Cookies.remove("sessionId");
    setUser(null);
    setSession(null);
    window.location.href = "/";
  };

  useEffect(() => {
    // Simulate fetching user and session data
    const fetchUserData = async () => {
      // Replace with actual user fetching logic
      const userData = {
        id: "12345",
        emailAddresses: [{ emailAddress: "user@example.com" }],
        firstName: "John",
        lastName: "Doe",
        username: username,
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
    <div className="min-h-screen bg-gradient-to-r from-slate-900 to-slate-800 items-center justify-items-center p-8 pb-20 gap-16 sm:p-20">
      <main className="max-w-4xl mx-auto">
        {/* Logout Button */}
        <div className="w-full max-w-md mx-auto mb-8">
          <button
            onClick={handleLogout}
            className="w-full bg-red-600 hover:bg-red-700 text-gray-100 font-bold py-3 px-6 rounded-md transition-all duration-200 shadow-lg hover:shadow-red-500/30"
          >
            Logout
          </button>
        </div>

        {/* Information Cards Container */}
        <div className="grid gap-6 md:grid-cols-2 auto-rows-min">
          {/* User Information Card */}
          {user && (
            <div className="bg-slate-800 rounded-lg shadow-lg shadow-cyan-500/10 p-6 border border-slate-700">
              <h2 className="text-2xl font-bold text-cyan-400 mb-4 border-b border-slate-700 pb-2">
                User Information
              </h2>
              <div className="space-y-3 text-gray-300">
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">ID:</span>
                  <span>{user.id}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">Email:</span>
                  <span>{user.emailAddresses[0]?.emailAddress}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">
                    First Name:
                  </span>
                  <span>{user.firstName}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">
                    Last Name:
                  </span>
                  <span>{user.lastName}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">Username:</span>
                  <span>{user.username}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">
                    Created At:
                  </span>
                  <span>
                    {user.createdAt
                      ? new Date(user.createdAt).toLocaleDateString()
                      : "N/A"}
                  </span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">
                    Updated At:
                  </span>
                  <span>
                    {user.updatedAt
                      ? new Date(user.updatedAt).toLocaleDateString()
                      : "N/A"}
                  </span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">
                    Primary Phone Number:
                  </span>
                  <span>{user.primaryPhoneNumber?.phoneNumber}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-cyan-300">
                    Primary Address:
                  </span>
                  <span>{user.primaryEmailAddress?.emailAddress}</span>
                </p>
              </div>
            </div>
          )}

          {/* Session Information Card */}
          {session && (
            <div className="bg-slate-800 rounded-lg shadow-lg shadow-emerald-500/10 p-6 border border-slate-700">
              <h2 className="text-2xl font-bold text-emerald-400 mb-4 border-b border-slate-700 pb-2">
                Session Information
              </h2>
              <div className="space-y-3 text-gray-300">
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-emerald-300">ID:</span>
                  <span>{session.id}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-emerald-300">
                    Created At:
                  </span>
                  <span>
                    {session.createdAt
                      ? new Date(session.createdAt).toLocaleDateString()
                      : "N/A"}
                  </span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-emerald-300">
                    Updated At:
                  </span>
                  <span>
                    {session.updatedAt
                      ? new Date(session.updatedAt).toLocaleDateString()
                      : "N/A"}
                  </span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-emerald-300">
                    Last Active At:
                  </span>
                  <span>
                    {session.lastActiveAt
                      ? new Date(session.lastActiveAt).toLocaleDateString()
                      : "N/A"}
                  </span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-emerald-300">
                    Expires At:
                  </span>
                  <span>
                    {session.expireAt
                      ? new Date(session.expireAt).toLocaleDateString()
                      : "N/A"}
                  </span>
                </p>
              </div>
            </div>
          )}

          {/* Browser Information Card */}
          {browserInfo && (
            <div className="bg-slate-800 rounded-lg shadow-lg shadow-purple-500/10 p-6 border border-slate-700">
              <h2 className="text-2xl font-bold text-purple-400 mb-4 border-b border-slate-700 pb-2">
                Browser Information
              </h2>
              <div className="space-y-3 text-gray-300">
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-purple-300">
                    Browser:
                  </span>
                  <span>{browserInfo.browser.name}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-purple-300">
                    Browser Version:
                  </span>
                  <span>{browserInfo.browser.version}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-purple-300">
                    OS Name:
                  </span>
                  <span>{browserInfo.os.name}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-purple-300">
                    OS Version:
                  </span>
                  <span>{browserInfo.os.version}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-purple-300">
                    Device Type:
                  </span>
                  <span>{browserInfo.device.type || "N/A"}</span>
                </p>
              </div>
            </div>
          )}

          {/* Login Attempts Card */}
          {browserInfo && (
            <div className="bg-slate-800 rounded-lg shadow-lg shadow-amber-500/10 p-6 border border-slate-700">
              <h2 className="text-2xl font-bold text-amber-400 mb-4 border-b border-slate-700 pb-2">
                Login Attempts
              </h2>
              <div className="space-y-3 text-gray-300">
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-amber-300">Failed:</span>
                  <span>{loginAttempts.failed}</span>
                </p>
                <p className="flex justify-between items-center py-1 border-b border-slate-700">
                  <span className="font-semibold text-amber-300">
                    Successful:
                  </span>
                  <span>{loginAttempts.successful}</span>
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
