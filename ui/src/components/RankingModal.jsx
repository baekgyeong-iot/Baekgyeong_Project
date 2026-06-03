// src/components/RankingModal.jsx

import  {
  useState,
  useEffect
} from "react";

import RankingTab from "./RankingTab";
import GrowthTab from "./GrowthTab";

import {
  getRankingModalData
} from "../services/rankingService";

import "../styles/RankingModal.css";

export default function RankingModal({

  open,
  onClose

}) {

  const [activeTab, setActiveTab] =
    useState("ranking");

  const [loading, setLoading] =
    useState(false);

  const [rankings, setRankings] =
    useState({
      blue_red_flag: [],
      memory: [],
      red_light_green_light: []
    });

  const [growthInfo, setGrowthInfo] =
    useState(null);

  const [notice, setNotice] =
    useState("");

  useEffect(() => {

    if (!open) return;

    async function loadData() {

      try {

        setLoading(true);

        const data =
          await getRankingModalData();

        setRankings(
          data.rankings
        );

        setGrowthInfo(
          data.growthInfo
        );

        setNotice(
          data.notice
        );

      } catch (error) {

        console.error(
          "[RankingModal] loadData error",
          error
        );

      } finally {

        setLoading(false);

      }
    }

    loadData();

  }, [open]);

  if (!open) return null;

  return (
    <>
      <div
        className="ranking-overlay"
        onClick={onClose}
      />

      <div className="ranking-modal">

        {/* Header */}

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

        {/* Tabs */}

        <div className="ranking-tabs">

          <button
            className={
              activeTab === "ranking"
                ? "tab active"
                : "tab"
            }
            onClick={() =>
              setActiveTab(
                "ranking"
              )
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
              setActiveTab(
                "growth"
              )
            }
          >
            🌱 성장기록
          </button>

        </div>

        {/* Content */}

        <div className="ranking-content">

          {loading ? (

            <div className="modal-loading">

              데이터를 불러오는 중...

            </div>

          ) : activeTab === "ranking" ? (

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

          )}

        </div>

        {/* Footer */}

        {notice && (

          <div className="ranking-notice">

            {notice}

          </div>

        )}

      </div>
    </>
  );
}