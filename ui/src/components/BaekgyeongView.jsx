import WhaleAvatar from "./WhaleAvatar";

import "../styles/BaekgyeongView.css";

export default function BaekgyeongView({
    stateData,
    onInventoryClick
}) {

    const getMessage = () => {

        if (!stateData) {

            return "백경이가 헤엄치고 있어요 🐳";
        }

        if (stateData.runaway) {

            return "백경이가 가출했어요...";
        }

        if (stateData.isSleeping) {

            return "쿨쿨... 자는 중이에요 😴";
        }

        switch (stateData.mood) {

            case "HUNGRY":
                return "배고파요.. 크릴새우 주세요!";

            case "SLEEPY":
                return "졸려요...";

            case "BORED":
                return "같이 놀아요!";

            case "HAPPY":
                return "오늘 정말 행복해요!";

            case "RUNAWAY":
                return "집을 나가버렸어요...";

            case "SLEEPING":
                return "꿈나라 여행 중이에요 😴";

            default:
                return "백경이가 바다를 헤엄치고 있어요!";
        }
    };

    return (

        <div className="ocean-view">

            <div className="whale-container">

                <WhaleAvatar
                    growthStage={
                        stateData?.growthStage
                    }
                    isSleeping={
                        stateData?.isSleeping
                    }
                />

            </div>

            <div className="speech-bubble">

                {getMessage()}

            </div>

            <button
                className="inventory-button"
                onClick={onInventoryClick}
            >
                🎒 가방
            </button>

        </div>
    );
}