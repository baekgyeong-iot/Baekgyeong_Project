// src/components/InventoryDrawer.jsx

import WhaleAvatar from "./WhaleAvatar";
import GiftCard from "./GiftCard";

import "../styles/InventoryDrawer.css";

const TOTAL_SLOTS = 12;

export default function InventoryDrawer({
    open,
    onClose,
    growthStage,
    gifts,
    notice
}) {

    if (!open) return null;

    const inventory = gifts || [];

    const slots = [...inventory];

    while (slots.length < TOTAL_SLOTS) {
        slots.push(null);
    }

    return (
        <>
            <aside className="inventory-drawer">

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

                <div className="drawer-content">

                    <WhaleAvatar
                        growthStage={growthStage}
                    />

                    <p className="drawer-description">
                        백경이가 가져다 준 선물들이에요 ✨
                    </p>

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

                    <div className="inventory-tip">
                        💡 Tip :
                        호감도가 높을수록
                        선물을 받을 확률이 올라가요!
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