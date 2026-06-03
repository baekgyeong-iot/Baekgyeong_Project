// components/RankingTab.jsx
import "../styles/RankingTab.css";

export default function RankingTab({

    rankings

}) {

    const gameNames = {

        blue_red_flag:
            "청기백기 게임",

        memory:
            "암기 게임",

        red_light_green_light:
            "무궁화 꽃이 피었습니다"
    };

    const medals = [

        "🥇",
        "🥈",
        "🥉"
    ];

    return (

        <div className="ranking-list">

            {
                Object.entries(rankings)
                .map(
                    ([game, records]) => (

                        <div
                            key={game}
                            className="ranking-card"
                        >

                            <h3>
                                {
                                    gameNames[
                                        game
                                    ]
                                }
                            </h3>

                            {
                                records
                                .slice(0,3)
                                .map(
                                    (
                                        record,
                                        index
                                    ) => (

                                        <div
                                            key={index}
                                            className="ranking-item"
                                        >

                                            <span>

                                                {
                                                    medals[
                                                        index
                                                    ]
                                                }

                                            </span>

                                            <span>

                                                {
                                                    record.score
                                                }점

                                            </span>

                                            <span>

                                                {
                                                    record.date
                                                }

                                            </span>

                                        </div>

                                    )
                                )
                            }

                        </div>

                    )
                )
            }

        </div>
    );
}