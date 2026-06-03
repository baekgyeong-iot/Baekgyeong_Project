// src/components/InventoryDrawer.jsx

import { useEffect, useState } from "react";

import WhaleAvatar from "./WhaleAvatar";
import GiftCard from "./GiftCard";

import { getInventory } from "../services/rankingService";

import "../styles/InventoryDrawer.css";

const TOTAL_SLOTS = 12;

export default function InventoryDrawer({
  open,
  onClose,
  growthStage
}) {

  const [inventory, setInventory] = useState([]);
  const [notice, setNotice] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {

    if (!open) return;

    async function loadInventory() {

      try {

        setLoading(true);

        const data = await getInventory();

        setInventory(data.gifts || []);
        setNotice(data.notice || "");

      } catch (error) {

        console.error(
          "[InventoryDrawer] inventory load error",
          error
        );

      } finally {

        setLoading(false);

      }
    }

    loadInventory();

  }, [open]);

  if (!open) return null;

  const slots = [...inventory];

  while (slots.length < TOTAL_SLOTS) {
    slots.push(null);
  }

  return (
    <>
      <div
        className="drawer-overlay"
        onClick={onClose}
      />

      <aside className="inventory-drawer">

        {/* Header */}

        <div className="drawer-header">

          <div className="drawer-title">
            🎒 백경이의 가방
          </div>

          <button
            className="close-btn"
            onClick={onClose}
          >
            ✕
          </button>

        </div>

        {/* Content */}

        <div className="drawer-content">

          <WhaleAvatar
            growthStage={growthStage}
          />

          <p className="drawer-description">
            백경이가 쓰다듬기를 받을 때마다
            선물을 주었어요! ✨
          </p>

          {loading ? (

            <div className="inventory-loading">
              선물을 불러오는 중...
            </div>

          ) : (

            <div className="gift-grid">

              {slots.map((gift, index) => {

                if (!gift) {

                  return (

                    <div
                      key={`empty-${index}`}
                      className="empty-slot"
                    >
                      ?
                    </div>

                  );
                }

                return (

                  <GiftCard
                    key={gift.gift_id}
                    gift={gift}
                    isNew={gift.is_new}
                  />

                );
              })}

            </div>

          )}

          <div className="inventory-tip">
            💡 Tip :
            백경이를 더 많이 쓰다듬으면
            신비한 선물을 더 받을 수 있어요!
          </div>

          {notice && (
            <div className="inventory-notice">
              {notice}
            </div>
          )}

        </div>

      </aside>
    </>
  );
}