import { useRouter } from "next/router";
import { useEffect } from "react";
import Link from "next/link";
import Head from "next/head";

const Custom404 = () => {
  const router = useRouter();

  // Auto-redirect to homepage after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      router.push("/");
    }, 5000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <>
      <Head>
        <title>404 - Page Not Found</title>
      </Head>
      <div style={styles.container}>
        <h1 style={styles.title}>🚫 404 - Page Not Found</h1>
        <p style={styles.message}>
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>

        <Link href="/">
          <a style={styles.button}>🏠 Go Back Home</a>
        </Link>

        <p style={styles.redirectMessage}>
          Redirecting you automatically in 5 seconds...
        </p>
      </div>
    </>
  );
};

// Inline CSS styles
const styles = {
  container: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    backgroundColor: "#f8f8f8",
  },
  title: {
    fontSize: "3rem",
    color: "#FF4B4B",
  },
  message: {
    fontSize: "1.2rem",
    color: "#333",
  },
  button: {
    marginTop: "20px",
    padding: "12px 24px",
    backgroundColor: "#0070f3",
    color: "#fff",
    textDecoration: "none",
    borderRadius: "5px",
  },
  redirectMessage: {
    marginTop: "10px",
    fontSize: "0.9rem",
    color: "#888",
  },
};

export default Custom404;
