// pages/Dashboard.jsx

import { useEffect, useState } from "react";

import StatusPanel from "../components/StatusPanel";
import BaekgyeongView from "../components/BaekgyeongView";
import LogsTicker from "../components/LogsTicker";
import InventoryDrawer from "../components/InventoryDrawer";
import RankingModal from "../components/RankingModal";

import useStatePolling from "../hooks/useStatePolling";
import useLogsPolling from "../hooks/useLogsPolling";

import {
    getRankings,
    getInventory
} from "../services/rankingService";

import "../styles/dashboard.css";

export default function Dashboard() {

    const {
        state: stateData,
        loading,
        error
    } = useStatePolling(3000);

    const {
        logs
    } = useLogsPolling(3000);

    const [rankings, setRankings] =
        useState({
            blue_red_flag: [],
            memory: [],
            red_light_green_light: []
        });

    const [rankingNotice, setRankingNotice] =
        useState("");

    const [gifts, setGifts] =
        useState([]);

    const [inventoryNotice, setInventoryNotice] =
        useState("");

    const [inventoryOpen, setInventoryOpen] =
        useState(false);

    const [rankingOpen, setRankingOpen] =
        useState(false);

    /*
    ---------------------------------
    랭킹 조회
    ---------------------------------
    */

    async function loadRankings() {

        try {

            const data =
                await getRankings();

            setRankings(
                data.rankings
            );

            setRankingNotice(
                data.notice
            );

        } catch (err) {

            console.error(
                "[Dashboard] rankings error",
                err
            );
        }
    }

    /*
    ---------------------------------
    인벤토리 조회
    ---------------------------------
    */

    async function loadInventory() {

        try {

            const data =
                await getInventory();

            setGifts(
                data.gifts || []
            );

            setInventoryNotice(
                data.notice || ""
            );

        } catch (err) {

            console.error(
                "[Dashboard] inventory error",
                err
            );
        }
    }

    /*
    ---------------------------------
    초기 데이터
    ---------------------------------
    */

    useEffect(() => {

        loadRankings();
        loadInventory();

    }, []);

    /*
    ---------------------------------
    Loading
    ---------------------------------
    */

    if (loading) {

        return (
            <div className="loading-screen">
                🐳 백경이를 불러오는 중...
            </div>
        );
    }

    /*
    ---------------------------------
    Error
    ---------------------------------
    */

    if (error) {

        return (
            <div className="error-screen">
                상태 조회 실패
            </div>
        );
    }

    return (

        <div
            className={
                stateData?.isSleeping
                    ? "dashboard night"
                    : "dashboard day"
            }
        >

            <header className="header">

                <h1>
                    🐳 스마트 백경이 룸
                </h1>

                <button
                    className="ranking-button"
                    onClick={() =>
                        setRankingOpen(true)
                    }
                >
                    🏆 성장기록 / 랭킹
                </button>

            </header>

            <div className="content">

                <StatusPanel
                    stateData={stateData}
                />

                <BaekgyeongView
                    stateData={stateData}
                    onInventoryClick={() =>
                        setInventoryOpen(true)
                    }
                />

                <LogsTicker
                    logs={logs}
                />

            </div>

            <InventoryDrawer
                open={inventoryOpen}
                onClose={() =>
                    setInventoryOpen(false)
                }
                gifts={gifts}
                growthStage={
                    stateData?.growthStage
                }
                notice={
                    inventoryNotice
                }
            />

            <RankingModal
                open={rankingOpen}
                onClose={() =>
                    setRankingOpen(false)
                }
                rankings={rankings}
                growthInfo={stateData}
                notice={rankingNotice}
            />

        </div>
    );
}