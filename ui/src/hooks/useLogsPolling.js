// src/hooks/useLogsPolling.js

import { useEffect, useState } from "react";

const API_BASE_URL =
  "http://localhost:5000/api";

export default function useLogsPolling(
  interval = 3000
) {

  const [logs, setLogs] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  useEffect(() => {

    let mounted = true;

    const fetchLogs = async () => {

      try {

        const response =
          await fetch(
            `${API_BASE_URL}/logs`
          );

        if (!response.ok) {

          throw new Error(
            `로그 조회 실패 (${response.status})`
          );
        }

        const data =
          await response.json();

        if (!mounted) return;

        const logs =
          Array.isArray(data.logs)
            ? data.logs
            : [];

        setLogs(logs);

        setError(null);

      } catch (err) {

        console.error(
          "[useLogsPolling]",
          err
        );

        setError(err.message);

      } finally {

        setLoading(false);
      }
    };

    fetchLogs();

    const timer =
      setInterval(
        fetchLogs,
        interval
      );

    return () => {

      mounted = false;

      clearInterval(timer);
    };

  }, [interval]);

  return {

    logs,

    loading,

    error
  };
}