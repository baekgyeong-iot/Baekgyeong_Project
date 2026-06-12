import { useState } from "react";

import RankingTab from "./RankingTab";
import GrowthTab from "./GrowthTab";

import "../styles/RankingModal.css";

export default function RankingModal({
    open,
    onClose,
    rankings,
    growthInfo,
    notice
}) {

    const [activeTab, setActiveTab] =
        useState("ranking");

    if (!open) return null;

    return (

        <div className="ranking-modal">

            <div className="ranking-header">

                <h2>
                    🏆 명예의 전당 &
                    성장 다이어리
                </h2>

                <button
                    className="close-btn"
                    onClick={onClose}
                >
                    ✕
                </button>

            </div>

            <div className="ranking-tabs">

                <button
                    className={
                        activeTab === "ranking"
                            ? "tab active"
                            : "tab"
                    }
                    onClick={() =>
                        setActiveTab("ranking")
                    }
                >
                    🏆 랭킹
                </button>

                <button
                    className={
                        activeTab === "growth"
                            ? "tab active"
                            : "tab"
                    }
                    onClick={() =>
                        setActiveTab("growth")
                    }
                >
                    🌱 성장기록
                </button>

            </div>

            <div className="ranking-content">

                {
                    activeTab === "ranking" ? (

                        <RankingTab
                            rankings={rankings}
                        />

                    ) : (

                        <GrowthTab
                            growthStage={
                                growthInfo?.growthStage ||
                                "BABY"
                            }
                            birthDate={
                                growthInfo?.birthDate
                            }
                            mood={
                                growthInfo?.mood
                            }
                            favorability={
                                growthInfo?.favorability
                            }
                            hunger={
                                growthInfo?.hunger
                            }
                            fun={
                                growthInfo?.fun
                            }
                            energy={
                                growthInfo?.energy
                            }
                            isSleeping={
                                growthInfo?.isSleeping
                            }
                        />

                    )
                }

            </div>

            {notice && (

                <div className="ranking-notice">

                    {notice}

                </div>

            )}

        </div>

    );
}