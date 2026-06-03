// components/LogsTicker.jsx
import "../styles/LogsTicker.css";

function getStoryMessage(log) {

    switch (log.event) {

        case "FEED_GAME_FINISHED":
            return "🍖 백경이가 맛있게 식사를 했어요!";

        case "PLAY_GAME_FINISHED":
            return "🎮 백경이가 신나게 놀았어요!";

        case "SLEEP_STARTED":
            return "😴 백경이가 잠들었어요.";

        case "SLEEP_ENDED":
            return "☀️ 백경이가 기분 좋게 일어났어요.";

        case "STROKE_RESULT":

            if (log.payload?.success) {

                return "🤍 백경이를 쓰다듬어 호감도가 상승했어요!";
            }

            return "🖐️ 오늘은 이미 쓰다듬었어요.";

        case "EVO_EVENT_TRIGGERED":

            return `🌱 ${
                log.payload?.to_stage || ""
            } 단계로 성장했어요!`;

        case "RUNAWAY_EVENT_TRIGGERED":

            return "💨 백경이가 가출해버렸어요...";

        default:
            return null;
    }
}

export default function LogsTicker({

    logs = []

}) {

    const filteredLogs = logs
        .filter(log => getStoryMessage(log))
        .slice(-15)
        .reverse();

    return (

        <div className="logs-ticker">

            <div className="logs-header">

                📖 백경이 이야기

            </div>

            <div className="logs-list">

                {
                    filteredLogs.length === 0 && (

                        <div className="empty-log">

                            아직 기록이 없어요

                        </div>

                    )
                }

                {
                    filteredLogs.map((log, index) => (

                        <div
                            key={index}
                            className="log-card"
                        >

                            <div className="log-message">

                                {
                                    getStoryMessage(log)
                                }

                            </div>

                            <div className="log-time">

                                {
                                    log.timestamp
                                        ?.replace("T", " ")
                                        ?.substring(0, 16)
                                }

                            </div>

                        </div>

                    ))
                }

            </div>

        </div>

    );
}