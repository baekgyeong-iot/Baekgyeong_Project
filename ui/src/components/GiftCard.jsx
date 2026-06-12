// components/GiftCard.jsx
import "../styles/GiftCard.css";

import shellImg from "../assets/gifts/shell.png";
import stoneImg from "../assets/gifts/stone.png";
import glassImg from "../assets/gifts/glass.png";

export default function GiftCard({

    gift,
    isNew
}) {

    const giftImages = {
        1:shellImg,
        2:stoneImg,
        3:glassImg
    };

    return (

        <div className="gift-card">

            {isNew && (
                <div className="new-badge">
                    NEW
                </div>
            )}

            <img
                src = {giftImages[gift.gift_id]}
                alt = {gift.name}
                className="gift-image"
            />

            <div className="gift-name">
                {gift.name}
            </div>

            <div className="gift-description">
                {gift.description}
            </div>

            <div className="gift-count">
                x {gift.count}
            </div>

        </div>
    );
}