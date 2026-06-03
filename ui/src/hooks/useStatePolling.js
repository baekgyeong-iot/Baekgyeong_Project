import { useState, useEffect } from "react";

const API_BASE_URL = "http://localhost:5000/api";

export default function useStatePolling(
  interval = 3000
) {
  const [state, setState] = useState({
    birthDate: null,
    hunger: 40,
    fun: 40,
    energy: 40,
    favorability: 0,
    mood: "NORMAL",
    growthStage: "BABY",
    isSleeping: false
  });

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  useEffect(() => {
    let mounted = true;

    const fetchState = async () => {
      try {
        const response =
          await fetch(
            `${API_BASE_URL}/state`
          );

        if (!response.ok) {
          throw new Error(
            `상태 조회 실패 (${response.status})`
          );
        }

        const data =
          await response.json();

        if (!mounted) return;

        setState({
          birthDate:
            data.birth_date,

          hunger:
            data.hunger ?? 40,

          fun:
            data.fun ?? 40,

          energy:
            data.energy ?? 40,

          favorability:
            data.favorability ?? 0,

          mood:
            data.mood ?? "NORMAL",

          growthStage:
            data.growth_stage ?? "BABY",

          isSleeping:
            data.is_sleeping ?? false,

          feedCount:
            data.feed_count ?? 0,

          playCount:
            data.play_count ?? 0,

          sleepCount:
            data.sleep_count ?? 0,

          runaway:
            data.is_runaway ?? false
        });

        setError(null);
      } catch (err) {
        console.error(
          "[useStatePolling]",
          err
        );

        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchState();

    const timer =
      setInterval(
        fetchState,
        interval
      );

    return () => {
      mounted = false;
      clearInterval(timer);
    };
  }, [interval]);

  return {
    state,
    loading,
    error
  };
}