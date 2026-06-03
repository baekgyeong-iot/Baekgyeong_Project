// src/components/GrowthTab.jsx
import "../styles/GrowthTab.css";

export default function GrowthTab({

    growthStage,
    birthDate,
    mood,
    favorability,
    hunger,
    fun,
    energy,
    isSleeping

}) {

    const currentStage =
        growthStage || "BABY";

    const stages = [

        {
            id: "BABY",
            label: "아기",
            icon: "🐣"
        },

        {
            id: "CHILD",
            label: "청소년",
            icon: "🐳"
        },

        {
            id: "ADULT",
            label: "성인",
            icon: "👑"
        }

    ];

    return (

        <div className="growth-container">

            {/* 성장 트리 */}

            <div className="growth-tree">

                {stages.map((stage) => {

                    const isUnlocked =
                        stages.findIndex(
                            s => s.id === stage.id
                        )
                        <=
                        stages.findIndex(
                            s => s.id === currentStage
                        );

                    return (

                        <div
                            key={stage.id}
                            className={

                                isUnlocked
                                    ? "stage-card active"
                                    : "stage-card locked"
                            }
                        >

                            <div className="stage-icon">

                                {
                                    isUnlocked
                                        ? stage.icon
                                        : "🔒"
                                }

                            </div>

                            <div className="stage-title">

                                {stage.label}

                            </div>

                            <div className="stage-subtitle">

                                {stage.id}

                            </div>

                        </div>

                    );
                })}

            </div>

            {/* 상태 정보 */}

            <div className="growth-info-card">

                <h3>
                    🌱 성장 다이어리
                </h3>

                <div className="info-grid">

                    <div>
                        📅 탄생일
                    </div>

                    <div>
                        {birthDate || "-"}
                    </div>

                    <div>
                        🐳 성장단계
                    </div>

                    <div>
                        {currentStage}
                    </div>

                    <div>
                        😊 현재기분
                    </div>

                    <div>
                        {mood}
                    </div>

                    <div>
                        ❤️ 호감도
                    </div>

                    <div>
                        {favorability}
                    </div>

                    <div>
                        🍖 허기
                    </div>

                    <div>
                        {hunger}
                    </div>

                    <div>
                        🎉 재미
                    </div>

                    <div>
                        {fun}
                    </div>

                    <div>
                        ⚡ 기력
                    </div>

                    <div>
                        {energy}
                    </div>

                    <div>
                        😴 상태
                    </div>

                    <div>

                        {
                            isSleeping
                                ? "잠자는 중"
                                : "깨어있음"
                        }

                    </div>

                </div>

            </div>

        </div>
    );
}