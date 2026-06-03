// components/GiftCard.jsx
import "../styles/GiftCard.css";

export default function GiftCard({

    gift,
    isNew
}) {

    return (

        <div className="gift-card">

            {isNew && (
                <div className="new-badge">
                    NEW
                </div>
            )}

            <div className="gift-icon">

                {gift.icon}

            </div>

            <div className="gift-name">

                {gift.name}

            </div>

            <div className="gift-count">

                x {gift.count}

            </div>

        </div>
    );
}