export default function StatusPanel({ stateData }) {

    const safeState = {
        favorability: stateData?.favorability ?? 0,
        hunger: stateData?.hunger ?? 0,
        energy: stateData?.energy ?? 0,
        fun: stateData?.fun ?? 0
    };

    return (

        <div className="status-panel">

            <StatusBar
                label="❤️ 호감도"
                value={safeState.favorability}
            />

            <StatusBar
                label="🍖 배고픔"
                value={safeState.hunger}
            />

            <StatusBar
                label="⚡ 기력"
                value={safeState.energy}
            />

            <StatusBar
                label="🎉 재미"
                value={safeState.fun}
            />

        </div>
    );
}

function StatusBar({ label, value }) {

    const normalizedValue =
        Math.max(
            0,
            Math.min(
                100,
                Number(value) || 0
            )
        );

    return (

        <div className="status-item">

            <div className="status-row">

                <span>{label}</span>

                <strong>
                    {normalizedValue}/100
                </strong>

            </div>

            <div className="progress">

                <div
                    className="fill"
                    style={{
                        width: `${normalizedValue}%`
                    }}
                />

            </div>

        </div>
    );
}
